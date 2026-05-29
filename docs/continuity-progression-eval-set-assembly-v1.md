# Continuity / Progression Eval Set Assembly v1

## Status
Draft v1.0

## Purpose
Define the first governed evaluation-set assembly plan for the `continuity-progression-reasoning` lane.

This artifact does **not** contain the final case pack yet.

It defines:

- target first-pass case count
- required category coverage
- required scope coverage
- case metadata requirements
- assembly workflow
- acceptance posture for the eval set itself

This exists so challenger testing is built on an intentional case set instead of ad hoc examples.

---

## 1. Lane under test

- **lane id:** `continuity-progression-reasoning`
- **family:** `analysis`
- **role:** bounded cross-scene / scene-window reasoning
- **artifact posture:** candidate-only
- **primary consumer:** Bloom
- **secondary consumer:** ANVIL
- **required route:** `HIGH_QUALITY_LOCAL`
- **fallback posture:** fail closed

---

## 2. Eval-set objective

The first-pass eval set should answer a practical question:

**Can a local reasoning-capable model produce review-grade bounded candidate findings for continuity and progression issues without hallucinating, overreaching, or breaking scope?**

The eval set is not a generic benchmark.

It is a lane-specific trust-discovery instrument.

That means it must pressure the lane on:

- true positives
- false-positive resistance
- restraint on acceptable abruptness
- evidence discipline
- scope discipline
- candidate-language discipline
- schema compliance

---

## 3. Target first-pass size

Recommended target:

- **16 total cases**

Acceptable early range:

- **14 to 18 cases** if assembly reality forces slight variation

Reason:

This is large enough to expose major trust failures, but still small enough to review manually with discipline.

---

## 4. Scope mix

## 4.1 Primary scope distribution

Recommended first-pass distribution:

- **10–12 `adjacent_scene` cases**
- **4–6 `scene_window` cases**
- **0 `chapter_window` cases** in v1 unless a specific case truly requires it

## 4.2 Why this mix

The lane’s most important early duty is bounded local review between nearby story units.

That means adjacent-scene reasoning should dominate the first pass.

`scene_window` cases are included to test slightly broader state carry-forward and progression analysis without expanding too early into long-range memory claims.

`chapter_window` is intentionally deferred because it raises complexity, ambiguity, and memory-pressure risk too early.

---

## 5. Required category coverage

The first-pass set should include at least one case from each of the following categories.

## 5.1 True issue categories

1. **true continuity tension**
   - a detail appears to conflict or fail to carry forward in a review-worthy way

2. **true progression break**
   - the narrative movement or state change feels missing, under-bridged, or improperly advanced

3. **state carry-forward issue**
   - a scene-local or nearby state appears not to carry coherently into the next bounded scope

4. **descriptive mismatch worth review**
   - description changes in a way that plausibly merits review

5. **repeated movement worth flagging**
   - a motion/action/progression beat seems redundantly re-staged or duplicated in a review-worthy way

6. **unclear causal link**
   - a key action, reaction, or transition lacks sufficient nearby causal grounding

## 5.2 False-positive resistance categories

7. **apparent but not real continuity tension**
   - looks suspicious at first glance but is acceptable on close reading

8. **acceptable abrupt transition**
   - quick or sharp transition is stylistically acceptable and should not be over-flagged

9. **repeated movement not worth flagging**
   - some repetition exists but is natural, functional, or below review threshold

10. **ambiguous edge case**
   - the case is legitimately debatable and tests restraint, confidence calibration, and candidate framing

---

## 6. Category balance targets

A healthy v1 set should lean slightly toward false-positive resistance pressure.

Recommended rough balance:

- **7–8 true-issue cases**
- **6–7 false-positive resistance cases**
- **2–3 ambiguous edge cases**

Reason:

This lane is dangerous if it becomes a confident over-flagger.

The eval set must therefore test whether the model can **decline to invent problems**.

---

## 7. Case design principles

Each eval case should be designed to pressure one primary question, even if secondary signals exist.

## 7.1 One dominant lesson per case

Each case should have one main review target, such as:

- detect a real progression gap
- resist a fake continuity issue
- flag a plausible descriptive mismatch with evidence
- refuse to escalate weak repetition into noise

Do not build cases that are too tangled to score cleanly in v1.

## 7.2 Bounded evidence should be sufficient

The case should contain enough nearby text for a careful reviewer to justify a bounded candidate finding.

If the case requires broad story memory to interpret fairly, it likely does not belong in v1.

## 7.3 Prefer realistic authoring texture

Cases should resemble real manuscript conditions:

- imperfect transitions
- natural stylistic abruptness
- partial state reminders
- subtle repetition
- non-mechanical phrasing

Avoid synthetic toy cases that teach the wrong lesson.

## 7.4 Avoid trivial gotchas

The goal is not to bait the model with obvious contradictions only.

The best cases are review-realistic, where a disciplined model should either:

- flag a plausible candidate issue with evidence
- or consciously refrain from overclaiming

---

## 8. Required metadata per case

Each case in the eventual eval pack should include at minimum:

- **case id**
- **lane id**
- **scope label**
- **primary category**
- **secondary category** if applicable
- **source text units** included in the case
- **expected review posture**
- **expected restraint posture**
- **whether a finding is expected**
- **whether no finding is a good result**
- **case rationale**
- **notes for reviewer**

