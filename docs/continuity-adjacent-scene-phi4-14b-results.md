# phi4:14b First-Pass Results — Adjacent-Scene Cases

Date: 2026-03-14
Model: phi4:14b
Case pack: continuity-progression-case-pack-v1
Cases: cp-001 through cp-012 (adjacent-scene subset)
Runs: run-2026-03-14-001 through run-2026-03-14-012

---

## Summary

phi4:14b completed all 12 adjacent-scene cases with zero schema failures. Schema reliability is clean. Behavioral reliability is not.

The model produced valid JSON envelopes on every run. It used the correct field names, approved finding_type values, and required evidence span structure throughout. The contract infrastructure holds under phi4:14b load.

The scoring picture is poor. The model failed 3 of 4 restraint traps (false positive rate: 75%) and missed 2 of 5 hard true-positive cases (false negative rate: 40% on the hard cases). It used `moderate` confidence on every single finding — no calibration whatsoever.

phi4:14b is **not suitable as a lane baseline** in its current form.

---

## Per-case results

| case_id | expected | findings | finding_type | conf | verdict |
|---------|----------|----------|--------------|------|---------|
| cp-001 | yes | 1 | continuity_tension | moderate | true positive |
| cp-002 | no (restraint) | 1 | transition_gap | moderate | false positive |
| cp-003 | yes | 1 | progression_break | moderate | true positive |
| cp-004 | no (restraint) | 1 | transition_gap | moderate | false positive |
| cp-005 | yes | 1 | repeated_movement | moderate | true positive |
| cp-006 | no (restraint) | 1 | state_carry_forward_issue | moderate | false positive |
| cp-007 | yes | 1 | descriptive_mismatch | moderate | true positive |
| cp-008 | partial | 1 | transition_gap | moderate | borderline |
| cp-009 | yes (hard) | 0 | — | — | false negative |
| cp-010 | yes | 1 | transition_gap | moderate | partial (correct flag, weak type) |
| cp-011 | no (restraint) | 0 | — | — | true negative |
| cp-012 | yes (hard) | 0 | — | — | false negative |

---

## Schema reliability

- Valid envelopes: 12 / 12
- Fail-closed envelopes: 0 / 12
- Hard schema failures (validator exit 2): 0

The contract path is confirmed end-to-end. Every run produced a parseable, valid-schema envelope.

---

## Confidence calibration

phi4:14b reported `moderate` on every finding across all 12 cases.

This is not calibration. The model is using a single default value regardless of evidence strength. A well-calibrated model should vary confidence based on:

- Directness of the contradiction (descriptive_mismatch cases warrant higher confidence than ambiguous transition_gap cases)
- Number and quality of evidence spans
- Whether the finding is within or across scene boundaries

Until phi4:14b demonstrates confidence variation, its confidence scores carry no information.

---

## Restraint performance

Restraint cases: cp-002, cp-004, cp-006, cp-011

| case_id | category | model behavior | verdict |
|---------|----------|---------------|---------|
| cp-002 | apparent_not_real | flagged transition_gap | false positive |
| cp-004 | acceptable_abrupt_transition | flagged transition_gap | false positive |
| cp-006 | repeated_movement_not_worth_flagging | flagged state_carry_forward_issue | false positive |
| cp-011 | apparent_not_real (v2) | no finding | true negative |

3/4 restraint failures. The one clean pass (cp-011) involved an unusually explicit narrative marker ("The district was already placed in both their minds and the map was reference, not proof") — the model was given the answer in the prose.

The dominant pattern: phi4:14b treats every scene transition as a `transition_gap` finding unless the prose explicitly resolves the gap within the text. It cannot infer acceptable compression from narrative context.

---

## Detection performance

True-positive cases: cp-001, cp-003, cp-005, cp-007, cp-008 (partial), cp-009, cp-010, cp-012

| case_id | expected | model behavior | verdict |
|---------|----------|---------------|---------|
| cp-001 | continuity_tension (injured hand) | flagged continuity_tension | true positive |
| cp-003 | progression_break (warden meeting) | flagged progression_break | true positive |
| cp-005 | repeated_movement (window-cross) | flagged repeated_movement | true positive |
| cp-007 | descriptive_mismatch (rain→dry) | flagged descriptive_mismatch | true positive |
| cp-008 | ambiguous edge | flagged transition_gap | borderline |
| cp-009 | emotional collapse→procedural (hard) | no finding | false negative |
| cp-010 | glance→certainty causal link | flagged transition_gap | partial |
| cp-012 | accord→disconnected referral (hard) | no finding | false negative |

