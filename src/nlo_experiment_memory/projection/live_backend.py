"""Live Graphiti/Neo4j projection adapter (post-gate phase).

The G-01..G-05 gates passed and were operator-accepted, and G-06 verified the
pinned backend live, so Graphiti may now be wired (plan README gate). This
adapter stays strictly deterministic:

- it writes the projector's canonical export as graphiti EntityNode /
  EntityEdge objects using our deterministic ids as uuids — no LLM
  extraction, no embeddings, no external transmission;
- entity_type -> node label, business_key -> node name,
  relationship_type -> edge name, effective_at -> valid_at,
  superseded_at -> invalid_at (graphiti business-time validity),
  graph schema version -> group_id;
- every node/edge carries its full canonical payload in the
  `nlo_canonical_json` attribute, so a backend read-back reconstructs the
  export byte-for-byte and the provenance fingerprint can be re-verified
  against the projection report (the live adapter proof demanded by
  G-09-COMPARATIVE-EVALUATION.md).

Doctrine guards:
- graphiti-core/neo4j imports are lazy: NLO and the rest of this package
  import cleanly when requirements-graphiti.txt is not installed (fail open);
- non-loopback URIs are refused (plan 05 bind posture);
- writes are scoped to the pilot group_id and a clean group rewrite is
  idempotent; canonical records are never touched.
"""

from __future__ import annotations

import asyncio
import json
from datetime import datetime
from urllib.parse import urlparse

from ..identity.ids import GRAPH_SCHEMA_VERSION, graph_fingerprint
from ..identity.normalize import canonical_json

CANONICAL_ATTRIBUTE = "nlo_canonical_json"
_LOOPBACK_HOSTS = {"127.0.0.1", "localhost", "::1"}


class LiveBackendError(RuntimeError):
    pass


def _require_graphiti():
    try:
        from graphiti_core.driver.neo4j_driver import Neo4jDriver
        from graphiti_core.edges import EntityEdge
        from graphiti_core.nodes import EntityNode
    except ImportError as exc:
        raise LiveBackendError(
            "graphiti-core is not installed; install the pinned pilot dependencies "
            "first: pip install -r requirements-graphiti.txt"
        ) from exc
    return Neo4jDriver, EntityNode, EntityEdge


def _parse_ts(text: str) -> datetime:
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


class GraphitiNeo4jBackend:
    """Deterministic projection writer/reader over graphiti-core + pinned Neo4j."""

    def __init__(self, uri: str, user: str, password: str,
                 group_id: str = GRAPH_SCHEMA_VERSION):
        if not password:
            raise LiveBackendError(
                "Neo4j password required (set NLO_GRAPH_NEO4J_PASSWORD; "
                "see .env.graphiti.example)"
            )
        host = urlparse(uri).hostname
        if host not in _LOOPBACK_HOSTS:
            raise LiveBackendError(
                f"refusing non-loopback graph URI {uri!r}: the pilot backend is "
                "loopback-only (docs/plans/graphiti/05-DATA-SECURITY-AND-CLASSIFICATION.md)"
            )
        driver_cls, self._node_cls, self._edge_cls = _require_graphiti()
        self.group_id = group_id
        self._driver = driver_cls(uri, user, password)

    def close(self) -> None:
        asyncio.run(self._driver.close())

    # --- write -------------------------------------------------------------

    def write_export(self, export: dict) -> dict:
        """Clean group rewrite of the canonical export. Returns write counts."""
        return asyncio.run(self._write(export))

    async def _write(self, export: dict) -> dict:
        await self._node_cls.delete_by_group_id(self._driver, self.group_id)
        for node in export["nodes"]:
            entity = self._node_cls(
                uuid=node["node_id"],
                name=node["business_key"],
                group_id=self.group_id,
                labels=[node["entity_type"]],
                created_at=_parse_ts(node["provenance"]["recorded_at"]),
                summary="",
                attributes={
                    CANONICAL_ATTRIBUTE: canonical_json(node),
                    "entity_type": node["entity_type"],
                    "source_record_id": node["provenance"]["source_record_id"],
                },
            )
            await entity.save(self._driver)
        for edge in export["edges"]:
            superseded_at = edge.get("superseded_at")
            entity_edge = self._edge_cls(
                uuid=edge["edge_id"],
                group_id=self.group_id,
                source_node_uuid=edge["source_node_id"],
                target_node_uuid=edge["target_node_id"],
                created_at=_parse_ts(edge["provenance"]["recorded_at"]),
                name=edge["relationship_type"],
                fact=(
                    f"{edge['relationship_type']} asserted by canonical record "
                    f"{edge['provenance']['source_record_id']}"
                ),
                episodes=[],
                valid_at=_parse_ts(edge["effective_at"]),
                invalid_at=_parse_ts(superseded_at) if superseded_at else None,
                attributes={
                    CANONICAL_ATTRIBUTE: canonical_json(edge),
                    "source_record_id": edge["provenance"]["source_record_id"],
                },
            )
            await entity_edge.save(self._driver)
        return {"nodes_written": len(export["nodes"]), "edges_written": len(export["edges"])}

    # --- read --------------------------------------------------------------

    def read_export(self) -> dict:
        """Reconstruct the canonical export from the backend, byte-for-byte."""
        return asyncio.run(self._read())

    async def _read(self) -> dict:
        nodes = await self._node_cls.get_by_group_ids(self._driver, [self.group_id])
        edges = await self._edge_cls.get_by_group_ids(self._driver, [self.group_id])
        node_dicts = [json.loads(n.attributes[CANONICAL_ATTRIBUTE]) for n in nodes]
        edge_dicts = [json.loads(e.attributes[CANONICAL_ATTRIBUTE]) for e in edges]
        return {
            "graph_schema_version": self.group_id,
            "nodes": sorted(node_dicts, key=lambda d: d["node_id"]),
            "edges": sorted(edge_dicts, key=lambda d: d["edge_id"]),
        }

    # --- proof ---------------------------------------------------------------

    def roundtrip_proof(self, export: dict) -> dict:
        """Write the export, read it back, and compare provenance fingerprints."""
        counts = self.write_export(export)
        readback = self.read_export()
        file_fingerprint = graph_fingerprint(export)
        backend_fingerprint = graph_fingerprint(readback)
        return {
            **counts,
            "nodes_read": len(readback["nodes"]),
            "edges_read": len(readback["edges"]),
            "file_fingerprint": file_fingerprint,
            "backend_fingerprint": backend_fingerprint,
            "provenance_equal": (
                file_fingerprint == backend_fingerprint
                and canonical_json(export) == canonical_json(readback)
            ),
            "readback": readback,
        }
