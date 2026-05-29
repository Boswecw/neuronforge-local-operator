#!/usr/bin/env bash
set -euo pipefail

# run-style-analysis.sh
#
# Executor for task: analyze.style.scene.v1
# Route class:       WORKHORSE_LOCAL
# Trust posture:     candidate_only
# Output mode:       STRUCTURED_ANALYSIS
# Fallback policy:   degraded_allowed
#
# Usage:
#   scripts/run-style-analysis.sh [--dry-run] <model> <scene_file> [<output_dir>]
#
# Arguments:
#   model       Ollama model name (WORKHORSE_LOCAL tier, e.g. qwen2.5:14b)
#   scene_file  Plain text file containing the scene to analyze
#   output_dir  Directory for output files (default: outputs)

TASK_ID="analyze.style.scene.v1"
CONTRACT_VERSION="v1"
ROUTE_CLASS="WORKHORSE_LOCAL"
PROMPT_FILE="prompts/style-analysis-scene-v1.md"

DRY_RUN=0
if [ "${1:-}" = "--dry-run" ]; then
  DRY_RUN=1
  shift
fi

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 [--dry-run] <model> <scene_file> [<output_dir>]"
  echo
  echo "  model       Ollama model name (WORKHORSE_LOCAL tier)"
  echo "  scene_file  Plain text file containing the scene text"
  echo "  output_dir  Output directory (default: outputs)"
  exit 1
fi

MODEL="$1"
SCENE_FILE="$2"
OUTPUT_DIR="${3:-outputs}"

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# --- Prerequisite checks ---

if [ ! -f "$PROMPT_FILE" ]; then
  echo "Error: prompt file not found: $PROMPT_FILE" >&2
  exit 1
fi

if [ ! -f "$SCENE_FILE" ]; then
  echo "Error: scene file not found: $SCENE_FILE" >&2
  exit 1
fi

for cmd in ollama python3; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Error: $cmd is not installed or not on PATH" >&2
    exit 1
  fi
done

if [ ! -f scripts/next-run-id.sh ] || [ ! -x scripts/next-run-id.sh ]; then
  echo "Error: scripts/next-run-id.sh missing or not executable" >&2
  exit 1
fi

if [ ! -f scripts/log-run.sh ] || [ ! -x scripts/log-run.sh ]; then
  echo "Error: scripts/log-run.sh missing or not executable" >&2
  exit 1
fi

# --- Dry run ---

if [ "$DRY_RUN" -eq 1 ]; then
  MODEL_SLUG="$(printf '%s' "$MODEL" | tr ':/' '--')"
  echo "Dry run only. No model call. No log written."
  echo "  task:       $TASK_ID"
  echo "  model:      $MODEL"
  echo "  scene file: $SCENE_FILE"
  echo "  output dir: $OUTPUT_DIR"
  exit 0
fi

# --- Generate run identifiers ---

RUN_ID="$(scripts/next-run-id.sh)"
DATE_STR="$(date +%F)"
TIMESTAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
MODEL_SLUG="$(printf '%s' "$MODEL" | tr ':/' '--')"
SCENE_SLUG="$(basename "$SCENE_FILE" .txt | tr ' ' '-' | cut -c1-40)"

# --- Output paths ---

mkdir -p "$OUTPUT_DIR"
RAW_OUTPUT_FILE="$OUTPUT_DIR/${MODEL_SLUG}-style-${SCENE_SLUG}-${RUN_ID}.raw.txt"
ENVELOPE_FILE="$OUTPUT_DIR/${MODEL_SLUG}-style-${SCENE_SLUG}-${RUN_ID}.envelope.json"

# --- Shared fail envelope writer ---

write_fail_envelope() {
  local failure_reason="$1"
  python3 - <<PYEOF
import json, sys
envelope = {
    "task_id": "${TASK_ID}",
    "contract_version": "${CONTRACT_VERSION}",
    "route_class": "${ROUTE_CLASS}",
    "model_id": "${MODEL}",
    "run_id": "${RUN_ID}",
    "timestamp": "${TIMESTAMP}",
    "envelope_status": "failed",
    "failure_reason": """$failure_reason""",
    "route_class": "WORKHORSE_LOCAL",
    "model_id": "${MODEL}",
    "runtime_mode_used": "WORKHORSE_LOCAL",
    "provenance_class": "inferred_candidate",
    "schema_validation_status": "failed",
    "warnings": ["""$failure_reason"""],
    "output_payload": None
}
with open("${ENVELOPE_FILE}", "w") as f:
    json.dump(envelope, f, indent=2)
PYEOF
  echo "Fail envelope written: $ENVELOPE_FILE"
}

