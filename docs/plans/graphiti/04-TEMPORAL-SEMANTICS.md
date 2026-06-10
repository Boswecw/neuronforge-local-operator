# Temporal Semantics

## Purpose

Prevent ambiguous use of timestamps in a temporal graph.

## Canonical Time Fields

- `occurred_at`: when the underlying experiment event happened.
- `recorded_at`: when the canonical record was persisted.
- `reviewed_at`: when an evaluator reviewed the run.
- `effective_at`: when a decision became operationally valid.
- `superseded_at`: when a prior fact stopped being current.
- `observed_at`: when NLO observed a relationship or result.
- `projected_at`: when the graph projection was produced.
- `ingested_at`: when the backend accepted the projection write.

Only `occurred_at`, `effective_at`, and `superseded_at` participate in business-time validity.

`projected_at` and `ingested_at` are operational metadata only.

## Baseline Example

```text
run-005 became baseline on 2026-03-13
run-022 replaced it on 2026-06-10
```

Represent:

```text
run-005 → BECAME_BASELINE_FOR → analyze.style.scene.v1
effective_at: 2026-03-13T19:00:00Z
superseded_at: 2026-06-10T15:30:00Z
source_record_id: decision-005

run-022 → BECAME_BASELINE_FOR → analyze.style.scene.v1
effective_at: 2026-06-10T15:30:00Z
superseded_at: null
source_record_id: decision-022

run-022 → SUPERSEDED → run-005
occurred_at: 2026-06-10T15:30:00Z
source_record_id: decision-022
```

The prior fact remains historically valid. It is not deleted.

## Ordering Rules

When timestamps collide, order by:

1. canonical sequence number if present;
2. `recorded_at`;
3. canonical `record_id`.

Do not infer order from graph insertion order.

## Clock-Skew Handling

Records with impossible temporal ordering are quarantined.

Examples:

- `reviewed_at < occurred_at`;
- `superseded_at < effective_at`;
- decision references future run;
- baseline supersedes itself.

## Bi-Temporal Extension

Transaction-time history may be added later, but it is not required for the first pilot. If added, it must not overload business-time fields.
