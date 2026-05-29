# Continuity / Progression Candidate Schema

Date: 2026-03-14

## Purpose

Define the strict structured output contract for the `continuity-progression-reasoning` lane.

This schema exists so NeuronForge Local can produce candidate findings in a shape that is:

- reviewable
- auditable
- bounded by scope
- resistant to authority leakage
- stable enough for challenger comparison

This is a **candidate artifact schema**.

It is not a canonical story schema.

It is not a truth-bearing authority record.

---

## Lane context

- **lane id:** `continuity-progression-reasoning`
- **contract family:** `analysis`
- **strictness:** `STRICT_STRUCTURED`
- **artifact posture:** candidate-only
- **preferred route:** `HIGH_QUALITY_LOCAL`
- **fallback posture:** fail closed

---

## Schema doctrine

This lane is reasoning-sensitive and review-facing.

That means the output contract must optimize for:

- bounded claims
- explicit scope
- evidence discipline
- confidence restraint
- operator review speed
- repeatable evaluation

A polished but structurally weak output is worse than no output.

Malformed output should be treated as lane failure.

---

## Top-level object

The lane should return one top-level object for each analysis run.

### Required top-level fields

- `schema_version`
- `lane_id`
- `analysis_scope_type`
- `analysis_scope_bounds`
- `input_unit_ids`
- `candidate_findings`
- `overall_run_note`
- `run_posture`

### Example shape

```json
{
  "schema_version": "1.0",
  "lane_id": "continuity-progression-reasoning",
  "analysis_scope_type": "adjacent_scene",
  "analysis_scope_bounds": {
    "chapter_ids": ["ch-04"],
    "scene_ids": ["sc-041", "sc-042"],
    "scene_positions": [41, 42]
  },
  "input_unit_ids": ["sc-041", "sc-042"],
  "candidate_findings": [],
  "overall_run_note": "No strong continuity or progression issue detected within the bounded scope.",
  "run_posture": "candidate_only"
}
```

---

## Field definitions

### `schema_version`

**Type:** string

Schema version for contract governance.

Initial value:

- `1.0`

---

### `lane_id`

**Type:** string

Must equal:

- `continuity-progression-reasoning`

Any other value is invalid for this lane.

---

### `analysis_scope_type`

**Type:** enum string

Allowed values:

- `scene_local`
- `adjacent_scene`
- `scene_window`
- `chapter_window`

The lane must declare scope explicitly.

---

### `analysis_scope_bounds`

**Type:** object

Defines the exact bounded review window.

#### Required subfields

- `scene_ids`

#### Optional subfields

- `chapter_ids`
- `scene_positions`
- `window_start_scene_id`
- `window_end_scene_id`

#### Example

```json
{
  "chapter_ids": ["ch-07"],
  "scene_ids": ["sc-071", "sc-072", "sc-073"],
  "scene_positions": [71, 72, 73],
  "window_start_scene_id": "sc-071",
  "window_end_scene_id": "sc-073"
}
```

If scope bounds are missing or vague, the output should fail.

---

### `input_unit_ids`

**Type:** array of strings

Identifiers for the units actually analyzed.

These should normally match or be consistent with the scene ids in `analysis_scope_bounds`.

---

### `candidate_findings`

**Type:** array of finding objects

May be empty.

A zero-finding result is valid if it is structurally correct and genuinely restrained.

Each finding object must follow the finding schema below.

---

### `overall_run_note`

**Type:** string

A short summary note for the operator.

This field should:

- summarize the run at a glance
- stay candidate-framed
- avoid truth-language leakage
- remain short and review-friendly

Examples:

- `No strong continuity or progression issue detected within the bounded scope.`
- `Two candidate review points were identified: one possible abrupt transition and one possible descriptive mismatch.`

---

### `run_posture`

**Type:** enum string

Must equal:

- `candidate_only`

Any value suggesting authority posture is invalid.

---

## Finding object schema

Each entry in `candidate_findings` must contain the following required fields.

### Required finding fields

- `finding_id`
- `finding_label`
- `finding_type`
- `claim`
- `scope_type`
- `scope_bounds`
- `evidence_spans`
- `confidence`
- `uncertainty_note`
- `review_note`
- `candidate_state`

### Optional finding fields

- `related_finding_ids`
- `severity_hint`
- `taxonomy_tags`

---

## Required finding field definitions

### `finding_id`

**Type:** string

Unique within the candidate set.

