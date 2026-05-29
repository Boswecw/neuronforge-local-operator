# Continuity Adjacent-Scene First-Pass Results

Date: 2026-03-14
Case pack: continuity-progression-case-pack-v1
Cases: cp-001 through cp-012 (adjacent-scene subset)
Challengers: phi4:14b, qwen2.5:14b

---

## Purpose

Synthesize the first governed challenger comparison for the `continuity-progression-reasoning` lane.

Both models ran against the identical 12 frozen adjacent-scene cases. This document covers per-case outcome comparison, schema reliability, restraint performance, detection performance, and the lane recommendation.

---

## Schema reliability

Both models produced valid-schema envelopes on all 12 runs.

| model | cases_run | valid_envelopes | fail_closed | hard_fail_count |
|-------|-----------|-----------------|-------------|----------------|
| phi4:14b | 12 | 12 | 0 | 0 |
| qwen2.5:14b | 12 | 12 | 0 | 0 |

The contract path is confirmed end-to-end for both models. Schema compliance is not a differentiator at this stage.

---

## Per-case outcome comparison

| case_id | category | finding_expected | phi4:14b | qwen2.5:14b |
|---------|----------|-----------------|----------|-------------|
| cp-001 | state_carry_forward | yes | 1 finding — true positive | 1 finding — true positive |
| cp-002 | apparent_not_real | no (restraint) | 1 finding — false positive | 1 finding — false positive |
| cp-003 | true_progression_break | yes | 1 finding — true positive | 1 finding — true positive |
| cp-004 | acceptable_abrupt_transition | no (restraint) | 1 finding — false positive | 0 findings — true negative |
| cp-005 | repeated_movement | yes | 1 finding — true positive | 0 findings — false negative |
| cp-006 | repeated_movement_not_worth_flagging | no (restraint) | 1 finding — false positive | 0 findings — true negative |
| cp-007 | descriptive_mismatch | yes | 1 finding — true positive | 1 finding — true positive |
| cp-008 | ambiguous_edge | partial | 1 finding — borderline | 0 findings — acceptable restraint |
| cp-009 | state_carry_forward (hard) | yes | 0 findings — false negative | 0 findings — false negative |
| cp-010 | unclear_causal_link | yes | 1 finding — partial (wrong type) | 0 findings — false negative |
| cp-011 | apparent_not_real (v2) | no (restraint) | 0 findings — true negative | 0 findings — true negative |
| cp-012 | true_progression_break (hard) | yes | 0 findings — false negative | 0 findings — false negative |

---

## Restraint performance

Restraint cases: cp-002, cp-004, cp-006, cp-011

| case_id | phi4:14b | qwen2.5:14b |
|---------|----------|-------------|
| cp-002 (apparent_not_real) | false positive | false positive |
| cp-004 (acceptable_abrupt_transition) | false positive | true negative |
| cp-006 (repeated_movement_not_worth_flagging) | false positive | true negative |
| cp-011 (apparent_not_real v2) | true negative | true negative |

| model | restraint cases passed | restraint failure rate |
|-------|----------------------|----------------------|
| phi4:14b | 1 / 4 | 75% |
| qwen2.5:14b | 3 / 4 | 25% |

qwen2.5:14b is significantly more restrained. phi4:14b flagged every acceptable compression it could reach.

The one shared restraint failure (cp-002) is notable: both models flagged movement from window to table as a continuity issue despite scene B explicitly narrating that movement. This is not a transition gap — it is a misread of the scene structure. It is a harder failure to fix because it is not transition inflation; it is a structural parsing error.

---

## Detection performance

True-positive cases: cp-001, cp-003, cp-005, cp-007, cp-009 (hard), cp-010, cp-012 (hard)

| case_id | phi4:14b | qwen2.5:14b |
|---------|----------|-------------|
| cp-001 (carry-forward) | true positive | true positive |
| cp-003 (progression_break) | true positive | true positive |
| cp-005 (repeated_movement) | true positive | false negative |
| cp-007 (descriptive_mismatch) | true positive | true positive (type imprecise) |
| cp-009 (emotional carry-forward — hard) | false negative | false negative |
| cp-010 (causal link) | partial (wrong type) | false negative |
| cp-012 (action-step gap — hard) | false negative | false negative |

| model | surface TP cases correct | hard TP cases correct |
|-------|-------------------------|-----------------------|
| phi4:14b | 4 / 5 (80%) | 0 / 2 (0%) |
| qwen2.5:14b | 3 / 5 (60%) | 0 / 2 (0%) |

phi4:14b is more sensitive at the surface level. qwen2.5:14b missed cp-005 (a repeated physical action that is unambiguously flaggable) and cp-010 (a causal link that phi4 at least partially detected).

Both models failed completely on the hard cases (cp-009 and cp-012). Neither model reached the level of character-state inference required to detect emotional carry-forward or action-step gap issues. This is a shared ceiling.

---

## Confidence calibration

Both models used `moderate` confidence on every finding.