4 clean true positives. The model correctly identified surface-readable contradictions: an injury not carried forward, a meeting not shown, a repeated physical action, a weather mismatch. These are all cases where the issue is visible in the literal text.

2 hard false negatives: cp-009 (emotional carry-forward) and cp-012 (action-step gap between private accord and procedural referral). Both require inferential reasoning about character state across scenes, not just text-surface comparison. phi4:14b does not reach this level of analysis.

cp-010 is a partial: the model flagged something but used the wrong type (`transition_gap` instead of `unclear_causal_link`). The finding is directionally correct but not precise.

---

## Evidence quality

Evidence spans were structurally present in all findings. Quality varied:

- **Strong:** cp-001 (exact quoted text for carry-forward), cp-007 (weather contradiction directly quoted)
- **Acceptable:** cp-003, cp-005 — spans present and relevant
- **Weak:** cp-002, cp-004, cp-006 — spans present but the finding itself is wrong, so evidence quality is moot
- **Missing:** cp-009, cp-012 — zero findings, no spans to evaluate

Uncertainty notes were consistently minimal. The model used phrasing like "this may represent a continuity issue" without distinguishing degrees of ambiguity. Review notes were present but generic.

---

## Failure mode taxonomy

### 1. Transition inflation (dominant)

phi4:14b treats scene transitions as inherently suspicious. Any gap in narrated action between scenes becomes a `transition_gap` finding unless the prose provides an explicit resolution within the text itself. The model cannot distinguish between acceptable compression (the reader infers what happened) and a real progression break.

This produced 3 false positives on the 4 restraint cases.

### 2. Interpretive state blindness

phi4:14b cannot track character state that requires cross-scene inference:
- cp-009: emotional collapse in scene A should make the mechanical procedural behavior in scene B a notable carry-forward issue. The model saw no problem.
- cp-012: explicit "shared accord on a necessary next step" in scene A should make the disconnected referral scene B a genuine gap. The model saw no problem.

Both cases require holding a model of character interiority and checking whether subsequent behavior is consistent with it. phi4:14b does not attempt this.

### 3. Zero confidence calibration

Every finding carries `moderate`. This is a non-signal. A model that gives the same confidence to a direct weather contradiction and an ambiguous emotional transition is not helping a reviewer prioritize review effort.

---

## Comparison to expected behavior

The case pack design intentionally probes three model properties:
1. Can it flag real issues? (detection)
2. Can it stay quiet on acceptable variation? (restraint)
3. Does it reach interpretive depth on hard cases? (analysis depth)

| property | expected | phi4:14b result |
|----------|----------|----------------|
| detection (surface) | high | high (4/5 surface cases correct) |
| detection (interpretive) | moderate | low (0/2 hard cases correct) |
| restraint | high | low (1/4 restraint cases correct) |
| confidence calibration | present | absent |
| evidence specificity | present | present but generic |

---

## Lane adoption assessment

phi4:14b is **not recommended as the first-pass lane baseline** for `continuity-progression-reasoning`.

Specific disqualifying signals:

1. **Restraint failure rate (75%)** — a model that flags 3/4 acceptable compressions would bury real findings in noise. The signal-to-noise ratio is too low for reviewer trust.

2. **Hard false negative rate (100% on interpretive cases)** — the cases that most need a reviewer's attention (cp-009, cp-012) are the ones phi4:14b silently passes. This is the worst failure mode: confident silence on genuine problems.

3. **No confidence calibration** — all findings carry identical confidence, making triage impossible.

The model can operate as schema-valid output source. It cannot operate as a reliable content analyst at the level this lane requires.

---

## What to run next

Continue the first-pass comparison with `qwen2.5:14b` against the same 12 frozen cases.

If qwen2.5:14b shows better restraint (flags fewer acceptable compressions) and better interpretive depth (catches cp-009 and/or cp-012), it becomes the first candidate for baseline consideration.

If qwen2.5:14b fails in the same patterns, the conclusion is that prompt revision is required before either model can serve as lane baseline — and the next step is prompt iteration, not model switching.

---

## Freeze note

This document covers phi4:14b results only.

The comparative first-pass synthesis (phi4:14b vs qwen2.5:14b) will be written as:

`docs/continuity-adjacent-scene-first-pass-results.md`

after the qwen2.5:14b pass is complete.
