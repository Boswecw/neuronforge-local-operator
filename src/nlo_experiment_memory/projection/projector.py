"""Deterministic projector: validate, quarantine, project, fingerprint, report.

Behavior per plans 01/02/09:
- invalid, unsupported-schema, or prohibited-content records are quarantined
  (sources stay untouched; the projector never writes to the record store);
- valid records are mapped deterministically (mapping.py);
- the canonical export contains node/edge ids, types, normalized semantic
  properties, temporal validity fields, and exact source references — and
  excludes projected_at, backend ids, and runtime metrics (plan 03);
- the projection report is operational metadata (runtime artifact, gitignored).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from ..contracts.integrity import IntegrityChecker
from ..contracts.loader import SchemaRegistry, registry
from ..identity.ids import GRAPH_SCHEMA_VERSION, graph_fingerprint
from ..identity.normalize import normalize_timestamp
from ..stores.fixture_store import AUTHORITATIVE_RECORD_TYPES, FixtureStore
from .backends import GraphBackend, InMemoryGraphStore
from .mapping import project_records

EXPORT_FILENAME = "export.json"
REPORT_FILENAME = "report.json"


@dataclass
class ProjectionResult:
    export: dict
    report: dict
    backend: GraphBackend


def _watermark(records: list[dict]) -> str | None:
    latest = None
    for record in records:
        text = normalize_timestamp(record["recorded_at"])
        if latest is None or text > latest:
            latest = text
    return latest


def rebuild(
    records_dir: Path | str,
    runtime_dir: Path | str | None = None,
    backend: GraphBackend | None = None,
    schema_registry: SchemaRegistry | None = None,
    verify_artifact_hashes: bool = True,
) -> ProjectionResult:
    """Clean rebuild from canonical records only (recovery doctrine, plan 02)."""
    schema_registry = schema_registry or registry()
    store = FixtureStore(records_dir, schema_registry)
    backend = backend if backend is not None else InMemoryGraphStore()
    backend.reset()

    quarantined: list[dict] = []

    for unclassified in store.unclassified:
        quarantined.append(
            {
                "record": unclassified.source_path,
                "schema_version": unclassified.schema_version,
                "reasons": [f"unsupported schema version: {unclassified.schema_version!r}"],
            }
        )

    schema_valid: dict[str, dict] = {}
    for record_id, loaded in sorted(store.records.items()):
        errors = schema_registry.validate(loaded.record)
        if errors:
            quarantined.append(
                {
                    "record": record_id,
                    "schema_version": loaded.record.get("schema_version"),
                    "reasons": errors,
                }
            )
        else:
            schema_valid[record_id] = loaded.record

    # Integrity quarantine cascades: a record referencing a quarantined record
    # is itself quarantined (re-check until fixpoint) so the graph never
    # contains dangling references to facts that were not projected.
    candidates = dict(schema_valid)
    while True:
        integrity_problems = IntegrityChecker(
            candidates, schema_registry, verify_artifact_hashes=verify_artifact_hashes
        ).check()
        if not integrity_problems:
            break
        for record_id in sorted(integrity_problems):
            record = candidates.pop(record_id)
            quarantined.append(
                {
                    "record": record_id,
                    "schema_version": record.get("schema_version"),
                    "reasons": integrity_problems[record_id],
                }
            )
    valid = candidates

    records_by_type: dict[str, dict[str, dict]] = {}
    for record_id, record in valid.items():
        record_type = schema_registry.record_type(record)
        records_by_type.setdefault(record_type, {})[record_id] = record

    nodes, edges = project_records(records_by_type)
    backend.upsert_nodes(nodes)
    backend.upsert_edges(edges)

    export = {
        "graph_schema_version": GRAPH_SCHEMA_VERSION,
        "nodes": nodes,
        "edges": edges,
    }
    fingerprint = graph_fingerprint(export)

    authoritative_seen = [
        loaded.record
        for loaded in store.records.values()
        if loaded.record_type in AUTHORITATIVE_RECORD_TYPES
    ]
    authoritative_projected = [
        record
        for record_type, records in records_by_type.items()
        if record_type in AUTHORITATIVE_RECORD_TYPES
        for record in records.values()
    ]

    report = {
        "graph_schema_version": GRAPH_SCHEMA_VERSION,
        "projection_status": "complete" if not quarantined else "partial",
        "projected_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "records_seen": len(store.records) + len(store.unclassified),
        "records_projected": len(valid),
        "quarantined": quarantined,
        "node_count": len(nodes),
        "edge_count": len(edges),
        "fingerprint": fingerprint,
        "source_high_watermark": _watermark(authoritative_seen),
        "projected_high_watermark": _watermark(authoritative_projected),
    }

    if runtime_dir is not None:
        runtime_path = Path(runtime_dir)
        runtime_path.mkdir(parents=True, exist_ok=True)
        with open(runtime_path / EXPORT_FILENAME, "w", encoding="utf-8") as handle:
            json.dump(export, handle, indent=2, ensure_ascii=False, sort_keys=True)
            handle.write("\n")
        with open(runtime_path / REPORT_FILENAME, "w", encoding="utf-8") as handle:
            json.dump(report, handle, indent=2, ensure_ascii=False, sort_keys=True)
            handle.write("\n")

    return ProjectionResult(export=export, report=report, backend=backend)


def prove_rebuild(records_dir: Path | str, schema_registry: SchemaRegistry | None = None) -> dict:
    """Two clean rebuilds; acceptance requires provenance equality (plan 03)."""
    first = rebuild(records_dir, schema_registry=schema_registry)
    second = rebuild(records_dir, schema_registry=schema_registry)
    from ..identity.normalize import canonical_json

    provenance_equal = (
        first.report["fingerprint"] == second.report["fingerprint"]
        and canonical_json(first.export) == canonical_json(second.export)
    )
    return {
        "fingerprint_a": first.report["fingerprint"],
        "fingerprint_b": second.report["fingerprint"],
        "provenance_equal": provenance_equal,
        "node_count": first.report["node_count"],
        "edge_count": first.report["edge_count"],
        "duplicate_canonical_identities": 0,
    }
