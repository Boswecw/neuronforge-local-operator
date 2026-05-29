#!/usr/bin/env bash
set -euo pipefail

# test-continuity-adjacent-scene.sh
#
# Unit tests for analyze.continuity.adjacent_scene.v1
#
# Tests the schema validator and fail-closed behavior using synthetic
# model outputs. Does not call ollama.
#
# Usage:
#   tests/test-continuity-adjacent-scene.sh
#
# Exit codes:
#   0 = all tests passed
#   1 = one or more tests failed

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

VALIDATOR="scripts/validate-continuity-candidate.py"
RENDERER="scripts/render-continuity-candidate.sh"

PASS=0
FAIL=0

# --- Test harness ---

assert_exit() {
  local name="$1"
  local expected_exit="$2"
  local actual_exit="$3"
  if [ "$actual_exit" -eq "$expected_exit" ]; then
    echo "  PASS: $name"
    PASS=$((PASS + 1))
  else
    echo "  FAIL: $name (expected exit $expected_exit, got $actual_exit)"
    FAIL=$((FAIL + 1))
  fi
}

assert_json_field() {
  local name="$1"
  local json="$2"
  local field="$3"
  local expected="$4"
  local actual
  actual="$(printf '%s' "$json" | jq -r "$field" 2>/dev/null || echo "PARSE_ERROR")"
  if [ "$actual" = "$expected" ]; then
    echo "  PASS: $name"
    PASS=$((PASS + 1))
  else
    echo "  FAIL: $name (expected $expected, got $actual)"
    FAIL=$((FAIL + 1))
  fi
}

run_validator() {
  local json_input="$1"
  local tmp
  tmp="$(mktemp)"
  printf '%s' "$json_input" > "$tmp"
  local result exit_code
  result="$(python3 "$VALIDATOR" "$tmp" 2>/dev/null)" && exit_code=$? || exit_code=$?
  rm -f "$tmp"
  printf '%s\n%d' "$result" "$exit_code"
}

get_exit_from_output() {
  # Last line of run_validator output is the exit code
  printf '%s' "$1" | tail -n 1
}

get_json_from_output() {
  # All lines except the last are the JSON result
  printf '%s' "$1" | head -n -1
}

# --- Synthetic fixtures ---

VALID_FINDING='{
  "finding_id": "cpf-001",
  "finding_label": "Possible abrupt emotional transition",
  "finding_type": "transition_gap",
  "claim": "The emotional handoff from sc-041 to sc-042 may feel more abrupt than the visible transition support justifies.",
  "scope_type": "adjacent_scene",
  "scope_bounds": { "scene_ids": ["sc-041", "sc-042"] },
  "evidence_spans": [
    {
      "scene_id": "sc-041",
      "span_text": "Rawn was still laughing as they reached the ford.",
      "span_role": "setup",
      "position_hint": "ending"
    },
    {
      "scene_id": "sc-042",
      "span_text": "Rawn dismounted without speaking, his expression closed and flat.",
      "span_role": "contrast",
      "position_hint": "opening"
    }
  ],
  "confidence": "moderate",
  "uncertainty_note": "The shift may be intentional and could be supported by context outside the bounded two-scene window.",
  "review_note": "Check whether the end of sc-041 or start of sc-042 supplies enough transition signal for the emotional shift.",
  "candidate_state": "candidate_unreviewed",
  "severity_hint": "moderate",
  "taxonomy_tags": ["emotion", "transition"]
}'

VALID_OUTPUT="{
  \"schema_version\": \"1.0\",
  \"lane_id\": \"continuity-progression-reasoning\",
  \"analysis_scope_type\": \"adjacent_scene\",
  \"analysis_scope_bounds\": { \"scene_ids\": [\"sc-041\", \"sc-042\"] },
  \"input_unit_ids\": [\"sc-041\", \"sc-042\"],
  \"candidate_findings\": [$VALID_FINDING],
  \"overall_run_note\": \"One candidate review point identified: a possible abrupt emotional transition.\",
  \"run_posture\": \"candidate_only\"
}"

