# G-09 Comparative Evaluation

Date: 2026-06-10
Evaluator: Codex, using the committed NLO experiment-memory fixture set and tests

## Scope

This closes G-09 by freezing the scoring rubric and applying it to the current
evidence. It does not make the G-10 keep/revise/remove decision.

The live Graphiti adapter is not treated as proven. Graphiti is not installed,
the `GraphitiNeo4jBackend` remains gated, and G-06 live backend verification is
still pending operator hardware. Any Graphiti score must come from a future
adapter proof that writes and reads the canonical projection and matches the
golden evidence.

## Evidence Set

| Item | Value |
| --- | --- |
| Fixture set | `tests/fixtures/experiment_memory/records/` |
| Records | 23 canonical records |
| Contract under test | `proofread.lore_safe.v1` |
| Historical runs | `run-2026-03-13-002`, `run-2026-03-13-003`, `run-2026-03-13-005`, `run-2026-03-13-016` |
| Fixture-modeled event | `run-fixture-oom-001` / `failure-fixture-oom-001`, excluded from default trend analytics |
| Frozen fingerprint | `857c29e55d8c3988bf5c4da46c683ca98e30ac29c29e0730af2be14a270b5ae1` |
| Backend proven | Deterministic projector/export with in-memory replay store |
| Backend not proven | Real Graphiti + Neo4j adapter |

## Mandatory Gates

| Gate | Current Result | Evidence |
| --- | --- | --- |
| Exact source traceability | Pass | Every projected node/edge carries source record id, type, schema version, content hash, store, and recorded timestamp. |
| Deterministic provenance-equal rebuild | Pass | `nlo-graph rebuild --prove` produced matching fingerprints. |
| Fail-open isolation from NLO execution | Pass | Graph package is optional; NLO run path does not import or require Graphiti. |
| Fail-closed advisory integrity | Pass | Query tests refuse missing, stale, invalid, quarantine-bearing, and source-incomplete projections. |
| No canonical-only facts in projection | Pass | Graph objects are derived from committed records only. |
| No prohibited data transmission | Pass | Ingestion filter rejects secrets and bulk content; no external enrichment is enabled. |
| No automatic promotion path | Pass | Query evidence is `authoritative: false`; decisions remain operator records. |
| Bounded decommission path | Pass | Decommission scope remains one bounded package/docs/runtime removal. |
| Real Graphiti live proof | Not run | G-06 live backend and Graphiti adapter proof remain pending. This blocks any G-10 keep decision for Graphiti itself. |

## Frozen Scoring Rubric

Scores are 0-5. Weighted points are `score / 5 * weight`.

| Criterion | Weight |
| --- | ---: |
| Source traceability and auditability | 30 |
| Temporal/cross-run answer quality | 25 |
| Deterministic rebuild and idempotency | 15 |
| Operator usefulness | 10 |
| Interactive latency | 10 |
| Setup and maintenance cost | 10 |

| Alternative | Traceability 30 | Answer Quality 25 | Determinism 15 | Usefulness 10 | Latency 10 | Cost 10 | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| SQL/SQLite joins over canonical records | 30 | 20 | 15 | 8 | 10 | 10 | 93 |
| Current deterministic projection/query layer | 30 | 20 | 15 | 8 | 10 | 9 | 92 |
| Full-text search over records/docs | 18 | 10 | 15 | 6 | 10 | 10 | 69 |
| Vector search over records/docs | 12 | 10 | 6 | 6 | 6 | 4 | 44 |
| Real Graphiti + Neo4j adapter | Not scored | Not scored | Not scored | Not scored | Not scored | Not scored | Gated |

## Test Question Results

