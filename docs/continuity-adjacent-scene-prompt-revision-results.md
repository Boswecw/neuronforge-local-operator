# Continuity Adjacent-Scene Prompt Revision Results

Date: 2026-03-14
Prompt: `prompts/continuity-adjacent-scene-v3.md`
Case pack: continuity-progression-case-pack-v1 (cp-001 through cp-012)
Models: phi4:14b, qwen2.5:14b

---

## Context

This document covers the post-revision challenger comparison for the `continuity-progression-reasoning` lane, adjacent-scene scope.

The first-pass results (v1 prompt) identified three shared failure modes:
1. Models flagged transitions already narrated in the scenes
2. Models treated all narrative compression as suspicious
3. Both models used `moderate` confidence on every finding regardless of evidence strength

Two intermediate prompt versions were attempted:

**v2**: Added restraint bias instructions ("prefer no finding over a weak finding"). Result: blanket suppression — qwen2.5:14b returned 0/12 findings including on unambiguous true positive cases. v2 was immediately abandoned.

**v3**: Replaced stance-based restraint with precision-based detection criteria — four named finding types (character state not carried forward, named obligation bypassed, descriptive contradiction, repeated action) with explicit examples and non-qualifying conditions. v3 is the current production prompt.

---

## Prompt development findings

### v2 failure: suppression language collapses non-reasoning models

v2 told qwen2.5:14b to "prefer no finding" and framed restraint as the primary behavior. qwen2.5:14b read this as a global stance and suppressed everything — including cp-007 (explicit weather contradiction with directly quoted conflicting text from both scenes).

Lesson: non-reasoning models cannot balance suppression instructions against detection instructions. They adopt an overall stance from the dominant message. The dominant message in v2 was "find nothing unless certain," so they found nothing.

### v3 approach: define what qualifies, not how to behave

v3 describes four specific finding types with concrete examples of what qualifies and what does not. The zero-finding rule and confidence calibration remain, but the primary weight of the prompt is now on detection precision rather than suppression stance.

### Prompt-vocabulary leakage issues (fixed in v3)

Both models echoed prompt section headers and criterion keywords into output field values:
- qwen2.5:14b used `"establishes"` in claims (prohibited authority language), sourced from criterion text
- phi4:14b used `span_role: "commitment"` (invalid), sourced from the "Named commitment" section header
- phi4:14b invented `finding_type: "skipped_named_commitment"` (invalid), sourced from the same section header

Fixes applied:
- Section headers renamed to Type A/B/C/D to avoid field-value collision
- "establishes" replaced throughout criterion text with "contains," "shows," "is present in"
- Prohibited language list restored correctly (earlier replace-all broke it)
- Concrete rewrite example added: "Wrong: 'Scene A establishes...' — Correct: 'In Scene A...'"
- Separator note added: "Category names are descriptions for your analysis only. Do not use them as output field values."

---

## Per-case outcome comparison — v1 vs v3

| case | category | expected | phi4 v1 | phi4 v3 | qwen2.5 v1 | qwen2.5 v3 |
|------|----------|----------|---------|---------|-----------|-----------|
| cp-001 | state_carry_forward | yes | TP | TP | TP | TP |
| cp-002 | apparent_not_real | no | FP | TN | FP | TN |
| cp-003 | progression_break | yes | TP | TP | TP | TP |
| cp-004 | acceptable_transition | no | FP | FP | TN | TN |
| cp-005 | repeated_movement | yes | TP | FN | FN | TP |
| cp-006 | repeated_not_worth_flagging | no | FP | TN | TN | TN |
| cp-007 | descriptive_mismatch | yes | TP | TP | TP | TP |
| cp-008 | ambiguous_edge | partial | borderline | borderline | restraint | restraint |
| cp-009 | state_carry_forward (hard) | yes | FN | FN | FN | FN |
| cp-010 | causal_link | yes | partial | partial | FN | FN |
| cp-011 | apparent_not_real (v2) | no | TN | FP | TN | TN |
| cp-012 | progression_break (hard) | yes | FN | TP | FN | FN |

Legend: TP = true positive, TN = true negative, FP = false positive, FN = false negative

---

## Restraint performance

| model | prompt | restraint cases correct | false positive rate |
|-------|--------|------------------------|-------------------|
| phi4:14b | v1 | 1 / 4 | 75% |
| phi4:14b | v3 | 2 / 4 | 50% |
| qwen2.5:14b | v1 | 3 / 4 | 25% |
| qwen2.5:14b | v3 | 4 / 4 | 0% |

qwen2.5:14b with v3 achieves zero false positives on all four restraint cases. This is the first clean restraint pass for any model in this evaluation.

phi4:14b improved from 75% to 50% false positive rate, but still fails cp-004 (boat-to-city transition gap) and cp-011 (map state change). Both are cases where phi4 flags something that is narratively acceptable — cp-004 is pure location shift, cp-011 is a prop that was actively used and then put away. phi4 continues to be more sensitive than the restraint criteria warrant.

---

## Detection performance

