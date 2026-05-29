#!/usr/bin/env python3
import json
import sys
from pathlib import Path

TASK_ID = "analyze.continuity.adjacent_scene.v1"
REQUIRED_STRING_FIELDS = [
    "scene_a_id",
    "scene_b_id",
    "scene_a_text",
    "scene_b_text",
]
CONTEXT_FIELDS = [
    "task_intent_id",
    "context_bundle_id",
    "context_bundle_hash",
]
OPTIONAL_CONTEXT_REFS = [
    "context_manifest_ref",
    "context_payload_ref",
]


def clean_string(value):
    if value is None:
        return ""
    if not isinstance(value, str):
        raise TypeError("value must be a string")
    return value


def maybe_add_string(result, data, key):
    if key in data and data[key] is not None:
        if not isinstance(data[key], str):
            raise TypeError(f"field {key} must be a string when present")
        result[key] = data[key]


def build_failure(reason, data=None):
    data = data or {}
    result = {
        "intake_status": "fail_closed",
        "failure_reason": reason,
        "task_id": data.get("task_id", TASK_ID) if isinstance(data.get("task_id"), str) else TASK_ID,
        "scope_label": data.get("scope_label", "adjacent_scene") if isinstance(data.get("scope_label"), str) else "adjacent_scene",
        "scene_packet_id": data.get("scene_packet_id", "unknown") if isinstance(data.get("scene_packet_id"), str) else "unknown",
        "scene_a_id": data.get("scene_a_id", "") if isinstance(data.get("scene_a_id"), str) else "",
        "scene_b_id": data.get("scene_b_id", "") if isinstance(data.get("scene_b_id"), str) else "",
    }
    for key in CONTEXT_FIELDS + OPTIONAL_CONTEXT_REFS:
        if key in data and isinstance(data[key], str):
            result[key] = data[key]
    return result


def main() -> int:
    if len(sys.argv) != 2:
        print(json.dumps(build_failure("usage: read-context-intake.py <request_file>"), indent=2))
        return 2

    request_path = Path(sys.argv[1])
    try:
        with request_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError:
        print(json.dumps(build_failure(f"request file not found: {request_path}"), indent=2))
        return 1
    except json.JSONDecodeError as exc:
        print(json.dumps(build_failure(f"request file is not valid JSON: {exc}"), indent=2))
        return 1

    if not isinstance(data, dict):
        print(json.dumps(build_failure("request payload must be a JSON object", data), indent=2))
        return 1

    try:
        task_id = clean_string(data.get("task_id", TASK_ID))
        scope_label = clean_string(data.get("scope_label", "adjacent_scene")) or "adjacent_scene"
        scene_packet_id = clean_string(data.get("scene_packet_id", "unknown")) or "unknown"
    except TypeError as exc:
        print(json.dumps(build_failure(str(exc), data), indent=2))
        return 1

    if task_id != TASK_ID:
        print(json.dumps(build_failure(f"task_id must be {TASK_ID}", data), indent=2))
        return 1

    normalized = {
        "intake_status": "valid",
        "task_id": task_id,
        "scope_label": scope_label,
        "scene_packet_id": scene_packet_id,
        "packet_metadata": data.get("packet_metadata", {}),
    }

    if normalized["packet_metadata"] is None:
        normalized["packet_metadata"] = {}
    if not isinstance(normalized["packet_metadata"], dict):
        print(json.dumps(build_failure("packet_metadata must be an object when present", data), indent=2))
        return 1

    for field in REQUIRED_STRING_FIELDS:
        if field not in data:
            print(json.dumps(build_failure(f"missing required field: {field}", data), indent=2))
            return 1
        if not isinstance(data[field], str) or not data[field]:
            print(json.dumps(build_failure(f"field {field} must be a non-empty string", data), indent=2))
            return 1
        normalized[field] = data[field]

    try:
        for key in CONTEXT_FIELDS + OPTIONAL_CONTEXT_REFS:
            maybe_add_string(normalized, data, key)
    except TypeError as exc:
        print(json.dumps(build_failure(str(exc), data), indent=2))
        return 1

    context_presence = {key: bool(normalized.get(key, "")) for key in CONTEXT_FIELDS}
    present_count = sum(context_presence.values())
    refs_present = any(bool(normalized.get(key, "")) for key in OPTIONAL_CONTEXT_REFS)

    if present_count not in (0, len(CONTEXT_FIELDS)):
        print(
            json.dumps(
                build_failure(
                    "context lineage fields are partially present; require task_intent_id, context_bundle_id, and context_bundle_hash together",
                    normalized,
                ),
                indent=2,
            )
        )
        return 1

    if refs_present and present_count != len(CONTEXT_FIELDS):
        print(
            json.dumps(
                build_failure(
                    "context refs require a connected request with task_intent_id, context_bundle_id, and context_bundle_hash",
                    normalized,
                ),
                indent=2,
            )
        )
        return 1

    print(json.dumps(normalized, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
