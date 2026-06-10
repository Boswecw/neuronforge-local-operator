# Operator Query Contracts

## Principle

Evidence first. Narrative second.

## Result Types

### OperatorQueryEvidence.v1

```yaml
query_id:
query_type:
subject_id:
graph_status:
source_high_watermark:
projected_high_watermark:
projection_lag_seconds:
supporting_record_ids:
contradicting_record_ids:
timeline_events:
facts:
authoritative: false
```

### OperatorQueryNarrative.v1

Optional human-readable framing built only from the evidence object.

It may not:

- add source IDs;
- remove contradictions;
- raise confidence;
- claim authority;
- change temporal order.

## Initial Commands

```text
nlo graph current-baseline <contract>
nlo graph baseline-history <contract>
nlo graph recurring-failures <contract>
nlo graph compare-runs <run-a> <run-b>
nlo graph explain-candidate <candidate-id>
```

## Output Order

1. projection status;
2. freshness;
3. canonical supporting records;
4. canonical contradicting records;
5. timeline;
6. derived interpretation.

## Query Integrity

Reject the query when:

- graph status is invalid;
- projection lag exceeds policy;
- required source IDs are missing;
- graph fingerprint is not verified;
- rebuild status is incomplete;
- unsupported schema versions exist.

## Golden Query Fixtures

Each query must have an exact expected evidence set.

Example:

```json
{
  "query_type": "current_baseline",
  "subject_id": "analyze.style.scene.v1",
  "supporting_record_ids": ["decision-022", "evaluation-022"],
  "contradicting_record_ids": ["evaluation-021"],
  "authoritative": false
}
```
