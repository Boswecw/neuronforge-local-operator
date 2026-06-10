#!/bin/bash
# Diagnose the pilot graph surface. Reports one of the plan-10 health states:
# healthy | degraded | stale | rebuilding | invalid | unavailable
set -uo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO_ROOT"

echo "== files =="
for f in docker-compose.graphiti-pilot.yml .env.graphiti.example; do
  [[ -f "$f" ]] && echo "ok      $f" || echo "MISSING $f"
done
[[ -f .env.graphiti ]] && echo "ok      .env.graphiti" \
  || echo "absent  .env.graphiti (backend opt-in not configured; this is fine for NLO runs)"

echo ""
echo "== docker =="
if command -v docker >/dev/null 2>&1; then
  docker --version
  STATE="$(docker inspect -f '{{.State.Status}} (health: {{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}})' nlo-graphiti-pilot-neo4j 2>/dev/null || echo 'not created')"
  echo "container nlo-graphiti-pilot-neo4j: $STATE"
  if [[ "$STATE" == running* ]]; then
    echo "port bindings:"
    docker port nlo-graphiti-pilot-neo4j | sed 's/^/  /'
    if docker port nlo-graphiti-pilot-neo4j | grep -vE '127\.0\.0\.1|\[::1\]' | grep -q ':'; then
      echo "WARNING: binding beyond loopback violates the pilot security posture"
    fi
  fi
else
  echo "docker not available (backend unavailable; NLO runs are unaffected — fail open)"
fi

echo ""
echo "== projection =="
export PYTHONPATH="$REPO_ROOT/src:${PYTHONPATH:-}"
python3 -m nlo_experiment_memory.cli status || true
