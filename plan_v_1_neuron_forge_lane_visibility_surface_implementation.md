# Plan v1 — NeuronForge Lane Visibility Surface Implementation

## Purpose

Provide an implementation-ready plan for VS Code Opus to build the first working NeuronForge lane visibility surface for ForgeCommand.

This plan is intentionally specific.

It defines:

- what must be built
- where files must live
- what each component must do
- what must be validated
- what must not be assumed
- how success will be tested

This is not a conceptual architecture note.

This is a build plan.

---

## Objective

Implement a machine-readable lane visibility surface in NeuronForge so ForgeCommand can read governed lane state without scraping prose docs or inferring state from repo structure.

The first implementation will use **repo-local JSON lane records** stored in:

```text
analytics/lanes/*.json
```

These records will be the published lane-state surface.

NeuronForge remains the owner of:

- eval documents
- calibration docs
- status docs
- prompts
- runs
- supporting prose

ForgeCommand will consume only the stable visibility surface.

---

## Scope of v1

Build the minimum complete path for one real lane and the supporting validation infrastructure.

### In scope

1. JSON schema file for lane analytics records
2. one live lane record for the continuity lane
3. CI/local validation script for lane records
4. consistency checks between `lane_id` and filename stem
5. consistency checks for required fields
6. consistency checks for enum values
7. consistency checks for date format
8. documentation for update workflow
9. documentation for ForgeCommand ingest expectations

### Out of scope for v1

- runtime service API
- websocket/event transport
- automatic extraction from prose docs
- multi-repo synchronization
- cross-repo telemetry aggregation
- auto-generation of lane records from eval markdown

The lane record may be manually maintained in v1, but it must be validated automatically.

---

## Required deliverables

VS Code Opus must create or update the following files.

### 1. JSON schema

Create:

```text
schemas/lane-analytics.schema.json
```

Purpose:

- machine validation of lane record shape
- IDE support through `$schema`
- stable validation anchor for CI and local checks

### 2. Lane analytics directory

Create if missing:

```text
analytics/lanes/
```

### 3. First live lane record

Create:

```text
analytics/lanes/continuity-progression-reasoning.json
```

This must be a valid record conforming to the schema and visibility contract.

### 4. Validation script

Create:

```text
scripts/validate-lane-records.(js|ts|py)
```

Use the project’s most appropriate scripting language.

Purpose:

- scan all `analytics/lanes/*.json`
- validate JSON parseability
- validate against schema
- validate filename/lane-id match
- validate required visibility fields
- emit non-zero exit on failure

### 5. Validation documentation

Create or update:

```text
docs/lane-record-validation.md
```

Purpose:

- explain how validation works
- explain failure states
- explain required update coupling in PRs

### 6. Optional convenience command

If the repo has an existing scripts/task runner pattern, add a command entry such as:

```text
npm run validate:lanes
```

or repo-equivalent.

Do not invent a new toolchain if one already exists.

---

## Required source documents to honor

Implementation must align with these existing design documents already created on canvas and intended as source direction:

1. **Lane Analytics Schema**
2. **ForgeCommand Lane Visibility Contract**

If local repo docs already exist with overlapping intent, implementation should reconcile to these principles rather than creating a conflicting parallel contract.

---

## Canonical v1 record shape

The schema and record must support at minimum these required top-level fields:

- `$schema`
- `schema_version`
- `lane_id`
- `lane_name`
- `lane_type`
- `status`
- `required_route_class`
- `adoption_posture`
- `current_baseline_model`
- `current_baseline_prompt_profile`
- `anchor_input`
- `anchor_run_id`
- `last_evaluated_date`
- `current_judgment`
- `calibration_doc`
- `status_doc`
- `metrics`
- `next_required_decision`

### Nullability rule

The following fields may be `null` where appropriate, but the keys must still exist:

- `current_baseline_model`
- `current_baseline_prompt_profile`
- `anchor_input`
- `anchor_run_id`
- `calibration_doc`
- `status_doc`

Missing key is a validation failure.

---

