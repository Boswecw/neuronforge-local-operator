# Continuity / Progression Eval Set Plan

Date: 2026-03-14

## Purpose

Define the first bounded evaluation set plan for the `continuity-progression-reasoning` lane.

This document exists to make challenger comparison possible in a controlled, reviewable way.

It does not yet contain the actual finalized eval corpus.

It defines:

- what kinds of examples are needed
- what balance the set should have
- what failure cases must be represented
- what metadata each eval case should carry
- how the set should be used during lane review

---

## Lane context

- **lane id:** `continuity-progression-reasoning`
- **contract family:** `analysis`
- **strictness:** `STRICT_STRUCTURED`
- **artifact posture:** candidate-only
- **preferred route:** `HIGH_QUALITY_LOCAL`
- **fallback posture:** fail closed

This lane is review-facing and reasoning-sensitive.

That means the eval set must measure more than whether the model can produce plausible-looking findings.

It must measure whether the model can produce:

- bounded findings
- evidence-grounded findings
- restrained findings
- review-usable findings
- candidate-not-authority findings

---

## Eval doctrine

The eval set should be designed to test lane trustworthiness, not just lane activity.

A model should not score well merely because it produces many findings.

The set should reward:

- correct restraint
- scope honesty
- evidence quality
- calibrated confidence
- stable structure

The set should expose:

- over-extraction
- overreach
- false continuity claims
- false progression claims
- schema weakness
- authority leakage

---

## Primary use of the set

This eval set is meant to support:

- challenger model comparison
- prompt revision comparison
- repeated-run drift observation
- trust advancement decisions for the lane

It is not meant to be a public benchmark.

It is an internal governance instrument.

---

## Initial scope strategy

The first eval set should stay bounded and operationally realistic.

Recommended initial composition:

- mostly adjacent-scene comparisons
- some short scene-window cases
- very limited or no chapter-window cases in the first round

### Why

Adjacent-scene and short scene-window review are the lowest-risk entry points for this lane.

They are easier to judge, easier to bound, and less likely to reward vague global reasoning.

Chapter-window reasoning should come later, after the lane shows stable behavior in smaller windows.

---

## Target eval-set size

Recommended first-pass size:

- **12 to 20 cases** total

Recommended starting target:

- **16 cases**

That is large enough to expose major weaknesses without creating unnecessary review drag in the first governed cycle.

---

## Case type coverage

The first set should include cases across the following categories.

### 1. True continuity tension

Cases where a real bounded continuity problem exists and should be review-flagged.

Examples:

- injury state changes without support
- possession state changes without handoff
- travel state mismatch
- descriptive contradiction inside a bounded window

### 2. Apparent but not real continuity tension

Cases that look suspicious at first glance but are acceptable on closer reading.

These cases are essential for testing restraint.

Examples:

- perspective-limited wording
- intentionally ambiguous detail
- compressed narration that remains coherent

### 3. True progression break

Cases where emotional, causal, or scene-to-scene movement feels insufficiently supported.

Examples:

- abrupt emotional state shift
- abrupt allegiance or motivation shift
- consequence missing from the next scene where it should likely carry forward

### 4. Acceptable abrupt transition

Cases where the prose moves fast but does not actually create a review-worthy progression issue.

These cases are essential for preventing transition inflation.

### 5. Repeated movement worth flagging

Cases where adjacent or near-adjacent scenes repeat function, movement, or dramatic work in a way that is plausibly review-worthy.

### 6. Repeated movement not worth flagging

Cases where related scenes are similar by design but not redundant in a lane-worthy sense.

### 7. Descriptive mismatch worth review

Cases where an attribute, condition, or framing shifts enough to justify review.

### 8. Ambiguous edge case

Cases where a good model should remain cautious, candidate-framed, and uncertainty-aware.

These are especially useful for confidence calibration review.

---

## Recommended case distribution

For a 16-case first pass, a good distribution would be:

- 3 true continuity tension cases
- 2 apparent but not real continuity tension cases
- 3 true progression break cases
- 2 acceptable abrupt transition cases
- 2 repeated movement worth flagging cases
- 1 repeated movement not worth flagging case
- 2 descriptive mismatch worth review cases
- 1 ambiguous edge case

