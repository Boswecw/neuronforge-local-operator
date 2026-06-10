# Deterministic Mapping Specification (G-05)

Graph schema version: `nlo-graph-schema-v1`.

This specification is the complete, reviewable mapping from canonical experiment
records to graph nodes and edges. The projector (`src/nlo_experiment_memory/projection/`)
implements exactly this table and nothing else. No LLM extraction is used for core facts.

## Node Identity

`node_id = SHA256(graph_schema_version + ":" + entity_type + ":" + canonical_business_key)`
(per plan 03; keys are NFC-normalized UTF-8).

| Entity type | Business key | Source |
| --- | --- | --- |
| `Run` | `run_id` | `NLORunRecord.v1` |
| `ModelVersion` | `model_id` (+ `@<model_digest>` when present) | `NLORunRecord.v1` |
| `PromptVersion` | `prompt_id@sha256-<prompt_content_hash>` | `NLORunRecord.v1` |
| `InputVersion` | `input_id@sha256-<input_content_hash>` | `NLORunRecord.v1` |
| `TaskContractVersion` | `task_contract` | `NLORunRecord.v1` |
| `Evaluation` | `evaluation_id` | `NLOEvaluationRecord.v1` |
| `FailureObservation` | `failure_id` | `NLOFailureObservation.v1` |
| `OperatorDecision` | `decision_id` | `NLOOperatorDecision.v1` |
| `HardwareProfile` | `hardware_profile_id` | `NLOHardwareProfile.v1` |

## Edge Identity

`edge_id = SHA256(graph_schema_version + ":" + relationship_type + ":" + source_node_id
+ ":" + target_node_id + ":" + source_record_id + ":" + effective_at)` (per plan 03).
Every edge carries an `effective_at` drawn from its source record as listed below.

## Field-to-Graph Mapping Table

| Source field(s) | Edge | `effective_at` | Source record |
| --- | --- | --- | --- |
| `run.model_id` (+digest) | `Run USED_MODEL ModelVersion` | `run.occurred_at` | run record |
| `run.prompt_id` + `run.prompt_content_hash` | `Run USED_PROMPT PromptVersion` | `run.occurred_at` | run record |
| `run.input_id` + `run.input_content_hash` | `Run USED_INPUT InputVersion` | `run.occurred_at` | run record |
| `run.task_contract` | `Run EXECUTED_UNDER TaskContractVersion` | `run.occurred_at` | run record |
| `run.hardware_profile_id` (optional) | `Run EXECUTED_ON HardwareProfile` | `run.occurred_at` | run record |
| `evaluation.run_id` | `Evaluation EVALUATES Run` | `evaluation.reviewed_at` | evaluation record |
| `failure.evaluation_id` (when present) | `Evaluation FOUND_FAILURE FailureObservation` | `failure.observed_at` | failure observation |
| `failure.run_id` (when no `evaluation_id`) | `Run FOUND_FAILURE FailureObservation` | `failure.observed_at` | failure observation |
| `decision.target_run_id`, `decision_type=accept_baseline` | `OperatorDecision APPROVES Run` | `decision.effective_at` | decision record |
| `decision.target_run_id`, `decision_type=reject_candidate` | `OperatorDecision REJECTS Run` | `decision.effective_at` | decision record |
| `decision.task_contract`, `decision_type=accept_baseline` | `Run BECAME_BASELINE_FOR TaskContractVersion` (carries `superseded_at`) | `decision.effective_at` | decision record |
| `decision.supersedes_run_id` (optional) | `Run SUPERSEDED Run` (new baseline → prior baseline) | `decision.effective_at` | decision record |

`NLOExperimentEvent.v1` envelopes are projection inputs only; they group records for
one bounded experiment event and produce no nodes or edges of their own.

## Projected Node Properties (least-data, per plan 05)

| Entity | Semantic properties projected |
| --- | --- |
| `Run` | `run_id`, `task_contract`, `model_id`, `prompt_id`, `input_id`, `status`, `occurred_at` |
| `ModelVersion` | `model_id`, `model_digest` (when present) |
| `PromptVersion` | `prompt_id`, `prompt_content_hash`, `prompt_path` |
| `InputVersion` | `input_id`, `input_content_hash`, `input_path` |
| `TaskContractVersion` | `task_contract` |
| `Evaluation` | `evaluation_id`, `run_id`, `outcome`, `reviewed_at` |
| `FailureObservation` | `failure_id`, `taxonomy_version`, `failure_class`, `severity`, `confidence`, `reproducibility`, `observed_at` |
| `OperatorDecision` | `decision_id`, `decision_type`, `task_contract`, `target_run_id`, `effective_at`, `superseded_at` |
| `HardwareProfile` | `hardware_profile_id`, `captured_at`, `cpu_cores`, `mem_total_gb` (when present) |

Reviewer notes, rationale text, findings text, and output content are **not** projected
(Restricted/Minimized classes in plan 05). Operators open the canonical record by id.

## Provenance (attached to every node and edge)

`source_record_id`, `source_record_type`, `source_schema_version`,
`source_content_hash` (SHA256 of the record's canonical JSON), `source_store`,
`recorded_at` — per plan 02. Provenance participates in the graph fingerprint
(provenance equality).

## Exclusions From the Fingerprint

Backend-generated ids, insertion order, `projected_at`, `ingested_at`, runtime metrics,
and connection metadata are never part of node/edge identity or the fingerprint (plan 03).
