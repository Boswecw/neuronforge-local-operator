#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 4 ] || [ "$#" -gt 5 ]; then
  echo "Usage: scripts/review-proofread.sh <model> <prompt_file> <input_file> <output_file> [prior_output_file]"
  exit 1
fi

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

MODEL="$1"
PROMPT_FILE="$2"
INPUT_FILE="$3"
OUTPUT_FILE="$4"
PRIOR_OUTPUT="${5:-}"

if [ ! -x scripts/run-proofread.sh ]; then
  echo "Error: scripts/run-proofread.sh is missing or not executable" >&2
  exit 1
fi

if [ -n "$PRIOR_OUTPUT" ] && [ ! -f "$PRIOR_OUTPUT" ]; then
  echo "Error: prior output file not found: $PRIOR_OUTPUT" >&2
  exit 1
fi

scripts/run-proofread.sh \
  "$MODEL" \
  "$PROMPT_FILE" \
  "$INPUT_FILE" \
  "$OUTPUT_FILE"

echo
echo "=== NEW OUTPUT ==="
cat "$OUTPUT_FILE"
echo

if [ -n "$PRIOR_OUTPUT" ]; then
  echo
  echo "=== DIFF VS PRIOR OUTPUT ==="
  diff -u "$PRIOR_OUTPUT" "$OUTPUT_FILE" || true
fi
