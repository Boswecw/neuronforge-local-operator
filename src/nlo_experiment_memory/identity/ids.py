"""Canonical node, edge, and graph identity (plan 03 formulas, verbatim)."""

from __future__ import annotations

from .normalize import canonical_json, nfc, normalize_timestamp, sha256_hex

GRAPH_SCHEMA_VERSION = "nlo-graph-schema-v1"


def node_id(
    entity_type: str,
    canonical_business_key: str,
    graph_schema_version: str = GRAPH_SCHEMA_VERSION,
) -> str:
    return sha256_hex(
        f"{nfc(graph_schema_version)}:{nfc(entity_type)}:{nfc(canonical_business_key)}"
    )


def edge_id(
    relationship_type: str,
    source_node_id: str,
    target_node_id: str,
    source_record_id: str,
    effective_at: str,
    graph_schema_version: str = GRAPH_SCHEMA_VERSION,
) -> str:
    return sha256_hex(
        ":".join(
            [
                nfc(graph_schema_version),
                nfc(relationship_type),
                source_node_id,
                target_node_id,
                nfc(source_record_id),
                normalize_timestamp(effective_at),
            ]
        )
    )


def graph_fingerprint(canonical_export: dict) -> str:
    """Fingerprint over the canonical export (provenance equality level).

    The export must already exclude backend ids, insertion order, projected_at,
    runtime metrics, and connection metadata; the projector guarantees this by
    construction.
    """
    return sha256_hex(canonical_json(canonical_export))
