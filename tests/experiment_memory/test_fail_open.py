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


def test_live_deps_stay_off_the_core_import_path(repo_root):
    """graphiti-core/neo4j are optional pinned deps (requirements-graphiti.txt).

    The install gate passed (G-01..G-05 accepted, G-06 verified), so they MAY
    be installed — but importing the package and every core module must never
    pull them in. NLO execution stays fail-open whether or not they exist.
    """
    import os
    import subprocess
    import sys

    code = (
        "import sys; "
        "import nlo_experiment_memory.contracts, nlo_experiment_memory.identity, "
        "nlo_experiment_memory.stores, nlo_experiment_memory.projection, "
        "nlo_experiment_memory.queries, nlo_experiment_memory.enrichment, "
        "nlo_experiment_memory.cli.__main__; "
        "assert 'graphiti_core' not in sys.modules, 'graphiti_core imported eagerly'; "
        "assert 'neo4j' not in sys.modules, 'neo4j imported eagerly'"
    )
    env = dict(os.environ, PYTHONPATH=str(repo_root / "src"))
    subprocess.run([sys.executable, "-c", code], check=True, env=env)


def test_live_backend_refuses_missing_password():
    from nlo_experiment_memory.projection.live_backend import (
        GraphitiNeo4jBackend,
        LiveBackendError,
    )

    with pytest.raises(LiveBackendError, match="password"):
        GraphitiNeo4jBackend("bolt://127.0.0.1:7687", "neo4j", "")


def test_live_backend_refuses_non_loopback_uri():
    from nlo_experiment_memory.projection.live_backend import (
        GraphitiNeo4jBackend,
        LiveBackendError,
    )

    with pytest.raises(LiveBackendError, match="loopback"):
        GraphitiNeo4jBackend("bolt://graph.example.com:7687", "neo4j", "not-a-real-pw")


def test_pinned_graphiti_requirements_exist(repo_root):
    text = (repo_root / "requirements-graphiti.txt").read_text(encoding="utf-8")
    assert "graphiti-core==" in text
    assert "neo4j==" in text


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