This is not mathematically fixed.

It is an operationally sane first balance.

---

## Scope distribution

Recommended mix:

- **10 adjacent-scene cases**
- **6 scene-window cases**

Optional first-pass chapter-window cases:

- **0**

A later expansion set can add chapter-window cases once the lane demonstrates acceptable bounded reasoning and scope honesty at smaller scales.

---

## Metadata required for each eval case

Each eval case should carry the following metadata.

### Required fields

- `case_id`
- `case_title`
- `scope_type`
- `scene_ids`
- `chapter_ids` if available
- `case_category`
- `case_intent`
- `operator_expected_posture`
- `review_notes`

### Optional but useful fields

- `expected_finding_types`
- `expected_restraint_note`
- `likely_failure_modes`
- `difficulty_level`

---

## Field guidance

### `case_id`

Stable identifier such as:

- `cpe-001`
- `cpe-002`

`cpe` = continuity/progression eval.

### `case_title`

Short human-readable label.

Example:

- `Injury carry-forward mismatch across adjacent scenes`

### `scope_type`

Allowed values:

- `adjacent_scene`
- `scene_window`

Use `chapter_window` later only after first trust-building rounds.

### `scene_ids`

Exact scene identifiers included in the case.

### `chapter_ids`

Include when known and helpful.

### `case_category`

Use one of the approved categories:

- `true_continuity_tension`
- `apparent_not_real_continuity_tension`
- `true_progression_break`
- `acceptable_abrupt_transition`
- `repeated_movement_flaggable`
- `repeated_movement_not_flaggable`
- `descriptive_mismatch_review_worthy`
- `ambiguous_edge_case`

### `case_intent`

Short note describing what the case is meant to test.

Example:

- `tests whether the model can detect a possession-state handoff gap without inventing missing action`

### `operator_expected_posture`

Short guidance for the reviewer on what success should look like.

Examples:

- `should likely produce one restrained candidate finding with explicit uncertainty`
- `should likely produce zero findings and preserve candidate posture`
- `should flag only if evidence is cited from both scenes`

### `review_notes`

Short operator note about what matters most in judging the output.

---

## Optional metadata guidance

### `expected_finding_types`

Use when you want to indicate plausible acceptable labels without over-prescribing the exact answer.

Example:

- `["state_carry_forward_issue"]`

### `expected_restraint_note`

Use when the case exists mainly to test non-overreaction.

Example:

- `do not penalize zero findings if the model explains restraint through candidate-framed run note`

### `likely_failure_modes`

Examples:

- `invented bridge`
- `transition inflation`
- `confidence inflation`
- `scope overreach`
- `authority leakage`

### `difficulty_level`

Allowed suggested values:

- `low`
- `moderate`
- `high`

This is reviewer planning metadata, not lane output.

---

## Case construction rules

Each case should be built so the reviewer can judge it without needing the entire manuscript.

That means:

- keep scope bounded
- keep the case self-contained enough for review
- avoid requiring hidden global lore to interpret the case
- avoid cases where only the original author can tell whether something is wrong

The first eval set should prioritize clarity of review over literary complexity.

---

## Ground-truth doctrine

This lane is candidate-only and reasoning-sensitive.

That means evals should **not** use simplistic binary answer keys.

Instead, each case should define a bounded operator expectation.

### Good operator expectation examples

- one restrained finding is likely justified
- zero findings is acceptable if scope is respected and uncertainty is handled well
- only a descriptive mismatch candidate should be acceptable here
- a high-confidence claim would be inappropriate for this case

### Bad operator expectation examples

- the model must say exactly X
- the model must emit two findings and no more
- the correct answer is fully deterministic when the case is intentionally ambiguous

The eval set should guide judgment, not force fake precision.

---

## What a strong case looks like

A strong eval case:

- has clear bounded scope
- tests one or two main failure modes
- is reviewable without hidden knowledge
- supports meaningful rubric scoring
- does not force one brittle phrasing outcome

---

## What a weak case looks like

A weak eval case:

