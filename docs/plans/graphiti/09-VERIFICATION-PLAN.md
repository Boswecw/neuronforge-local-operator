# Verification Plan

## Verification Goals

Prove:

- schemas are strict;
- mappings are deterministic;
- IDs are stable;
- rebuilds are provenance-equal;
- source references are exact;
- graph outages do not break NLO runs;
- stale graphs do not advise promotion;
- query evidence is correct;
- prohibited data is rejected.

## Test Categories

### Contract Tests

- valid/invalid schema fixtures;
- round-trip serialization;
- taxonomy-version checks;
- referential integrity;
- hash verification;
- temporal-order validation.

### Identity Tests

- stable IDs across runs;
- Unicode normalization;
- property-order independence;
- set-order normalization;
- collision detection;
- edge uniqueness.

### Projection Tests

- duplicate replay;
- partial write failure;
- unsupported schema quarantine;
- deterministic clean rebuild;
- mapping mutation detection;
- source-reference preservation.

### Query Tests

- golden evidence sets;
- contradictions preserved;
- stale graph rejection;
- missing source ID rejection;
- narrative cannot alter evidence;
- exact temporal ordering.

### Operational Failure Matrix

| Failure | Expected Behavior |
|---|---|
| Graph unavailable during NLO run | Run succeeds; projection skipped or queued |
| Invalid canonical record | Record quarantined; source unchanged |
| Partial rebuild | Graph marked unusable |
| Fingerprint mismatch | Query surface disabled |
| Stale projection | Query returns stale or refuses advisory output |
| Missing source ID | Result rejected |
| Unsupported schema | Record quarantined |
| Backend restart | Reconnect or explicit degraded status |
| Corrupted graph state | Clean rebuild required |
| External enrichment disabled | No external calls possible |

## Advanced Tests

- property-based identity tests;
- mutation tests for mappings;
- contradictory historical fixtures;
- clock-skew fixtures;
- backend restart tests;
- corrupted state tests;
- prohibited-content tests;
- decommission rehearsal.

## Exit Gate

No Graphiti query is accepted unless:

- provenance equality passes;
- golden evidence tests pass;
- fail-open run tests pass;
- fail-closed advisory tests pass;
- no prohibited data leaves the local process.