# --- Build model input ---

echo "Starting run: $RUN_ID"
echo "  task:   $TASK_ID"
echo "  model:  $MODEL"
echo "  scene:  $SCENE_FILE"

TMP_INPUT="$(mktemp)"
TMP_ERR="$(mktemp)"
cleanup() {
  rm -f "$TMP_INPUT" "$TMP_ERR"
}
trap cleanup EXIT

{
  cat "$PROMPT_FILE"
  printf '\n\n'
  cat "$SCENE_FILE"
} > "$TMP_INPUT"

# --- Run model ---

echo "Running model..."
if ! ollama run "$MODEL" < "$TMP_INPUT" > "$RAW_OUTPUT_FILE" 2>"$TMP_ERR"; then
  echo "Error: model run failed for: $MODEL" >&2
  if grep -qi 'requires more system memory' "$TMP_ERR" 2>/dev/null; then
    echo "Cause: insufficient memory for this model" >&2
  fi
  cat "$TMP_ERR" >&2
  write_fail_envelope "model execution failed"
  exit 1
fi

echo "Raw output saved: $RAW_OUTPUT_FILE"

# --- Normalize and validate using Python normalizer ---

echo "Normalizing output..."
NORMALIZE_RESULT="$(python3 - "$RAW_OUTPUT_FILE" "${MODEL}" <<'PYEOF'
import sys
import json
from pathlib import Path

# Allow running from project root regardless of cwd
project_root = Path(__file__).resolve().parent if hasattr(Path(__file__), 'resolve') else Path.cwd()
# Add scripts/ to path so style_analysis package is importable
import sys
sys.path.insert(0, str(Path(sys.argv[0]).resolve().parent.parent / "scripts"))

from style_analysis.normalizer import normalize_model_output

raw_file = sys.argv[1]
model_id = sys.argv[2]

with open(raw_file, encoding="utf-8") as f:
    raw_text = f.read()

response = normalize_model_output(raw_text, model_id=model_id)
print(json.dumps(response.model_dump(), indent=2))
PYEOF
)" || true

if [ -z "$NORMALIZE_RESULT" ]; then
  NORMALIZE_RESULT='{"schema_validation_status":"failed","warnings":["normalizer produced no output"]}'
fi

VALIDATION_STATUS="$(printf '%s' "$NORMALIZE_RESULT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('schema_validation_status','failed'))" 2>/dev/null || echo "failed")"

# Merge run metadata into envelope
python3 - <<PYEOF
import json, sys

with open("${ENVELOPE_FILE}", "w") as f:
    data = json.loads(r"""${NORMALIZE_RESULT}""")
    data["task_id"] = "${TASK_ID}"
    data["contract_version"] = "${CONTRACT_VERSION}"
    data["run_id"] = "${RUN_ID}"
    data["timestamp"] = "${TIMESTAMP}"
    data["run_metadata"] = {
        "prompt_file": "${PROMPT_FILE}",
        "scene_file": "${SCENE_FILE}",
        "raw_output_file": "${RAW_OUTPUT_FILE}"
    }
    json.dump(data, f, indent=2)
PYEOF

echo "Envelope written: $ENVELOPE_FILE"
echo "  schema_validation_status: $VALIDATION_STATUS"

# --- Log run (all outcomes) ---

scripts/log-run.sh \
  "$RUN_ID" \
  "$DATE_STR" \
  "$MODEL" \
  "$PROMPT_FILE" \
  "$SCENE_FILE" \
  "$ENVELOPE_FILE" \
  "$TASK_ID" \
  "style analysis, status: ${VALIDATION_STATUS}"

echo
echo "Run complete and logged:"
echo "  run id:   $RUN_ID"
echo "  envelope: $ENVELOPE_FILE"
echo "  status:   $VALIDATION_STATUS"