- depends on broad manuscript context not present in the case
- is so obvious that every model will pass trivially
- is so vague that no stable judgment is possible
- mixes too many unrelated issues together
- rewards verbosity instead of disciplined reasoning

---

## Example case record

```json
{
  "case_id": "cpe-003",
  "case_title": "Possession-state handoff gap across adjacent scenes",
  "scope_type": "adjacent_scene",
  "scene_ids": ["sc-031", "sc-032"],
  "chapter_ids": ["ch-03"],
  "case_category": "true_continuity_tension",
  "case_intent": "tests whether the model can notice a likely possession-state gap without inventing the missing transfer event as fact",
  "operator_expected_posture": "should likely produce one restrained candidate finding with evidence from both scenes and explicit uncertainty",
  "review_notes": "penalize invented bridge language or authority phrasing",
  "expected_finding_types": ["state_carry_forward_issue"],
  "likely_failure_modes": ["invented bridge", "confidence inflation", "authority leakage"],
  "difficulty_level": "moderate"
}
```

---

## Use with the rubric

Each case should be reviewed using the existing Continuity / Progression Review Rubric.

The eval set and rubric work together like this:

- eval case defines what is being tested
- lane output provides candidate findings in schema form
- rubric scores the output for review-grade usefulness and governance discipline

Do not treat the eval set as sufficient without rubric scoring.

---

## Use with challenger comparison

A challenger comparison cycle should normally:

1. run the same eval cases through each candidate model/prompt combination
2. capture raw structured outputs
3. score each case with the rubric
4. note hard fails separately from normal scores
5. compare patterns, not just totals

Important comparison patterns include:

- who over-flags
- who under-flags
- who invents bridges
- who leaks authority tone
- who breaks schema
- who produces the most review-usable evidence notes

---

## Repeatability and drift use

The set should also support repeated-run observation.

This does not require exact wording repeatability.

It requires semantic stability strong enough that:

- the same obvious issues are not wildly reinterpreted across runs
- confidence does not swing irrationally
- structure remains valid
- review conclusions would remain materially similar

Drift notes should be recorded alongside rubric scores for repeated runs.

---

## Recommended assembly workflow

A practical first assembly workflow:

1. identify candidate scene pairs and short windows from current manuscript material or lane test assets
2. classify each candidate into one of the approved case categories
3. discard cases that require too much hidden context
4. draft metadata records for the strongest 20–24 candidates
5. cut down to a first governed set of 16 balanced cases
6. dry-run rubric scoring on a small sample to verify the cases are actually judgeable
7. freeze v1 of the set for challenger comparison

---

## Versioning posture

The eval set should be versioned.

Recommended first version:

- `continuity-progression-eval-set-v1`

Do not silently swap cases in or out once challenger comparison has begun.

If cases need to change materially, create a new version.

---

## Initial exclusions

The first version of the eval set should avoid:

- manuscript-wide continuity problems requiring broad context
- lore disputes requiring external canonical source resolution
- cases where truth depends on unpublished author intent not visible in the scene set
- giant windows that reward vagueness
- cases that are mostly style preference rather than continuity/progression reasoning

---

## Acceptance posture for v1 assembly

The first eval-set version is good enough when:

- coverage is balanced across the main case categories
- most cases are adjacent-scene or short scene-window
- each case has usable operator expectation notes
- the set can expose both overreach and under-detection
- the set is practical to review during challenger comparison

Perfection is not required for v1.

Reviewability and governance usefulness are the priority.

---

## Current judgment

This plan is sufficient to assemble the first governed eval set for the `continuity-progression-reasoning` lane.

It keeps the initial set:

- bounded
- reviewable
- useful for challenger testing
- resistant to fake benchmark behavior
- aligned with candidate-only doctrine

That is the correct posture for the first evaluation cycle.

---

## Restart note

If resuming later, this plan is ready to drive:

- case selection
- metadata drafting
- v1 eval-set assembly
- challenger comparison against the review rubric and candidate schema

Most natural next artifact:

**High-Quality-Local Challenger Evaluation Plan for Continuity / Progression Reasoning**