VALID_EMPTY_OUTPUT='{
  "schema_version": "1.0",
  "lane_id": "continuity-progression-reasoning",
  "analysis_scope_type": "adjacent_scene",
  "analysis_scope_bounds": { "scene_ids": ["sc-041", "sc-042"] },
  "input_unit_ids": ["sc-041", "sc-042"],
  "candidate_findings": [],
  "overall_run_note": "No strong continuity or progression issue detected within the bounded scope.",
  "run_posture": "candidate_only"
}'

# --- Tests ---

echo
echo "=== Continuity Adjacent-Scene Slice 1 Tests ==="
echo

echo "--- Test 1: Valid structured output with findings ---"
OUTPUT="$(run_validator "$VALID_OUTPUT")"
EXIT_CODE="$(get_exit_from_output "$OUTPUT")"
JSON="$(get_json_from_output "$OUTPUT")"
assert_exit "exit code is 0" 0 "$EXIT_CODE"
assert_json_field "validation_result is valid" "$JSON" ".validation_result" "valid"
assert_json_field "findings_count is 1" "$JSON" ".findings_count" "1"

echo
echo "--- Test 2: Valid output with zero findings ---"
OUTPUT="$(run_validator "$VALID_EMPTY_OUTPUT")"
EXIT_CODE="$(get_exit_from_output "$OUTPUT")"
JSON="$(get_json_from_output "$OUTPUT")"
assert_exit "exit code is 0" 0 "$EXIT_CODE"
assert_json_field "validation_result is valid" "$JSON" ".validation_result" "valid"
assert_json_field "findings_count is 0" "$JSON" ".findings_count" "0"

echo
echo "--- Test 3: Malformed input (prose, not JSON) ---"
OUTPUT="$(run_validator "The scenes appear to be consistent. No issues found.")"
EXIT_CODE="$(get_exit_from_output "$OUTPUT")"
JSON="$(get_json_from_output "$OUTPUT")"
assert_exit "exit code is 2" 2 "$EXIT_CODE"
assert_json_field "validation_result is fail_closed" "$JSON" ".validation_result" "fail_closed"

