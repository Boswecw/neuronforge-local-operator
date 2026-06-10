#!/bin/bash
# Secure reset of the pilot graph backend (plan 13 secure-deletion steps 1-3, 8):
# stop containers, remove containers, remove the named volume, clear runtime
# projection artifacts. The graph is rebuildable from canonical records only.
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO_ROOT"
# shellcheck source=scripts/graph/_compose.sh
source "$REPO_ROOT/scripts/graph/_compose.sh"

if [[ "${1:-}" != "--yes" ]]; then
  echo "This deletes the graph volume and runtime projection artifacts." >&2
  echo "The graph is disposable and rebuilds from canonical records, but the" >&2
  echo "deletion is immediate. Re-run with --yes to proceed." >&2
  exit 1
fi

require_docker
detect_compose
load_graph_env 0

"${COMPOSE[@]}" -f "$COMPOSE_FILE" down -v
rm -rf runtime/graph
echo "graph backend reset: containers removed, volume removed, runtime/graph cleared"
echo "rebuild with: scripts/graph/nlo-graph rebuild --prove"
