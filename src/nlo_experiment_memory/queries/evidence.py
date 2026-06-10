"""OperatorQueryEvidence.v1 builders with fail-closed integrity gating.

Advisory queries are answered only from a verified projection. They refuse
(fail closed, plans 01/08) when the projection is missing, its fingerprint
does not verify, records were quarantined, source references are incomplete,
or canonical records are newer than the projection by more than the lag
policy (default 0 seconds; NLO_GRAPH_MAX_PROJECTION_LAG_SECONDS).

Every evidence object carries `authoritative: false`. The operator remains
the sole promotion authority.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from ..identity.ids import graph_fingerprint, node_id
from ..identity.normalize import normalize_timestamp
from ..projection.projector import EXPORT_FILENAME, REPORT_FILENAME
from ..stores.fixture_store import FixtureStore

_PROVENANCE_REQUIRED = (
    "source_record_id",
    "source_record_type",
    "source_schema_version",
    "source_content_hash",
    "source_store",
    "recorded_at",
)


class QueryRefusedError(RuntimeError):
    def __init__(self, graph_status: str, reasons: list[str]):
        self.graph_status = graph_status
        self.reasons = reasons
        super().__init__(
            f"advisory query refused (graph status: {graph_status}): " + "; ".join(reasons)
        )


def _parse(ts: str) -> datetime:
    return datetime.fromisoformat(normalize_timestamp(ts).replace("Z", "+00:00"))


@dataclass
class GraphStatus:
    status: str
    reasons: list[str]
    source_high_watermark: str | None
    projected_high_watermark: str | None
    projection_lag_seconds: float


def compute_graph_status(
    export: dict | None,
    report: dict | None,
    live_source_high_watermark: str | None,
    max_lag_seconds: float = 0.0,
) -> GraphStatus:
    if export is None or report is None:
        return GraphStatus("unavailable", ["no projection artifacts found"],
                           live_source_high_watermark, None, 0.0)

    reasons: list[str] = []
    projected_wm = report.get("projected_high_watermark")
    source_wm = live_source_high_watermark

    if report.get("projection_status") == "failed":
        return GraphStatus("invalid", ["last projection failed"], source_wm, projected_wm, 0.0)

    if graph_fingerprint(export) != report.get("fingerprint"):
        return GraphStatus(
            "invalid", ["projection fingerprint does not verify against export"],
            source_wm, projected_wm, 0.0,
        )

    for kind in ("nodes", "edges"):
        for item in export.get(kind, []):
            provenance = item.get("provenance", {})
            missing = [field for field in _PROVENANCE_REQUIRED if not provenance.get(field)]
            if missing:
                return GraphStatus(
                    "invalid",
                    [f"{kind[:-1]} {item.get('node_id') or item.get('edge_id')} "
                     f"missing source references: {', '.join(missing)}"],
                    source_wm, projected_wm, 0.0,
                )

    if report.get("quarantined"):
        reasons.append(
            f"{len(report['quarantined'])} record(s) quarantined in last projection"
        )
        return GraphStatus("degraded", reasons, source_wm, projected_wm, 0.0)

    lag = 0.0
    if source_wm is not None:
        if projected_wm is None:
            lag = float("inf")
        elif _parse(source_wm) > _parse(projected_wm):
            lag = (_parse(source_wm) - _parse(projected_wm)).total_seconds()
    if lag > max_lag_seconds:
        reasons.append(
            f"canonical records newer than projection by {lag} seconds "
            f"(policy allows {max_lag_seconds})"
        )
        return GraphStatus("stale", reasons, source_wm, projected_wm, lag)

    return GraphStatus("healthy", [], source_wm, projected_wm, lag)


class OperatorQueries:
    """Answers the five plan-08 queries from a verified canonical export."""

    def __init__(self, export: dict, status: GraphStatus):
        self.export = export
        self.status = status
        self.nodes_by_id = {node["node_id"]: node for node in export["nodes"]}
        self.edges = export["edges"]

    # --- gating --------------------------------------------------------------

    def _require_healthy(self):
        if self.status.status != "healthy":
            raise QueryRefusedError(self.status.status, self.status.reasons or
                                    [f"graph status is {self.status.status}"])

    def _evidence(self, query_type: str, subject_id: str, supporting: list[str],
                  contradicting: list[str], timeline: list[dict], facts: dict) -> dict:
        return {
            "query_id": f"{query_type}:{subject_id}",
            "query_type": query_type,
            "subject_id": subject_id,
            "graph_status": self.status.status,
            "source_high_watermark": self.status.source_high_watermark,
            "projected_high_watermark": self.status.projected_high_watermark,
            "projection_lag_seconds": self.status.projection_lag_seconds,
            "supporting_record_ids": sorted(set(supporting)),
            "contradicting_record_ids": sorted(set(contradicting)),
            "timeline_events": sorted(
                timeline, key=lambda e: (e["at"], e["event"], e["record_id"])
            ),
            "facts": facts,
            "authoritative": False,
        }

    # --- graph helpers -------------------------------------------------------

    def _node(self, entity_type: str, business_key: str) -> dict | None:
        return self.nodes_by_id.get(node_id(entity_type, business_key))

    def _edges_of(self, relationship_type: str) -> list[dict]:
        return [e for e in self.edges if e["relationship_type"] == relationship_type]

    def _runs_under_contract(self, contract_node_id: str) -> dict[str, dict]:
        runs = {}
        for edge in self._edges_of("EXECUTED_UNDER"):
            if edge["target_node_id"] == contract_node_id:
                run_node = self.nodes_by_id[edge["source_node_id"]]
                runs[run_node["properties"]["run_id"]] = run_node
        return runs

    def _evaluations_of_run(self, run_node_id: str) -> list[dict]:
        return [
            self.nodes_by_id[edge["source_node_id"]]
            for edge in self._edges_of("EVALUATES")
            if edge["target_node_id"] == run_node_id
        ]

    def _failures_of_run(self, run_id: str) -> list[dict]:
        run_node_id = node_id("Run", run_id)
        evaluation_node_ids = {
            node["node_id"] for node in self._evaluations_of_run(run_node_id)
        }
        failures = []
        for edge in self._edges_of("FOUND_FAILURE"):
            if edge["source_node_id"] == run_node_id or edge["source_node_id"] in evaluation_node_ids:
                failures.append(self.nodes_by_id[edge["target_node_id"]])
        return failures

    def _decisions_about_run(self, run_id: str) -> list[dict]:
        return sorted(
            (
                node for node in self.nodes_by_id.values()
                if node["entity_type"] == "OperatorDecision"
                and node["properties"]["target_run_id"] == run_id
            ),
            key=lambda node: (node["properties"]["effective_at"],
                              node["properties"]["decision_id"]),
        )

    def _run_timeline(self, run_node: dict) -> list[dict]:
        run_id = run_node["properties"]["run_id"]
        events = [{
            "at": run_node["properties"]["occurred_at"],
            "event": "RUN_OCCURRED",
            "record_id": run_id,
            "subject": run_id,
        }]
        for evaluation in self._evaluations_of_run(run_node["node_id"]):
            events.append({
                "at": evaluation["properties"]["reviewed_at"],
                "event": "EVALUATED",
                "record_id": evaluation["properties"]["evaluation_id"],
                "subject": run_id,
            })
        for failure in self._failures_of_run(run_id):
            events.append({
                "at": failure["properties"]["observed_at"],
                "event": "FAILURE_OBSERVED",
                "record_id": failure["properties"]["failure_id"],
                "subject": run_id,
            })
        for decision in self._decisions_about_run(run_id):
            events.append({
                "at": decision["properties"]["effective_at"],
                "event": "DECIDED",
                "record_id": decision["properties"]["decision_id"],
                "subject": run_id,
            })
        return events

    # --- queries -------------------------------------------------------------

    def current_baseline(self, task_contract: str) -> dict:
        self._require_healthy()
        contract_node_id = node_id("TaskContractVersion", task_contract)
        baseline_edges = [
            edge for edge in self._edges_of("BECAME_BASELINE_FOR")
            if edge["target_node_id"] == contract_node_id
        ]
        timeline = [
            {
                "at": edge["effective_at"],
                "event": "BECAME_BASELINE_FOR",
                "record_id": edge["provenance"]["source_record_id"],
                "subject": task_contract,
            }
            for edge in baseline_edges
        ]
        current = [e for e in baseline_edges if e.get("superseded_at") is None]
        if not current:
            return self._evidence(
                "current_baseline", task_contract, [], [], timeline,
                {"task_contract": task_contract, "baseline_run_id": None},
            )
        edge = max(current, key=lambda e: e["effective_at"])
        run_node = self.nodes_by_id[edge["source_node_id"]]
        run_id = run_node["properties"]["run_id"]
        decision_id = edge["provenance"]["source_record_id"]

        supporting = [decision_id]
        contradicting: list[str] = []
        for evaluation in self._evaluations_of_run(run_node["node_id"]):
            if evaluation["properties"]["outcome"] == "accepted":
                supporting.append(evaluation["properties"]["evaluation_id"])
            elif evaluation["properties"]["outcome"] == "rejected":
                contradicting.append(evaluation["properties"]["evaluation_id"])
        for failure in self._failures_of_run(run_id):
            contradicting.append(failure["properties"]["failure_id"])

        facts = {
            "task_contract": task_contract,
            "baseline_run_id": run_id,
            "model_id": run_node["properties"]["model_id"],
            "prompt_id": run_node["properties"]["prompt_id"],
            "decision_id": decision_id,
            "effective_at": edge["effective_at"],
            "superseded_at": edge.get("superseded_at"),
        }
        return self._evidence(
            "current_baseline", task_contract, supporting, contradicting, timeline, facts
        )

    def baseline_history(self, task_contract: str) -> dict:
        self._require_healthy()
        contract_node_id = node_id("TaskContractVersion", task_contract)
        entries = []
        supporting = []
        timeline = []
        for edge in self._edges_of("BECAME_BASELINE_FOR"):
            if edge["target_node_id"] != contract_node_id:
                continue
            run_node = self.nodes_by_id[edge["source_node_id"]]
            decision_id = edge["provenance"]["source_record_id"]
            entries.append({
                "run_id": run_node["properties"]["run_id"],
                "decision_id": decision_id,
                "effective_at": edge["effective_at"],
                "superseded_at": edge.get("superseded_at"),
            })
            supporting.append(decision_id)
            timeline.append({
                "at": edge["effective_at"],
                "event": "BECAME_BASELINE_FOR",
                "record_id": decision_id,
                "subject": task_contract,
            })
        entries.sort(key=lambda entry: (entry["effective_at"], entry["decision_id"]))
        facts = {"task_contract": task_contract, "entries": entries}
        return self._evidence(
            "baseline_history", task_contract, supporting, [], timeline, facts
        )

    def recurring_failures(self, task_contract: str) -> dict:
        self._require_healthy()
        contract_node_id = node_id("TaskContractVersion", task_contract)
        runs = self._runs_under_contract(contract_node_id)
        by_class: dict[str, dict] = {}
        supporting = []
        timeline = []
        for run_id in runs:
            for failure in self._failures_of_run(run_id):
                failure_id = failure["properties"]["failure_id"]
                failure_class = failure["properties"]["failure_class"]
                bucket = by_class.setdefault(
                    failure_class, {"count": 0, "failure_ids": [], "run_ids": []}
                )
                bucket["count"] += 1
                bucket["failure_ids"].append(failure_id)
                if run_id not in bucket["run_ids"]:
                    bucket["run_ids"].append(run_id)
                supporting.append(failure_id)
                timeline.append({
                    "at": failure["properties"]["observed_at"],
                    "event": "FAILURE_OBSERVED",
                    "record_id": failure_id,
                    "subject": run_id,
                })
        for bucket in by_class.values():
            bucket["failure_ids"].sort()
            bucket["run_ids"].sort()
        facts = {
            "task_contract": task_contract,
            "failure_classes": {key: by_class[key] for key in sorted(by_class)},
            "recurring_classes": sorted(
                key for key, bucket in by_class.items() if bucket["count"] >= 2
            ),
        }
        return self._evidence(
            "recurring_failures", task_contract, supporting, [], timeline, facts
        )

    def compare_runs(self, run_a: str, run_b: str) -> dict:
        self._require_healthy()
        subject = f"{run_a}..{run_b}"
        nodes = {}
        for run_id in (run_a, run_b):
            run_node = self._node("Run", run_id)
            if run_node is None:
                raise QueryRefusedError(
                    self.status.status, [f"run not found in projection: {run_id}"]
                )
            nodes[run_id] = run_node

        supporting = [run_a, run_b]
        timeline = []
        comparison = {}
        evaluation_outcomes = {}
        failure_classes = {}
        decisions = {}
        for run_id, run_node in nodes.items():
            properties = run_node["properties"]
            comparison[run_id] = {
                "run_id": run_id,
                "task_contract": properties["task_contract"],
                "model_id": properties["model_id"],
                "prompt_id": properties["prompt_id"],
                "input_id": properties["input_id"],
                "status": properties["status"],
            }
            evaluations = self._evaluations_of_run(run_node["node_id"])
            evaluation_outcomes[run_id] = sorted(
                evaluation["properties"]["outcome"] for evaluation in evaluations
            )
            supporting.extend(
                evaluation["properties"]["evaluation_id"] for evaluation in evaluations
            )
            failures = self._failures_of_run(run_id)
            failure_classes[run_id] = sorted(
                failure["properties"]["failure_class"] for failure in failures
            )
            supporting.extend(
                failure["properties"]["failure_id"] for failure in failures
            )
            run_decisions = self._decisions_about_run(run_id)
            decisions[run_id] = [
                {
                    "decision_id": decision["properties"]["decision_id"],
                    "decision_type": decision["properties"]["decision_type"],
                }
                for decision in run_decisions
            ]
            supporting.extend(
                decision["properties"]["decision_id"] for decision in run_decisions
            )
            timeline.extend(self._run_timeline(run_node))

        differing = sorted(
            field
            for field in ("task_contract", "model_id", "prompt_id", "input_id", "status")
            if comparison[run_a][field] != comparison[run_b][field]
        )
        facts = {
            "run_a": comparison[run_a],
            "run_b": comparison[run_b],
            "differing_fields": differing,
            "evaluation_outcomes": evaluation_outcomes,
            "failure_classes": failure_classes,
            "decisions": decisions,
        }
        return self._evidence("compare_runs", subject, supporting, [], timeline, facts)

    def explain_candidate(self, run_id: str) -> dict:
        self._require_healthy()
        run_node = self._node("Run", run_id)
        if run_node is None:
            raise QueryRefusedError(
                self.status.status, [f"run not found in projection: {run_id}"]
            )
        evaluations = self._evaluations_of_run(run_node["node_id"])
        failures = self._failures_of_run(run_id)
        decisions = self._decisions_about_run(run_id)
        latest = decisions[-1] if decisions else None
        disposition = "undecided"
        if latest is not None:
            disposition = {
                "accept_baseline": "accepted_baseline",
                "reject_candidate": "rejected",
                "retire_baseline": "retired",
            }[latest["properties"]["decision_type"]]

        supporting = [run_id]
        supporting.extend(d["properties"]["decision_id"] for d in decisions)
        supporting.extend(e["properties"]["evaluation_id"] for e in evaluations)
        contradicting = [f["properties"]["failure_id"] for f in failures]

        facts = {
            "run_id": run_id,
            "model_id": run_node["properties"]["model_id"],
            "prompt_id": run_node["properties"]["prompt_id"],
            "status": run_node["properties"]["status"],
            "disposition": disposition,
            "decision_id": latest["properties"]["decision_id"] if latest else None,
            "evaluation_outcomes": sorted(
                e["properties"]["outcome"] for e in evaluations
            ),
            "failure_classes": sorted(
                f["properties"]["failure_class"] for f in failures
            ),
        }
        return self._evidence(
            "explain_candidate", run_id, supporting, contradicting,
            self._run_timeline(run_node), facts,
        )


def open_queries(
    records_dir: Path | str,
    runtime_dir: Path | str,
    max_lag_seconds: float = 0.0,
) -> OperatorQueries:
    """Load the persisted projection, gate it against live canonical records."""
    runtime_path = Path(runtime_dir)
    export = report = None
    export_path = runtime_path / EXPORT_FILENAME
    report_path = runtime_path / REPORT_FILENAME
    if export_path.is_file() and report_path.is_file():
        with open(export_path, encoding="utf-8") as handle:
            export = json.load(handle)
        with open(report_path, encoding="utf-8") as handle:
            report = json.load(handle)

    source_wm = None
    records_path = Path(records_dir)
    if records_path.is_dir():
        source_wm = FixtureStore(records_path).source_high_watermark()

    status = compute_graph_status(export, report, source_wm, max_lag_seconds)
    if export is None:
        raise QueryRefusedError(status.status, status.reasons)
    return OperatorQueries(export, status)