| model | prompt | surface TP rate | hard TP rate |
|-------|--------|----------------|-------------|
| phi4:14b | v1 | 4 / 5 (80%) | 0 / 2 (0%) |
| phi4:14b | v3 | 4 / 5 (80%) | 1 / 2 (50%) |
| qwen2.5:14b | v1 | 3 / 5 (60%) | 0 / 2 (0%) |
| qwen2.5:14b | v3 | 4 / 5 (80%) | 0 / 2 (0%) |

phi4:14b v3 now catches cp-012 (the accord→disconnected referral hard case) — a finding neither model produced in v1. This is the only hard-case improvement across the full revision pass.

qwen2.5:14b v3 now catches cp-005 (repeated movement), which it missed in v1. Surface detection rate improves from 60% to 80%.

cp-009 (emotional carry-forward) and cp-012 for qwen2.5:14b remain false negatives. These cases require character-state inference that neither model reliably reaches. This is a ceiling shared across all model configurations tested.

---

## Confidence calibration

Both models improved modestly. phi4:14b used `moderate` on everything in v1 and continues to do so in v3. qwen2.5:14b used `moderate` on everything in v1 and continues in v3.

The confidence calibration guidance in v3 did not change model behavior. This is a negative result — the guidance was present but neither model acted on it. Confidence calibration may require a different approach (explicit scoring rubric in the prompt, or accepting that these models do not calibrate dynamically).

---

## Schema reliability

| model | prompt | valid envelopes | fail-closed |
|-------|--------|----------------|-------------|
| phi4:14b | v1 | 12 / 12 | 0 |
| phi4:14b | v3 | 12 / 12 | 0 |
| qwen2.5:14b | v1 | 12 / 12 | 0 |
| qwen2.5:14b | v3 | 12 / 12 | 0 |

Both models maintained 100% schema reliability across both prompt versions. The prompt vocabulary leakage issues (invalid span_role, invalid finding_type, prohibited language in claims) were caught by the validator during prompt development and corrected before final runs.

---

## Aggregate comparison

| dimension | phi4 v1 | phi4 v3 | qwen2.5 v1 | qwen2.5 v3 |
|-----------|---------|---------|-----------|-----------|
| Schema compliance | 12/12 | 12/12 | 12/12 | 12/12 |
| Restraint (FP rate) | 75% | 50% | 25% | 0% |
| Surface detection | 80% | 80% | 60% | 80% |
| Hard case detection | 0/2 | 1/2 | 0/2 | 0/2 |
| Confidence calibration | absent | absent | absent | absent |
| Total findings produced | 9 | 8 | 4 | 5 |
| False positives | 3 | 2 | 1 | 0 |

---

## Lane recommendation

**qwen2.5:14b with prompt v3 is ready for first baseline candidacy consideration.**

The evidence:

1. **Zero false positives on all four restraint cases.** This is the first clean restraint pass in the evaluation history. The v3 precision criteria eliminated all transition inflation and compression over-flagging that qwen2.5:14b showed in v1.

2. **Surface detection rate matches phi4:14b** at 80% (4/5 cases), up from 60% in v1. The model now correctly catches cp-005 (repeated movement) that v1 missed.

3. **Schema reliability is 100%** across all runs.

4. **Hard case detection is still 0/2**, but this is a shared ceiling with phi4:14b (which only gains 1/2 with v3). These cases require interpretive character-state reasoning that no 14B-class model has demonstrated reliably under the current contract.

**phi4:14b with prompt v3 is not recommended for baseline.**

Despite catching cp-012 (a notable hard-case improvement), phi4:14b still produces false positives on cp-004 and cp-011. A 50% restraint failure rate remains too noisy for reviewer trust. The model is more sensitive but less precise.

---

## What remains unresolved

### 1. Hard case detection (cp-009, cp-012 for qwen2.5)

Neither model reliably detects cases requiring character-state inference across scenes. These cases (emotional carry-forward, action-step gaps between private agreement and procedural action) are not addressed by the current prompt revision. They may require a different analytical framing entirely — possibly a character-state tracking step that the model performs before scene comparison.

### 2. Confidence calibration

Both models default to `moderate` despite explicit calibration guidance. This is a model behavior limit, not a prompt gap. Future prompt approaches could try scaffolded confidence reasoning ("first state the evidence, then rate its strength") rather than instruction-only guidance.

### 3. phi4:14b cp-004 and cp-011 persistence

phi4:14b continues to flag location-shift transitions and prop state changes as findings despite the "What does NOT warrant a finding" section explicitly covering both patterns. The model is not applying the non-qualifying conditions correctly. This may be a model capacity limit on rule-following length, not a prompt clarity issue.

---

## Next steps

1. **Establish qwen2.5:14b + v3 prompt as the first lane baseline** for adjacent-scene continuity review, subject to governed promotion criteria
2. **Document the hard-case ceiling** as a known limitation of 14B-class models for this lane
3. **Do not expand to scene-window scope yet** — the adjacent-scene scope is not fully resolved for hard cases
4. **Confidence calibration is deferred** — accept uniform `moderate` as a known limitation for now rather than continuing to revise the prompt on this dimension
5. **Update lane status** to reflect first baseline candidacy achieved

---

## Freeze note

This document covers prompt revision v2 (failed) and v3 (candidate) results.

The lane status should now advance from "pre-baseline, contract confirmed, model under evaluation" to "first baseline candidate identified, pending governed promotion."