This is not calibration. The models are using a single default value regardless of:
- Directness of the contradiction
- Number of evidence spans
- Ambiguity of the case

Until either model demonstrates confidence variation, confidence scores carry no reviewer-facing information.

---

## Finding type precision

| model | correct type | imprecise type | wrong type |
|-------|-------------|---------------|------------|
| phi4:14b | 4 correct | 0 | 1 (cp-010: transition_gap for causal_link case) |
| qwen2.5:14b | 3 correct | 1 (cp-007: state_carry_forward for descriptive_mismatch) | 0 |

Both models use the correct approved type vocabulary. Precision is moderate. phi4:14b made a worse type error (completely wrong category); qwen2.5:14b used a related but imprecise type.

---

## Aggregate scoring

| dimension | phi4:14b | qwen2.5:14b | edge |
|-----------|----------|-------------|------|
| Schema compliance | 12/12 | 12/12 | tie |
| Restraint (false positive rate) | 75% | 25% | qwen2.5 |
| Surface detection (true positive rate) | 80% | 60% | phi4 |
| Hard case detection | 0/2 | 0/2 | tie |
| Confidence calibration | absent | absent | tie |
| Total findings produced | 9 | 4 | — |
| False positive count | 3 | 1 | qwen2.5 |
| False negative count | 2 | 4 | phi4 |

---

## Shared failure modes

### 1. Hard case blindness

Neither model detected cp-009 (emotional collapse → procedural work) or cp-012 (private accord → disconnected referral). Both require holding a character-state model across scenes and checking whether subsequent behavior is consistent with it. Neither model attempts this level of analysis.

This is a capability ceiling, not a configuration issue. It may not be addressable by prompt revision alone at this model tier.

### 2. cp-002 structural misread

Both models flagged cp-002 despite scene B explicitly narrating the transition the models claimed was missing. This is a structural parsing error — the model is not reading scene B carefully before deciding there is a gap.

This is addressable by prompt revision. The prompt should require the model to confirm whether the claimed gap is narrated within the scenes before raising a finding.

### 3. Zero confidence calibration

Both models: `moderate` on everything. The prompt does not give the model guidance on how to calibrate confidence. This is a prompt gap, not a model capability gap.

---

## Divergent failure modes

### phi4:14b: transition inflation

phi4:14b treats scene transitions as inherently suspicious. Any gap in narrated action becomes a `transition_gap` unless prose resolves it explicitly. It cannot infer acceptable compression from narrative context. This produced 3 false positives on 4 restraint cases.

### qwen2.5:14b: over-suppression

qwen2.5:14b is more restrained but suppresses too aggressively on borderline cases. It missed cp-005 (repeated_movement — a surface-readable, unambiguous flag case) and cp-010 (causal link — where even phi4 produced a partial signal). It appears to default toward no-finding when evidence is ambiguous or the issue requires inference.

---

## Lane recommendation

Neither model is suitable as lane baseline without prompt revision.

However, the failure modes are not symmetric.

**qwen2.5:14b is the stronger starting point for prompt iteration.**

Reasons:
1. Its restraint rate is substantially better (25% vs 75% false positive rate). A model that over-suppresses is safer than one that floods with false positives — reviewer trust depends on precision, not recall.
2. Its false positives are fewer (1 vs 3) and one of them (cp-002) is a shared failure mode that affects phi4:14b equally.
3. It is less likely to condition reviewers to dismiss findings as noise.

phi4:14b's advantage (higher surface detection rate) does not compensate for the volume of noise it generates. A reviewer confronted with 9 findings across 12 cases, 3 of which are false positives, will calibrate trust downward across the board.

The next prompt iteration should target:
1. Structural parsing check before flagging: require the model to confirm the gap is not narrated within the provided scenes
2. Confidence calibration: give explicit guidance on when to use low/moderate/high
3. Compression tolerance: teach the model to distinguish acceptable narrative compression from genuine progression breaks
4. Hard case framing: describe character-state tracking as a required analysis step

After prompt revision, re-run both models against the same frozen case pack before any baseline adoption decision.

---

## What this first pass established

1. The contract infrastructure works. Zero schema failures across 24 runs, two models, 12 cases each.
2. The executor, validator, and renderer pipeline is confirmed end-to-end.
3. Both 14B-class models can produce schema-valid output reliably but cannot yet serve as trustworthy content analysts for this lane.
4. The case pack successfully discriminates between models: qwen2.5:14b and phi4:14b produced meaningfully different behavioral profiles.
5. Hard cases (cp-009, cp-012) represent a genuine capability ceiling for this model tier. These cases should be retained in the pack as a ceiling probe.

---

## Next steps

1. Prompt revision targeting the failure modes identified above
2. Re-run phi4:14b and qwen2.5:14b against frozen pack after revision
3. If either model reaches restraint rate below 25% false positive AND maintains surface detection above 60%, consider it for baseline candidacy
4. Do not promote either current model to lane baseline
5. Lane status remains: pre-baseline, contract confirmed, model under evaluation
