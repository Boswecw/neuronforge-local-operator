import copy

import pytest
from jsonschema import Draft202012Validator

from nlo_skillopt.continuity_cases import (
    build_continuity_eval_cases,
    build_fixture_baseline_report,
    build_skill_spec,
)
from nlo_skillopt.schemas import SCHEMA_DIR, SchemaValidationError, load_schema, validate_instance


SCHEMAS = (
    "skill-candidate.v1.schema.json",
    "skill-spec.v1.schema.json",
    "skill-eval-case.v1.schema.json",
    "skill-eval-run.v1.schema.json",
)


def test_skill_optimization_schemas_are_valid_json_schema():
    for schema_name in SCHEMAS:
        Draft202012Validator.check_schema(load_schema(schema_name))


def test_skill_spec_fixture_is_schema_valid():
    spec = build_skill_spec()
    validate_instance(spec, "skill-spec.v1.schema.json")
    assert spec["skill_id"] == "skill-authorforge-continuity-progression-reasoning"
    assert spec["artifact_posture"] == "candidate_only"
    assert spec["state"] == "candidate_baseline"


def test_continuity_case_packets_convert_to_eval_cases():
    cases = build_continuity_eval_cases()
    assert len(cases) == 12
    assert {case["case_id"] for case in cases} == {f"cp-{i:03d}" for i in range(1, 13)}
    assert all(case["active"] for case in cases)
    assert all(case["blocked_reason"] is None for case in cases)
    assert [case["split"] for case in cases].count("train") == 6
    assert [case["split"] for case in cases].count("validation") == 4
    assert [case["split"] for case in cases].count("regression") == 2
    assert all(case["source_packet_hash"].startswith("sha256:") for case in cases)
    assert all(case["source_refs"] for case in cases)


def test_partial_expectations_are_preserved():
    cases = {case["case_id"]: case for case in build_continuity_eval_cases()}
    assert cases["cp-005"]["no_finding_acceptable"] == "partial"
    assert cases["cp-008"]["finding_expected"] == "partial"
    assert "finding_partial" in cases["cp-008"]["scoring_tags"]


def test_eval_case_schema_rejects_missing_hash():
    case = copy.deepcopy(build_continuity_eval_cases()[0])
    case.pop("source_packet_hash")
    with pytest.raises(SchemaValidationError) as exc:
        validate_instance(case, "skill-eval-case.v1.schema.json")
    assert "source_packet_hash" in str(exc.value)


def test_fixture_baseline_report_is_schema_valid_and_not_model_claim():
    report = build_fixture_baseline_report()
    validate_instance(report, "skill-eval-run.v1.schema.json")
    assert report["runner_mode"] == "fixture"
    assert report["model_id"] is None
    assert report["summary"]["cases_total"] == 12
    assert report["summary"]["schema_valid_count"] == 12
    assert report["summary"]["blocking_failure_count"] == 0
    assert report["summary"]["aggregate_score"] == 0.9917
    assert "not a real-model performance claim" in report["notes"]


def test_schema_directory_is_repo_local(repo_root):
    assert SCHEMA_DIR == repo_root / "schemas" / "skill_optimization"
