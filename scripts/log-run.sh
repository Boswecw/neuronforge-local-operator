#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 8 ]; then
  echo "Usage: scripts/log-run.sh <run_id> <date> <model> <prompt_file> <input_file> <output_file> <task> <notes>"
  exit 1
fi

RUN_ID="$1"
DATE_VALUE="$2"
MODEL="$3"
PROMPT_FILE="$4"
INPUT_FILE="$5"
OUTPUT_FILE="$6"
TASK="$7"
NOTES="$8"

cat >> registry/runs.md <<EOF

- run id: $RUN_ID
  date: $DATE_VALUE
  model: $MODEL
  prompt file: $PROMPT_FILE
  input file: $INPUT_FILE
  output file: $OUTPUT_FILE
  task: $TASK
  notes: $NOTES
EOF

echo "Logged run: $RUN_ID"