## Required enum rules

### Closed enums in v1

The validator must treat these as strict enums.

#### `status`
Allowed values:

- `planned`
- `implementing`
- `evaluating`
- `candidate_baseline`
- `approved_baseline`
- `deferred`
- `blocked`
- `retired`

#### `adoption_posture`
Allowed values:

- `blocked`
- `experimental_only`
- `review_assist_only`
- `operator_assist`
- `trusted_with_review`
- `trusted_default`

### Open extensible fields in v1

These must be required as strings but must not be treated as closed enums in v1:

- `lane_type`
- `required_route_class`

Do not over-constrain them yet.

---

## Metrics storage rule

Metrics must be stored as numeric values, not percent strings.

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

UI formatting is not part of the lane record.

---

## Required validation behavior

The validation script must perform all of the following.

### 1. File discovery

Scan:

```text
analytics/lanes/*.json
```

### 2. JSON parse validation

For each file:

- confirm valid JSON
- report parse errors clearly

### 3. Schema validation

Validate each record against `schemas/lane-analytics.schema.json`.

### 4. Filename-to-id validation

For each file:

- derive filename stem
- confirm `lane_id === filename_stem`

Example:

- file: `analytics/lanes/continuity-progression-reasoning.json`
- `lane_id` must equal `continuity-progression-reasoning`

### 5. Date validation

Validate `last_evaluated_date` as a valid `YYYY-MM-DD` date string with no time component.

### 6. Required field validation

Confirm all required top-level fields exist.

### 7. Nullability validation

Fields allowed to be null must still exist as keys.

### 8. Optional path existence check

If practical and low-risk, validate that referenced repo-local docs exist for:

- `anchor_input`
- `calibration_doc`
- `status_doc`

This may be a warning in v1 rather than a hard error if repo refactoring is still in progress.

### 9. Exit behavior

- zero exit code if all records pass
- non-zero exit code if any hard validation fails

---

## Required failure states

The validator must emit explicit machine-readable or clearly structured failure categories.

Minimum failure states:

- `malformed_json`
- `schema_validation_failed`
- `missing_required_field`
- `invalid_enum`
- `id_mismatch`
- `invalid_date`
- `unsupported_schema_version`

Recommended warning states:

- `missing_referenced_path`
- `stale_record`

`stale_record` should be warning-only in v1 unless the repo already has a policy threshold.

---

## First live record requirements

The file:

```text
analytics/lanes/continuity-progression-reasoning.json
```

must be created as the first anchor implementation.

### Required constraints

- valid JSON
- valid against schema
- matches filename stem
- uses numeric metrics
- uses `$schema`
- uses `schema_version: "1.0"`
- contains concise dashboard-ready `current_judgment`
- contains concise dashboard-ready `next_required_decision`

### Seed values to use

Use this exact starting shape unless the repo already contains authoritative values that should replace placeholders:

```json
{
  "$schema": "../../schemas/lane-analytics.schema.json",
  "schema_version": "1.0",
  "lane_id": "continuity-progression-reasoning",
  "lane_name": "Continuity / Progression Reasoning",
  "lane_type": "continuity_reasoning",
  "status": "candidate_baseline",
  "required_route_class": "HIGH_QUALITY_LOCAL",
  "adoption_posture": "review_assist_only",
  "current_baseline_model": "qwen2.5:14b",
  "current_baseline_prompt_profile": "continuity-adjacent-scene-v3",
  "anchor_input": "inputs/continuity-test-001.md",
  "anchor_run_id": "run-2026-03-14-007",
  "last_evaluated_date": "2026-03-14",
  "current_judgment": "Qwen 2.5 14B with continuity-adjacent-scene-v3 is the current candidate baseline for adjacent-scene continuity review.",
  "calibration_doc": "evals/continuity-progression-calibration-2026-03-14.md",
  "status_doc": "evals/continuity-progression-status-2026-03-14.md",
  "metrics": {
    "schema_reliability": 1.0,
    "false_positive_rate": 0.0,
    "surface_detection_rate": 0.8
  },
  "next_required_decision": "Approve or defer qwen2.5:14b with continuity-adjacent-scene-v3 as adjacent-scene continuity baseline."
}
```

