# G-10 Decision Record

Status: unsigned template
Decision date: TBD
Evaluator / operator: TBD

## Decision

Select exactly one outcome before this record is final:

- [ ] Keep
- [ ] Revise
- [ ] Remove

Operator signature / initials: TBD

## Evidence Base

| Item | Value |
| --- | --- |
| Fixture set | `tests/fixtures/experiment_memory/records/` |
| Records | 23 canonical records |
| Contract under test | `proofread.lore_safe.v1` |
| Historical runs | `run-2026-03-13-002`, `run-2026-03-13-003`, `run-2026-03-13-005`, `run-2026-03-13-016` |
| Fixture-modeled event | `run-fixture-oom-001` / `failure-fixture-oom-001`, excluded from default trend analytics |
| Frozen fingerprint | `857c29e55d8c3988bf5c4da46c683ca98e30ac29c29e0730af2be14a270b5ae1` |
| Backend/version | Neo4j Community `5.26.0`; optional `graphiti-core==0.29.2`; `neo4j==6.2.0` |
| Live proof | Operator-confirmed PASS on 2026-06-10 via `nlo-graph verify-live` |

## Mandatory Gate Results

| Gate | Result | Evidence |
| --- | --- | --- |
| Exact source traceability | Pass | Every projected node/edge carries source record id, type, schema version, content hash, store, and recorded timestamp. |
| Deterministic provenance-equal rebuild | Pass | `nlo-graph rebuild --prove`; file projection, report, and live backend fingerprint matched. |
| Fail-open isolation from NLO execution | Pass | Graph package is optional; NLO run path does not import or require Graphiti. |
| Fail-closed promotion-advisory integrity | Pass | Query tests refuse missing, stale, invalid, quarantine-bearing, and source-incomplete projections. |
| No canonical-only facts in Graphiti | Pass | Live adapter writes only deterministic canonical export data. |
| No prohibited data transmission | Pass | No LLM extraction or embeddings; writes route around Graphiti native vector procedure assumptions. |
| No automatic promotion path | Pass | Query evidence is `authoritative: false`; decisions remain operator records. |
| Bounded decommission path | Pass | `13-DECOMMISSION-PLAN.md` keeps removal scoped to graph runtime/deps/docs while retaining schemas, fixtures, taxonomy, and evidence contracts. |

## Scoring Table

Scores are 0-5. Weighted points are `score / 5 * weight`.

| Alternative | Traceability 30 | Answer Quality 25 | Determinism 15 | Usefulness 10 | Latency 10 | Cost 10 | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| SQL/SQLite joins over canonical records | 30 | 20 | 15 | 8 | 10 | 10 | 93 |
| Current deterministic projection/query layer | 30 | 20 | 15 | 8 | 10 | 9 | 92 |
| Full-text search over records/docs | 18 | 10 | 15 | 6 | 10 | 10 | 69 |
| Vector search over records/docs | 12 | 10 | 6 | 6 | 6 | 4 | 44 |
| Real Graphiti + Neo4j adapter | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

## Keep Criteria Check

Graphiti must satisfy every item before a Keep decision is valid:

- [ ] Materially outperforms simpler alternatives on at least three test questions.
- [x] Preserves exact source traceability.
- [x] Rebuilds deterministically / reads back provenance-equal.
- [x] Remains operationally optional.
- [ ] Stays within agreed maintenance cost.
- [ ] Reduces operator cognitive load.

## Facts To Weigh

Positive findings:

- Live adapter proof passed against real Neo4j 5.26.0 on operator hardware.
- 26 nodes and 34 edges were written and read back provenance-equal.
- All five golden evidence queries matched from backend read-back.
- Bi-temporal mapping fit cleanly: `effective_at` maps to `valid_at`; `superseded_at` maps to `invalid_at`.
- Graphiti adds durable graph storage and traversal surface while staying optional.

Limitations:

- The five operator questions are currently answered identically by the file projection alone.
- Graphiti has not yet shown material advantage over SQL/SQLite or the deterministic query layer on three questions.
- `graphiti-core` native `EntityNode.save` / `EntityEdge.save` assumes Neo4j vector procedures and embeddings; the adapter must route around that to honor the no-embedding policy.
- The optional dependency set is heavier than the deterministic file projection.
- G-10 must account for ongoing maintenance cost, not just proof viability.

## Outcome-Specific Next Step

If Keep:

- Promote the pilot to a standing optional operator surface.
- Keep `requirements-graphiti.txt`, the live adapter, graph scripts, and live proof tests.
- Define the minimum recurring live-proof cadence and expected operator workflow.

If Revise:

- Scope the next bounded iteration here before any further graph expansion.
- State the specific questions Graphiti must outperform on.
- Define measurable operator-cognitive-load and maintenance-cost gates.

If Remove:

- Execute `13-DECOMMISSION-PLAN.md`.
- Retain normalized experiment schemas, fixtures, failure taxonomy, hardware provenance, source-of-truth matrix, and operator evidence contracts.
- Verify NLO tests pass without Graphiti dependencies or runtime artifacts.

## Final Rationale

TBD. The final rationale must explain why the selected outcome follows from
the scoring table, the mandatory gates, and the keep criteria.
