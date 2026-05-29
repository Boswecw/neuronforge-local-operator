#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 4 ]; then
  echo "Usage: scripts/run-proofread.sh <model> <prompt_file> <input_file> <output_file>"
  exit 1
fi

MODEL="$1"
PROMPT_FILE="$2"
INPUT_FILE="$3"
OUTPUT_FILE="$4"

if [ ! -f "$PROMPT_FILE" ]; then
  echo "Prompt file not found: $PROMPT_FILE" >&2
  exit 1
fi

if [ ! -f "$INPUT_FILE" ]; then
  echo "Input file not found: $INPUT_FILE" >&2
  exit 1
fi

if ! command -v ollama >/dev/null 2>&1; then
  echo "Error: ollama is not installed or not on PATH" >&2
  exit 1
fi

mkdir -p "$(dirname "$OUTPUT_FILE")"

TMP_OUTPUT="$(mktemp)"
TMP_ERR="$(mktemp)"
cleanup() {
  rm -f "$TMP_OUTPUT" "$TMP_ERR"
}
trap cleanup EXIT

if ! (
  cat "$PROMPT_FILE"
  printf '\n\nPASSAGE:\n\n'
  cat "$INPUT_FILE"
) | ollama run "$MODEL" >"$TMP_OUTPUT" 2>"$TMP_ERR"; then
  echo "Error: proofreading run failed for model: $MODEL" >&2

  if grep -qi 'requires more system memory' "$TMP_ERR"; then
    echo "Cause: insufficient available system memory for this model." >&2
  fi

  echo "--- ollama stderr ---" >&2
  cat "$TMP_ERR" >&2

  rm -f "$OUTPUT_FILE"
  exit 1
fi

mv "$TMP_OUTPUT" "$OUTPUT_FILE"
echo "Saved output to: $OUTPUT_FILE"
