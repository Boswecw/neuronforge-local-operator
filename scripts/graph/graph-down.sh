#!/bin/bash
# Stop the pilot graph backend; data volume is retained (use graph-reset.sh to wipe).
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO_ROOT"
docker compose --env-file .env.graphiti -f docker-compose.graphiti-pilot.yml down
echo "graph backend stopped (volume retained)"
