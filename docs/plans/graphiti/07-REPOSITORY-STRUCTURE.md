# Repository Structure

## Recommended Package Layout

```text
src/nlo_experiment_memory/
├── contracts/
├── identity/
├── stores/
├── projection/
├── queries/
├── cli/
└── enrichment/

schemas/experiment_memory/
tests/fixtures/experiment_memory/
tests/experiment_memory/
docs/plans/graphiti/
scripts/graph/
```

Do not place executable service code under `analytics/`.

## File Policy

### Committed

- schemas;
- typed contract definitions;
- deterministic mappings;
- test fixtures;
- golden query results;
- architecture documents;
- pinned compose files;
- non-sensitive sample configuration;
- promotion manifests;
- reviewed proof reports where appropriate.

### Ignored

- graph database volumes;
- runtime logs;
- local credentials;
- temporary exports;
- raw manuscript extracts;
- local embedding caches;
- projection scratch files;
- Docker state;
- generated backend indexes.

## Suggested `.gitignore` Additions

```text
.graphiti/
.neo4j/
.falkordb/
runtime/graph/
artifacts/graph-runtime/
*.graph-snapshot
.env.graphiti
```

## Module Boundaries

- `contracts`: canonical and projection-facing types.
- `identity`: IDs, normalization, hashing, fingerprints.
- `stores`: file fixture and DataForge Local adapters.
- `projection`: deterministic mapping and graph writes.
- `queries`: evidence retrieval only.
- `cli`: operator presentation.
- `enrichment`: optional, disabled, isolated.

Graphiti-specific types must not leak into canonical NLO task contracts.
