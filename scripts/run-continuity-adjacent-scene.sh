#!/usr/bin/env bash
set -euo pipefail

# run-continuity-adjacent-scene.sh
#
# Executor for task: analyze.continuity.adjacent_scene.v1
# Route class:       HIGH_QUALITY_LOCAL
# Trust posture:     candidate_only
# Fail-closed:       yes
#
# Usage:
#   scripts/run-continuity-adjacent-scene.sh [--dry-run] <model> <request_file> [<output_dir>]
#
# Arguments:
#   model        Ollama model name (must be HIGH_QUALITY_LOCAL tier, e.g. phi4-reasoning:latest)
#   request_file JSON file with adjacent scene request packet
#   output_dir   Directory for output files (default: outputs)

TASK_ID="analyze.continuity.adjacent_scene.v1"
CONTRACT_VERSION="1.0"
ROUTE_CLASS="HIGH_QUALITY_LOCAL"
PROMPT_FILE="prompts/continuity-adjacent-scene-v3.md"

DRY_RUN=0
if [ "${1:-}" = "--dry-run" ]; then
  DRY_RUN=1
  shift
fi

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 [--dry-run] <model> <request_file> [<output_dir>]"
  echo
  echo "  model        Ollama model name (HIGH_QUALITY_LOCAL tier)"
  echo "  request_file JSON file with adjacent scene request packet"
  echo "  output_dir   Output directory (default: outputs)"
  exit 1
fi

MODEL="$1"
REQUEST_FILE="$2"
OUTPUT_DIR="${3:-outputs}"

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# --- Prerequisite checks ---

if [ ! -f "$PROMPT_FILE" ]; then
  echo "Error: prompt file not found: $PROMPT_FILE" >&2
  exit 1
fi

if [ ! -f "$REQUEST_FILE" ]; then
  echo "Error: request file not found: $REQUEST_FILE" >&2
  exit 1
fi

for cmd in ollama python3 jq; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Error: $cmd is not installed or not on PATH" >&2
    exit 1
  fi
done

for required_file in \
  scripts/validate-continuity-candidate.py \
  scripts/read-context-intake.py \
  scripts/next-run-id.sh \
  scripts/log-run.sh
  do
  if [ ! -f "$required_file" ]; then
    echo "Error: required file not found: $required_file" >&2
    exit 1
  fi
done

if [ ! -x scripts/next-run-id.sh ]; then
  echo "Error: scripts/next-run-id.sh missing or not executable" >&2
  exit 1
fi

if [ ! -x scripts/log-run.sh ]; then
  echo "Error: scripts/log-run.sh missing or not executable" >&2
  exit 1
fi

# --- Read and validate request fields ---

set +e
INTAKE_JSON="$(python3 scripts/read-context-intake.py "$REQUEST_FILE")"
INTAKE_EXIT=$?
set -e
INTAKE_STATUS="$(printf '%s' "$INTAKE_JSON" | jq -r '.intake_status // "fail_closed"')"
if [ "$INTAKE_EXIT" -ne 0 ] && [ "$INTAKE_STATUS" = "valid" ]; then
  INTAKE_STATUS="fail_closed"
  INTAKE_JSON='{"intake_status":"fail_closed","failure_reason":"request intake helper failed unexpectedly"}'
fi

SCENE_PACKET_ID="$(printf '%s' "$INTAKE_JSON" | jq -r '.scene_packet_id // "unknown"')"
SCOPE_LABEL="$(printf '%s' "$INTAKE_JSON" | jq -r '.scope_label // "adjacent_scene"')"
SCENE_A_ID="$(printf '%s' "$INTAKE_JSON" | jq -r '.scene_a_id // empty')"
SCENE_B_ID="$(printf '%s' "$INTAKE_JSON" | jq -r '.scene_b_id // empty')"
SCENE_A_TEXT="$(printf '%s' "$INTAKE_JSON" | jq -r '.scene_a_text // empty')"
SCENE_B_TEXT="$(printf '%s' "$INTAKE_JSON" | jq -r '.scene_b_text // empty')"
TASK_INTENT_ID="$(printf '%s' "$INTAKE_JSON" | jq -r '.task_intent_id // empty')"
CONTEXT_BUNDLE_ID="$(printf '%s' "$INTAKE_JSON" | jq -r '.context_bundle_id // empty')"
CONTEXT_BUNDLE_HASH="$(printf '%s' "$INTAKE_JSON" | jq -r '.context_bundle_hash // empty')"
CONTEXT_MANIFEST_REF="$(printf '%s' "$INTAKE_JSON" | jq -r '.context_manifest_ref // empty')"
CONTEXT_PAYLOAD_REF="$(printf '%s' "$INTAKE_JSON" | jq -r '.context_payload_ref // empty')"

