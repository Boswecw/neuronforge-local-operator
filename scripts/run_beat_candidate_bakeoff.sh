#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <model_name> <scene_file>"
  echo "Example: $0 qwen2.5:14b inputs/beat_candidate_bakeoff/scene_001.md"
  exit 1
fi

MODEL="$1"
SCENE_FILE="$2"

PROMPT_FILE="prompts/beat_candidate_bakeoff/beat_candidate_extraction_v1.md"

if [ ! -f "$PROMPT_FILE" ]; then
  echo "Missing prompt file: $PROMPT_FILE"
  exit 1
fi

if [ ! -f "$SCENE_FILE" ]; then
  echo "Missing scene file: $SCENE_FILE"
  exit 1
fi

SCENE_ID="$(basename "$SCENE_FILE" .md)"
MODEL_SAFE="$(echo "$MODEL" | tr ':/' '__')"
OUT_DIR="outputs/beat_candidate_bakeoff/${SCENE_ID}"
mkdir -p "$OUT_DIR"

TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
RAW_OUT="${OUT_DIR}/${MODEL_SAFE}-${TIMESTAMP}.json"

{
  cat "$PROMPT_FILE"
  echo
  echo "Scene ID: ${SCENE_ID}"
  echo
  echo "Scene text:"
  cat "$SCENE_FILE"
} | ollama run "$MODEL" > "$RAW_OUT"

echo "Saved output:"
echo "$RAW_OUT"