echo
echo "--- Test 4: JSON in markdown fences ---"
FENCED_OUTPUT="\`\`\`json
$VALID_EMPTY_OUTPUT
\`\`\`"
OUTPUT="$(run_validator "$FENCED_OUTPUT")"
EXIT_CODE="$(get_exit_from_output "$OUTPUT")"
JSON="$(get_json_from_output "$OUTPUT")"
assert_exit "exit code is 0 (extracted from fences)" 0 "$EXIT_CODE"
assert_json_field "validation_result is valid" "$JSON" ".validation_result" "valid"

echo
echo "--- Test 5: Wrong lane_id ---"
BAD_LANE='{
  "schema_version": "1.0",
  "lane_id": "wrong-lane",
  "analysis_scope_type": "adjacent_scene",
  "analysis_scope_bounds": { "scene_ids": ["sc-041", "sc-042"] },
  "input_unit_ids": ["sc-041", "sc-042"],
  "candidate_findings": [],
  "overall_run_note": "No issues.",
  "run_posture": "candidate_only"
}'
OUTPUT="$(run_validator "$BAD_LANE")"
EXIT_CODE="$(get_exit_from_output "$OUTPUT")"
JSON="$(get_json_from_output "$OUTPUT")"
assert_exit "exit code is 1" 1 "$EXIT_CODE"
assert_json_field "validation_result is fail_closed" "$JSON" ".validation_result" "fail_closed"

echo
echo "--- Test 6: Wrong run_posture ---"
BAD_POSTURE='{
  "schema_version": "1.0",
  "lane_id": "continuity-progression-reasoning",
  "analysis_scope_type": "adjacent_scene",
  "analysis_scope_bounds": { "scene_ids": ["sc-041", "sc-042"] },
  "input_unit_ids": ["sc-041", "sc-042"],
  "candidate_findings": [],
  "overall_run_note": "No issues.",
  "run_posture": "authoritative"
}'
OUTPUT="$(run_validator "$BAD_POSTURE")"
EXIT_CODE="$(get_exit_from_output "$OUTPUT")"
JSON="$(get_json_from_output "$OUTPUT")"
assert_exit "exit code is 1" 1 "$EXIT_CODE"
assert_json_field "validation_result is fail_closed" "$JSON" ".validation_result" "fail_closed"

echo
echo "--- Test 7: Missing evidence spans (empty array) ---"
NO_EVIDENCE="{
  \"schema_version\": \"1.0\",
  \"lane_id\": \"continuity-progression-reasoning\",
  \"analysis_scope_type\": \"adjacent_scene\",
  \"analysis_scope_bounds\": { \"scene_ids\": [\"sc-041\", \"sc-042\"] },
  \"input_unit_ids\": [\"sc-041\", \"sc-042\"],
  \"candidate_findings\": [{
    \"finding_id\": \"cpf-001\",
    \"finding_label\": \"Possible issue\",
    \"finding_type\": \"transition_gap\",
    \"claim\": \"The transition may be abrupt.\",
    \"scope_type\": \"adjacent_scene\",
    \"scope_bounds\": { \"scene_ids\": [\"sc-041\", \"sc-042\"] },
    \"evidence_spans\": [],
    \"confidence\": \"moderate\",
    \"uncertainty_note\": \"May be intentional.\",
    \"review_note\": \"Check the transition between the two scenes.\",
    \"candidate_state\": \"candidate_unreviewed\"
  }],
  \"overall_run_note\": \"One possible issue.\",
  \"run_posture\": \"candidate_only\"
}"
OUTPUT="$(run_validator "$NO_EVIDENCE")"
EXIT_CODE="$(get_exit_from_output "$OUTPUT")"
JSON="$(get_json_from_output "$OUTPUT")"
assert_exit "exit code is 1" 1 "$EXIT_CODE"
assert_json_field "validation_result is fail_closed" "$JSON" ".validation_result" "fail_closed"

echo
echo "--- Test 8: Authority language in claim ---"
AUTH_CLAIM="{
  \"schema_version\": \"1.0\",
  \"lane_id\": \"continuity-progression-reasoning\",
  \"analysis_scope_type\": \"adjacent_scene\",
  \"analysis_scope_bounds\": { \"scene_ids\": [\"sc-041\", \"sc-042\"] },
  \"input_unit_ids\": [\"sc-041\", \"sc-042\"],
  \"candidate_findings\": [{
    \"finding_id\": \"cpf-001\",
    \"finding_label\": \"Emotional inconsistency\",
    \"finding_type\": \"transition_gap\",
    \"claim\": \"The character is definitely inconsistent here.\",
    \"scope_type\": \"adjacent_scene\",
    \"scope_bounds\": { \"scene_ids\": [\"sc-041\", \"sc-042\"] },
    \"evidence_spans\": [
      { \"scene_id\": \"sc-041\", \"span_text\": \"He was laughing.\", \"span_role\": \"setup\" },
      { \"scene_id\": \"sc-042\", \"span_text\": \"He was silent.\", \"span_role\": \"contrast\" }
    ],
    \"confidence\": \"high\",
    \"uncertainty_note\": \"May be intentional.\",
    \"review_note\": \"Check the emotional carry-forward between scenes.\",
    \"candidate_state\": \"candidate_unreviewed\"
  }],
  \"overall_run_note\": \"One definite issue found.\",
  \"run_posture\": \"candidate_only\"
}"
OUTPUT="$(run_validator "$AUTH_CLAIM")"
EXIT_CODE="$(get_exit_from_output "$OUTPUT")"
JSON="$(get_json_from_output "$OUTPUT")"
assert_exit "exit code is 1" 1 "$EXIT_CODE"
assert_json_field "validation_result is fail_closed" "$JSON" ".validation_result" "fail_closed"

echo
echo "--- Test 9: Out-of-scope scene reference in finding ---"
OUT_OF_SCOPE="{
  \"schema_version\": \"1.0\",
  \"lane_id\": \"continuity-progression-reasoning\",
  \"analysis_scope_type\": \"adjacent_scene\",
  \"analysis_scope_bounds\": { \"scene_ids\": [\"sc-041\", \"sc-042\"] },
  \"input_unit_ids\": [\"sc-041\", \"sc-042\"],
  \"candidate_findings\": [{
    \"finding_id\": \"cpf-001\",
    \"finding_label\": \"Scope violation finding\",
    \"finding_type\": \"continuity_tension\",
    \"claim\": \"There may be an issue spanning multiple scenes.\",
    \"scope_type\": \"adjacent_scene\",
    \"scope_bounds\": { \"scene_ids\": [\"sc-041\", \"sc-042\", \"sc-099\"] },
    \"evidence_spans\": [
      { \"scene_id\": \"sc-041\", \"span_text\": \"Some text.\", \"span_role\": \"setup\" },
      { \"scene_id\": \"sc-099\", \"span_text\": \"Out of scope text.\", \"span_role\": \"contrast\" }
    ],
    \"confidence\": \"low\",
    \"uncertainty_note\": \"Limited to the provided window.\",
    \"review_note\": \"Check across the scenes.\",
    \"candidate_state\": \"candidate_unreviewed\"
  }],
  \"overall_run_note\": \"One candidate finding.\",
  \"run_posture\": \"candidate_only\"
}"
OUTPUT="$(run_validator "$OUT_OF_SCOPE")"
EXIT_CODE="$(get_exit_from_output "$OUTPUT")"
JSON="$(get_json_from_output "$OUTPUT")"
assert_exit "exit code is 1" 1 "$EXIT_CODE"
assert_json_field "validation_result is fail_closed" "$JSON" ".validation_result" "fail_closed"

echo
echo "--- Test 10: Trivial uncertainty_note ---"
TRIVIAL_UNCERTAINTY="{
  \"schema_version\": \"1.0\",
  \"lane_id\": \"continuity-progression-reasoning\",
  \"analysis_scope_type\": \"adjacent_scene\",
  \"analysis_scope_bounds\": { \"scene_ids\": [\"sc-041\", \"sc-042\"] },
  \"input_unit_ids\": [\"sc-041\", \"sc-042\"],
  \"candidate_findings\": [{
    \"finding_id\": \"cpf-001\",
    \"finding_label\": \"Possible issue\",
    \"finding_type\": \"transition_gap\",
    \"claim\": \"The transition may be abrupt.\",
    \"scope_type\": \"adjacent_scene\",
    \"scope_bounds\": { \"scene_ids\": [\"sc-041\", \"sc-042\"] },
    \"evidence_spans\": [
      { \"scene_id\": \"sc-041\", \"span_text\": \"He laughed.\", \"span_role\": \"setup\" },
      { \"scene_id\": \"sc-042\", \"span_text\": \"He was silent.\", \"span_role\": \"contrast\" }
    ],
    \"confidence\": \"moderate\",
    \"uncertainty_note\": \"None\",
    \"review_note\": \"Check the transition between the two scenes.\",
    \"candidate_state\": \"candidate_unreviewed\"
  }],
  \"overall_run_note\": \"One finding.\",
  \"run_posture\": \"candidate_only\"
}"
OUTPUT="$(run_validator "$TRIVIAL_UNCERTAINTY")"
EXIT_CODE="$(get_exit_from_output "$OUTPUT")"
JSON="$(get_json_from_output "$OUTPUT")"
assert_exit "exit code is 1" 1 "$EXIT_CODE"
assert_json_field "validation_result is fail_closed" "$JSON" ".validation_result" "fail_closed"

echo
echo "--- Test 11: Invalid finding_type ---"
BAD_TYPE="{
  \"schema_version\": \"1.0\",
  \"lane_id\": \"continuity-progression-reasoning\",
  \"analysis_scope_type\": \"adjacent_scene\",
  \"analysis_scope_bounds\": { \"scene_ids\": [\"sc-041\", \"sc-042\"] },
  \"input_unit_ids\": [\"sc-041\", \"sc-042\"],
  \"candidate_findings\": [{
    \"finding_id\": \"cpf-001\",
    \"finding_label\": \"Invented type\",
    \"finding_type\": \"narrative_flaw\",
    \"claim\": \"The scenes may not connect well.\",
    \"scope_type\": \"adjacent_scene\",
    \"scope_bounds\": { \"scene_ids\": [\"sc-041\", \"sc-042\"] },
    \"evidence_spans\": [
      { \"scene_id\": \"sc-041\", \"span_text\": \"He laughed.\", \"span_role\": \"setup\" },
      { \"scene_id\": \"sc-042\", \"span_text\": \"He was silent.\", \"span_role\": \"contrast\" }
    ],
    \"confidence\": \"low\",
    \"uncertainty_note\": \"May be intentional authorial choice.\",
    \"review_note\": \"Check the scene connection.\",
    \"candidate_state\": \"candidate_unreviewed\"
  }],
  \"overall_run_note\": \"One candidate finding.\",
  \"run_posture\": \"candidate_only\"
}"
OUTPUT="$(run_validator "$BAD_TYPE")"
EXIT_CODE="$(get_exit_from_output "$OUTPUT")"
JSON="$(get_json_from_output "$OUTPUT")"
assert_exit "exit code is 1" 1 "$EXIT_CODE"
assert_json_field "validation_result is fail_closed" "$JSON" ".validation_result" "fail_closed"

echo
echo "--- Test 12: Fail-closed envelope renders without error ---"
TMP_FAIL_ENVELOPE="$(mktemp --suffix=.json)"
TMP_RENDER_OUTPUT="$(mktemp)"
cleanup_test12() { rm -f "$TMP_FAIL_ENVELOPE" "$TMP_RENDER_OUTPUT"; }
trap cleanup_test12 EXIT

cat > "$TMP_FAIL_ENVELOPE" <<'EOF'
{
  "task_id": "analyze.continuity.adjacent_scene.v1",
  "contract_version": "1.0",
  "route_class": "HIGH_QUALITY_LOCAL",
  "model_id": "phi4-reasoning:latest",
  "run_id": "run-2026-03-14-001",
  "timestamp": "2026-03-14T12:00:00Z",
  "scene_packet_id": "test-packet-001",
  "scope_label": "adjacent_scene",
  "envelope_status": "fail_closed",
  "failure_reason": "JSON parse error: Expecting value: line 1 column 1 (char 0)",
  "candidate_findings": [],
  "validation_result": null,
  "run_metadata": {
    "prompt_file": "prompts/continuity-adjacent-scene-v1.md",
    "request_file": "inputs/continuity-adjacent-scene-test-001.json",
    "raw_output_file": null
  }
}
EOF

RENDER_EXIT=0
bash "$RENDERER" "$TMP_FAIL_ENVELOPE" > "$TMP_RENDER_OUTPUT" 2>&1 || RENDER_EXIT=$?
assert_exit "renderer exits 0 on fail-closed envelope" 0 "$RENDER_EXIT"

RENDER_CONTENT="$(cat "$TMP_RENDER_OUTPUT")"
if printf '%s' "$RENDER_CONTENT" | grep -q "Fail Closed"; then
  echo "  PASS: renderer shows Fail Closed heading"
  PASS=$((PASS + 1))
else
  echo "  FAIL: renderer missing Fail Closed heading"
  FAIL=$((FAIL + 1))
fi

if printf '%s' "$RENDER_CONTENT" | grep -qi "canonical"; then
  echo "  FAIL: renderer contains canonicality language"
  FAIL=$((FAIL + 1))
else
  echo "  PASS: renderer free of canonicality language"
  PASS=$((PASS + 1))
fi

# --- Results ---

echo
echo "=== Results ==="
echo "  Passed: $PASS"
echo "  Failed: $FAIL"
echo

if [ "$FAIL" -gt 0 ]; then
  exit 1
fi

exit 0