# --- Dry run (before run ID generation to avoid next-run-id.sh side effects) ---

if [ "$DRY_RUN" -eq 1 ]; then
  if [ "$INTAKE_STATUS" != "valid" ]; then
    FAILURE_REASON="$(printf '%s' "$INTAKE_JSON" | jq -r '.failure_reason // "request intake failed"')"
    echo "Dry run intake failed. No model call. No log written." >&2
    echo "  task:       $TASK_ID" >&2
    echo "  request:    $REQUEST_FILE" >&2
    echo "  failure:    $FAILURE_REASON" >&2
    exit 1
  fi

  echo "Dry run only. No model call. No log written."
  echo "  task:       $TASK_ID"
  echo "  model:      $MODEL"
  echo "  request:    $REQUEST_FILE"
  echo "  scene a:    $SCENE_A_ID"
  echo "  scene b:    $SCENE_B_ID"
  if [ -n "$TASK_INTENT_ID" ]; then
    echo "  task intent: $TASK_INTENT_ID"
    echo "  context id:  $CONTEXT_BUNDLE_ID"
    echo "  context hash:$CONTEXT_BUNDLE_HASH"
  else
    echo "  context:    none"
  fi
  echo "  output dir: $OUTPUT_DIR"
  exit 0
fi

# --- Generate run identifiers ---

RUN_ID="$(scripts/next-run-id.sh)"
DATE_STR="$(date +%F)"
TIMESTAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
MODEL_SLUG="$(printf '%s' "$MODEL" | tr ':/' '--')"

# --- Output paths ---

mkdir -p "$OUTPUT_DIR"
RAW_OUTPUT_FILE="$OUTPUT_DIR/${MODEL_SLUG}-continuity-adj-${SCENE_A_ID:-intake}-${SCENE_B_ID:-failed}-${RUN_ID}.raw.txt"
ENVELOPE_FILE="$OUTPUT_DIR/${MODEL_SLUG}-continuity-adj-${SCENE_A_ID:-intake}-${SCENE_B_ID:-failed}-${RUN_ID}.envelope.json"

# --- Shared fail-closed envelope writer ---

write_fail_envelope() {
  local failure_reason="$1"
  local raw_file="${2:-null}"
  local validation_json="${3:-null}"

  if [ "$raw_file" = "null" ]; then
    raw_file_json="null"
  else
    raw_file_json="\"$raw_file\""
  fi

  if [ "$validation_json" = "null" ]; then
    validation_block="null"
  else
    validation_block="$validation_json"
  fi

  jq -n \
    --arg task_id "$TASK_ID" \
    --arg contract_version "$CONTRACT_VERSION" \
    --arg route_class "$ROUTE_CLASS" \
    --arg model "$MODEL" \
    --arg run_id "$RUN_ID" \
    --arg timestamp "$TIMESTAMP" \
    --arg scene_packet_id "$SCENE_PACKET_ID" \
    --arg scope_label "$SCOPE_LABEL" \
    --arg failure_reason "$failure_reason" \
    --arg prompt_file "$PROMPT_FILE" \
    --arg request_file "$REQUEST_FILE" \
    --arg task_intent_id "$TASK_INTENT_ID" \
    --arg context_bundle_id "$CONTEXT_BUNDLE_ID" \
    --arg context_bundle_hash "$CONTEXT_BUNDLE_HASH" \
    --arg context_manifest_ref "$CONTEXT_MANIFEST_REF" \
    --arg context_payload_ref "$CONTEXT_PAYLOAD_REF" \
    --argjson raw_file_json "$raw_file_json" \
    --argjson validation_result "$validation_block" \
    '
    {
      task_id: $task_id,
      contract_version: $contract_version,
      route_class: $route_class,
      model_id: $model,
      run_id: $run_id,
      timestamp: $timestamp,
      scene_packet_id: $scene_packet_id,
      scope_label: $scope_label,
      envelope_status: "fail_closed",
      failure_reason: $failure_reason,
      candidate_findings: [],
      validation_result: $validation_result,
      run_metadata: (
        {
          prompt_file: $prompt_file,
          request_file: $request_file,
          raw_output_file: $raw_file_json
        }
        + (if $context_manifest_ref != "" then {context_manifest_ref: $context_manifest_ref} else {} end)
        + (if $context_payload_ref != "" then {context_payload_ref: $context_payload_ref} else {} end)
      )
    }
    + (if $task_intent_id != "" then {task_intent_id: $task_intent_id} else {} end)
    + (if $context_bundle_id != "" then {context_bundle_id: $context_bundle_id} else {} end)
    + (if $context_bundle_hash != "" then {context_bundle_hash: $context_bundle_hash} else {} end)
    ' > "$ENVELOPE_FILE"

  echo "Fail-closed envelope written: $ENVELOPE_FILE"
}

