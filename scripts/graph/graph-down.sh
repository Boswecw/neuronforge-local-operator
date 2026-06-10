#!/bin/bash
# Stop the pilot graph backend; data volume is retained (use graph-reset.sh to wipe).
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO_ROOT"
# shellcheck source=scripts/graph/_compose.sh
source "$REPO_ROOT/scripts/graph/_compose.sh"

require_docker
detect_compose
load_graph_env 0

"${COMPOSE[@]}" -f "$COMPOSE_FILE" down
echo "graph backend stopped (volume retained)"
