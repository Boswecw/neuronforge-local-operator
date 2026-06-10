"""Deterministic record -> nodes/edges mapping.

Implements docs/plans/graphiti/MAPPING-SPEC.md exactly. Core facts are mapped
field-by-field; no LLM extraction. Every node and edge carries exact
provenance (plan 02). Shared entity nodes (ModelVersion, PromptVersion,
InputVersion, TaskContractVersion) take provenance from the earliest
contributing record, ordered by (recorded_at, record_id) — the plan 04
ordering rule — so rebuild output never depends on insertion order.
"""

from __future__ import annotations

from ..identity.ids import GRAPH_SCHEMA_VERSION, edge_id, node_id
from ..identity.normalize import canonical_json, normalize_timestamp, sha256_hex

SOURCE_STORE = "git"


def record_provenance(record: dict, record_type: str) -> dict:
    return {
        "source_record_id": _record_id(record, record_type),
        "source_record_type": record_type,
        "source_schema_version": record["schema_version"],
        "source_content_hash": sha256_hex(canonical_json(record)),
        "source_store": SOURCE_STORE,
        "recorded_at": normalize_timestamp(record["recorded_at"]),
    }


_ID_FIELDS = {
    "run": "run_id",
    "evaluation": "evaluation_id",
    "failure_observation": "failure_id",
    "operator_decision": "decision_id",
    "hardware_profile": "hardware_profile_id",
}


def _record_id(record: dict, record_type: str) -> str:
    return record[_ID_FIELDS[record_type]]


def _model_business_key(run: dict) -> str:
    digest = run.get("model_digest")
    return f"{run['model_id']}@{digest}" if digest else run["model_id"]


class _GraphBuilder:
    def __init__(self):
        self.nodes: dict[str, dict] = {}
        self.edges: dict[str, dict] = {}

    def add_node(self, entity_type: str, business_key: str, properties: dict,
                 provenance: dict) -> str:
        nid = node_id(entity_type, business_key)
        candidate = {
            "node_id": nid,
            "entity_type": entity_type,
            "business_key": business_key,
            "properties": properties,
            "provenance": provenance,
        }
        existing = self.nodes.get(nid)
        if existing is None:
            self.nodes[nid] = candidate
            return nid
        if canonical_json(existing["properties"]) != canonical_json(properties):
            raise ValueError(
                f"node identity collision: {entity_type}:{business_key} mapped with "
                "different semantic properties"
            )
        # Deterministic provenance for shared nodes: earliest canonical observer.
        current = (existing["provenance"]["recorded_at"], existing["provenance"]["source_record_id"])
        incoming = (provenance["recorded_at"], provenance["source_record_id"])
        if incoming < current:
            self.nodes[nid] = candidate
        return nid

    def add_edge(self, relationship_type: str, source_node: str, target_node: str,
                 effective_at: str, provenance: dict, temporal: dict | None = None):
        normalized_effective = normalize_timestamp(effective_at)
        eid = edge_id(
            relationship_type, source_node, target_node,
            provenance["source_record_id"], normalized_effective,
        )
        edge = {
            "edge_id": eid,
            "relationship_type": relationship_type,
            "source_node_id": source_node,
            "target_node_id": target_node,
            "effective_at": normalized_effective,
            "provenance": provenance,
        }
        if temporal:
            edge.update(temporal)
        self.edges[eid] = edge


