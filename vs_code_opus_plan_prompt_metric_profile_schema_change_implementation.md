# VS Code Opus Plan/Prompt — Metric Profile Schema Change Implementation

## Revision

- Revision: 1
- Status: Implementation Prompt
- Audience: VS Code Opus
- Scope: NeuronForge lane analytics schema + validator + lane record fleet backfill + docs

---

# Part 1 — Implementation Plan

## Objective

Implement the next governed evolution of the NeuronForge lane visibility surface by adding `metric_profile` to the lane analytics schema and backfilling the current lane fleet.

This work must preserve the existing governance posture already established for:

- `metric_provenance`
- `metrics_gate_eligible`
- `provenance_notes`

The implementation must treat `metric_profile` as an **interpretation contract**, not a decorative taxonomy label.

---

## Why this change exists

The current lane fleet now contains materially different lane types:

- `continuity-progression-reasoning`
- `general-grammar-cleanup`
- `lore-safe-proofreading`

The existing shared metric trio:

- `schema_reliability`
- `false_positive_rate`
- `surface_detection_rate`

still exists in all records, but those fields are no longer the same semantic center for all lane types.

That is acceptable only as a transitional state.

We now need a governed field that tells downstream consumers which metric family is actually primary for interpreting a lane.

---

## Implementation goals

1. Add a required `metric_profile` field to lane analytics records.
2. Keep the initial enum intentionally small and tied to real active lanes.
3. Update the validator to enforce the new field.
4. Backfill all current lane records.
5. Update docs so authoring and interpretation rules are explicit.
6. Do **not** overfit the schema by storing all profile semantics redundantly in every lane record.

---

## Non-goals

This implementation does **not**:

- redesign the legacy metric trio yet
- add profile-specific primary metric fields yet
- implement ForgeCommand UI
- add every future profile category now
- collapse profile and provenance into one field

---

## Required implementation scope

### 1. Schema change

Update:

- `schemas/lane-analytics.schema.json`

Add new required field:

- `metric_profile`

Type:

- string enum

Initial allowed values:

- `detection_reasoning`
- `editing_cleanup`
- `lore_protection_editing`

This must be a closed enum in this revision.

### 2. Validator update

Update:

- `scripts/validate-lane-records.py`

Add validation for:

- presence of `metric_profile`
- valid enum membership

Do not invent profile/provenance coupling rules beyond what is already explicitly defined.

Optional validator warnings are acceptable only if they are clearly justified and non-disruptive.

### 3. Lane fleet backfill

Backfill the current three lane records with the correct `metric_profile` values:

- `continuity-progression-reasoning` → `detection_reasoning`
- `general-grammar-cleanup` → `editing_cleanup`
- `lore-safe-proofreading` → `lore_protection_editing`

Only use repo-verified paths and existing values.

Do not invent supporting docs.

### 4. Documentation update

Update or create docs that explain:

- what `metric_profile` means
- how it differs from `metric_provenance`
- why the current metric trio is canonical for some lanes and translated for others
- current mapping for the lane fleet

Docs should make clear that profile semantics are a governed interpretation layer, not merely descriptive metadata.

### 5. Validation pass

Run fleet validation and confirm clean pass.

Primary validation command:

```bash
python3 scripts/validate-lane-records.py
```

---

## Acceptance criteria

The implementation is complete only if all of the following are true:

1. `metric_profile` exists in the schema.
2. `metric_profile` is required.
3. `metric_profile` is a closed enum with exactly the three approved values.
4. The validator hard-fails missing or invalid `metric_profile` values.
5. All current lane records are backfilled correctly.
6. Validation passes fleet-wide.
7. Documentation explicitly distinguishes profile from provenance.
8. No fake files, fake paths, or speculative records are introduced.

---

## Guardrails

- Do not widen the enum beyond the approved three values.
- Do not add extra schema fields unless strictly necessary to complete this change safely.
- Do not remove the legacy trio in this change set.
- Do not weaken current provenance governance.
- Do not encode all profile interpretation logic as repeated JSON fields in every lane record.
- Prefer minimal, disciplined edits over broad refactoring.