Recommended format:

- `cpf-001`
- `cpf-002`

`cpf` = continuity/progression finding.

---

### `finding_label`

**Type:** string

Short, review-friendly label.

Good examples:

- `Possible abrupt emotional transition`
- `Possible travel-state mismatch`
- `Possible repeated movement across adjacent scenes`

Bad examples:

- `Issue`
- `Problem detected`
- `Potential narrative inconsistency and maybe also emotional drift depending on interpretation`

---

### `finding_type`

**Type:** enum string

Allowed values:

- `continuity_tension`
- `progression_break`
- `transition_gap`
- `descriptive_mismatch`
- `repeated_movement`
- `escalation_mismatch`
- `state_carry_forward_issue`
- `causal_link_unclear`

These labels should stay narrow and stable.

Do not add new values casually without governance review.

---

### `claim`

**Type:** string

Short candidate-framed statement of the possible issue.

The claim must:

- stay inside scope
- avoid declaring story truth
- avoid invented off-page facts
- describe what should be reviewed

Good example:

- `The emotional handoff from scene sc-041 to sc-042 may feel more abrupt than the evidence in the transition supports.`

Bad example:

- `The character is definitely inconsistent here.`

---

### `scope_type`

**Type:** enum string

Allowed values:

- `scene_local`
- `adjacent_scene`
- `scene_window`
- `chapter_window`

This must align with the lane run scope or be narrower.

A finding must never declare a broader scope than the run itself.

---

### `scope_bounds`

**Type:** object

Required subfields:

- `scene_ids`

Optional subfields:

- `chapter_ids`
- `scene_positions`

This field declares the exact evidence window for the finding itself.

A finding that references scenes outside its own scope bounds is invalid.

---

### `evidence_spans`

**Type:** array of evidence objects

Minimum required length:

- at least `1`

Recommended normal minimum for cross-scene claims:

- at least `2` spans when comparing two scenes or more

Each evidence object must follow the evidence schema below.

Material claims without evidence should hard-fail.

---

### `confidence`

**Type:** enum string

Allowed values:

- `low`
- `moderate`
- `high`

No stronger value is allowed.

Use `high` sparingly.

If evidence is partial or ambiguous, use `low` or `moderate`.

---

### `uncertainty_note`

**Type:** string

Required note explaining why the finding may be wrong, incomplete, or scope-limited.

This field is mandatory because the lane is candidate-only and reasoning-sensitive.

Good examples:

- `The transition may be intentionally abrupt, and the bounded scene window may omit setup that resolves the issue elsewhere.`
- `The descriptive mismatch may reflect perspective limitation rather than true continuity tension.`

Bad examples:

- `None`
- `No uncertainty`

---

### `review_note`

**Type:** string

Short instruction telling the reviewer what to inspect.

Good examples:

- `Check whether the emotional tone at the end of sc-041 provides enough setup for the opening posture in sc-042.`
- `Verify whether the possession state of the item is clearly handed off between the two scenes.`

Bad examples:

- `Review this`
- `See issue`

---

### `candidate_state`

**Type:** enum string

Allowed initial values:

- `candidate_unreviewed`

Other downstream values may exist later in governed systems:

- `candidate_review_in_progress`
- `candidate_retained`
- `candidate_rejected`
- `candidate_promoted`

For raw lane output, initial generation should normally use:

- `candidate_unreviewed`

---

## Optional finding fields

### `related_finding_ids`

**Type:** array of strings

Use when two findings are meaningfully linked.

Example:

- a `transition_gap` finding related to a `state_carry_forward_issue`

---

### `severity_hint`

**Type:** enum string

Allowed values:

- `minor`
- `moderate`
- `major`

This is a review hint only.

It must not be treated as truth or policy.

If included, it should remain conservative.

---

### `taxonomy_tags`

**Type:** array of strings

Optional narrow tags for review grouping.

Examples:

- `emotion`
- `injury-state`
- `travel`
- `inventory`
- `tone`
- `cause-effect`

Tags should remain small and stable.

---

## Evidence object schema

Each evidence span must contain:

- `scene_id`
- `span_text`
- `span_role`

Optional:

- `chapter_id`
- `position_hint`

### Field definitions

#### `scene_id`

**Type:** string

Must identify the scene from which the evidence was drawn.

#### `span_text`

**Type:** string

Short supporting text span.

This should be long enough to justify review but short enough to stay usable.

#### `span_role`

**Type:** enum string