| Question | Best Current Answer Path | Result |
| --- | --- | --- |
| Why is the current run the baseline? | Current deterministic query or SQL joins | `run-2026-03-13-005` is current because `decision-2026-03-13-lore-safe-baseline-001` accepted it at `2026-03-13T19:00:00Z`; accepted evaluation evidence supports it and no supersession exists. |
| What changed from the prior baseline? | Current deterministic query or SQL joins | No prior baseline is present in the current historical fixtures; the comparable rejected candidate `run-2026-03-13-016` differs by model only (`gemma3:4b` vs `qwen2.5:14b`). |
| Which failure classes recur? | Current deterministic query or SQL joins | Historical default: `SCHEMA_INVALID` recurs across runs 002 and 003. Fixture-modeled `OUT_OF_MEMORY` is excluded unless `--include-fixtures` is set. |
| Which model/prompt combinations regress? | Current deterministic query or SQL joins | `gemma3:4b` with `lore-safe-proofread-003` regressed in run 016 with `FALSE_NEGATIVE` and `STYLE_REGRESSION`; qwen2.5:14b run 005 is the accepted baseline for the same prompt/input. |
| What evidence supports or opposes promotion? | Current deterministic query or SQL joins | Candidate explanation preserves support (`eval-run-2026-03-13-016-review-01`, rejection decision) and contradictions (`failure-run-2026-03-13-016-false-negative-01`, `failure-run-2026-03-13-016-style-regression-01`). |

## Evaluation

SQL/SQLite joins and the current deterministic projection both answer all five
pilot questions with exact source traceability, deterministic rebuild behavior,
low latency, and low maintenance cost. SQL/SQLite has the simpler operational
story if the pilot grows beyond committed JSON fixtures, but the current
projection already proves the evidence contract without adding a database.

Full-text search is useful for finding prose but does not reliably preserve
typed relationships, baseline state, or contradiction sets. Vector search is
weaker for this governance surface because approximate retrieval makes exact
traceability and deterministic replay harder, and it adds embedding/storage
maintenance before the pilot has shown a need for semantic retrieval.

Real Graphiti may still have value for richer temporal exploration, but that
value is unproven here. The current G-09 result gives Graphiti no keep credit
until a live adapter proves:

- clean write/read of the canonical projection;
- output equality with the five golden evidence queries;
- deterministic rebuild or a deterministic export/fingerprint bridge;
- materially better operator answers than SQL/SQLite on at least three test questions;
- acceptable setup, latency, and maintenance cost on the operator machine.

## G-09 Exit

G-09 is complete: the scoring rubric is frozen and applied to the available
evidence.

The input to G-10 is not "keep Graphiti." The defensible G-10 posture from the
current evidence is:

- keep the normalized canonical records, failure taxonomy, provenance checks,
  deterministic projector, and evidence-query contract;
- do not keep a Graphiti dependency unless a future live adapter proof clears
  the missing gate above and materially outperforms SQL/SQLite.

## Addendum — Live Adapter Proof Result (2026-06-10)

The adapter proof this evaluation required before scoring real Graphiti has
passed, in the implementation environment (Neo4j Community 5.26.0 tarball)
and confirmed by the operator against the Docker-composed pinned backend:

- 26 nodes / 34 edges written via the graphiti-core 0.29.2 driver and read
  back via graphiti's own models;
- file = backend = report fingerprint (`857c29e55d8c3988…`), provenance
  equal byte-for-byte;
- all five golden evidence queries MATCH when answered from the backend
  read-back; idempotent double-write confirmed
  (`tests/experiment_memory/test_live_backend.py`, `NLO_GRAPH_LIVE_TEST=1`).

Fit finding to weigh in scoring: graphiti-core 0.29.2's native
`EntityNode.save`/`EntityEdge.save` unconditionally invoke Neo4j vector
procedures and fail without embeddings, which the pilot's data policy
forbids; the adapter therefore writes graphiti-schema-shaped Cypher through
the graphiti driver while reads use graphiti's models. Graphiti's bi-temporal
edge fields (`valid_at`/`invalid_at`) mapped cleanly onto the pilot's
`effective_at`/`superseded_at`.

Scores and the G-10 keep/revise/remove decision remain with the operator.