---

# Part 2 — Schema Change Draft v2

## Revision

- Revision: 2
- Status: Draft for implementation
- Target: `schemas/lane-analytics.schema.json`

---

## Purpose

Add a new governed field, `metric_profile`, to lane analytics records so downstream systems can interpret lane metrics according to lane type rather than assuming one shared semantic center.

This is an additive schema revision intended to preserve current fleet operability while making lane interpretation safer and more explicit.

---

## New field

### `metric_profile`

Type:

- `string`

Required:

- yes

Enum values:

- `detection_reasoning`
- `editing_cleanup`
- `lore_protection_editing`

---

## Field meaning

### `detection_reasoning`

Use for lanes whose primary task is to detect, surface, assess, or reason about structured conditions in governed input material.

For this profile, the current legacy trio remains the canonical metric center.

### `editing_cleanup`

Use for lanes whose primary task is general cleanup, grammar correction, or light editorial improvement where restraint is central.

For this profile, the current legacy trio may remain present but is interpreted as translated transitional visibility rather than the canonical long-term metric family.

### `lore_protection_editing`

Use for editing lanes where preservation of protected terms, canon facts, continuity anchors, or manuscript-local truth is a dominant constraint.

For this profile, the current legacy trio may remain present but is not the canonical long-term metric center, and downstream comparison should be handled more conservatively.

---

## Current fleet mapping

- `continuity-progression-reasoning` → `detection_reasoning`
- `general-grammar-cleanup` → `editing_cleanup`
- `lore-safe-proofreading` → `lore_protection_editing`

---

## JSON schema shape

Example JSON fragment:

```json
{
  "metric_profile": {
    "type": "string",
    "enum": [
      "detection_reasoning",
      "editing_cleanup",
      "lore_protection_editing"
    ]
  }
}
```

The field must also be added to the schema’s required keys list.

---

## Backward compatibility posture

This is an additive revision in design.

Operationally, because the field is required, the schema update and lane record backfill must land in the same change set.

---

# Part 3 — Senior Engineer Review of Schema Change Draft v2

## Executive review

The schema change is correct in direction and is appropriately narrower than the earlier metric-profile draft.

It avoids the biggest overdesign risk: turning every lane record into a bloated policy bundle.

Adding only `metric_profile` now is the right move.

However, a few implementation concerns need to be explicitly handled so the change remains crisp and governance-safe.

---

## What is strong about the draft

### 1. Properly scoped field introduction

Only one new field is being added.

That keeps the change set understandable, reduces migration risk, and avoids prematurely freezing too much policy into the schema.

### 2. The enum is intentionally small

That is a real engineering improvement over the broader earlier taxonomy.

The schema is being grounded in real active lanes, not hypothetical future categories.

### 3. Correct separation from provenance

The draft does not try to make `metric_profile` carry evidence-strength meaning.

That is correct.

Profile and provenance must remain separate.

### 4. Transitional compatibility is preserved

The change does not attempt to remove or redefine the legacy trio during the same change set.

That is the right call.

---

## Risks and required corrections

### Risk 1 — profile may be treated as descriptive only

If docs and validator updates are minimal, future consumers may read `metric_profile` but not actually change behavior.

#### Required correction

Documentation must explicitly state that `metric_profile` is an interpretation contract for downstream systems, not merely a reporting label.

### Risk 2 — hidden overcoupling in future validator logic

There will be a temptation to start inferring correctness of metric values from profile too early.

That would be premature.

#### Required correction

Validator scope in this revision should remain limited to:

- field presence
- enum validity

Do not add speculative profile-specific metric policing yet.

### Risk 3 — schema drift from future profile expansion

If future teams add profile enum values casually, meaning will drift.

#### Required correction

The enum should remain closed and any future additions should require an explicit schema revision and governance note.

