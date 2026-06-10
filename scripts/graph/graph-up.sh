#!/bin/bash
# Start the pinned pilot graph backend (operator opt-in only; never run by NLO).
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO_ROOT"

if ! command -v docker >/dev/null 2>&1; then
  echo "docker is not available; the graph backend is optional and NLO runs do not need it" >&2
  exit 1
fi
if [[ ! -f .env.graphiti ]]; then
  echo "missing .env.graphiti — run: cp .env.graphiti.example .env.graphiti  (then set a local password)" >&2
  exit 1
fi

docker compose --env-file .env.graphiti -f docker-compose.graphiti-pilot.yml up -d --wait

echo "verifying loopback-only binding..."
BINDINGS="$(docker port nlo-graphiti-pilot-neo4j)"
echo "$BINDINGS"
if echo "$BINDINGS" | grep -vE '127\.0\.0\.1|\[::1\]' | grep -q ':'; then
  echo "ERROR: backend is bound beyond loopback; stopping it" >&2
  bash "$REPO_ROOT/scripts/graph/graph-down.sh"
  exit 1
fi
echo "graph backend up (loopback only). Stop with scripts/graph/graph-down.sh"