---

## 9. Expected review posture field

Each case should explicitly state what kind of response a good model should produce.

Suggested allowed values:

- `candidate_issue_expected`
- `restraint_expected`
- `ambiguous_candidate_allowed`

### Meaning

- **`candidate_issue_expected`**
  - a good run should usually surface at least one review-worthy candidate finding

- **`restraint_expected`**
  - a good run should usually avoid escalating the case into a strong issue claim

- **`ambiguous_candidate_allowed`**
  - a cautious candidate finding may be acceptable, but overconfidence should be penalized

---

## 10. Expected restraint posture field

Each case should also declare what kind of restraint is correct.

Suggested values:

- `high_restraint`
- `moderate_restraint`
- `low_restraint`

### Meaning

- **`high_restraint`**
  - model should be very careful, because the evidence is weak, stylistically valid, or intentionally ambiguous

- **`moderate_restraint`**
  - model may flag a candidate concern, but should remain bounded and cautious

- **`low_restraint`**
  - model can more confidently surface a candidate concern because evidence is strong within scope

This field helps distinguish a real miss from an acceptable cautious response.

---

## 11. Proposed first-pass case matrix

Below is a recommended v1 assembly matrix.

### Adjacent-scene cases

1. true continuity tension
2. apparent but not real continuity tension
3. true progression break
4. acceptable abrupt transition
5. repeated movement worth flagging
6. repeated movement not worth flagging
7. descriptive mismatch worth review
8. ambiguous edge case
9. state carry-forward issue
10. unclear causal link
11. additional false-positive resistance case
12. additional true-issue case

### Scene-window cases

13. multi-scene state carry-forward issue
14. scene-window progression break
15. scene-window acceptable abruptness / restraint case
16. scene-window ambiguous edge case

This matrix gives the first pass enough breadth without overcomplicating scoring.

---

## 12. Source-material selection guidance

## 12.1 Preferred material shape

Use source material that already contains:

- multiple adjacent scenes
- meaningful transitions
- visible state changes
- physical movement or staging
- emotional escalation or de-escalation
- descriptive carry-forward opportunities

## 12.2 Preferred material quality

The best assembly material is not perfectly polished.

It should resemble actual working-draft manuscript conditions where review help matters.

## 12.3 Exclusion guidance

Avoid source passages that are:

- too short to support bounded reasoning
- too dependent on distant unseen context
- too mechanically perfect to reveal useful failure modes
- too chaotic to score fairly

---

## 13. Assembly workflow

## 13.1 Step 1 — collect candidate source passages

Gather manuscript segments that appear promising for:

- nearby continuity checks
- adjacent-scene transitions
- scene-window progression reasoning
- descriptive carry-forward review

## 13.2 Step 2 — identify candidate case types

For each promising passage cluster, label the likely case type:

- true issue
- false-positive resistance
- ambiguous edge

## 13.3 Step 3 — trim to bounded scope

Create case packets that include only the minimum text needed for a disciplined bounded review.

Do not include extra context unless required.

## 13.4 Step 4 — write expected posture metadata

Before model testing, define:

- whether a finding is expected
- what level of restraint is correct
- why the case exists
- what bad behavior the case is meant to expose

## 13.5 Step 5 — review for scoring clarity

Ensure each case can actually be judged consistently by a human reviewer.

If a case cannot be scored with confidence, it is not ready.

## 13.6 Step 6 — freeze v1 pack before challenger comparison

Do not keep changing the case pack during the first challenger bakeoff unless a case is truly invalid.

The point is comparable evidence.

---

## 14. Eval-set acceptance criteria

The v1 eval set is acceptable when it is:

- broad enough to pressure true positives and false positives
- bounded enough for manual disciplined review
- realistic enough to reflect manuscript conditions
- explicit enough to score consistently
- diverse enough to test restraint, evidence, and scope honesty

---

## 15. Eval-set failure modes

The v1 eval set should be revised if it suffers from any of these:

- too many obvious easy wins
- too few restraint cases
- too much dependence on hidden long-range knowledge
- unclear scoring posture
- insufficient category diversity
- cases so synthetic they distort lane behavior

---

## 16. Relationship to challenger evaluation

This eval-set assembly artifact feeds directly into the challenger plan.

Once the v1 case pack is assembled, the next operational artifact should be a run worksheet that records:

- challenger model
- prompt/profile version
- case-by-case output path
- schema pass/fail
- hard-fail notes
- comparative judgment notes
- repeatability notes for selected anchor cases

---

## 17. Immediate next artifact after this one

Recommended next artifact:

**Continuity / Progression Review Worksheet v1**

That worksheet should let you score each challenger run per case using the already-stable rubric dimensions, with explicit checkboxes or fields for:

- schema validity
- hard-fail presence
- evidence quality
- scope honesty
- restraint
- candidate-language discipline
- reviewer usefulness
- drift notes

---

## 18. Current recommendation

Proceed with v1 case assembly using a target of **16 cases**, weighted toward:

- adjacent-scene bounded review
- false-positive resistance
- realistic manuscript texture
- explicit scoring posture

Do not start broad challenger bakeoff work until the v1 case pack is frozen.

