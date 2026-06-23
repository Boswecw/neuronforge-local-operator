from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from .schemas import REPO_ROOT, validate_instance

LANE_ID = "continuity-progression-reasoning"
SKILL_ID = "skill-authorforge-continuity-progression-reasoning"
SKILL_VERSION = "0.1.0-baseline"
CASE_PACK_ID = "continuity-progression-case-pack-v1"
RUBRIC_REF = "docs/continuity-progression-review-rubric.md"
CREATED_AT = "2026-06-23T00:00:00Z"
FIXTURE_ID = "continuity-progression-case-pack-v1-fixture-baseline"

CASE_PACKET_DIR = REPO_ROOT / "inputs" / "case-packets"

SPLIT_BY_CASE_ID = {
    "cp-001": "train",
    "cp-002": "train",
    "cp-003": "train",
    "cp-004": "train",
    "cp-005": "train",
    "cp-006": "train",
    "cp-007": "validation",
    "cp-008": "validation",
    "cp-009": "validation",
    "cp-010": "validation",
    "cp-011": "regression",
    "cp-012": "regression",
}


def canonical_json(data: Any) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_json(data: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(data).encode("utf-8")).hexdigest()


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def repo_relative(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def load_case_packet(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def packet_paths(case_packet_dir: Path = CASE_PACKET_DIR) -> list[Path]:
    return sorted(case_packet_dir.glob("cp-[0-9][0-9][0-9].json"))


def scoring_tags(packet: dict[str, Any]) -> list[str]:
    metadata = packet["packet_metadata"]
    tags = {
        metadata["primary_category"],
        metadata.get("secondary_category") or "no_secondary_category",
        metadata["expected_review_posture"],
        metadata["expected_restraint_posture"],
    }
    if metadata.get("finding_expected") is True:
        tags.add("finding_expected")
    elif metadata.get("finding_expected") == "partial":
        tags.add("finding_partial")
    else:
        tags.add("finding_not_expected")
    if metadata.get("no_finding_acceptable") is True:
        tags.add("no_finding_acceptable")
    elif metadata.get("no_finding_acceptable") == "partial":
        tags.add("no_finding_partially_acceptable")
    else:
        tags.add("no_finding_not_acceptable")
    return sorted(tags)


def source_refs(packet: dict[str, Any]) -> list[dict[str, str]]:
    refs: list[dict[str, str]] = []
    if "scene_a_text" in packet and "scene_a_id" in packet:
        refs.append({
            "unit_id": packet["scene_a_id"],
            "field": "scene_a_text",
            "content_hash": sha256_text(packet["scene_a_text"]),
        })
    if "scene_b_text" in packet and "scene_b_id" in packet:
        refs.append({
            "unit_id": packet["scene_b_id"],
            "field": "scene_b_text",
            "content_hash": sha256_text(packet["scene_b_text"]),
        })
    if not refs:
        refs.append({
            "unit_id": packet["scene_packet_id"],
            "field": "source_packet",
            "content_hash": sha256_json(packet),
        })
    return refs


def input_unit_ids(packet: dict[str, Any]) -> list[str]:
    ids = []
    for field in ("scene_a_id", "scene_b_id", "scene_packet_id"):
        value = packet.get(field)
        if value and value not in ids:
            ids.append(value)
    return ids


def build_skill_eval_case(path: Path) -> dict[str, Any]:
    packet = load_case_packet(path)
    metadata = packet["packet_metadata"]
    case_id = packet["scene_packet_id"]
    record = {
        "schema_version": "skill-eval-case-v1",
        "case_id": case_id,
        "skill_id": SKILL_ID,
        "lane_id": LANE_ID,
        "case_pack_id": CASE_PACK_ID,
        "split": SPLIT_BY_CASE_ID.get(case_id, "blocked"),
        "active": case_id in SPLIT_BY_CASE_ID,
        "blocked_reason": None if case_id in SPLIT_BY_CASE_ID else "case not assigned to first executable split",
        "task_id": packet["task_id"],
        "scope_label": packet["scope_label"],
        "source_packet_ref": repo_relative(path),
        "source_packet_hash": sha256_json(packet),
        "input_unit_ids": input_unit_ids(packet),
        "primary_category": metadata["primary_category"],
        "secondary_category": metadata.get("secondary_category"),
        "expected_review_posture": metadata["expected_review_posture"],
        "expected_restraint_posture": metadata["expected_restraint_posture"],
        "finding_expected": metadata["finding_expected"],
        "no_finding_acceptable": metadata["no_finding_acceptable"],
        "scoring_tags": scoring_tags(packet),
        "case_purpose": metadata["case_purpose"],
        "reviewer_note": metadata.get("reviewer_note"),
        "source_refs": source_refs(packet),
        "created_at": CREATED_AT,
    }
    validate_instance(record, "skill-eval-case.v1.schema.json")
    return record


def build_continuity_eval_cases(case_packet_dir: Path = CASE_PACKET_DIR) -> list[dict[str, Any]]:
    cases = [build_skill_eval_case(path) for path in packet_paths(case_packet_dir)]
    case_ids = [case["case_id"] for case in cases]
    if len(case_ids) != len(set(case_ids)):
        raise ValueError("duplicate continuity/progression case ids found")
    return cases


def build_skill_spec() -> dict[str, Any]:
    spec = {
        "schema_version": "skill-spec-v1",
        "skill_id": SKILL_ID,
        "skill_version": SKILL_VERSION,
        "lane_id": LANE_ID,
        "owner": "neuronforge-local-operator",
        "state": "candidate_baseline",
        "artifact_posture": "candidate_only",
        "source_path": "docs/continuity-progression-review-rubric.md",
        "skill_document_hash": sha256_text((REPO_ROOT / RUBRIC_REF).read_text(encoding="utf-8")),
        "compatible_contracts": ["analyze.continuity.adjacent_scene.v1"],
        "compatible_consumers": ["authorforge"],
        "model_compatibility": [],
        "supersedes": None,
        "created_at": CREATED_AT,
        "updated_at": CREATED_AT,
        "notes": "Baseline fixture skill spec for governed skill-optimization foundation.",
    }
    validate_instance(spec, "skill-spec.v1.schema.json")
    return spec


def expected_fixture_result(case: dict[str, Any]) -> dict[str, Any]:
    finding_expected = case["finding_expected"]
    no_finding_acceptable = case["no_finding_acceptable"]
    if finding_expected is True:
        finding_status = "pass"
    elif finding_expected == "partial":
        finding_status = "partial"
    else:
        finding_status = "pass" if no_finding_acceptable is True else "fail"

    restraint_status = "pass"
    false_positive_severity = "none"
    if case["expected_review_posture"] == "restraint_expected":
        false_positive_severity = "none"

    score = {
        "schema_validity": 1.0,
        "finding": 1.0 if finding_status == "pass" else 0.5 if finding_status == "partial" else 0.0,
        "restraint": 1.0 if restraint_status == "pass" else 0.0,
        "evidence": 1.0,
        "confidence": 1.0,
    }
    score["total"] = round(sum(score.values()) / len(score), 4)

    fixture_output = {
        "case_id": case["case_id"],
        "fixture_id": FIXTURE_ID,
        "expected_review_posture": case["expected_review_posture"],
        "expected_restraint_posture": case["expected_restraint_posture"],
        "finding_expected": finding_expected,
        "no_finding_acceptable": no_finding_acceptable,
    }

    return {
        "case_id": case["case_id"],
        "split": case["split"],
        "source_packet_hash": case["source_packet_hash"],
        "output_hash": sha256_json(fixture_output),
        "structured_output_valid": True,
        "finding_correctness": finding_status,
        "restraint_correctness": restraint_status,
        "evidence_span_status": "not_scored",
        "confidence_calibration": "not_scored",
        "false_positive_severity": false_positive_severity,
        "regression_status": "pass" if case["split"] == "regression" else "not_applicable",
        "score": score,
        "notes": "Fixture baseline scores expectations, not model behavior.",
    }


def build_fixture_baseline_report(cases: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    eval_cases = cases or build_continuity_eval_cases()
    active_cases = [case for case in eval_cases if case["active"]]
    results = [expected_fixture_result(case) for case in active_cases]
    aggregate_score = round(
        sum(result["score"]["total"] for result in results) / len(results), 4
    ) if results else 0.0
    report = {
        "schema_version": "skill-eval-run-v1",
        "eval_run_id": "skill-eval-run-continuity-progression-fixture-baseline-20260623",
        "skill_id": SKILL_ID,
        "skill_version": SKILL_VERSION,
        "lane_id": LANE_ID,
        "case_pack_id": CASE_PACK_ID,
        "runner_mode": "fixture",
        "fixture_id": FIXTURE_ID,
        "model_id": None,
        "started_at": CREATED_AT,
        "finished_at": CREATED_AT,
        "case_results": results,
        "summary": {
            "cases_total": len(results),
            "schema_valid_count": len(results),
            "blocking_failure_count": 0,
            "aggregate_score": aggregate_score,
            "high_risk_false_positive_count": 0,
            "regression_failure_count": 0,
        },
        "blocking_failures": [],
        "notes": "Deterministic fixture baseline. This is not a real-model performance claim.",
    }
    validate_instance(report, "skill-eval-run.v1.schema.json")
    return report


def dump_json(data: Any) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="SkillOpt continuity/progression fixture tooling.")
    parser.add_argument(
        "command",
        choices=["skill-spec", "eval-cases", "fixture-baseline"],
        help="Record type to emit as JSON.",
    )
    args = parser.parse_args()

    if args.command == "skill-spec":
        print(dump_json(build_skill_spec()), end="")
    elif args.command == "eval-cases":
        print(dump_json(build_continuity_eval_cases()), end="")
    else:
        print(dump_json(build_fixture_baseline_report()), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
