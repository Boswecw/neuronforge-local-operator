# Lane Record Validation

Date: 2026-03-14

## Where lane records live

```
analytics/lanes/*.json
```

One file per lane. The filename stem must match the `lane_id` field in the record.

Example:

```
analytics/lanes/continuity-progression-reasoning.json
  → lane_id must equal "continuity-progression-reasoning"
```

## Why lane records exist

Lane records are the machine-readable publication surface for NeuronForge lane state. They exist so ForgeCommand and other consumers can read governed lane status without scraping prose docs or inferring state from repo structure.

NeuronForge remains the owner of eval documents, calibration docs, status docs, prompts, runs, and supporting prose. Lane records are the stable visibility layer extracted from that work.

Lane records are manually maintained in v1. They must be validated automatically.

## Schema

All lane records must conform to:

```
schemas/lane-analytics.schema.json
```

The schema is JSON Schema draft-07. It enforces:

- Required top-level fields (see list below)
- Strict enum values for `status` and `adoption_posture`
- String typing for `lane_type` and `required_route_class` (open, not enumerated in v1)
- Numeric typing for all `metrics` values (not percent strings)
- Nullable typing for designated nullable fields (key must exist; value may be null or string)

## What the validator checks

Run:

```bash
python3 scripts/validate-lane-records.py
```

The validator performs these checks on every `analytics/lanes/*.json` file:

| Check | Type |
|-------|------|
| JSON parseability | Hard failure |
| `schema_version` is a supported value (`"1.0"`) | Hard failure |
| All required fields are present | Hard failure |
| Nullable fields have keys (even if value is null) | Hard failure |
| `status` is a valid enum value | Hard failure |
| `adoption_posture` is a valid enum value | Hard failure |
| `metric_provenance` is a valid enum value | Hard failure |
| `metric_profile` is a valid enum value | Hard failure |
| `operator_judged` provenance with `metrics_gate_eligible: true` | Hard failure |
| `operator_judged` or `mixed` provenance without non-empty `provenance_notes` | Hard failure |
| `lane_id` matches filename stem | Hard failure |
| `last_evaluated_date` is valid YYYY-MM-DD | Hard failure |
| `metrics` fields are numbers, not strings | Hard failure |
| `metrics` values are in range 0.0–1.0 | Hard failure |
| Required string fields are non-empty | Hard failure |
| Referenced paths exist on disk | Warning only |

## Hard failure vs warning states

**Hard failures** cause the validator to exit with code 1. The record does not pass.

| Failure category | Meaning |
|-----------------|---------|
| `malformed_json` | File is not valid JSON or cannot be read |
| `unsupported_schema_version` | `schema_version` is not a known supported value |
| `missing_required_field` | A required top-level field or nullable field key is absent |
| `schema_validation_failed` | A field has wrong type, wrong shape, or empty value |
| `invalid_enum` | `status`, `adoption_posture`, `metric_provenance`, or `metric_profile` is not an allowed value |
| `invalid_provenance` | Provenance governance rule violated (see metric provenance section) |
| `id_mismatch` | `lane_id` does not match the filename stem |
| `invalid_date` | `last_evaluated_date` is not a valid YYYY-MM-DD calendar date |

**Warnings** are reported but do not cause a non-zero exit.

| Warning category | Meaning |
|-----------------|---------|
| `missing_referenced_path` | A path field (`anchor_input`, `calibration_doc`, `status_doc`) references a path that does not exist in the repo |

Path reference warnings are warnings only because docs may legitimately not exist yet (null is the correct value when nothing exists; a non-null path that does not resolve is worth inspecting but may not block).

## Required fields

All lane records must contain these top-level fields:

```
$schema
schema_version
lane_id
lane_name
lane_type
status
required_route_class
adoption_posture
current_baseline_model       (nullable — key must exist)
current_baseline_prompt_profile  (nullable — key must exist)
anchor_input                 (nullable — key must exist)
anchor_run_id                (nullable — key must exist)
last_evaluated_date
current_judgment
calibration_doc              (nullable — key must exist)
status_doc                   (nullable — key must exist)
metrics
next_required_decision
metric_provenance
metrics_gate_eligible
provenance_notes               (nullable — key must exist; non-null required for operator_judged/mixed)
metric_profile
```

