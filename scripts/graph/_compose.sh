# Shared helpers for the pilot graph scripts. Source, don't execute.
#
# Portability notes:
# - Ubuntu's docker.io package does not ship the Compose v2 plugin; detect
#   `docker compose` first, fall back to legacy `docker-compose`, and explain
#   how to install the plugin otherwise.
# - Environment is passed to compose by sourcing .env.graphiti (set -a),
#   not via `--env-file`, which older CLIs reject.

COMPOSE_FILE="docker-compose.graphiti-pilot.yml"
GRAPH_CONTAINER="nlo-graphiti-pilot-neo4j"

# Repo convention (requirements.txt): deps live in .venv. Prefer it when the
# caller is not already inside a virtualenv (PEP 668 hosts). Callers must set
# REPO_ROOT before sourcing this file.
nlo_python() {
  if [[ -z "${VIRTUAL_ENV:-}" && -x "$REPO_ROOT/.venv/bin/python3" ]]; then
    echo "$REPO_ROOT/.venv/bin/python3"
  else
    echo "python3"
  fi
}

require_docker() {
  if ! command -v docker >/dev/null 2>&1; then
    echo "docker is not available; the graph backend is optional and NLO runs do not need it" >&2
    return 1
  fi
  local info_err
  if ! info_err="$(docker info 2>&1 >/dev/null)"; then
    if grep -qi "permission denied" <<<"$info_err"; then
      echo "docker daemon is running but you lack permission to use it." >&2
      echo "Fix:  sudo usermod -aG docker \$USER   (then log out and back in, or run: newgrp docker)" >&2
    else
      echo "docker CLI found but the daemon is not reachable." >&2
      echo "Fix:  sudo systemctl enable --now docker   (then re-run this script)" >&2
    fi
    return 1
  fi
}

# Selects a compose invocation into the COMPOSE array, e.g. "${COMPOSE[@]}" ...
detect_compose() {
  if docker compose version >/dev/null 2>&1; then
    COMPOSE=(docker compose)
    return 0
  fi
  if command -v docker-compose >/dev/null 2>&1; then
    COMPOSE=(docker-compose)
    return 0
  fi
  echo "Docker Compose is not installed (the docker.io package alone does not include it)." >&2
  echo "On Ubuntu/Debian:  sudo apt install docker-compose-v2" >&2
  echo "Other platforms:   https://docs.docker.com/compose/install/" >&2
  return 1
}

# strict=1 requires .env.graphiti (up); strict=0 tolerates its absence (down/reset).
load_graph_env() {
  local strict="${1:-1}"
  if [[ -f .env.graphiti ]]; then
    set -a
    # shellcheck disable=SC1091
    source ./.env.graphiti
    set +a
  elif [[ "$strict" == "1" ]]; then
    echo "missing .env.graphiti — run: cp .env.graphiti.example .env.graphiti  (then set a local password)" >&2
    return 1
  else
    # compose evaluates ${NLO_GRAPH_NEO4J_PASSWORD:?} even for down/reset
    export NLO_GRAPH_NEO4J_PASSWORD="${NLO_GRAPH_NEO4J_PASSWORD:-unused-for-teardown}"
  fi
}
