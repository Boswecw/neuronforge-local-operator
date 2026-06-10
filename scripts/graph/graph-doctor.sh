#!/bin/bash
# Diagnose the pilot graph surface. Reports one of the plan-10 health states:
# healthy | degraded | stale | rebuilding | invalid | unavailable
set -uo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO_ROOT"
# shellcheck source=scripts/graph/_compose.sh
source "$REPO_ROOT/scripts/graph/_compose.sh"

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
  if detect_compose 2>/dev/null; then
    echo "compose: ${COMPOSE[*]} ($("${COMPOSE[@]}" version --short 2>/dev/null || echo version unknown))"
  else
    echo "compose: NOT INSTALLED — on Ubuntu/Debian: sudo apt install docker-compose-v2"
  fi
  STATE="$(docker inspect -f '{{.State.Status}} (health: {{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}})' "$GRAPH_CONTAINER" 2>/dev/null || echo 'not created')"
  echo "container $GRAPH_CONTAINER: $STATE"
  if [[ "$STATE" == running* ]]; then
    echo "port bindings:"
    docker port "$GRAPH_CONTAINER" | sed 's/^/  /'
    if docker port "$GRAPH_CONTAINER" | grep -vE '127\.0\.0\.1|\[::1\]' | grep -q ':'; then
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

echo ""
echo "== rebuild determinism =="
python3 - <<'PY' || true
import json
from pathlib import Path

report_path = Path("runtime/graph/report.json")
frozen_path = Path("tests/fixtures/experiment_memory/golden/fingerprint.txt")
if not report_path.is_file():
    print("no runtime/graph/report.json yet (run: scripts/graph/nlo-graph rebuild --prove)")
else:
    report = json.loads(report_path.read_text(encoding="utf-8"))
    frozen = frozen_path.read_text(encoding="utf-8").strip()
    print(f"report: nodes={report.get('node_count')} edges={report.get('edge_count')} "
          f"seen={report.get('records_seen')} projected={report.get('records_projected')} "
          f"quarantined={len(report.get('quarantined', []))}")
    if report.get("fingerprint") == frozen:
        print("fingerprint matches the frozen golden value (committed fixture records)")
    else:
        print("WARNING: fingerprint differs from the frozen golden value:")
        print(f"  report : {report.get('fingerprint')}")
        print(f"  frozen : {frozen}")
        print("  If this projection was rebuilt from the default fixture records, the")
        print("  records tree differs from the committed state (extra, missing, or")
        print("  locally modified record files). Diagnose with:")
        print("    git status tests/fixtures/experiment_memory/records/")
        print("    python3 -m pytest tests/experiment_memory/ -q")
        print("    bash scripts/graph/nlo-graph rebuild --prove")
PY
