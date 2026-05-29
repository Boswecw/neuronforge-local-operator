#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

RUNS_FILE="registry/runs.md"
TODAY="$(date +%F)"

if [ ! -f "$RUNS_FILE" ]; then
  echo "run-$TODAY-001"
  exit 0
fi

LAST_NUM="$(
  { grep -oE "run-$TODAY-[0-9]{3}" "$RUNS_FILE" || :; } \
    | sed -E "s/run-$TODAY-([0-9]{3})/\1/" \
    | sort -n \
    | tail -n 1
)"

if [ -z "${LAST_NUM:-}" ]; then
  NEXT_NUM="001"
else
  NEXT_NUM="$(printf "%03d" $((10#$LAST_NUM + 1)))"
fi

echo "run-$TODAY-$NEXT_NUM"
