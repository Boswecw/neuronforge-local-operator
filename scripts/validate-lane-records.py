#!/usr/bin/env python3
"""
NeuronForge lane analytics record validator.

Scans analytics/lanes/*.json and validates each record against:
  - JSON parseability
  - Schema conformance (schemas/lane-analytics.schema.json)
  - Filename stem matches lane_id
  - Required field presence
  - Enum constraints (status, adoption_posture, metric_provenance)
  - Date format (YYYY-MM-DD)
  - Nullability rules (nullable keys must exist)
  - Numeric metrics (not percent strings)
  - Metric provenance rules (gate eligibility constraints, notes requirements)
  - Optional: referenced path existence (warnings only)

Exit codes:
  0 — all records pass
  1 — one or more hard failures
"""

import json
import os
import re
import sys
from datetime import datetime
from glob import glob
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LANES_DIR = PROJECT_ROOT / "analytics" / "lanes"
SCHEMA_PATH = PROJECT_ROOT / "schemas" / "lane-analytics.schema.json"

VALID_STATUS = {
    "planned",
    "implementing",
    "evaluating",
    "candidate_baseline",
    "approved_baseline",
    "deferred",
    "blocked",
    "retired",
}

VALID_ADOPTION_POSTURE = {
    "blocked",
    "experimental_only",
    "review_assist_only",
    "operator_assist",
    "trusted_with_review",
    "trusted_default",
}

REQUIRED_FIELDS = [
    "$schema",
    "schema_version",
    "lane_id",
    "lane_name",
    "lane_type",
    "status",
    "required_route_class",
    "adoption_posture",
    "current_baseline_model",
    "current_baseline_prompt_profile",
    "anchor_input",
    "anchor_run_id",
    "last_evaluated_date",
    "current_judgment",
    "calibration_doc",
    "status_doc",
    "metrics",
    "next_required_decision",
    "metric_provenance",
    "metrics_gate_eligible",
    "provenance_notes",
    "metric_profile",
]

NULLABLE_FIELDS = {
    "current_baseline_model",
    "current_baseline_prompt_profile",
    "anchor_input",
    "anchor_run_id",
    "calibration_doc",
    "status_doc",
    "provenance_notes",
}

VALID_METRIC_PROVENANCE = {
    "instrument_derived",
    "benchmark_derived",
    "automated_heuristic",
    "operator_judged",
    "mixed",
}

VALID_METRIC_PROFILE = {
    "detection_reasoning",
    "editing_cleanup",
    "lore_protection_editing",
}

# Provenance classes that require provenance_notes to be non-null
PROVENANCE_REQUIRES_NOTES = {"operator_judged", "mixed"}

# Provenance classes that may never set metrics_gate_eligible = true (hard failure)
PROVENANCE_GATE_INELIGIBLE = {"operator_judged"}

REQUIRED_METRICS = ["schema_reliability", "false_positive_rate", "surface_detection_rate"]

DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")

SUPPORTED_SCHEMA_VERSIONS = {"1.0"}

# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------


class Result:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.hard_failures: list[str] = []
        self.warnings: list[str] = []

    def fail(self, category: str, message: str):
        self.hard_failures.append(f"[{category}] {message}")

    def warn(self, category: str, message: str):
        self.warnings.append(f"[{category}] {message}")

    @property
    def passed(self) -> bool:
        return len(self.hard_failures) == 0


# ---------------------------------------------------------------------------
# Validation steps
# ---------------------------------------------------------------------------


