#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "Usage: scripts/compare-outputs.sh <file_a> <file_b>" >&2
  exit 1
fi

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

FILE_A="$1"
FILE_B="$2"

if [ ! -f "$FILE_A" ]; then
  echo "Error: first file not found: $FILE_A" >&2
  exit 1
fi

if [ ! -f "$FILE_B" ]; then
  echo "Error: second file not found: $FILE_B" >&2
  exit 1
fi

echo "=== FILE A: $FILE_A ==="
echo
cat "$FILE_A"
echo
echo "=== FILE B: $FILE_B ==="
echo
cat "$FILE_B"
echo
echo "=== DIFF ==="
diff -u "$FILE_A" "$FILE_B" || true
