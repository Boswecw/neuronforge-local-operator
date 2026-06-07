#!/bin/bash
set -euo pipefail

# NLO = NeuronForge Local Operator.
# The root system doc is prefixed (NLOSYSTEM.md) to make this repo's identity
# explicit and distinct from the public-facing NeuronForge system doc.
# The root NLOSYSTEM.md is the single canonical build artifact.
PARTS_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$PARTS_DIR/../.." && pwd)"
ROOT_OUTPUT="$REPO_ROOT/NLOSYSTEM.md"
TMP_OUTPUT="$(mktemp)"

echo "Assembling NLOSYSTEM.md..."

cat "$PARTS_DIR/_index.md" > "$TMP_OUTPUT"

for part in "$PARTS_DIR"/[0-9][0-9]-*.md; do
  echo "" >> "$TMP_OUTPUT"
  echo "---" >> "$TMP_OUTPUT"
  echo "" >> "$TMP_OUTPUT"
  cat "$part" >> "$TMP_OUTPUT"
done

cp "$TMP_OUTPUT" "$ROOT_OUTPUT"
chmod 664 "$ROOT_OUTPUT"

LINE_COUNT=$(wc -l < "$ROOT_OUTPUT")
rm -f "$TMP_OUTPUT"
echo "NLOSYSTEM.md assembled: $LINE_COUNT lines"
