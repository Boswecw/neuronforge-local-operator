"""Query tests (plan 09): golden evidence, fail-closed gates, narrative limits."""

import json
import re
import shutil

import pytest

from nlo_experiment_memory.projection.projector import rebuild
from nlo_experiment_memory.queries.evidence import QueryRefusedError, open_queries
from nlo_experiment_memory.queries.narrative import build_narrative

CONTRACT = "proofread.lore_safe.v1"


@pytest.fixture()
def runtime_dir(records_dir, tmp_path):
    runtime = tmp_path / "runtime"
    rebuild(records_dir, runtime_dir=runtime)
    return runtime


@pytest.fixture()
def queries(records_dir, runtime_dir):
    return open_queries(records_dir, runtime_dir, max_lag_seconds=0)


def _golden(golden_dir, name):
    with open(golden_dir / name, encoding="utf-8") as handle:
        return json.load(handle)


def test_golden_current_baseline(queries, golden_dir):
    assert queries.current_baseline(CONTRACT) == _golden(golden_dir, "current-baseline.json")


def test_golden_baseline_history(queries, golden_dir):
    assert queries.baseline_history(CONTRACT) == _golden(golden_dir, "baseline-history.json")


def test_golden_recurring_failures(queries, golden_dir):
    assert queries.recurring_failures(CONTRACT) == _golden(golden_dir, "recurring-failures.json")


def test_recurring_failures_excludes_fixture_modeled_by_default(queries):
    evidence = queries.recurring_failures(CONTRACT)
    assert "OUT_OF_MEMORY" not in evidence["facts"]["failure_classes"]
    assert evidence["facts"]["excluded_failure_ids"] == ["failure-fixture-oom-001"]
    assert "failure-fixture-oom-001" not in evidence["supporting_record_ids"]


def test_recurring_failures_can_include_fixture_modeled(queries):
    evidence = queries.recurring_failures(CONTRACT, include_fixtures=True)
    assert "OUT_OF_MEMORY" in evidence["facts"]["failure_classes"]
    assert evidence["facts"]["excluded_failure_ids"] == []
    assert "failure-fixture-oom-001" in evidence["supporting_record_ids"]


def test_golden_compare_runs(queries, golden_dir):
    evidence = queries.compare_runs("run-2026-03-13-005", "run-2026-03-13-016")
    assert evidence == _golden(golden_dir, "compare-runs.json")


def test_golden_explain_candidate(queries, golden_dir):
    evidence = queries.explain_candidate("run-2026-03-13-016")
    assert evidence == _golden(golden_dir, "explain-candidate.json")


def test_contradictions_are_preserved(queries):
    evidence = queries.explain_candidate("run-2026-03-13-016")
    assert evidence["contradicting_record_ids"] == [
        "failure-run-2026-03-13-016-false-negative-01",
        "failure-run-2026-03-13-016-style-regression-01",
    ]
    assert evidence["authoritative"] is False


def test_temporal_order_is_exact(queries):
    evidence = queries.compare_runs("run-2026-03-13-005", "run-2026-03-13-016")
    times = [event["at"] for event in evidence["timeline_events"]]
    assert times == sorted(times)
    assert evidence["timeline_events"][0]["event"] == "RUN_OCCURRED"
    assert evidence["timeline_events"][-1]["event"] == "DECIDED"


def test_missing_projection_refused(records_dir, tmp_path):
    with pytest.raises(QueryRefusedError) as refusal:
        open_queries(records_dir, tmp_path / "empty-runtime", 0)
    assert refusal.value.graph_status == "unavailable"


