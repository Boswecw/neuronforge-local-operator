#!/usr/bin/env python3
"""
Strict schema validator for continuity-progression-reasoning candidate output.

Task contract: analyze.continuity.adjacent_scene.v1
Schema:        continuity candidate schema v1.0

Usage:
  python3 scripts/validate-continuity-candidate.py <json_file>
  python3 scripts/validate-continuity-candidate.py -   (reads stdin)

Exit codes:
  0  = valid
  1  = schema violation (fail-closed)
  2  = cannot parse JSON (fail-closed)

Outputs validation result JSON to stdout.
"""

import json
import re
import sys
from datetime import datetime, timezone

LANE_ID = "continuity-progression-reasoning"
SCHEMA_VERSION = "1.0"
RUN_POSTURE = "candidate_only"

VALID_SCOPE_TYPES = {
    "scene_local",
    "adjacent_scene",
    "scene_window",
    "chapter_window",
}

VALID_FINDING_TYPES = {
    "continuity_tension",
    "progression_break",
    "transition_gap",
    "descriptive_mismatch",
    "repeated_movement",
    "escalation_mismatch",
    "state_carry_forward_issue",
    "causal_link_unclear",
}

VALID_CONFIDENCE = {"low", "moderate", "high"}

VALID_SPAN_ROLES = {
    "setup",
    "contrast",
    "carry_forward",
    "mismatch_signal",
    "transition_signal",
    "progression_signal",
}

VALID_CANDIDATE_STATES = {
    "candidate_unreviewed",
    "candidate_review_in_progress",
    "candidate_retained",
    "candidate_rejected",
    "candidate_promoted",
}

VALID_SEVERITY_HINTS = {"minor", "moderate", "major"}

AUTHORITY_PATTERNS = [
    r"\bdefinitely\b",
    r"\bproves\b",
    r"\bconfirms\b",
    r"\bestablishes\b",
    r"\bcanonically shows\b",
    r"\bis true that\b",
    r"\bcertainly\b",
    r"\bundeniably\b",
]

TRIVIAL_NOTES = {"none", "no uncertainty", "n/a", "", "review this", "see issue", "review"}


