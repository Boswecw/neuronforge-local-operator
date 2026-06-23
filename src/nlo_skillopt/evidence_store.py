from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .candidate_packages import load_candidate_package, validation_report
from .continuity_cases import (
    build_continuity_eval_cases,
    build_fixture_baseline_report,
    build_skill_spec,
    dump_json,
    sha256_json,
)
from .schemas import validate_instance

DEFAULT_EVIDENCE_DIR = Path("evidence") / "skill_optimization"

SKILL_SPEC_FILE = "skill-spec.json"
EVAL_CASES_FILE = "eval-cases.jsonl"
EVAL_RUNS_FILE = "eval-runs.jsonl"
CANDIDATE_PACKAGES_FILE = "candidate-packages.jsonl"
CANDIDATE_VALIDATION_REPORTS_FILE = "candidate-validation-reports.jsonl"
MANIFEST_FILE = "manifest.json"


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump_json(data), encoding="utf-8")


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if line.strip():
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    raise ValueError(f"{path}:{line_number}: invalid JSONL record: {exc}") from exc
    return records


def build_manifest(
    *,
    skill_spec: dict[str, Any],
    eval_cases: list[dict[str, Any]],
    eval_runs: list[dict[str, Any]],
    candidate_packages: list[dict[str, Any]] | None = None,
    validation_reports: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    candidate_packages = candidate_packages or []
    validation_reports = validation_reports or []
    return {
        "schema_version": "skillopt-evidence-manifest-v1",
        "skill_id": skill_spec["skill_id"],
        "skill_version": skill_spec["skill_version"],
        "lane_id": skill_spec["lane_id"],
        "record_counts": {
            "skill_specs": 1,
            "eval_cases": len(eval_cases),
            "eval_runs": len(eval_runs),
            "candidate_packages": len(candidate_packages),
            "candidate_validation_reports": len(validation_reports),
        },
        "record_hashes": {
            "skill_spec": sha256_json(skill_spec),
            "eval_cases": sha256_json(eval_cases),
            "eval_runs": sha256_json(eval_runs),
            "candidate_packages": sha256_json(candidate_packages),
            "candidate_validation_reports": sha256_json(validation_reports),
        },
    }


def write_foundation_snapshot(evidence_dir: Path) -> dict[str, Any]:
    skill_spec = build_skill_spec()
    eval_cases = build_continuity_eval_cases()
    eval_runs = [build_fixture_baseline_report(eval_cases)]

    write_json(evidence_dir / SKILL_SPEC_FILE, skill_spec)
    write_jsonl(evidence_dir / EVAL_CASES_FILE, eval_cases)
    write_jsonl(evidence_dir / EVAL_RUNS_FILE, eval_runs)
    write_jsonl(evidence_dir / CANDIDATE_PACKAGES_FILE, [])
    write_jsonl(evidence_dir / CANDIDATE_VALIDATION_REPORTS_FILE, [])

    manifest = build_manifest(
        skill_spec=skill_spec,
        eval_cases=eval_cases,
        eval_runs=eval_runs,
    )
    write_json(evidence_dir / MANIFEST_FILE, manifest)
    return manifest


def read_skill_spec(evidence_dir: Path) -> dict[str, Any]:
    with (evidence_dir / SKILL_SPEC_FILE).open(encoding="utf-8") as handle:
        spec = json.load(handle)
    validate_instance(spec, "skill-spec.v1.schema.json")
    return spec


def read_eval_cases(evidence_dir: Path) -> list[dict[str, Any]]:
    cases = read_jsonl(evidence_dir / EVAL_CASES_FILE)
    for case in cases:
        validate_instance(case, "skill-eval-case.v1.schema.json")
    return cases


def read_eval_runs(evidence_dir: Path) -> list[dict[str, Any]]:
    runs = read_jsonl(evidence_dir / EVAL_RUNS_FILE)
    for run in runs:
        validate_instance(run, "skill-eval-run.v1.schema.json")
    return runs


def reconstruct_eval_run(evidence_dir: Path, eval_run_id: str) -> dict[str, Any]:
    for run in read_eval_runs(evidence_dir):
        if run["eval_run_id"] == eval_run_id:
            return run
    raise KeyError(f"eval run not found: {eval_run_id}")


def append_candidate_evidence(evidence_dir: Path, candidate: dict[str, Any]) -> dict[str, Any]:
    validate_instance(candidate, "skill-candidate.v1.schema.json")
    report = validation_report(candidate)
    append_jsonl(evidence_dir / CANDIDATE_PACKAGES_FILE, candidate)
    append_jsonl(evidence_dir / CANDIDATE_VALIDATION_REPORTS_FILE, report)

    skill_spec = read_skill_spec(evidence_dir)
    eval_cases = read_eval_cases(evidence_dir)
    eval_runs = read_eval_runs(evidence_dir)
    candidate_packages = read_jsonl(evidence_dir / CANDIDATE_PACKAGES_FILE)
    validation_reports = read_jsonl(evidence_dir / CANDIDATE_VALIDATION_REPORTS_FILE)
    manifest = build_manifest(
        skill_spec=skill_spec,
        eval_cases=eval_cases,
        eval_runs=eval_runs,
        candidate_packages=candidate_packages,
        validation_reports=validation_reports,
    )
    write_json(evidence_dir / MANIFEST_FILE, manifest)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Store/read local SkillOpt evidence receipts.")
    parser.add_argument(
        "command",
        choices=["export-foundation", "read-baseline", "append-candidate"],
    )
    parser.add_argument(
        "--evidence-dir",
        type=Path,
        default=DEFAULT_EVIDENCE_DIR,
        help="Evidence directory. Default: evidence/skill_optimization",
    )
    parser.add_argument(
        "--eval-run-id",
        default="skill-eval-run-continuity-progression-fixture-baseline-20260623",
        help="Eval run id for read-baseline.",
    )
    parser.add_argument(
        "--candidate-package",
        type=Path,
        help="SkillCandidate.v1 package for append-candidate.",
    )
    args = parser.parse_args()

    if args.command == "export-foundation":
        print(dump_json(write_foundation_snapshot(args.evidence_dir)), end="")
        return 0
    if args.command == "read-baseline":
        print(dump_json(reconstruct_eval_run(args.evidence_dir, args.eval_run_id)), end="")
        return 0
    if not args.candidate_package:
        parser.error("--candidate-package is required for append-candidate")
    candidate = load_candidate_package(args.candidate_package)
    report = append_candidate_evidence(args.evidence_dir, candidate)
    print(dump_json(report), end="")
    return 0 if report["validation_result"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
