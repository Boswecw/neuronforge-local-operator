# Schema and Contract Plan

## Initial Canonical Records

1. `NLORunRecord.v1`
2. `NLOEvaluationRecord.v1`
3. `NLOFailureObservation.v1`
4. `NLOOperatorDecision.v1`
5. `NLOHardwareProfile.v1`

## Projection Input Envelope

`NLOExperimentEvent.v1` is a projection assembly envelope, not an authoritative domain record.

It links immutable records under one bounded experiment event.

Example:

```yaml
schema_version: nlo-experiment-event-v1
experiment_event_id: exp-2026-03-13-005-review-01
run_record_id: run-2026-03-13-005
evaluation_record_id: eval-run-005-review-01
failure_observation_ids: []
decision_record_id: decision-run-005-01
observed_at: 2026-03-13T19:00:00Z
```

## Required Registries

- `ExperimentRecordType.v1`
- `GraphEntityType.v1`
- `GraphRelationshipType.v1`
- `ExperimentStatus.v1`
- `FailureTaxonomy.v1`
- `ProjectionStatus.v1`
- `GraphHealthStatus.v1`

## Referential Integrity

- every evaluation references an existing run;
- every failure observation references a run or evaluation;
- every decision references an existing candidate or baseline;
- every taxonomy code exists in the declared taxonomy version;
- every source hash matches canonical content;
- every prompt/model/task-contract reference resolves;
- unsupported schema versions are quarantined.

## Failure Taxonomy v1

Initial categories:

```text
LORE_HALLUCINATION
PROTECTED_TERM_MUTATION
MEANING_DRIFT
OMISSION
OVER_EDITING
SCHEMA_INVALID
MISSING_EVIDENCE
WEAK_EVIDENCE
FALSE_POSITIVE
FALSE_NEGATIVE
STYLE_REGRESSION
CONTINUITY_MISS
CONTEXT_OVERFLOW
OUT_OF_MEMORY
MODEL_UNAVAILABLE
RUNTIME_TIMEOUT
NONDETERMINISTIC_OUTPUT
PROMPT_ASSEMBLY_FAILURE
```

Every failure observation includes:

- taxonomy version;
- failure class;
- severity;
- confidence;
- source reference;
- output reference;
- reviewer note;
- reproducibility status.

## Validation Rules

Schemas use strict JSON Schema and mirrored typed models where useful.

Tests include:

- valid examples;
- invalid examples;
- unknown fields;
- missing required fields;
- invalid enum values;
- taxonomy mismatch;
- bad references;
- bad hashes;
- round-trip serialization;
- temporal inconsistency.
