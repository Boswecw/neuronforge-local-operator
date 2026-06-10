"""Graph backends.

InMemoryGraphStore is the pilot's test double: it proves identity, idempotent
replay, and provenance-equal rebuilds without installing Graphiti (the plan
README forbids installing Graphiti before G-01..G-05 pass). It is not a second
production backend (plan 14 anti-patterns); the one pinned real backend is
Neo4j Community via docker-compose.graphiti-pilot.yml.
"""

from __future__ import annotations

from typing import Iterable, Protocol

from ..identity.normalize import canonical_json


class NodeCollision(ValueError):
    """Same canonical identity replayed with different content — a mapping bug."""


class GraphBackend(Protocol):
    def reset(self) -> None: ...
    def upsert_nodes(self, nodes: Iterable[dict]) -> None: ...
    def upsert_edges(self, edges: Iterable[dict]) -> None: ...


class InMemoryGraphStore:
    def __init__(self):
        self.nodes: dict[str, dict] = {}
        self.edges: dict[str, dict] = {}
        self._node_payloads: dict[str, str] = {}
        self._edge_payloads: dict[str, str] = {}

    def reset(self) -> None:
        self.nodes.clear()
        self.edges.clear()
        self._node_payloads.clear()
        self._edge_payloads.clear()

    def upsert_nodes(self, nodes: Iterable[dict]) -> None:
        for node in nodes:
            payload = canonical_json(node)
            existing = self._node_payloads.get(node["node_id"])
            if existing is not None and existing != payload:
                raise NodeCollision(
                    f"node {node['node_id']} replayed with different content"
                )
            self._node_payloads[node["node_id"]] = payload
            self.nodes[node["node_id"]] = node

    def upsert_edges(self, edges: Iterable[dict]) -> None:
        for edge in edges:
            payload = canonical_json(edge)
            existing = self._edge_payloads.get(edge["edge_id"])
            if existing is not None and existing != payload:
                raise NodeCollision(
                    f"edge {edge['edge_id']} replayed with different content"
                )
            self._edge_payloads[edge["edge_id"]] = payload
            self.edges[edge["edge_id"]] = edge


# The live Graphiti/Neo4j adapter became available after the G-01..G-05 gates
# were operator-accepted and G-06 verified the pinned backend (REVIEW.md).
# It lives in live_backend.py with lazy dependency imports so this module —
# and the whole package — still imports without requirements-graphiti.txt.
from .live_backend import GraphitiNeo4jBackend, LiveBackendError  # noqa: E402,F401
