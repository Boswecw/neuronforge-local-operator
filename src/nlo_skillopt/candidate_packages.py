from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .schemas import SchemaValidationError, validate_instance

ALLOWED_TARGET_PREFIXES = (
    "skills/",
    "docs/plans/skill-opt/candidates/",
)
FORBIDDEN_TARGET_PREFIXES = (
    "doc/system/",
    "apps/Author-Forge/",
    "ecosystem/Forge_Command/",
    "ecosystem/local-systems/neuronforge-local-operator/doc/system/",
)
MAX_TOTAL_CHANGED_LINES = 64


def load_candidate_package(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def target_path_policy_errors(path: str) -> list[str]:
    errors: list[str] = []
    if path.startswith("/"):
        errors.append(f"{path}: absolute paths are forbidden")
    if ".." in Path(path).parts:
        errors.append(f"{path}: parent directory traversal is forbidden")
    if any(path.startswith(prefix) for prefix in FORBIDDEN_TARGET_PREFIXES):
        errors.append(f"{path}: forbidden canonical or consumer target path")
    if not any(path.startswith(prefix) for prefix in ALLOWED_TARGET_PREFIXES):
        errors.append(
            f"{path}: target_path must start with one of {', '.join(ALLOWED_TARGET_PREFIXES)}"
        )
    return errors


def policy_errors(candidate: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    total_changed_lines = 0
    for index, patch in enumerate(candidate.get("patch_set", [])):
        prefix = f"patch_set[{index}]"
        errors.extend(f"{prefix}.target_path: {error}" for error in target_path_policy_errors(patch["target_path"]))
        changed_lines = patch["added_lines_count"] + patch["removed_lines_count"]
        total_changed_lines += changed_lines
        if changed_lines == 0:
            errors.append(f"{prefix}: patch must change at least one line")

    if total_changed_lines > MAX_TOTAL_CHANGED_LINES:
        errors.append(
            f"patch_set: total changed lines {total_changed_lines} exceeds {MAX_TOTAL_CHANGED_LINES}"
        )

    eval_summary = candidate.get("eval_summary", {})
    if candidate.get("package_state") == "ready_for_review":
        if eval_summary.get("validation_status") != "passed":
            errors.append("package_state ready_for_review requires eval_summary.validation_status passed")
        if not eval_summary.get("candidate_eval_run_id"):
            errors.append("package_state ready_for_review requires candidate_eval_run_id")
        if eval_summary.get("blocking_regressions"):
            errors.append("package_state ready_for_review cannot include blocking_regressions")

    return errors


def validate_candidate_package(candidate: dict[str, Any]) -> list[str]:
    try:
        validate_instance(candidate, "skill-candidate.v1.schema.json")
    except SchemaValidationError as exc:
        return [f"schema: {error}" for error in exc.errors]
    return policy_errors(candidate)


def validation_report(candidate: dict[str, Any]) -> dict[str, Any]:
    errors = validate_candidate_package(candidate)
    patch_count = len(candidate.get("patch_set", []))
    total_changed_lines = sum(
        patch.get("added_lines_count", 0) + patch.get("removed_lines_count", 0)
        for patch in candidate.get("patch_set", [])
    )
    return {
        "schema_version": "skill-candidate-validation-report-v1",
        "candidate_id": candidate.get("candidate_id"),
        "validation_result": "passed" if not errors else "failed",
        "allowed_target_prefixes": list(ALLOWED_TARGET_PREFIXES),
        "forbidden_target_prefixes": list(FORBIDDEN_TARGET_PREFIXES),
        "patch_count": patch_count,
        "total_changed_lines": total_changed_lines,
        "errors": errors,
        "next_action": (
            "candidate package is eligible for eval execution"
            if not errors
            else "fix schema or policy errors before eval execution"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a manual SkillCandidate.v1 package.")
    parser.add_argument("candidate_package", type=Path)
    args = parser.parse_args()

    try:
        candidate = load_candidate_package(args.candidate_package)
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({
            "schema_version": "skill-candidate-validation-report-v1",
            "candidate_id": None,
            "validation_result": "failed",
            "errors": [str(exc)],
            "next_action": "provide a readable JSON candidate package",
        }, indent=2, sort_keys=True))
        return 2

    report = validation_report(candidate)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["validation_result"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