def test_stale_projection_refused(records_dir, runtime_dir, tmp_path):
    """A canonical record newer than the projection fails advisory queries closed."""
    newer_records = tmp_path / "records"
    shutil.copytree(records_dir, newer_records)
    run = json.loads((newer_records / "run-2026-03-13-005.run.json").read_text(encoding="utf-8"))
    run["run_id"] = "run-2026-03-13-099"
    run["occurred_at"] = "2026-03-13T23:00:00Z"
    run["recorded_at"] = "2026-03-13T23:00:00Z"
    (newer_records / "run-2026-03-13-099.run.json").write_text(json.dumps(run), encoding="utf-8")
    queries = open_queries(newer_records, runtime_dir, max_lag_seconds=0)
    assert queries.status.status == "stale"
    with pytest.raises(QueryRefusedError):
        queries.current_baseline(CONTRACT)
    # generous lag policy may allow it (documented operator override)
    relaxed = open_queries(newer_records, runtime_dir, max_lag_seconds=7200)
    assert relaxed.status.status == "healthy"


def test_fingerprint_mismatch_refused(records_dir, runtime_dir):
    export_path = runtime_dir / "export.json"
    export = json.loads(export_path.read_text(encoding="utf-8"))
    export["nodes"][0]["properties"]["tampered"] = True
    export_path.write_text(json.dumps(export), encoding="utf-8")
    queries = open_queries(records_dir, runtime_dir, 0)
    assert queries.status.status == "invalid"
    with pytest.raises(QueryRefusedError):
        queries.current_baseline(CONTRACT)


def test_quarantined_projection_refused(records_dir, invalid_dir, tmp_path):
    workdir = tmp_path / "records"
    shutil.copytree(records_dir, workdir)
    shutil.copy(invalid_dir / "run-unsupported-schema.json", workdir)
    runtime = tmp_path / "runtime"
    rebuild(workdir, runtime_dir=runtime)
    queries = open_queries(workdir, runtime, 0)
    assert queries.status.status == "degraded"
    with pytest.raises(QueryRefusedError):
        queries.recurring_failures(CONTRACT)


def test_missing_source_ids_refused(records_dir, runtime_dir):
    export_path = runtime_dir / "export.json"
    report_path = runtime_dir / "report.json"
    export = json.loads(export_path.read_text(encoding="utf-8"))
    export["nodes"][0]["provenance"]["source_record_id"] = ""
    export_path.write_text(json.dumps(export), encoding="utf-8")
    # keep the fingerprint consistent so the missing-source check itself fires
    from nlo_experiment_memory.identity.ids import graph_fingerprint

    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["fingerprint"] = graph_fingerprint(export)
    report_path.write_text(json.dumps(report), encoding="utf-8")
    queries = open_queries(records_dir, runtime_dir, 0)
    assert queries.status.status == "invalid"
    assert any("missing source references" in reason for reason in queries.status.reasons)


def test_unknown_run_refused(queries):
    with pytest.raises(QueryRefusedError):
        queries.compare_runs("run-2026-03-13-005", "run-never-happened")


_ID_PATTERN = re.compile(r"\b(?:run|eval|failure|decision|hw|exp)-[a-z0-9][a-z0-9-]*\b")


def _ids_in(value):
    found = set()
    if isinstance(value, dict):
        for child in value.values():
            found |= _ids_in(child)
    elif isinstance(value, list):
        for child in value:
            found |= _ids_in(child)
    elif isinstance(value, str):
        found |= set(_ID_PATTERN.findall(value))
    return found


def test_narrative_cannot_alter_or_extend_evidence(queries, golden_dir):
    for name, evidence in [
        ("current_baseline", queries.current_baseline(CONTRACT)),
        ("recurring_failures", queries.recurring_failures(CONTRACT)),
        ("compare_runs", queries.compare_runs("run-2026-03-13-005", "run-2026-03-13-016")),
        ("explain_candidate", queries.explain_candidate("run-2026-03-13-016")),
        ("baseline_history", queries.baseline_history(CONTRACT)),
    ]:
        snapshot = json.dumps(evidence, sort_keys=True)
        narrative = build_narrative(evidence)
        # narrative may not mutate the evidence object
        assert json.dumps(evidence, sort_keys=True) == snapshot, name
        # narrative may not introduce record ids absent from the evidence
        assert _ids_in(narrative) <= _ids_in(evidence), name
        # narrative may not claim authority
        assert "authoritative: false" in narrative
        # narrative may not hide contradictions
        for contradiction in evidence["contradicting_record_ids"]:
            assert contradiction in narrative, name