if [ "$INTAKE_STATUS" != "valid" ]; then
  FAILURE_REASON="$(printf '%s' "$INTAKE_JSON" | jq -r '.failure_reason // "request intake failed"')"
  echo "Request intake failed: $FAILURE_REASON" >&2
  write_fail_envelope "$FAILURE_REASON" "null" "null"
  exit 1
fi

# --- Build model input ---

echo "Starting run: $RUN_ID"
echo "  task:    $TASK_ID"
echo "  model:   $MODEL"
echo "  scene a: $SCENE_A_ID"
echo "  scene b: $SCENE_B_ID"
if [ -n "$TASK_INTENT_ID" ]; then
  echo "  task intent:  $TASK_INTENT_ID"
  echo "  context id:   $CONTEXT_BUNDLE_ID"
  echo "  context hash: $CONTEXT_BUNDLE_HASH"
fi

TMP_INPUT="$(mktemp)"
TMP_ERR="$(mktemp)"
cleanup() {
  rm -f "$TMP_INPUT" "$TMP_ERR"
}
trap cleanup EXIT

{
  cat "$PROMPT_FILE"
  printf '\n\nSCENE_A_ID: %s\n\nSCENE_A:\n\n%s\n\nSCENE_B_ID: %s\n\nSCENE_B:\n\n%s\n' \
    "$SCENE_A_ID" "$SCENE_A_TEXT" "$SCENE_B_ID" "$SCENE_B_TEXT"
} > "$TMP_INPUT"

# --- Run model ---

echo "Running model..."
if ! ollama run "$MODEL" < "$TMP_INPUT" > "$RAW_OUTPUT_FILE" 2>"$TMP_ERR"; then
  echo "Error: model run failed for: $MODEL" >&2
  if grep -qi 'requires more system memory' "$TMP_ERR" 2>/dev/null; then
    echo "Cause: insufficient memory for this model" >&2
  fi
  cat "$TMP_ERR" >&2
  write_fail_envelope "model execution failed" "null" "null"
  exit 1
fi

echo "Raw output saved: $RAW_OUTPUT_FILE"

# --- Validate schema ---

echo "Validating schema..."
VALIDATION_RESULT="$(python3 scripts/validate-continuity-candidate.py "$RAW_OUTPUT_FILE" 2>/dev/null || true)"

if [ -z "$VALIDATION_RESULT" ]; then
  VALIDATION_RESULT='{"validation_result":"fail_closed","failure_reason":"validator produced no output"}'
fi

VALIDATION_STATUS="$(printf '%s' "$VALIDATION_RESULT" | jq -r '.validation_result' 2>/dev/null || echo "fail_closed")"

if [ "$VALIDATION_STATUS" != "valid" ]; then
  FAILURE_REASON="$(printf '%s' "$VALIDATION_RESULT" | jq -r '.failure_reason // "schema validation failed"' 2>/dev/null || echo "schema validation failed")"
  echo "Schema validation failed: $FAILURE_REASON" >&2
  write_fail_envelope "$FAILURE_REASON" "$RAW_OUTPUT_FILE" "$VALIDATION_RESULT"
  exit 1
fi

echo "Schema valid."

# --- Extract validated candidate data ---

CANDIDATE_DATA="$(python3 - "$RAW_OUTPUT_FILE" <<'PYEOF'
import json, re, sys

def strip_think_blocks(text):
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)

def extract_json(text):
    text = strip_think_blocks(text).strip()
    if text.startswith("{"):
        return text
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        return match.group(1)
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return text[start:end+1]
    return None

with open(sys.argv[1], encoding="utf-8") as f:
    raw = f.read()

json_text = extract_json(raw)
if json_text is None:
    print("{}")
    sys.exit(1)

