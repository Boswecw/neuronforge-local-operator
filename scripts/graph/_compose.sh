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

require_docker() {
  if ! command -v docker >/dev/null 2>&1; then
    echo "docker is not available; the graph backend is optional and NLO runs do not need it" >&2
    return 1
  fi
  if ! docker info >/dev/null 2>&1; then
    echo "docker CLI found but the daemon is not reachable; start Docker and retry" >&2
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