Nullable fields may have `null` or a string value. An absent key is a hard failure.

## PR update coupling rule

**Any PR or commit set that changes lane trust posture must update the lane record in the same change set.**

This rule applies when the change involves:

- baseline promotion
- baseline rollback
- baseline model swap
- prompt profile adoption
- adoption posture change
- route-class requirement change
- status change (e.g. `evaluating` → `candidate_baseline`)

The validator must pass on the updated record before the PR is merged.

Do not merge posture changes without a simultaneous lane record update.

## How ForgeCommand is expected to consume lane records

ForgeCommand will read `analytics/lanes/*.json` directly from the repo as a stable publication layer.

It should treat these records as:

- read-only from its perspective
- authoritative for governed lane state
- versioned by `schema_version`

ForgeCommand must not attempt to parse prose docs, infer state from file presence, or assume state that is not in the lane record.

In v1, ForgeCommand consumes the records by reading them from disk (or via the repo). A runtime API or event transport is out of scope for v1.

## Metrics format requirement

Metrics must be stored as numeric values in range [0.0, 1.0]. Never use percent strings.

Correct:

```json
"metrics": {
  "schema_reliability": 1.0,
  "false_positive_rate": 0.0,
  "surface_detection_rate": 0.8
}
```

Incorrect:

```json
"metrics": {
  "schema_reliability": "100%"
}
```

The validator will hard-fail string metric values.

## Metric profile and provenance

Lane records carry two distinct metric governance fields. They are not the same and must not be conflated.

### `metric_profile` — interpretation contract

`metric_profile` tells downstream consumers what kind of lane they are reading and therefore how to interpret the metric trio (`schema_reliability`, `false_positive_rate`, `surface_detection_rate`).

It is **not** a label. It is an interpretation contract.

| Value | Meaning |
| ------- | --------- |
| `detection_reasoning` | Lane detects, surfaces, or reasons about conditions in governed input. Metric trio is canonical for this profile. |
| `editing_cleanup` | Lane performs grammar, readability, or light editorial cleanup. Metric trio is present but semantically translated — not equivalent to detection metrics. |
| `lore_protection_editing` | Editing lane with dominant preservation constraint (protected terms, canon facts, continuity anchors). Metric trio is present but must be interpreted more conservatively than detection metrics. |

**ForgeCommand must not directly compare metric values across different `metric_profile` values without surfacing this semantic difference.**

### `metric_provenance` — evidence class

`metric_provenance` tells consumers how the metric values were produced — the strength of the evidence behind the numbers.

| Value | Meaning |
| ------- | --------- |
| `benchmark_derived` | Metrics computed from a frozen labeled evaluation set (frozen case pack). Values are instrument-grade. |
| `instrument_derived` | Metrics from structured instrumentation or deterministic scoring logic. |
| `automated_heuristic` | Metrics from automated but non-authoritative scoring (rule-based, LLM-as-judge, etc.). |
| `operator_judged` | Metrics approximated from qualitative comparative review. Visibility-supporting, not hard empirical. |
| `mixed` | Materially blended evidence basis; `provenance_notes` must explain the blend. |

### Governance rules enforced by validator

- `operator_judged` + `metrics_gate_eligible: true` → hard failure. Operator-judged metrics cannot participate in automated promotion logic.
- `operator_judged` or `mixed` without non-empty `provenance_notes` → hard failure. The derivation method must be documented.

### Current fleet mapping

| Lane | `metric_profile` | `metric_provenance` | `metrics_gate_eligible` |
| ------ | ----------------- | -------------------- | ----------------------- |
| continuity-progression-reasoning | `detection_reasoning` | `benchmark_derived` | `true` |
| lore-safe-proofreading | `lore_protection_editing` | `operator_judged` | `false` |
| general-grammar-cleanup | `editing_cleanup` | `operator_judged` | `false` |

## Adding a new lane record

1. Create `analytics/lanes/<lane-id>.json`
2. Set `lane_id` to match the filename stem exactly
3. Fill all required fields (set nullable fields to `null` if not yet applicable)
4. Run `python3 scripts/validate-lane-records.py` and confirm all records pass
5. Include the new record in the same PR as the work that establishes the lane