def project_records(records_by_type: dict[str, dict[str, dict]]) -> tuple[list[dict], list[dict]]:
    """Project schema-valid, integrity-checked records into nodes and edges.

    `records_by_type` maps record_type -> {record_id: record}. Experiment-event
    envelopes are accepted and ignored (they produce no graph objects).
    Returns (nodes, edges) sorted by canonical id.
    """
    builder = _GraphBuilder()
    runs = records_by_type.get("run", {})

    for run in runs.values():
        provenance = record_provenance(run, "run")
        occurred_at = normalize_timestamp(run["occurred_at"])
        run_node = builder.add_node(
            "Run",
            run["run_id"],
            {
                "run_id": run["run_id"],
                "task_contract": run["task_contract"],
                "model_id": run["model_id"],
                "prompt_id": run["prompt_id"],
                "input_id": run["input_id"],
                "status": run["status"],
                "occurred_at": occurred_at,
                "record_origin": run.get("record_origin", "historical"),
            },
            provenance,
        )

        model_properties = {"model_id": run["model_id"]}
        if run.get("model_digest"):
            model_properties["model_digest"] = run["model_digest"]
        model_node = builder.add_node(
            "ModelVersion", _model_business_key(run), model_properties, provenance
        )
        builder.add_edge("USED_MODEL", run_node, model_node, occurred_at, provenance)

        prompt_node = builder.add_node(
            "PromptVersion",
            f"{run['prompt_id']}@sha256-{run['prompt_content_hash']}",
            {
                "prompt_id": run["prompt_id"],
                "prompt_content_hash": run["prompt_content_hash"],
                "prompt_path": run["prompt_path"],
            },
            provenance,
        )
        builder.add_edge("USED_PROMPT", run_node, prompt_node, occurred_at, provenance)

        input_node = builder.add_node(
            "InputVersion",
            f"{run['input_id']}@sha256-{run['input_content_hash']}",
            {
                "input_id": run["input_id"],
                "input_content_hash": run["input_content_hash"],
                "input_path": run["input_path"],
            },
            provenance,
        )
        builder.add_edge("USED_INPUT", run_node, input_node, occurred_at, provenance)

        contract_node = builder.add_node(
            "TaskContractVersion",
            run["task_contract"],
            {"task_contract": run["task_contract"]},
            provenance,
        )
        builder.add_edge("EXECUTED_UNDER", run_node, contract_node, occurred_at, provenance)

        hardware_id = run.get("hardware_profile_id")
        if hardware_id and hardware_id in records_by_type.get("hardware_profile", {}):
            profile = records_by_type["hardware_profile"][hardware_id]
            hardware_node = _add_hardware_node(builder, profile)
            builder.add_edge("EXECUTED_ON", run_node, hardware_node, occurred_at, provenance)

    for profile in records_by_type.get("hardware_profile", {}).values():
        _add_hardware_node(builder, profile)

    for evaluation in records_by_type.get("evaluation", {}).values():
        provenance = record_provenance(evaluation, "evaluation")
        reviewed_at = normalize_timestamp(evaluation["reviewed_at"])
        evaluation_node = builder.add_node(
            "Evaluation",
            evaluation["evaluation_id"],
            {
                "evaluation_id": evaluation["evaluation_id"],
                "run_id": evaluation["run_id"],
                "outcome": evaluation["outcome"],
                "reviewed_at": reviewed_at,
            },
            provenance,
        )
        run_node = node_id("Run", evaluation["run_id"])
        builder.add_edge("EVALUATES", evaluation_node, run_node, reviewed_at, provenance)

    for failure in records_by_type.get("failure_observation", {}).values():
        provenance = record_provenance(failure, "failure_observation")
        observed_at = normalize_timestamp(failure["observed_at"])
        failure_node = builder.add_node(
            "FailureObservation",
            failure["failure_id"],
            {
                "failure_id": failure["failure_id"],
                "taxonomy_version": failure["taxonomy_version"],
                "failure_class": failure["failure_class"],
                "severity": failure["severity"],
                "confidence": failure["confidence"],
                "reproducibility": failure["reproducibility"],
                "observed_at": observed_at,
                "record_origin": failure.get("record_origin", "historical"),
            },
            provenance,
        )
        if failure.get("evaluation_id"):
            source_node = node_id("Evaluation", failure["evaluation_id"])
        else:
            source_node = node_id("Run", failure["run_id"])
        builder.add_edge("FOUND_FAILURE", source_node, failure_node, observed_at, provenance)

    for decision in records_by_type.get("operator_decision", {}).values():
        provenance = record_provenance(decision, "operator_decision")
        effective_at = normalize_timestamp(decision["effective_at"])
        superseded_at = decision.get("superseded_at")
        normalized_superseded = (
            normalize_timestamp(superseded_at) if superseded_at is not None else None
        )
        decision_node = builder.add_node(
            "OperatorDecision",
            decision["decision_id"],
            {
                "decision_id": decision["decision_id"],
                "decision_type": decision["decision_type"],
                "task_contract": decision["task_contract"],
                "target_run_id": decision["target_run_id"],
                "effective_at": effective_at,
                "superseded_at": normalized_superseded,
            },
            provenance,
        )
        run_node = node_id("Run", decision["target_run_id"])
        if decision["decision_type"] == "accept_baseline":
            builder.add_edge("APPROVES", decision_node, run_node, effective_at, provenance)
            contract_node = node_id("TaskContractVersion", decision["task_contract"])
            builder.add_edge(
                "BECAME_BASELINE_FOR", run_node, contract_node, effective_at, provenance,
                temporal={"superseded_at": normalized_superseded},
            )
        elif decision["decision_type"] == "reject_candidate":
            builder.add_edge("REJECTS", decision_node, run_node, effective_at, provenance)
        elif decision["decision_type"] == "retire_baseline":
            builder.add_edge("REJECTS", decision_node, run_node, effective_at, provenance)
        if decision.get("supersedes_run_id"):
            prior_run_node = node_id("Run", decision["supersedes_run_id"])
            builder.add_edge("SUPERSEDED", run_node, prior_run_node, effective_at, provenance)

    nodes = sorted(builder.nodes.values(), key=lambda node: node["node_id"])
    edges = sorted(builder.edges.values(), key=lambda edge: edge["edge_id"])
    return nodes, edges


def _add_hardware_node(builder: _GraphBuilder, profile: dict) -> str:
    provenance = record_provenance(profile, "hardware_profile")
    properties = {
        "hardware_profile_id": profile["hardware_profile_id"],
        "captured_at": normalize_timestamp(profile["captured_at"]),
        "record_origin": profile.get("record_origin", "historical"),
    }
    if "cpu_cores" in profile:
        properties["cpu_cores"] = profile["cpu_cores"]
    if "mem_total_gb" in profile:
        properties["mem_total_gb"] = profile["mem_total_gb"]
    return builder.add_node(
        "HardwareProfile", profile["hardware_profile_id"], properties, provenance
    )


GRAPH_SCHEMA = GRAPH_SCHEMA_VERSION
