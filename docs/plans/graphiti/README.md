# NeuronForge Local Operator — Graphiti Experiment-Memory Pilot Plan Set

## Purpose

This plan set defines a governed pilot for using Graphiti as a **rebuildable, non-authoritative experiment-memory projection** for `neuronforge-local-operator` (NLO).

Graphiti may help operators understand:

- what was tested;
- what changed;
- what improved;
- what regressed;
- why a baseline was promoted;
- what evidence supports or contradicts a promotion;
- whether a failure pattern has appeared before.

Graphiti must never become:

- the source of truth;
- a promotion authority;
- a runtime dependency for NLO execution;
- a model router;
- a baseline selector;
- the only copy of any experiment, evaluation, or decision record.

## Governing Rule

> Graphiti may explain and suggest. Graphiti may not approve, promote, mutate, or assert canonical truth.

## Plan Set

1. `01-PILOT-ARCHITECTURE.md`
2. `02-EXPERIMENT-RECORD-AUTHORITY-MATRIX.md`
3. `03-GRAPH-IDENTITY-AND-FINGERPRINT-CONTRACT.md`
4. `04-TEMPORAL-SEMANTICS.md`
5. `05-DATA-SECURITY-AND-CLASSIFICATION.md`
6. `06-SCHEMA-AND-CONTRACT-PLAN.md`
7. `07-REPOSITORY-STRUCTURE.md`
8. `08-OPERATOR-QUERY-CONTRACTS.md`
9. `09-VERIFICATION-PLAN.md`
10. `10-PLATFORM-AND-DEPLOYMENT-PLAN.md`
11. `11-IMPLEMENTATION-SLICES.md`
12. `12-GO-NO-GO-EVALUATION.md`
13. `13-DECOMMISSION-PLAN.md`
14. `14-RISKS-ANTI-PATTERNS-AND-DECISIONS.md`

Implemented evaluation artifacts:

- `REVIEW.md`
- `G-09-COMPARATIVE-EVALUATION.md`
- `G-10-DECISION-RECORD.md` (unsigned operator template)

## Recommended Execution Order

```text
G-01 Governance and authority
→ G-02 Identity and temporal semantics
→ G-03 Schemas and validation
→ G-04 Historical fixtures and hardware provenance
→ G-05 Deterministic graph mapping specification
→ G-06 One-backend local pilot
→ G-07 Deterministic rebuild
→ G-08 Operator evidence queries
→ G-09 Comparative evaluation
→ G-10 Keep, revise, or remove
```

Do not install Graphiti before G-01 through G-05 pass.

## Current Readiness

The pilot is ready for documentation, schema work, fixture conversion, failure-taxonomy work, hardware provenance, identity design, and temporal-contract design.

It is not ready for Graphiti integration until authority, identity, temporal semantics, data classification, and query evidence contracts are locked.
