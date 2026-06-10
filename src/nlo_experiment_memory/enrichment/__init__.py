"""Optional semantic enrichment boundary — disabled, isolated (plan 05).

No enrichment is defined or tested in this pilot (REVIEW.md locked decision).
This module exists only to make the boundary explicit: enrichment requires
NLO_GRAPH_ENRICHMENT_ENABLED=true plus explicit data-policy approval, must use
separate derived_enrichment node/edge types, and must never change core graph
facts or feed promotion logic.
"""

from __future__ import annotations

import os


class EnrichmentDisabledError(RuntimeError):
    pass


def ensure_enrichment_allowed() -> None:
    if os.environ.get("NLO_GRAPH_ENRICHMENT_ENABLED", "false").lower() != "true":
        raise EnrichmentDisabledError(
            "Semantic enrichment is disabled by default (NLO_GRAPH_ENRICHMENT_ENABLED"
            "=false) and requires explicit data-policy approval per "
            "docs/plans/graphiti/05-DATA-SECURITY-AND-CLASSIFICATION.md."
        )


def enrich(*_args, **_kwargs):
    ensure_enrichment_allowed()
    raise NotImplementedError(
        "No enrichment is defined in this pilot; see docs/plans/graphiti/REVIEW.md."
    )
