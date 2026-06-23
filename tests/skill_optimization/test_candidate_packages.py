import json
import subprocess
import sys

from nlo_skillopt.candidate_packages import validate_candidate_package, validation_report
from nlo_skillopt.schemas import validate_instance


HASH_A = "sha256:" + "a" * 64
HASH_B = "sha256:" + "b" * 64
BASELINE_RUN_ID = "skill-eval-run-continuity-progression-fixture-baseline-20260623"


def candidate_package(**overrides):
    package = {
        "schema_version": "skill-candidate-v1",
        "candidate_id": "skill-candidate-continuity-restraint-001",
        "skill_id": "skill-authorforge-continuity-progression-reasoning",
        "base_skill_version": "0.1.0-baseline",
        "candidate_skill_version": "0.1.1-candidate.1",
        "lane_id": "continuity-progression-reasoning",
        "package_state": "draft",
        "candidate_kind": "manual_patch",
        "patch_author": "operator",
        "created_at": "2026-06-23T00:00:00Z",
        "rationale": "Downgrade confidence for implied continuity claims with thin evidence.",
        "base_skill_hash": HASH_A,
        "candidate_skill_hash": None,
        "patch_set": [
            {
                "target_path": "docs/plans/skill-opt/candidates/continuity-progression-reasoning.skill.md",
                "operation": "add",
                "section_ref": "confidence calibration",
                "diff_summary": "Add a rule that implied mismatches require moderate or low confidence unless backed by two spans.",
                "added_lines_count": 2,
                "removed_lines_count": 0,
                "evidence_refs": [
                    {"ref_type": "eval_case", "ref_id": "cp-002"},
                    {"ref_type": "baseline_report", "ref_id": BASELINE_RUN_ID},
                ],
            }
        ],
        "eval_summary": {
            "baseline_eval_run_id": BASELINE_RUN_ID,
            "candidate_eval_run_id": None,
            "validation_status": "not_run",
            "aggregate_delta": None,
            "blocking_regressions": [],
        },
    }
    package.update(overrides)
    return package


def test_skill_candidate_schema_accepts_manual_patch_package():
    package = candidate_package()
    validate_instance(package, "skill-candidate.v1.schema.json")
    assert validate_candidate_package(package) == []
    report = validation_report(package)
    assert report["validation_result"] == "passed"
    assert report["patch_count"] == 1
    assert report["total_changed_lines"] == 2


def test_forbidden_doc_system_target_is_rejected():
    package = candidate_package()
    package["patch_set"][0]["target_path"] = "doc/system/20_runtime/06-continuity-progression-reasoning-lane-plan.md"
    errors = validate_candidate_package(package)
    assert any("forbidden canonical or consumer target path" in error for error in errors)


def test_target_must_stay_inside_candidate_or_skill_prefix():
    package = candidate_package()
    package["patch_set"][0]["target_path"] = "docs/continuity-progression-review-rubric.md"
    errors = validate_candidate_package(package)
    assert any("target_path must start with one of" in error for error in errors)


def test_total_changed_line_budget_is_enforced():
    package = candidate_package()
    package["patch_set"] = [
        {
            **package["patch_set"][0],
            "section_ref": f"section {index}",
            "added_lines_count": 20,
            "removed_lines_count": 0,
        }
        for index in range(4)
    ]
    errors = validate_candidate_package(package)
    assert any("total changed lines 80 exceeds 64" in error for error in errors)


def test_ready_for_review_requires_candidate_eval_and_clean_validation():
    package = candidate_package(package_state="ready_for_review")
    errors = validate_candidate_package(package)
    assert any("validation_status passed" in error for error in errors)
    assert any("requires candidate_eval_run_id" in error for error in errors)

    package["eval_summary"] = {
        "baseline_eval_run_id": BASELINE_RUN_ID,
        "candidate_eval_run_id": "skill-eval-run-continuity-candidate-001",
        "validation_status": "passed",
        "aggregate_delta": 0.05,
        "blocking_regressions": [],
    }
    assert validate_candidate_package(package) == []


def test_cli_validation_reports_policy_failure(tmp_path, repo_root):
    package = candidate_package()
    package["patch_set"][0]["target_path"] = "apps/Author-Forge/src/forbidden.md"
    path = tmp_path / "candidate.json"
    path.write_text(json.dumps(package), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "scripts/skillopt/validate_candidate.py", str(path)],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    report = json.loads(result.stdout)
    assert report["validation_result"] == "failed"
    assert any("forbidden canonical or consumer target path" in error for error in report["errors"])
