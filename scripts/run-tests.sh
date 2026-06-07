#!/bin/bash
# Run the full NeuronForge Local Operator test surface, honestly.
#
# "Honestly" means HTTP/route tests are NOT allowed to silently skip when a
# dependency is missing: NF_REQUIRE_HTTP_TESTS=1 turns those skips into hard
# failures. Install deps first:  pip install -r requirements-dev.txt
#
# Usage:  bash scripts/run-tests.sh
set -uo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

export NF_REQUIRE_HTTP_TESTS=1
# Make in-repo packages importable (scripts/, service/, prompt_assembly/).
export PYTHONPATH="$REPO_ROOT/scripts:$REPO_ROOT:${PYTHONPATH:-}"

status=0
run() {
  echo ""
  echo "=== $1 ==="
  shift
  if "$@"; then
    echo "  -> PASS"
  else
    echo "  -> FAIL (exit $?)"
    status=1
  fi
}

run "style-analysis (python)"      python3 tests/test-style-analysis.py
run "cor-gnat handoff (python)"    python3 tests/test-cor-gnat-semantic-handoff.py
run "prompt_assembly (pytest)"     python3 -m pytest prompt_assembly/tests/ -q
run "continuity adjacent (shell)"  bash tests/test-continuity-adjacent-scene.sh

echo ""
if [[ "$status" -eq 0 ]]; then
  echo "ALL SUITES PASSED"
else
  echo "ONE OR MORE SUITES FAILED"
fi
exit "$status"