Allowed values:

- `setup`
- `contrast`
- `carry_forward`
- `mismatch_signal`
- `transition_signal`
- `progression_signal`

#### `chapter_id`

**Type:** string

Optional chapter reference when available.

#### `position_hint`

**Type:** string

Optional location note such as:

- `opening`
- `mid-scene`
- `ending`

---

## Example finding

```json
{
  "finding_id": "cpf-001",
  "finding_label": "Possible abrupt emotional transition",
  "finding_type": "transition_gap",
  "claim": "The emotional handoff from scene sc-041 to sc-042 may feel more abrupt than the visible transition support justifies.",
  "scope_type": "adjacent_scene",
  "scope_bounds": {
    "scene_ids": ["sc-041", "sc-042"],
    "scene_positions": [41, 42]
  },
  "evidence_spans": [
    {
      "scene_id": "sc-041",
      "span_text": "Rawn leaves the confrontation still joking with Amicae as they descend toward the river road.",
      "span_role": "setup",
      "position_hint": "ending"
    },
    {
      "scene_id": "sc-042",
      "span_text": "At the opening of the next scene, Rawn is immediately withdrawn and hostile without a visible transition marker.",
      "span_role": "contrast",
      "position_hint": "opening"
    }
  ],
  "confidence": "moderate",
  "uncertainty_note": "The change may be intentional and could be supported by omitted context outside the bounded two-scene window.",
  "review_note": "Check whether the end of sc-041 or start of sc-042 supplies enough transition signal for the emotional shift.",
  "candidate_state": "candidate_unreviewed",
  "severity_hint": "moderate",
  "taxonomy_tags": ["emotion", "transition"]
}
```

---

## Zero-finding example

```json
{
  "schema_version": "1.0",
  "lane_id": "continuity-progression-reasoning",
  "analysis_scope_type": "scene_window",
  "analysis_scope_bounds": {
    "scene_ids": ["sc-101", "sc-102", "sc-103"],
    "scene_positions": [101, 102, 103]
  },
  "input_unit_ids": ["sc-101", "sc-102", "sc-103"],
  "candidate_findings": [],
  "overall_run_note": "No strong continuity or progression issue detected in this bounded scene window.",
  "run_posture": "candidate_only"
}
```

A zero-finding result is valid only if the lane genuinely found no strong review-worthy issue.

It must not be used to hide schema weakness or under-response.

---

## Validation rules

The output should be rejected if any of the following are true:

- `lane_id` does not match the lane
- `analysis_scope_type` is missing or invalid
- `analysis_scope_bounds` is missing scene ids
- `run_posture` is not `candidate_only`
- any finding omits required fields
- any finding uses a non-approved `finding_type`
- any finding uses a non-approved `confidence`
- `candidate_findings` is not an array
- any material claim has no evidence span
- any finding scope exceeds run scope
- any field language presents the result as canonical truth

---

## Candidate-language rules

Allowed tone:

- possible
- may
- appears
- suggests
- worth review
- candidate

Disallowed tone:

- definitely
- proves
- confirms
- establishes
- canonically shows
- is true that

This lane must preserve candidate posture in schema content, not just in surrounding documentation.

---

## Fail-closed rules

The lane should fail closed instead of returning weak structure when:

- the model cannot produce valid JSON or structured output
- evidence spans cannot be grounded in scope
- scope cannot be stated clearly
- candidate posture cannot be maintained
- finding taxonomy cannot be kept inside approved values

No output is preferable to polished but unsafe output.

---

## Governance notes

This schema is intentionally narrow.

It should not be expanded casually.

Schema expansion should happen only when:

- a repeated review need is visible
- the new field improves auditability or review usability
- the new field does not blur candidate vs authority posture
- challengers can realistically satisfy the expanded contract on target hardware

---

## Current judgment

This schema is sufficient as the first strict structured contract for the `continuity-progression-reasoning` lane.

It gives the lane:

- explicit bounded scope
- stable finding taxonomy
- required evidence discipline
- mandatory uncertainty
- mandatory review actionability
- explicit candidate-only posture

That is enough to support:

- rubric-based review
- challenger comparison
- bounded eval set creation
- fail-closed implementation planning

---

## Restart note

If resuming later, this schema is ready to pair with:

- the continuity/progression review rubric
- an eval set plan
- a high-quality-local challenger comparison plan

Most natural next artifact:

**Continuity / Progression Eval Set Plan**

