"""Contract tests (plan 09): strict schemas, integrity, taxonomy, hashes, time."""

import json

import pytest

from nlo_experiment_memory.contracts.integrity import IntegrityChecker
from nlo_experiment_memory.contracts.loader import UnsupportedSchemaVersion, registry
from nlo_experiment_memory.identity.normalize import canonical_json
from nlo_experiment_memory.stores.fixture_store import FixtureStore


def _load(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def test_all_canonical_fixtures_schema_valid(records_dir):
    store = FixtureStore(records_dir)
    assert not store.unclassified
    for loaded in store.records.values():
        assert registry().validate(loaded.record) == [], loaded.record_id


def test_all_canonical_fixtures_integrity_clean(records_dir):
    store = FixtureStore(records_dir)
    problems = IntegrityChecker(store.as_plain_dict()).check()
    assert problems == {}


def test_real_artifact_hashes_verify(records_dir):
    """The converted fixtures carry real SHA256 digests of committed artifacts."""
    store = FixtureStore(records_dir)
    runs = store.by_type("run")
    checker = IntegrityChecker(store.as_plain_dict())
    for run_id, run in runs.items():
        errors = checker._verify_hash(run, "prompt_path", "prompt_content_hash")
        errors += checker._verify_hash(run, "input_path", "input_content_hash")
        errors += checker._verify_hash(run, "output_path", "output_content_hash")
        assert errors == [], run_id


def test_missing_committed_artifact_rejected(records_dir):
    store = FixtureStore(records_dir)
    records = store.as_plain_dict()
    record = json.loads(json.dumps(records["run-2026-03-13-005"]))
    record["prompt_path"] = "prompts/missing-lore-safe-proofread.md"
    records[record["run_id"]] = record
    problems = IntegrityChecker(records).check()
    assert any("does not resolve to a committed artifact" in message
               for message in problems[record["run_id"]])


def test_external_artifact_location_allows_missing_artifact(records_dir):
    store = FixtureStore(records_dir)
    records = store.as_plain_dict()
    record = json.loads(json.dumps(records["run-2026-03-13-005"]))
    record["artifact_location_class"] = "external"
    record["prompt_path"] = "operator-artifact-store/prompts/lore-safe-proofread-003.md"
    records[record["run_id"]] = record
    problems = IntegrityChecker(records).check()
    assert record["run_id"] not in problems


def test_unknown_field_rejected(invalid_dir):
    errors = registry().validate(_load(invalid_dir / "run-unknown-field.json"))
    assert any("surprise_field" in error for error in errors)


def test_missing_required_rejected(invalid_dir):
    errors = registry().validate(_load(invalid_dir / "run-missing-required.json"))
    assert any("prompt_content_hash" in error for error in errors)


def test_bad_enum_rejected(invalid_dir):
    errors = registry().validate(_load(invalid_dir / "run-bad-enum.json"))
    assert errors


def test_succeeded_run_requires_output(records_dir):
    record = _load(records_dir / "run-2026-03-13-005.run.json")
    record.pop("output_path")
    record.pop("output_content_hash")
    assert registry().validate(record)


def test_failed_run_does_not_require_output(records_dir):
    record = _load(records_dir / "run-fixture-oom-001.run.json")
    assert registry().validate(record) == []
    assert "output_path" not in record


def test_unsupported_schema_version_raises(invalid_dir):
    with pytest.raises(UnsupportedSchemaVersion):
        registry().validate(_load(invalid_dir / "run-unsupported-schema.json"))


def test_taxonomy_mismatch_caught(records_dir, invalid_dir):
    record = _load(invalid_dir / "failure-taxonomy-mismatch.json")
    assert registry().validate(record) == []  # pattern-valid, registry-invalid
    store = FixtureStore(records_dir)
    records = store.as_plain_dict()
    records[record["failure_id"]] = record
    problems = IntegrityChecker(records).check()
    assert any("NOT_A_REAL_CLASS" in message for message in problems[record["failure_id"]])


def test_bad_reference_caught(records_dir, invalid_dir):
    record = _load(invalid_dir / "eval-bad-reference.json")
    store = FixtureStore(records_dir)
    records = store.as_plain_dict()
    records[record["evaluation_id"]] = record
    problems = IntegrityChecker(records).check()
    assert any("does not resolve" in message for message in problems[record["evaluation_id"]])


def test_bad_hash_caught(records_dir, invalid_dir):
    record = _load(invalid_dir / "run-bad-hash.json")
    store = FixtureStore(records_dir)
    records = store.as_plain_dict()
    records[record["run_id"]] = record
    problems = IntegrityChecker(records).check()
    assert any("does not match canonical content" in message
               for message in problems[record["run_id"]])


def test_temporal_inconsistency_caught(records_dir, invalid_dir):
    store = FixtureStore(records_dir)
    records = store.as_plain_dict()
    evaluation = _load(invalid_dir / "eval-temporal-invalid.json")
    decision = _load(invalid_dir / "decision-superseded-before-effective.json")
    records[evaluation["evaluation_id"]] = evaluation
    records[decision["decision_id"]] = decision
    problems = IntegrityChecker(records).check()
    assert any("precedes" in message for message in problems[evaluation["evaluation_id"]])
    assert any("superseded_at" in message for message in problems[decision["decision_id"]])


def test_baseline_supersedes_itself_caught(records_dir):
    store = FixtureStore(records_dir)
    records = store.as_plain_dict()
    decision = json.loads(json.dumps(records["decision-2026-03-13-lore-safe-baseline-001"]))
    decision["decision_id"] = "decision-invalid-self-supersede"
    decision["supersedes_run_id"] = decision["target_run_id"]
    records[decision["decision_id"]] = decision
    problems = IntegrityChecker(records).check()
    assert any("supersedes itself" in message for message in problems[decision["decision_id"]])


def test_round_trip_serialization(records_dir):
    store = FixtureStore(records_dir)
    for loaded in store.records.values():
        round_tripped = json.loads(json.dumps(loaded.record))
        assert canonical_json(round_tripped) == canonical_json(loaded.record)


def test_schema_enums_match_registries():
    reg = registry()
    assert set(reg.experiment_status["entries"]) == {"succeeded", "failed"}
    assert reg.failure_taxonomy["taxonomy_version"] == "failure-taxonomy-v1"
    assert len(reg.failure_taxonomy["classes"]) == 18
    assert "OUT_OF_MEMORY" in reg.failure_taxonomy["classes"]
    assert set(reg.graph_health_status["entries"]) == {
        "healthy", "degraded", "stale", "rebuilding", "invalid", "unavailable"
    }
    assert set(reg.projection_status["entries"]) == {"complete", "partial", "failed"}
