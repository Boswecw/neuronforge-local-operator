#!/bin/bash
# Start the pinned pilot graph backend (operator opt-in only; never run by NLO).
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO_ROOT"
# shellcheck source=scripts/graph/_compose.sh
source "$REPO_ROOT/scripts/graph/_compose.sh"

require_docker
detect_compose
load_graph_env 1

"${COMPOSE[@]}" -f "$COMPOSE_FILE" up -d

echo "waiting for backend health (up to 3 minutes)..."
state="starting"
for _ in $(seq 1 36); do
  state="$(docker inspect -f '{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' "$GRAPH_CONTAINER" 2>/dev/null || echo missing)"
  if [[ "$state" == "healthy" ]]; then
    break
  fi
  if [[ "$state" == "exited" || "$state" == "dead" ]]; then
    echo "container is $state; inspect with: docker logs $GRAPH_CONTAINER" >&2
    exit 1
  fi
  sleep 5
done
if [[ "$state" != "healthy" ]]; then
  echo "backend did not report healthy in time (last state: $state)" >&2
  echo "inspect with: docker logs $GRAPH_CONTAINER" >&2
  exit 1
fi

echo "verifying loopback-only binding..."
BINDINGS="$(docker port "$GRAPH_CONTAINER")"
echo "$BINDINGS"
if echo "$BINDINGS" | grep -vE '127\.0\.0\.1|\[::1\]' | grep -q ':'; then
  echo "ERROR: backend is bound beyond loopback; stopping it" >&2
  bash "$REPO_ROOT/scripts/graph/graph-down.sh"
  exit 1
fi
echo "graph backend up (loopback only). Stop with scripts/graph/graph-down.sh"