### Risk 4 — consumer assumptions may still outrun schema semantics

Even with `metric_profile`, a downstream consumer could still build naive comparisons.

#### Required correction

The docs in this change set should record the interpretation posture clearly enough that future consumer work has a stable control reference.

---

## Senior engineer implementation recommendation

Approve this schema change with the following posture:

- add only `metric_profile`
- keep enum limited to three values
- update validator only for required presence and enum validity
- backfill current fleet immediately
- update documentation strongly enough to prevent descriptive-only interpretation

This is the smallest clean step that creates real future leverage without locking the system into early overdesign.

---

# Part 4 — Final VS Code Opus Prompt

Use the prompt below as the implementation prompt for VS Code Opus.

---

You are implementing a governed schema evolution in the NeuronForge repository.

Your task is to add `metric_profile` to the lane analytics schema, update the validator, backfill the current lane fleet, and update supporting documentation.

## Required context

The lane visibility surface already exists and is schema-validated.

The fleet currently includes three real lane records:

- `continuity-progression-reasoning`
- `general-grammar-cleanup`
- `lore-safe-proofreading`

The schema already includes governance around:

- `metric_provenance`
- `metrics_gate_eligible`
- `provenance_notes`

Do not disturb that existing governance behavior.

The purpose of this change is to add a governed interpretation field that tells downstream consumers what kind of lane they are reading.

This field is **not** provenance.

It is **not** a decorative taxonomy label.

It is an interpretation contract that will later support profile-aware comparison and consumer behavior.

## What to implement

### 1. Update the schema

File:

- `schemas/lane-analytics.schema.json`

Add a new required field:

- `metric_profile`

Rules:

- type must be `string`
- must be a closed enum
- allowed values must be exactly:
  - `detection_reasoning`
  - `editing_cleanup`
  - `lore_protection_editing`

Also add `metric_profile` to the required keys list.

Do not add any other schema fields unless strictly necessary.

### 2. Update the validator

File:

- `scripts/validate-lane-records.py`

Add validation that:

- `metric_profile` exists
- `metric_profile` is one of the approved enum values

Important constraint:

Do **not** add speculative logic that tries to infer whether the rest of the metrics are semantically correct for a given profile.

In this revision the validator should only enforce:

- presence
- enum validity

Leave deeper profile semantics to documentation and future consumer logic.

### 3. Backfill current lane records

Update the current lane fleet using only repo-verified values.

Required mappings:

- `continuity-progression-reasoning` → `detection_reasoning`
- `general-grammar-cleanup` → `editing_cleanup`
- `lore-safe-proofreading` → `lore_protection_editing`

Do not invent any files, paths, or supporting docs.

### 4. Update documentation

Update the relevant documentation so it clearly states:

- what `metric_profile` means
- how `metric_profile` differs from `metric_provenance`
- that `metric_profile` is an interpretation contract, not just descriptive metadata
- that the current legacy trio remains canonical for detection/reasoning lanes and transitional/translated for the editing lanes
- the current fleet mapping for the three active lanes

Keep the documentation grounded and implementation-oriented.

### 5. Validate

Run:

```bash
python3 scripts/validate-lane-records.py
```

Confirm clean pass.

## Guardrails

- Do not widen the enum.
- Do not remove or rename existing fields.
- Do not add profile/provenance coupling rules.
- Do not add future-facing profiles such as structured generation or classification review in this change.
- Do not invent supporting artifacts that do not exist.
- Prefer minimal, disciplined edits.

## Deliverables

Provide:

1. the updated schema
2. the updated validator
3. the updated lane records
4. the updated docs
5. the validation result
6. a concise summary of what changed and why

## Quality bar

This should land as a small, governed, implementation-safe schema revision.

The output should reflect senior-engineer judgment:

- minimal surface area
- clear separation of concerns
- no speculative overdesign
- no fake paths
- no semantic drift

If you encounter ambiguity, resolve it conservatively and explain the decision in the summary.

