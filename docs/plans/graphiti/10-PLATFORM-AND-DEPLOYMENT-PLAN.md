# Platform and Deployment Plan

## Pilot Backend Decision

Use one pinned local graph backend only.

Recommended initial choice:

```text
Neo4j Community in Docker
```

A different backend may be selected before implementation, but the pilot must support only one real backend.

## Required Files

```text
docker-compose.graphiti-pilot.yml
.env.graphiti.example
scripts/graph/graph-up.sh
scripts/graph/graph-down.sh
scripts/graph/graph-reset.sh
scripts/graph/graph-doctor.sh
```

## Platform Requirements

- loopback-only binding;
- fixed container image version;
- explicit memory and CPU limits;
- named local volume;
- health check;
- no automatic startup with NLO;
- no public port exposure;
- no production deployment;
- no cloud persistence.

## Health States

```text
healthy
degraded
stale
rebuilding
invalid
unavailable
```

## Freshness

Track:

- canonical source high-watermark;
- projected high-watermark;
- projection lag;
- last successful rebuild;
- last verified fingerprint.

## Startup Doctrine

Graph startup is operator opt-in.

NLO must not require Graphiti to launch, run local models, evaluate outputs, or record canonical results.

## Version Matrix

Pin:

- Python;
- Graphiti;
- graph backend;
- Docker Compose schema;
- embedding library;
- optional enrichment model/provider.

No floating `latest` tags.
