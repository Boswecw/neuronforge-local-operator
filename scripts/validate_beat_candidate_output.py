#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

REQUIRED_TOP = {"task_type", "source_scope", "candidates"}
REQUIRED_SCOPE = {"scope_type", "scene_id"}
REQUIRED_CANDIDATE = {
    "artifact_class",
    "beat_label",
    "beat_summary",
    "structural_role_hint",
    "confidence_class",
    "evidence_spans",
    "uncertainty_note",
    "review_note",
}
ALLOWED_CONFIDENCE = {"low", "moderate", "high"}


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    sys.exit(1)


def warn(msg: str) -> None:
    print(f"WARN: {msg}")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: validate_beat_candidate_output.py <json_file>")
        sys.exit(2)

    path = Path(sys.argv[1])
    if not path.exists():
        fail(f"file not found: {path}")

    raw = path.read_text(encoding="utf-8").strip()

    if raw.startswith("```"):
        fail("output contains markdown fences")

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        fail(f"invalid json: {e}")

    missing_top = REQUIRED_TOP - set(data.keys())
    if missing_top:
        fail(f"missing top-level keys: {sorted(missing_top)}")

    if data["task_type"] != "extract.beat_candidates.scene.v1":
        fail(f"unexpected task_type: {data['task_type']}")

    scope = data["source_scope"]
    missing_scope = REQUIRED_SCOPE - set(scope.keys())
    if missing_scope:
        fail(f"missing source_scope keys: {sorted(missing_scope)}")

    candidates = data["candidates"]
    if not isinstance(candidates, list):
        fail("candidates must be a list")

    if len(candidates) > 2:
        warn("candidate count > 2 (possible beat inflation)")

    for i, cand in enumerate(candidates):
        missing = REQUIRED_CANDIDATE - set(cand.keys())
        if missing:
            fail(f"candidate[{i}] missing keys: {sorted(missing)}")

        if cand["artifact_class"] != "candidate_beat":
            fail(f"candidate[{i}] wrong artifact_class: {cand['artifact_class']}")

        if cand["confidence_class"] not in ALLOWED_CONFIDENCE:
            fail(f"candidate[{i}] bad confidence_class: {cand['confidence_class']}")

        if not isinstance(cand["evidence_spans"], list) or not cand["evidence_spans"]:
            fail(f"candidate[{i}] must have at least one evidence span")

        if not str(cand["uncertainty_note"]).strip():
            fail(f"candidate[{i}] uncertainty_note is empty")

        if not str(cand["review_note"]).strip():
            fail(f"candidate[{i}] review_note is empty")

        if cand["confidence_class"] == "high" and len(cand["evidence_spans"]) < 2:
            warn(f"candidate[{i}] high confidence with fewer than 2 evidence spans")

    print("PASS")


if __name__ == "__main__":
    main()