def validate_json(file_path: Path, result: Result) -> dict | None:
    try:
        with open(file_path, encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        result.fail("malformed_json", f"JSON parse error: {e}")
        return None
    except OSError as e:
        result.fail("malformed_json", f"Cannot read file: {e}")
        return None


def validate_schema_version(record: dict, result: Result) -> bool:
    version = record.get("schema_version")
    if version not in SUPPORTED_SCHEMA_VERSIONS:
        result.fail(
            "unsupported_schema_version",
            f"schema_version must be one of {sorted(SUPPORTED_SCHEMA_VERSIONS)}, got: {version!r}",
        )
        return False
    return True


def validate_required_fields(record: dict, result: Result):
    for field in REQUIRED_FIELDS:
        if field not in record:
            result.fail("missing_required_field", f"Required field missing: '{field}'")


def validate_nullability(record: dict, result: Result):
    for field in NULLABLE_FIELDS:
        if field not in record:
            result.fail(
                "missing_required_field",
                f"Nullable field key must still exist: '{field}' is absent",
            )
        elif record[field] is not None and not isinstance(record[field], str):
            result.fail(
                "schema_validation_failed",
                f"Field '{field}' must be a string or null, got: {type(record[field]).__name__}",
            )


def validate_enums(record: dict, result: Result):
    status = record.get("status")
    if status is not None and status not in VALID_STATUS:
        result.fail(
            "invalid_enum",
            f"'status' value {status!r} is not valid. Allowed: {sorted(VALID_STATUS)}",
        )

    posture = record.get("adoption_posture")
    if posture is not None and posture not in VALID_ADOPTION_POSTURE:
        result.fail(
            "invalid_enum",
            f"'adoption_posture' value {posture!r} is not valid. Allowed: {sorted(VALID_ADOPTION_POSTURE)}",
        )

    provenance = record.get("metric_provenance")
    if provenance is not None and provenance not in VALID_METRIC_PROVENANCE:
        result.fail(
            "invalid_enum",
            f"'metric_provenance' value {provenance!r} is not valid. Allowed: {sorted(VALID_METRIC_PROVENANCE)}",
        )

    profile = record.get("metric_profile")
    if profile is not None and profile not in VALID_METRIC_PROFILE:
        result.fail(
            "invalid_enum",
            f"'metric_profile' value {profile!r} is not valid. Allowed: {sorted(VALID_METRIC_PROFILE)}",
        )


def validate_metric_provenance(record: dict, result: Result):
    provenance = record.get("metric_provenance")
    gate_eligible = record.get("metrics_gate_eligible")
    notes = record.get("provenance_notes")

    if provenance is None:
        return  # missing_required_field already caught

    # Rule: operator_judged cannot be gate eligible (hard failure)
    if provenance in PROVENANCE_GATE_INELIGIBLE and gate_eligible is True:
        result.fail(
            "invalid_provenance",
            f"'metrics_gate_eligible' cannot be true when 'metric_provenance' is {provenance!r}. "
            f"Gate eligibility requires benchmark_derived or instrument_derived evidence.",
        )

    # Rule: operator_judged and mixed require non-null provenance_notes
    if provenance in PROVENANCE_REQUIRES_NOTES:
        if notes is None:
            result.fail(
                "invalid_provenance",
                f"'provenance_notes' must be a non-null string when 'metric_provenance' is {provenance!r}. "
                f"Explain the derivation method.",
            )
        elif isinstance(notes, str) and len(notes.strip()) == 0:
            result.fail(
                "invalid_provenance",
                f"'provenance_notes' must not be empty when 'metric_provenance' is {provenance!r}.",
            )

    # Rule: metrics_gate_eligible must be a boolean
    if gate_eligible is not None and not isinstance(gate_eligible, bool):
        result.fail(
            "schema_validation_failed",
            f"'metrics_gate_eligible' must be a boolean, got: {type(gate_eligible).__name__}",
        )


def validate_id_match(record: dict, file_path: Path, result: Result):
    expected = file_path.stem
    actual = record.get("lane_id")
    if actual != expected:
        result.fail(
            "id_mismatch",
            f"'lane_id' ({actual!r}) does not match filename stem ({expected!r})",
        )


def validate_date(record: dict, result: Result):
    date_str = record.get("last_evaluated_date")
    if date_str is None:
        return  # missing_required_field already caught above
    if not isinstance(date_str, str):
        result.fail("invalid_date", f"'last_evaluated_date' must be a string, got: {type(date_str).__name__}")
        return
    if not DATE_PATTERN.match(date_str):
        result.fail("invalid_date", f"'last_evaluated_date' must be YYYY-MM-DD, got: {date_str!r}")
        return
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        result.fail("invalid_date", f"'last_evaluated_date' is not a valid calendar date: {date_str!r}")


def validate_metrics(record: dict, result: Result):
    metrics = record.get("metrics")
    if metrics is None:
        return  # missing_required_field already caught
    if not isinstance(metrics, dict):
        result.fail("schema_validation_failed", f"'metrics' must be an object, got: {type(metrics).__name__}")
        return

    for key in REQUIRED_METRICS:
        if key not in metrics:
            result.fail("missing_required_field", f"'metrics.{key}' is required")
        else:
            value = metrics[key]
            if isinstance(value, str):
                result.fail(
                    "schema_validation_failed",
                    f"'metrics.{key}' must be a number, not a string ({value!r}). Do not use percent strings.",
                )
            elif not isinstance(value, (int, float)):
                result.fail(
                    "schema_validation_failed",
                    f"'metrics.{key}' must be a number, got: {type(value).__name__}",
                )
            elif not (0.0 <= float(value) <= 1.0):
                result.fail(
                    "schema_validation_failed",
                    f"'metrics.{key}' must be between 0.0 and 1.0, got: {value}",
                )


def validate_string_fields(record: dict, result: Result):
    required_non_null_strings = [
        "$schema", "schema_version", "lane_id", "lane_name", "lane_type",
        "status", "required_route_class", "adoption_posture",
        "last_evaluated_date", "current_judgment", "next_required_decision",
        "metric_provenance", "metric_profile",
    ]
    for field in required_non_null_strings:
        value = record.get(field)
        if value is not None and not isinstance(value, str):
            result.fail(
                "schema_validation_failed",
                f"'{field}' must be a string, got: {type(value).__name__}",
            )
        elif isinstance(value, str) and len(value.strip()) == 0:
            result.fail(
                "schema_validation_failed",
                f"'{field}' must not be an empty string",
            )


def validate_path_references(record: dict, result: Result):
    path_fields = ["anchor_input", "calibration_doc", "status_doc"]
    for field in path_fields:
        value = record.get(field)
        if value is None:
            continue
        full_path = PROJECT_ROOT / value
        if not full_path.exists():
            result.warn(
                "missing_referenced_path",
                f"'{field}' references a path that does not exist: {value!r}",
            )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def validate_file(file_path: Path) -> Result:
    result = Result(str(file_path.relative_to(PROJECT_ROOT)))

    record = validate_json(file_path, result)
    if record is None:
        return result

    if not validate_schema_version(record, result):
        return result

    validate_required_fields(record, result)
    validate_nullability(record, result)
    validate_enums(record, result)
    validate_metric_provenance(record, result)
    validate_id_match(record, file_path, result)
    validate_date(record, result)
    validate_metrics(record, result)
    validate_string_fields(record, result)
    validate_path_references(record, result)

    return result


def main() -> int:
    if not LANES_DIR.exists():
        print(f"ERROR: Lane records directory not found: {LANES_DIR}", file=sys.stderr)
        return 1

    lane_files = sorted(LANES_DIR.glob("*.json"))
    if not lane_files:
        print(f"WARNING: No lane records found in {LANES_DIR}", file=sys.stderr)
        return 0

    all_passed = True
    for file_path in lane_files:
        result = validate_file(file_path)
        status_label = "PASS" if result.passed else "FAIL"
        print(f"{status_label}  {result.file_path}")

        for msg in result.hard_failures:
            print(f"       ERROR: {msg}")
            all_passed = False

        for msg in result.warnings:
            print(f"       WARN:  {msg}")

    print()
    if all_passed:
        print(f"All {len(lane_files)} lane record(s) passed validation.")
        return 0
    else:
        print(f"Validation failed. Fix errors above before committing.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