def build_result(valid, failure_reason=None, findings_count=None, warnings=None):
    r = {
        "validation_result": "valid" if valid else "fail_closed",
        "schema_version_checked": SCHEMA_VERSION,
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    if failure_reason is not None:
        r["failure_reason"] = failure_reason
    if findings_count is not None:
        r["findings_count"] = findings_count
    if warnings:
        r["warnings"] = warnings
    return r


def check_authority_language(text: str) -> list[str]:
    found = []
    for pattern in AUTHORITY_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            found.append(pattern.replace(r"\b", "").strip())
    return found


def validate_evidence_span(span, index: int, run_scene_ids: set, prefix: str):
    if not isinstance(span, dict):
        return f"{prefix}: must be an object"
    for sf in ("scene_id", "span_text", "span_role"):
        if sf not in span:
            return f"{prefix}: missing required field: {sf!r}"
    if span["span_role"] not in VALID_SPAN_ROLES:
        return f"{prefix}: invalid span_role: {span['span_role']!r}"
    if span["scene_id"] not in run_scene_ids:
        return f"{prefix}: scene_id {span['scene_id']!r} not in run scope {sorted(run_scene_ids)}"
    if not isinstance(span["span_text"], str) or not span["span_text"].strip():
        return f"{prefix}: span_text must be a non-empty string"
    return None


def validate_finding(finding, index: int, run_scene_ids: set) -> tuple[str | None, list[str]]:
    warnings = []
    prefix = f"finding[{index}]"

    if not isinstance(finding, dict):
        return f"{prefix}: must be an object", warnings

    required = (
        "finding_id", "finding_label", "finding_type", "claim",
        "scope_type", "scope_bounds", "evidence_spans",
        "confidence", "uncertainty_note", "review_note", "candidate_state",
    )
    for field in required:
        if field not in finding:
            return f"{prefix}: missing required field: {field!r}", warnings

    if finding["finding_type"] not in VALID_FINDING_TYPES:
        return f"{prefix}: invalid finding_type: {finding['finding_type']!r}", warnings

    if finding["confidence"] not in VALID_CONFIDENCE:
        return f"{prefix}: invalid confidence: {finding['confidence']!r}", warnings

    if finding["scope_type"] not in VALID_SCOPE_TYPES:
        return f"{prefix}: invalid scope_type: {finding['scope_type']!r}", warnings

    if finding["candidate_state"] not in VALID_CANDIDATE_STATES:
        return f"{prefix}: invalid candidate_state: {finding['candidate_state']!r}", warnings

    # Scope bounds
    fbounds = finding["scope_bounds"]
    if not isinstance(fbounds, dict) or "scene_ids" not in fbounds:
        return f"{prefix}: scope_bounds must be an object with scene_ids", warnings
    finding_scene_ids = set(fbounds["scene_ids"])
    out_of_scope = finding_scene_ids - run_scene_ids
    if out_of_scope:
        return (
            f"{prefix}: scope_bounds references scenes outside run scope: {sorted(out_of_scope)}",
            warnings,
        )

    # Evidence spans
    evidence = finding["evidence_spans"]
    if not isinstance(evidence, list) or len(evidence) == 0:
        return f"{prefix}: evidence_spans must be a non-empty array", warnings

    for j, span in enumerate(evidence):
        span_prefix = f"{prefix}.evidence_spans[{j}]"
        err = validate_evidence_span(span, j, run_scene_ids, span_prefix)
        if err:
            return err, warnings

    # Authority language in claim
    auth = check_authority_language(finding["claim"])
    if auth:
        return f"{prefix}: authority language detected in claim: {auth}", warnings

    # Substantive uncertainty note
    uncertainty_text = finding.get("uncertainty_note", "").strip().lower()
    if uncertainty_text in TRIVIAL_NOTES:
        return (
            f"{prefix}: uncertainty_note must be substantive, got: {finding['uncertainty_note']!r}",
            warnings,
        )

    # Substantive review note
    review_text = finding.get("review_note", "").strip().lower()
    if review_text in TRIVIAL_NOTES:
        return (
            f"{prefix}: review_note must be substantive, got: {finding['review_note']!r}",
            warnings,
        )

    # Optional field validation
    if "severity_hint" in finding and finding["severity_hint"] not in VALID_SEVERITY_HINTS:
        return f"{prefix}: invalid severity_hint: {finding['severity_hint']!r}", warnings

    # Cross-scene evidence warning
    if finding["scope_type"] in ("adjacent_scene", "scene_window", "chapter_window"):
        if len(evidence) < 2:
            warnings.append(
                f"{prefix}: cross-scene finding has only {len(evidence)} evidence span(s); "
                f"2+ recommended for cross-scene claims"
            )

    return None, warnings


def validate(data: dict) -> tuple[bool, str | None, list[str]]:
    warnings = []

    if not isinstance(data, dict):
        return False, "top-level output must be a JSON object", warnings

    required_top = (
        "schema_version", "lane_id", "analysis_scope_type",
        "analysis_scope_bounds", "input_unit_ids",
        "candidate_findings", "overall_run_note", "run_posture",
    )
    for field in required_top:
        if field not in data:
            return False, f"missing required top-level field: {field!r}", warnings

    if data["schema_version"] != SCHEMA_VERSION:
        return False, f"schema_version must be {SCHEMA_VERSION!r}, got: {data['schema_version']!r}", warnings

    if data["lane_id"] != LANE_ID:
        return False, f"lane_id must be {LANE_ID!r}, got: {data['lane_id']!r}", warnings

    if data["analysis_scope_type"] not in VALID_SCOPE_TYPES:
        return False, f"invalid analysis_scope_type: {data['analysis_scope_type']!r}", warnings

    if data["run_posture"] != RUN_POSTURE:
        return False, f"run_posture must be {RUN_POSTURE!r}, got: {data['run_posture']!r}", warnings

    scope_bounds = data["analysis_scope_bounds"]
    if not isinstance(scope_bounds, dict) or "scene_ids" not in scope_bounds:
        return False, "analysis_scope_bounds must be an object with scene_ids", warnings

    run_scene_ids = set(scope_bounds["scene_ids"])
    if len(run_scene_ids) == 0:
        return False, "analysis_scope_bounds.scene_ids must not be empty", warnings

    if not isinstance(data["input_unit_ids"], list):
        return False, "input_unit_ids must be an array", warnings

    if not isinstance(data["candidate_findings"], list):
        return False, "candidate_findings must be an array", warnings

    overall_note = data.get("overall_run_note", "")
    if not isinstance(overall_note, str) or not overall_note.strip():
        return False, "overall_run_note must be a non-empty string", warnings

    for i, finding in enumerate(data["candidate_findings"]):
        err, finding_warnings = validate_finding(finding, i, run_scene_ids)
        warnings.extend(finding_warnings)
        if err:
            return False, err, warnings

    return True, None, warnings


def strip_think_blocks(text: str) -> str:
    """Remove <think>...</think> blocks produced by reasoning models."""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)


def extract_json(text: str) -> str | None:
    """Extract JSON object from model output that may contain markdown fences or prose."""
    text = strip_think_blocks(text).strip()
    if text.startswith("{"):
        return text
    # Strip markdown fences
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        return match.group(1)
    # Find first { to last }
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return text[start : end + 1]
    return None


def main():
    if len(sys.argv) < 2:
        print(
            json.dumps({"error": "Usage: validate-continuity-candidate.py <file|->"}),
            file=sys.stderr,
        )
        sys.exit(2)

    arg = sys.argv[1]
    if arg == "-":
        raw = sys.stdin.read()
    else:
        try:
            with open(arg) as f:
                raw = f.read()
        except FileNotFoundError:
            out = build_result(False, f"file not found: {arg}")
            print(json.dumps(out, indent=2))
            sys.exit(1)

    json_text = extract_json(raw)
    if json_text is None:
        out = build_result(False, "cannot find JSON object in model output")
        print(json.dumps(out, indent=2))
        sys.exit(2)

    try:
        data = json.loads(json_text)
    except json.JSONDecodeError as e:
        out = build_result(False, f"JSON parse error: {e}")
        print(json.dumps(out, indent=2))
        sys.exit(2)

    valid, failure_reason, warnings = validate(data)
    findings_count = len(data.get("candidate_findings", [])) if valid else None
    out = build_result(
        valid,
        failure_reason=failure_reason,
        findings_count=findings_count,
        warnings=warnings if warnings else None,
    )
    print(json.dumps(out, indent=2))
    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