If any referenced document path does not exist in repo, Opus must either:

- replace it with the correct existing path if it can verify it, or
- set the field to `null` and document why in the implementation notes

It must not invent fake paths.

---

## JSON schema requirements

The schema file must:

- be valid JSON Schema
- require all mandatory top-level fields
- enforce object shape for `metrics`
- allow null for designated nullable fields
- enforce strict enums for `status` and `adoption_posture`
- require strings for `lane_type` and `required_route_class`
- require `schema_version`
- require `$schema` field in records even if the validator itself does not use it semantically

Recommended schema posture:

- keep top-level shape strict enough to prevent drift
- avoid prematurely freezing optional extension fields

Use `additionalProperties` thoughtfully.

Recommended approach:

- allow additional properties at top level in v1
- require the stable visibility surface plus required schema fields

This preserves forward extensibility while protecting the contract.

---

## Documentation requirements

### `docs/lane-record-validation.md`

This file must explain:

1. where lane records live
2. why they exist
3. what validator checks
4. hard failure vs warning states
5. PR update coupling rule
6. how ForgeCommand is expected to consume them

### Must include this rule clearly

Any PR or commit set that changes lane trust posture must update the lane record in the same change set.

Examples:

- baseline promotion
- baseline rollback
- baseline model swap
- prompt profile adoption
- adoption posture change
- route-class requirement change

---

## Implementation order

VS Code Opus should implement in this order.

### Step 1
Create `schemas/lane-analytics.schema.json`.

### Step 2
Create `analytics/lanes/continuity-progression-reasoning.json`.

### Step 3
Create `scripts/validate-lane-records.(js|ts|py)`.

### Step 4
Run the validator against the continuity record and fix all failures.

### Step 5
Create `docs/lane-record-validation.md`.

### Step 6
Wire a project command for validation if appropriate.

### Step 7
Provide a short implementation note summarizing:

- files created
- validation result
- assumptions made
- warnings remaining

---

## Acceptance criteria

Implementation is successful only if all of the following are true.

### A. Schema exists

`schemas/lane-analytics.schema.json` exists and validates the continuity record.

### B. Live record exists

`analytics/lanes/continuity-progression-reasoning.json` exists and passes validation.

### C. Validator works

The validator scans lane records and exits non-zero on hard failure.

### D. ID matching works

The validator fails if filename stem and `lane_id` differ.

### E. Enum enforcement works

The validator fails on invalid `status` or invalid `adoption_posture`.

### F. Date enforcement works

The validator fails if `last_evaluated_date` is not valid `YYYY-MM-DD`.

### G. Nullability rule works

The validator accepts nullable required fields only when the key exists.

### H. Numeric metrics rule works

The validator rejects percent-string metric values if schema typing covers them.

### I. Docs exist

`docs/lane-record-validation.md` exists and explains the workflow.

---

## Explicit non-goals

VS Code Opus must not do the following in this task.

- do not build a runtime HTTP API
- do not build ForgeCommand UI yet
- do not parse markdown evals into records automatically
- do not redesign NeuronForge lane architecture
- do not invent additional contract fields unless needed for schema correctness
- do not switch to percent-string metrics
- do not infer fake referenced paths

---

## Notes for implementation style

- prefer simple, inspectable code
- prefer deterministic validation output
- keep failure messages explicit
- keep schema and record readable by humans
- avoid overengineering the first pass

This task is about producing the first reliable governed visibility surface, not building the whole management plane.

---

## Final implementation instruction to VS Code Opus

Build the v1 lane visibility surface exactly as a repo-local, schema-validated JSON publication layer for NeuronForge.

NeuronForge remains the producer of lane truth summaries.
ForgeCommand will later become the consumer of this stable surface.

Your job in this task is to implement the publication layer, its schema, its first live record, and its validator so the system has a trustworthy foundation to build on.

