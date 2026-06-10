# Implementation Slices

## G-01 — Governance and Authority

Deliver:

- pilot architecture;
- authority matrix;
- anti-patterns;
- decommission conditions;
- one-backend decision.

Exit:

- all authority questions resolved;
- no Graphiti dependency installed.

## G-02 — Identity and Temporal Semantics

Deliver:

- node ID contract;
- edge ID contract;
- normalization rules;
- graph fingerprint contract;
- timestamp doctrine;
- baseline supersession example.

Exit:

- deterministic IDs testable without Graphiti.

## G-03 — Core Schemas and Validation

Deliver:

- run;
- evaluation;
- failure observation;
- operator decision;
- experiment event;
- enums and registries.

Exit:

- valid/invalid examples pass;
- referential integrity enforced;
- no graph dependency.

## G-04 — Historical Fixtures and Hardware Provenance

Deliver:

- one accepted baseline path;
- one rejected candidate path;
- one failure path;
- one OOM/hardware path;
- hardware capture script;
- graceful unsupported-metric behavior.

Exit:

- fixtures fully validate.

## G-05 — Deterministic Mapping Specification

Deliver field-to-graph mapping table.

Example:

| Source Field | Graph Object | Relationship |
|---|---|---|
| `run.model_id` | ModelVersion | Run USED_MODEL ModelVersion |
| `run.prompt_id` | PromptVersion | Run USED_PROMPT PromptVersion |
| `run.task_contract` | TaskContractVersion | Run EXECUTED_UNDER TaskContractVersion |
| `evaluation.run_id` | Evaluation | Evaluation EVALUATES Run |
| `failure.evaluation_id` | FailureObservation | Evaluation FOUND_FAILURE FailureObservation |
| `decision.target_id` | OperatorDecision | OperatorDecision APPROVES/REJECTS Target |

Exit:

- mapping review approved;
- LLM extraction not used for core facts.

## G-06 — Local Backend Pilot

Deliver:

- pinned local backend;
- compose;
- health checks;
- reset tooling;
- runtime package skeleton.

Exit:

- backend starts/stops cleanly;
- loopback only;
- resource limits verified.

## G-07 — Deterministic Projector and Rebuild

Deliver:

- fixture store;
- DataForge Local adapter interface;
- deterministic projector;
- projection report;
- clean rebuild command;
- provenance-equality fingerprint.

Exit:

- two rebuilds match exactly.

## G-08 — Operator Evidence Queries

Deliver:

- current baseline;
- baseline history;
- recurring failures;
- compare runs;
- explain candidate.

Exit:

- all golden evidence tests pass.

## G-09 — Comparative Evaluation

Compare:

- SQL/SQLite joins;
- full-text search;
- vector search;
- Graphiti.

Exit:

- frozen scoring rubric completed.

## G-10 — Decision

Choose:

- keep;
- revise;
- remove.

No silent continuation.
