import json
import subprocess
import sys

from nlo_skillopt.promotion_receipts import (
    APPROVAL_PHRASE,
    build_promotion_receipt,
    validate_promotion_receipt,
    validation_report,
)
from nlo_skillopt.schemas import validate_instance

HASH_A = "sha256:" + "a" * 64
HASH_B = "sha256:" + "b" * 64
HASH_C = "sha256:" + "c" * 64
BASELINE_RUN_ID = "skill-eval-run-continuity-progression-fixture-baseline-20260623"
CANDIDATE_RUN_ID = "skill-eval-run-continuity-candidate-001"


def candidate_package(**overrides):
    package = {
        "schema_version": "skill-candidate-v1",
        "candidate_id": "skill-candidate-continuity-restraint-001",
        "skill_id": "skill-authorforge-continuity-progression-reasoning",
        "base_skill_version": "0.1.0-baseline",
        "candidate_skill_version": "0.1.1",
        "lane_id": "continuity-progression-reasoning",
        "package_state": "ready_for_review",
        "candidate_kind": "manual_patch",
        "patch_author": "operator",
        "created_at": "2026-06-23T00:00:00Z",
        "rationale": "Downgrade confidence for implied continuity claims with thin evidence.",
        "base_skill_hash": HASH_A,
        "candidate_skill_hash": HASH_B,
        "patch_set": [
            {
                "target_path": "skills/continuity-progression-reasoning.skill.md",
                "operation": "replace",
                "section_ref": "confidence calibration",
                "diff_summary": "Require two spans before high confidence.",
                "added_lines_count": 2,
                "removed_lines_count": 1,
                "evidence_refs": [
                    {"ref_type": "eval_case", "ref_id": "cp-002"},
                    {"ref_type": "baseline_report", "ref_id": BASELINE_RUN_ID},
                ],
            }
        ],
        "eval_summary": {
            "baseline_eval_run_id": BASELINE_RUN_ID,
            "candidate_eval_run_id": CANDIDATE_RUN_ID,
            "validation_status": "passed",
            "aggregate_delta": 0.05,
            "blocking_regressions": [],
        },
    }
    package.update(overrides)
    return package


def dry_run_receipt(**overrides):
    receipt = {
        "receipt_id": "skillopt-dry-run-continuity-restraint-001",
        "status": "passed",
        "command_hash": HASH_B,
        "output_hash": HASH_C,
        "created_at": "2026-06-23T00:05:00Z",
    }
    receipt.update(overrides)
    return receipt


def promotion_receipt(candidate=None, **overrides):
    candidate = candidate or candidate_package()
    receipt = build_promotion_receipt(
        candidate,
        dry_run_receipt=dry_run_receipt(),
        approver="charlie",
        approved_at="2026-06-23T00:10:00Z",
        target_path="skills/promoted/continuity-progression-reasoning.skill.md",
        previous_promoted_version="0.1.0",
        previous_receipt_id="skill-promotion-receipt-continuity-restraint-000",
    )
    receipt.update(overrides)
    return receipt


def test_skill_promotion_receipt_schema_accepts_valid_receipt():
    candidate = candidate_package()
    receipt = promotion_receipt(candidate)

    validate_instance(receipt, "skill-promotion-receipt.v1.schema.json")
    assert validate_promotion_receipt(receipt, candidate) == []
    assert receipt["approval_phrase"] == APPROVAL_PHRASE
    assert receipt["rollback_ref"]["skill_version"] == "0.1.0"


def test_promotion_receipt_rejects_candidate_not_ready_for_review():
    candidate = candidate_package(package_state="validated")
    receipt = promotion_receipt(candidate)

    errors = validate_promotion_receipt(receipt, candidate)
    assert any("package_state must be ready_for_review" in error for error in errors)


def test_promotion_receipt_rejects_blocking_regressions():
    candidate = candidate_package()
    candidate["eval_summary"] = {
        **candidate["eval_summary"],
        "blocking_regressions": ["cp-011 regressed"],
    }
    receipt = promotion_receipt(candidate)

    errors = validate_promotion_receipt(receipt, candidate)
    assert any("blocking_regressions" in error for error in errors)


def test_promotion_receipt_rejects_failed_dry_run():
    candidate = candidate_package()
    receipt = promotion_receipt(candidate)
    receipt["dry_run_receipt"] = dry_run_receipt(status="failed")

    errors = validate_promotion_receipt(receipt, candidate)
    assert any("dry_run_receipt.status" in error for error in errors)


def test_promotion_receipt_rejects_noncanonical_target_path():
    candidate = candidate_package()
    receipt = promotion_receipt(candidate, target_path="skills/continuity.skill.md")

    errors = validate_promotion_receipt(receipt, candidate)
    assert any("target_path must start with skills/promoted/" in error for error in errors)


def test_promotion_receipt_rejects_candidate_lineage_mismatch():
    candidate = candidate_package()
    receipt = promotion_receipt(candidate, candidate_eval_run_id="skill-eval-run-other-001")

    errors = validate_promotion_receipt(receipt, candidate)
    assert any("candidate_eval_run_id must match source candidate" in error for error in errors)


def test_promotion_receipt_validation_report_is_stable():
    candidate = candidate_package()
    receipt = promotion_receipt(candidate)
    report = validation_report(receipt, candidate)

    assert report["validation_result"] == "passed"
    assert report["candidate_id"] == candidate["candidate_id"]
    assert report["canonical_promoted_skill_prefix"] == "skills/promoted/"


def test_cli_validation_reports_failure(tmp_path, repo_root):
    candidate = candidate_package()
    receipt = promotion_receipt(candidate)
    receipt["approval_phrase"] = "I approve something else"

    candidate_path = tmp_path / "candidate.json"
    receipt_path = tmp_path / "receipt.json"
    candidate_path.write_text(json.dumps(candidate), encoding="utf-8")
    receipt_path.write_text(json.dumps(receipt), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/skillopt/validate_promotion_receipt.py",
            str(receipt_path),
            "--candidate-package",
            str(candidate_path),
        ],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    report = json.loads(result.stdout)
    assert report["validation_result"] == "failed"
    assert any("approval_phrase" in error for error in report["errors"])
