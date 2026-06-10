"""Live adapter proof — operator opt-in integration test.

Requires the pinned backend running and the pilot env configured:

    bash scripts/graph/graph-up.sh
    NLO_GRAPH_LIVE_TEST=1 python3 -m pytest tests/experiment_memory/test_live_backend.py -q

Writes only the pilot group in the local loopback backend; canonical records
are never touched. Equivalent CLI: scripts/graph/nlo-graph verify-live.
"""

import json
import os

import pytest

from nlo_experiment_memory.projection.projector import rebuild

pytestmark = pytest.mark.skipif(
    os.environ.get("NLO_GRAPH_LIVE_TEST") != "1",
    reason="live backend proof is operator opt-in: start the backend with "
           "scripts/graph/graph-up.sh and run with NLO_GRAPH_LIVE_TEST=1",
)


def _backend():
    from nlo_experiment_memory.cli.__main__ import _load_env_graphiti
    from nlo_experiment_memory.projection.live_backend import GraphitiNeo4jBackend

    _load_env_graphiti()
    return GraphitiNeo4jBackend(
        os.environ.get("NLO_GRAPH_NEO4J_URI", "bolt://127.0.0.1:7687"),
        os.environ.get("NLO_GRAPH_NEO4J_USER", "neo4j"),
        os.environ.get("NLO_GRAPH_NEO4J_PASSWORD", ""),
    )


def test_live_roundtrip_provenance_and_golden_evidence(records_dir, golden_dir):
    result = rebuild(records_dir)
    backend = _backend()
    try:
        proof = backend.roundtrip_proof(result.export)
        # a second clean rewrite must land identically (idempotent group replay)
        proof_again = backend.roundtrip_proof(result.export)
    finally:
        backend.close()

    assert proof["provenance_equal"] is True
    assert proof["backend_fingerprint"] == result.report["fingerprint"]
    assert proof["nodes_read"] == result.report["node_count"]
    assert proof["edges_read"] == result.report["edge_count"]
    assert proof_again["provenance_equal"] is True
    assert proof_again["backend_fingerprint"] == proof["backend_fingerprint"]

    # the five plan-08 queries answered from the backend read-back must match
    # the frozen golden evidence exactly
    from nlo_experiment_memory.queries.evidence import OperatorQueries, compute_graph_status
    from nlo_experiment_memory.stores.fixture_store import FixtureStore

    status = compute_graph_status(
        proof["readback"], result.report,
        FixtureStore(records_dir).source_high_watermark(), 0,
    )
    assert status.status == "healthy"
    queries = OperatorQueries(proof["readback"], status)
    for filename, evidence in [
        ("current-baseline.json", queries.current_baseline("proofread.lore_safe.v1")),
        ("baseline-history.json", queries.baseline_history("proofread.lore_safe.v1")),
        ("recurring-failures.json", queries.recurring_failures("proofread.lore_safe.v1")),
        ("compare-runs.json", queries.compare_runs("run-2026-03-13-005", "run-2026-03-13-016")),
        ("explain-candidate.json", queries.explain_candidate("run-2026-03-13-016")),
    ]:
        expected = json.loads((golden_dir / filename).read_text(encoding="utf-8"))
        assert evidence == expected, filename
