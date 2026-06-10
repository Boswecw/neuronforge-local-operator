"""NLO experiment-memory pilot package.

Implements the governed Graphiti pilot defined in docs/plans/graphiti/:
deterministic identity, strict canonical-record contracts, a deterministic
projector with provenance-equal rebuilds, and evidence-first operator queries.

Governing rule: this package may explain and suggest. It may not approve,
promote, mutate, or assert canonical truth. It is not a runtime dependency
of NLO execution and must remain removable in one bounded change set
(docs/plans/graphiti/13-DECOMMISSION-PLAN.md).
"""

__all__ = ["contracts", "identity", "stores", "projection", "queries", "enrichment"]
