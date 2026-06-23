from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .candidate_packages import load_candidate_package
from .continuity_cases import sha256_json
from .schemas import SchemaValidationError, validate_instance

APPROVAL_PHRASE = "I approve this SkillOpt promotion"
CANONICAL_PROMOTED_SKILL_PREFIX = "skills/promoted/"
PROMOTION_RECEIPT_SCHEMA = "skill-promotion-receipt.v1.schema.json"


def load_promotion_receipt(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def target_path_errors(target_path: str) -> list[str]:
    errors: list[str] = []
    if target_path.startswith("/"):
        errors.append(f"{target_path}: absolute paths are forbidden")
    if ".." in Path(target_path).parts:
        errors.append(f"{target_path}: parent directory traversal is forbidden")
    if not target_path.startswith(CANONICAL_PROMOTED_SKILL_PREFIX):
        errors.append(
            f"{target_path}: target_path must start with {CANONICAL_PROMOTED_SKILL_PREFIX}"
        )
    return errors


def candidate_eligibility_errors(candidate: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    eval_summary = candidate.get("eval_summary", {})

    if candidate.get("package_state") != "ready_for_review":
        errors.append("candidate package_state must be ready_for_review")
    if eval_summary.get("validation_status") != "passed":
        errors.append("candidate eval_summary.validation_status must be passed")
    if not eval_summary.get("candidate_eval_run_id"):
        errors.append("candidate requires candidate_eval_run_id")
    if eval_summary.get("blocking_regressions"):
        errors.append("candidate must not include blocking_regressions")

    return errors


def receipt_lineage_errors(receipt: dict[str, Any], candidate: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    eval_summary = candidate.get("eval_summary", {})
    expected = {
        "candidate_id": candidate.get("candidate_id"),
        "skill_id": candidate.get("skill_id"),
        "lane_id": candidate.get("lane_id"),
        "base_skill_version": candidate.get("base_skill_version"),
        "promoted_skill_version": candidate.get("candidate_skill_version"),
        "source_candidate_hash": sha256_json(candidate),
        "baseline_eval_run_id": eval_summary.get("baseline_eval_run_id"),
        "candidate_eval_run_id": eval_summary.get("candidate_eval_run_id"),
        "validation_status": eval_summary.get("validation_status"),
        "aggregate_delta": eval_summary.get("aggregate_delta"),
    }
    for key, value in expected.items():
        if receipt.get(key) != value:
            errors.append(f"{key} must match source candidate ({value!r})")

    return errors


def semantic_errors(receipt: dict[str, Any], candidate: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    errors.extend(candidate_eligibility_errors(candidate))
    errors.extend(receipt_lineage_errors(receipt, candidate))
    errors.extend(target_path_errors(receipt.get("target_path", "")))

    if receipt.get("approval_phrase") != APPROVAL_PHRASE:
        errors.append("approval_phrase does not match required SkillOpt approval phrase")
    if receipt.get("dry_run_receipt", {}).get("status") != "passed":
        errors.append("dry_run_receipt.status must be passed")
    if receipt.get("blocking_regressions"):
        errors.append("receipt must not include blocking_regressions")

    rollback_ref = receipt.get("rollback_ref", {})
    previous_version = receipt.get("previous_promoted_version")
    if previous_version:
        if rollback_ref.get("rollback_type") != "previous_version":
            errors.append("rollback_ref.rollback_type must be previous_version")
        if rollback_ref.get("skill_version") != previous_version:
            errors.append("rollback_ref.skill_version must match previous_promoted_version")
    elif rollback_ref.get("rollback_type") != "none":
        errors.append("rollback_ref.rollback_type must be none without previous version")

    return errors


def validate_promotion_receipt(receipt: dict[str, Any], candidate: dict[str, Any]) -> list[str]:
    try:
        validate_instance(candidate, "skill-candidate.v1.schema.json")
        validate_instance(receipt, PROMOTION_RECEIPT_SCHEMA)
    except SchemaValidationError as exc:
        return [f"schema: {error}" for error in exc.errors]
    return semantic_errors(receipt, candidate)


def build_promotion_receipt(
    candidate: dict[str, Any],
    *,
    dry_run_receipt: dict[str, Any],
    approver: str,
    approved_at: str,
    target_path: str,
    previous_promoted_version: str | None = None,
    previous_receipt_id: str | None = None,
    notes: str | None = None,
) -> dict[str, Any]:
    eval_summary = candidate["eval_summary"]
    receipt_id = f"skill-promotion-receipt-{candidate['candidate_id'].removeprefix('skill-candidate-')}"
    rollback_ref = {
        "rollback_type": "previous_version" if previous_promoted_version else "none",
        "skill_version": previous_promoted_version,
        "target_path": target_path if previous_promoted_version else None,
        "receipt_id": previous_receipt_id,
    }
    receipt = {
        "schema_version": "skill-promotion-receipt-v1",
        "receipt_id": receipt_id,
        "candidate_id": candidate["candidate_id"],
        "skill_id": candidate["skill_id"],
        "lane_id": candidate["lane_id"],
        "base_skill_version": candidate["base_skill_version"],
        "promoted_skill_version": candidate["candidate_skill_version"],
        "source_candidate_hash": sha256_json(candidate),
        "baseline_eval_run_id": eval_summary["baseline_eval_run_id"],
        "candidate_eval_run_id": eval_summary["candidate_eval_run_id"],
        "validation_status": eval_summary["validation_status"],
        "aggregate_delta": eval_summary["aggregate_delta"],
        "blocking_regressions": [],
        "dry_run_receipt": dry_run_receipt,
        "promotion_decision": "approved",
        "approval_phrase": APPROVAL_PHRASE,
        "approver": approver,
        "approved_at": approved_at,
        "target_path": target_path,
        "previous_promoted_version": previous_promoted_version,
        "rollback_ref": rollback_ref,
    }
    if notes:
        receipt["notes"] = notes
    return receipt


def validation_report(receipt: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    errors = validate_promotion_receipt(receipt, candidate)
    return {
        "schema_version": "skill-promotion-receipt-validation-report-v1",
        "receipt_id": receipt.get("receipt_id"),
        "candidate_id": receipt.get("candidate_id"),
        "validation_result": "passed" if not errors else "failed",
        "canonical_promoted_skill_prefix": CANONICAL_PROMOTED_SKILL_PREFIX,
        "errors": errors,
        "next_action": (
            "receipt is eligible for governed promotion execution"
            if not errors
            else "fix promotion receipt before any governed promotion execution"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a SkillPromotionReceipt.v1 record.")
    parser.add_argument("receipt", type=Path)
    parser.add_argument("--candidate-package", type=Path, required=True)
    args = parser.parse_args()

    try:
        receipt = load_promotion_receipt(args.receipt)
        candidate = load_candidate_package(args.candidate_package)
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({
            "schema_version": "skill-promotion-receipt-validation-report-v1",
            "receipt_id": None,
            "candidate_id": None,
            "validation_result": "failed",
            "errors": [str(exc)],
            "next_action": "provide readable JSON receipt and candidate package files",
        }, indent=2, sort_keys=True))
        return 2

    report = validation_report(receipt, candidate)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["validation_result"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
