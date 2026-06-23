import json
import subprocess
import sys

from nlo_skillopt.evidence_store import (
    append_candidate_evidence,
    read_eval_cases,
    read_skill_spec,
    reconstruct_eval_run,
    write_foundation_snapshot,
)
from nlo_skillopt.schemas import validate_instance

HASH_A = "sha256:" + "a" * 64
BASELINE_RUN_ID = "skill-eval-run-continuity-progression-fixture-baseline-20260623"


def candidate_package():
    return {
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


def test_foundation_snapshot_is_reconstructable_from_evidence(tmp_path):
    manifest = write_foundation_snapshot(tmp_path)

    assert manifest["schema_version"] == "skillopt-evidence-manifest-v1"
    assert manifest["record_counts"]["eval_cases"] == 12
    assert manifest["record_counts"]["eval_runs"] == 1

    spec = read_skill_spec(tmp_path)
    cases = read_eval_cases(tmp_path)
    report = reconstruct_eval_run(tmp_path, BASELINE_RUN_ID)

    validate_instance(spec, "skill-spec.v1.schema.json")
    assert spec["skill_id"] == "skill-authorforge-continuity-progression-reasoning"
    assert len(cases) == 12
    assert report["summary"]["cases_total"] == 12
    assert report["notes"].endswith("not a real-model performance claim.")


def test_candidate_validation_evidence_updates_manifest(tmp_path):
    write_foundation_snapshot(tmp_path)
    package = candidate_package()

    report = append_candidate_evidence(tmp_path, package)
    assert report["validation_result"] == "passed"

    manifest = json.loads((tmp_path / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["record_counts"]["candidate_packages"] == 1
    assert manifest["record_counts"]["candidate_validation_reports"] == 1

    validation_lines = (tmp_path / "candidate-validation-reports.jsonl").read_text(encoding="utf-8").splitlines()
    validation_report = json.loads(validation_lines[0])
    assert validation_report["candidate_id"] == package["candidate_id"]
    assert validation_report["validation_result"] == "passed"


def test_evidence_cli_exports_and_reads_baseline(tmp_path, repo_root):
    export_result = subprocess.run(
        [
            sys.executable,
            "scripts/skillopt/evidence_store.py",
            "export-foundation",
            "--evidence-dir",
            str(tmp_path),
        ],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
    )
    assert export_result.returncode == 0
    assert json.loads(export_result.stdout)["record_counts"]["eval_cases"] == 12

    read_result = subprocess.run(
        [
            sys.executable,
            "scripts/skillopt/evidence_store.py",
            "read-baseline",
            "--evidence-dir",
            str(tmp_path),
        ],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
    )
    assert read_result.returncode == 0
    report = json.loads(read_result.stdout)
    assert report["eval_run_id"] == BASELINE_RUN_ID
    assert report["summary"]["cases_total"] == 12