data = json.loads(json_text)
print(json.dumps(data))
PYEOF
)"

FINDINGS="$(printf '%s' "$CANDIDATE_DATA" | jq '.candidate_findings')"
OVERALL_NOTE="$(printf '%s' "$CANDIDATE_DATA" | jq -r '.overall_run_note')"
FINDINGS_COUNT="$(printf '%s' "$FINDINGS" | jq 'length')"

# --- Build success envelope ---

jq -n \
  --arg task_id "$TASK_ID" \
  --arg contract_version "$CONTRACT_VERSION" \
  --arg route_class "$ROUTE_CLASS" \
  --arg model "$MODEL" \
  --arg run_id "$RUN_ID" \
  --arg timestamp "$TIMESTAMP" \
  --arg scene_packet_id "$SCENE_PACKET_ID" \
  --arg scope_label "$SCOPE_LABEL" \
  --arg task_intent_id "$TASK_INTENT_ID" \
  --arg context_bundle_id "$CONTEXT_BUNDLE_ID" \
  --arg context_bundle_hash "$CONTEXT_BUNDLE_HASH" \
  --arg context_manifest_ref "$CONTEXT_MANIFEST_REF" \
  --arg context_payload_ref "$CONTEXT_PAYLOAD_REF" \
  --argjson findings "$FINDINGS" \
  --arg overall_note "$OVERALL_NOTE" \
  --argjson validation_result "$VALIDATION_RESULT" \
  --arg prompt_file "$PROMPT_FILE" \
  --arg request_file "$REQUEST_FILE" \
  --arg raw_output_file "$RAW_OUTPUT_FILE" \
  '
  {
    task_id: $task_id,
    contract_version: $contract_version,
    route_class: $route_class,
    model_id: $model,
    run_id: $run_id,
    timestamp: $timestamp,
    scene_packet_id: $scene_packet_id,
    scope_label: $scope_label,
    envelope_status: "valid_candidate",
    candidate_findings: $findings,
    overall_run_note: $overall_note,
    validation_result: $validation_result,
    run_metadata: (
      {
        prompt_file: $prompt_file,
        request_file: $request_file,
        raw_output_file: $raw_output_file
      }
      + (if $context_manifest_ref != "" then {context_manifest_ref: $context_manifest_ref} else {} end)
      + (if $context_payload_ref != "" then {context_payload_ref: $context_payload_ref} else {} end)
    )
  }
  + (if $task_intent_id != "" then {task_intent_id: $task_intent_id} else {} end)
  + (if $context_bundle_id != "" then {context_bundle_id: $context_bundle_id} else {} end)
  + (if $context_bundle_hash != "" then {context_bundle_hash: $context_bundle_hash} else {} end)
  ' > "$ENVELOPE_FILE"

echo "Candidate artifact envelope written: $ENVELOPE_FILE"
echo "  findings: $FINDINGS_COUNT"
echo "  overall:  $OVERALL_NOTE"

# --- Log to registry (success only) ---

CONTEXT_NOTE="context=none"
if [ -n "$TASK_INTENT_ID" ]; then
  CONTEXT_NOTE="task_intent_id=${TASK_INTENT_ID}, context_bundle_id=${CONTEXT_BUNDLE_ID}, context_bundle_hash=${CONTEXT_BUNDLE_HASH}"
  if [ -n "$CONTEXT_MANIFEST_REF" ]; then
    CONTEXT_NOTE=", ${CONTEXT_NOTE}, context_manifest_ref=${CONTEXT_MANIFEST_REF}"
    CONTEXT_NOTE="${CONTEXT_NOTE#, }"
  fi
  if [ -n "$CONTEXT_PAYLOAD_REF" ]; then
    CONTEXT_NOTE="${CONTEXT_NOTE}, context_payload_ref=${CONTEXT_PAYLOAD_REF}"
  fi
fi

scripts/log-run.sh \
  "$RUN_ID" \
  "$DATE_STR" \
  "$MODEL" \
  "$PROMPT_FILE" \
  "$REQUEST_FILE" \
  "$ENVELOPE_FILE" \
  "$TASK_ID" \
  "adjacent_scene: ${SCENE_A_ID}+${SCENE_B_ID}, findings: ${FINDINGS_COUNT}, ${CONTEXT_NOTE}"

echo
echo "Run complete and logged:"
echo "  run id:   $RUN_ID"
echo "  envelope: $ENVELOPE_FILE"
