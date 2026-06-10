# Experiment-Memory (Graphiti) Pilot

## Status
Implemented through slice G-09 against an in-memory store; the pinned backend is verified live on operator hardware (2026-06-10: healthy, loopback-only); Graphiti itself not installed (gated). Governing plan set: `docs/plans/graphiti/`.

## Purpose
Give the operator a **rebuildable, non-authoritative experiment-memory projection** over canonical experiment records: what was tested, what changed, why a baseline was promoted, what evidence supports or contradicts a promotion, and whether a failure pattern recurs.

## Governing Rule

> The projection may explain and suggest. It may not approve, promote, mutate, or assert canonical truth.

NLO execution fails open with respect to the graph (runs never need it). Promotion-advisory queries fail closed: they refuse when the projection is missing, unverified, quarantine-bearing, or older than the canonical records (lag policy 0 by default via `NLO_GRAPH_MAX_PROJECTION_LAG_SECONDS`).

---

## 1. Authority

Per the authority matrix (`docs/plans/graphiti/02-EXPERIMENT-RECORD-AUTHORITY-MATRIX.md`): Git is the authority for every artifact type present in this repo today; DataForge Local does not exist here yet, so its adapter is a declared interface only (`src/nlo_experiment_memory/stores/dataforge_local.py`). Graph nodes/edges are derived only and are never the only copy of any fact.

## 2. Surfaces

| Surface | Location |
| --- | --- |
| Canonical record schemas (strict, v1) | `schemas/experiment_memory/*.schema.json` |
| Registries (record types, taxonomy, statuses, graph types) | `schemas/experiment_memory/registries/` |
| Package (contracts, identity, stores, projection, queries, cli, enrichment) | `src/nlo_experiment_memory/` |
| Canonical record fixtures (converted real history) | `tests/fixtures/experiment_memory/records/` |
| Golden query evidence + frozen fingerprint | `tests/fixtures/experiment_memory/golden/` |
| Comparative evaluation | `docs/plans/graphiti/G-09-COMPARATIVE-EVALUATION.md` |
| Test suite (59 tests) | `tests/experiment_memory/` (wired into `scripts/run-tests.sh`) |
| Operator CLI | `scripts/graph/nlo-graph` (`validate`, `rebuild [--prove]`, `status`, five plan-08 queries) |
| Hardware provenance capture | `scripts/graph/capture-hardware-profile.sh` |
| Pinned backend (opt-in) | `docker-compose.graphiti-pilot.yml` (`neo4j:5.26.0-community`, loopback only) + `scripts/graph/graph-{up,down,reset,doctor}.sh` + `.env.graphiti.example` |
| Deterministic mapping spec | `docs/plans/graphiti/MAPPING-SPEC.md` |
| Plan-set review and locked decisions | `docs/plans/graphiti/REVIEW.md` |

## 3. Canonical Records (v1)

`NLORunRecord`, `NLOEvaluationRecord`, `NLOFailureObservation` (18-class `failure-taxonomy-v1`, including `OUT_OF_MEMORY` for the documented Ollama memory boundary), `NLOOperatorDecision`, `NLOHardwareProfile`, plus the non-authoritative `NLOExperimentEvent` envelope. Validation is strict JSON Schema plus cross-record integrity: referential resolution, taxonomy membership, artifact-hash verification against committed files, and temporal-order rules with quarantine cascade.

Records may declare `record_origin` as `historical`, `fixture_modeled`, or `synthetic_test`. Default operator trend analytics include historical records only; fixture-modeled events are opt-in (`recurring-failures --include-fixtures`) so synthetic evidence does not distort operational recurrence claims. Run artifact references are treated as committed by default and missing committed files fail integrity unless the run explicitly declares `artifact_location_class: external`.

## 4. Identity and Rebuild Doctrine

Node/edge ids are SHA256 over `nlo-graph-schema-v1` plus canonical business keys (NFC, sorted keys, sorted set-like arrays, UTC-Z timestamps). A clean rebuild from canonical records must be **provenance-equal**: two rebuilds produce identical fingerprints (`scripts/graph/nlo-graph rebuild --prove`; also enforced in tests, with the expected fingerprint frozen at `tests/fixtures/experiment_memory/golden/fingerprint.txt`).

## 5. Operator Queries

Evidence first, narrative second. `nlo-graph current-baseline|baseline-history|recurring-failures <contract>`, `compare-runs <a> <b>`, `explain-candidate <id>` emit `OperatorQueryEvidence.v1` (always `authoritative: false`), printing projection status, freshness, supporting records, contradicting records, timeline, then a derived narrative that cannot add ids, hide contradictions, or claim authority.

## 6. Gates

Graphiti is **not installed**. The plan README forbids installation before G-01..G-05 pass; the projector and queries are proven against an in-memory store, and `GraphitiNeo4jBackend` refuses instantiation until the operator wires it after gate acceptance. G-09 is complete as a frozen comparative evaluation; it does not credit real Graphiti until a live adapter proof matches golden evidence and materially outperforms SQL/SQLite. G-10 (keep/revise/remove) remains pending. Decommission stays one bounded change set per `docs/plans/graphiti/13-DECOMMISSION-PLAN.md`.
