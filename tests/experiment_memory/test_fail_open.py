"""Fail-open / boundary tests: NLO execution must not depend on this package.

Plan 01: NLO runs fail open with respect to graph availability; the graph is
never on the canonical run path. Plan README: Graphiti is not installed before
G-01..G-05 pass. Plan 05: enrichment is disabled by default.
"""

import inspect

import pytest

OPERATOR_RUN_SCRIPTS = [
    "scripts/run-proofread.sh",
    "scripts/run-and-log-proofread.sh",
    "scripts/log-run.sh",
    "scripts/review-proofread.sh",
    "scripts/compare-outputs.sh",
    "scripts/next-run-id.sh",
]

GRAPH_MARKERS = ("nlo_experiment_memory", "experiment_memory", "graphiti", "nlo-graph", "neo4j")


def test_canonical_run_path_has_no_graph_dependency(repo_root):
    for script in OPERATOR_RUN_SCRIPTS:
        path = repo_root / script
        assert path.is_file(), f"expected operator script missing: {script}"
        text = path.read_text(encoding="utf-8").lower()
        for marker in GRAPH_MARKERS:
            assert marker not in text, f"{script} references {marker!r}"


def test_run_tests_keeps_suites_independent(repo_root):
    """The experiment-memory suite is additive; existing suites stay listed."""
    text = (repo_root / "scripts" / "run-tests.sh").read_text(encoding="utf-8")
    assert "tests/test-style-analysis.py" in text
    assert "tests/experiment_memory" in text


def test_graphiti_backend_is_gated():
    from nlo_experiment_memory.projection.backends import GraphitiNeo4jBackend

    with pytest.raises(RuntimeError, match="G-01..G-05"):
        GraphitiNeo4jBackend()


def test_graphiti_is_not_installed():
    """The plan README forbids installing Graphiti before G-01..G-05 pass."""
    with pytest.raises(ImportError):
        import graphiti_core  # noqa: F401


def test_dataforge_adapter_is_interface_only():
    from nlo_experiment_memory.stores.dataforge_local import DataForgeLocalAdapter

    assert inspect.isabstract(DataForgeLocalAdapter)
    with pytest.raises(TypeError):
        DataForgeLocalAdapter()  # type: ignore[abstract]


def test_enrichment_disabled_by_default(monkeypatch):
    from nlo_experiment_memory.enrichment import EnrichmentDisabledError, enrich

    monkeypatch.delenv("NLO_GRAPH_ENRICHMENT_ENABLED", raising=False)
    with pytest.raises(EnrichmentDisabledError):
        enrich()
