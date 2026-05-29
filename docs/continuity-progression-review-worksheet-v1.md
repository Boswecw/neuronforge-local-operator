# Continuity / Progression Review Worksheet v1

## Status
Draft v1.0

## Purpose
Provide a governed reviewer worksheet for scoring challenger outputs in the `continuity-progression-reasoning` lane.

This worksheet is meant to be used **per challenger run, per eval case**.

It is designed to support:

- consistent manual review
- hard-fail detection
- comparable challenger judgments
- repeatability notes
- adoption-readiness evidence collection

This is a review instrument, not a runtime artifact.

---

## 1. Lane under review

- **lane id:** `continuity-progression-reasoning`
- **family:** `analysis`
- **artifact posture:** candidate-only
- **required route:** `HIGH_QUALITY_LOCAL`
- **trust posture:** review-grade candidate output only

---

## 2. Worksheet use rule

Complete one worksheet for each:

- challenger model
- prompt/profile version
- eval case
- run instance

If repeatability is being checked, each repeat run gets its own worksheet entry.

---

## 3. Run metadata block

Record the following before qualitative review begins.

- **case id**
- **run id**
- **date**
- **challenger model**
- **prompt/profile id**
- **scope label declared by task**
- **scope label declared by model output**
- **route class**
- **output path**
- **schema version expected**
- **schema version produced**

---

## 4. Case posture reference block

Copy or reference the expected eval-case posture so the run is judged against the right standard.

- **primary category**
- **secondary category**
- **expected review posture**
- **expected restraint posture**
- **finding expected?**
- **no-finding acceptable?**
- **reviewer notes for case**

---

## 5. First gate — schema validity

This gate is checked before quality scoring.

### 5.1 Schema pass/fail

Record:

- **schema valid:** yes / no
- **top-level structure valid:** yes / no
- **required fields present:** yes / no
- **enum values valid:** yes / no
- **finding objects valid:** yes / no
- **evidence objects valid:** yes / no
- **candidate-language requirement met:** yes / no

### 5.2 Schema notes

Record any issues such as:

- malformed top-level object
- missing required finding fields
- invalid enum labels
- missing evidence basis
- authority language in prohibited fields
- broken or ambiguous confidence representation

### 5.3 Schema gate result

Choose one:

- `pass`
- `soft_issue`
- `hard_fail`

#### Guidance

- **pass** = structure is usable and compliant
- **soft_issue** = minor schema problems but still reviewable
- **hard_fail** = structure is not trustworthy enough for lane use

---

## 6. Second gate — hard-fail behavior

Check all that apply.

### 6.1 Hard-fail checklist

- unsupported claim presented as fact
- invented event or action
- invented transition or causal bridge
- scope violation
- authority-language leakage
- material evidence omission paired with strong claim
- fabricated continuity violation from weak resemblance
- inflated harmless repetition into strong issue claim
- malformed structured output severe enough to break review use

### 6.2 Hard-fail result

Choose one:

- `none`
- `present_single`
- `present_multiple`

### 6.3 Hard-fail notes

Record the specific finding or line of behavior that triggered the judgment.

---

## 7. Quality scoring dimensions

Use the following dimensions for manual scoring.

Suggested scale for each:

- **0 = unacceptable**
- **1 = weak**
- **2 = mixed / borderline**
- **3 = solid**
- **4 = strong**

---

## 8. Dimension A — usefulness

### Question
Does this output actually help a reviewer inspect the case?

### Score
0 / 1 / 2 / 3 / 4

### Notes
Record whether the output is practically useful, noisy, vague, or insightfully bounded.

---

## 9. Dimension B — evidence quality

### Question
Are the findings anchored to real nearby textual evidence in a review-usable way?

### Score
0 / 1 / 2 / 3 / 4

### Notes
Record whether evidence is:

- explicit
- weakly implied
- incomplete
- selective
- well matched to the claim

---

## 10. Dimension C — scope honesty

### Question
Does the output stay within the declared scope and avoid broader story claims?

### Score
0 / 1 / 2 / 3 / 4

### Notes
Record whether the model remained bounded or drifted into wider unsupported claims.

---

## 11. Dimension D — restraint

### Question
Did the model show the right level of caution for this case?

### Score
0 / 1 / 2 / 3 / 4

### Notes
Record whether it:

- over-flagged
- under-flagged
- escalated too aggressively
- stayed appropriately candidate-framed

---

## 12. Dimension E — label quality

### Question
Are the chosen finding labels/taxonomy categories appropriate and stable?

### Score
0 / 1 / 2 / 3 / 4

### Notes
Record whether the labels fit the case cleanly or show taxonomy drift.

---

## 13. Dimension F — review usability

### Question
Would a human reviewer find this easy to act on without being misled?

### Score
0 / 1 / 2 / 3 / 4

### Notes
Record whether the output is:

- clear
- overloaded
- too vague
- well prioritized
- easy to inspect

---

## 14. Dimension G — confidence calibration

### Question
Does the confidence posture match the evidence strength and ambiguity of the case?

### Score
0 / 1 / 2 / 3 / 4

### Notes
Record whether confidence is inflated, timid, reasonable, or unstable.

---

## 15. Dimension H — canonicality control

### Question
Does the output remain clearly candidate-only rather than implying story truth?

### Score
0 / 1 / 2 / 3 / 4

### Notes
Record any candidate-language strength or leakage into declarative authority tone.

---

## 16. Dimension I — drift resistance

### Question
For repeat-run cases, does this output remain behaviorally stable enough for governed use?

### Score
0 / 1 / 2 / 3 / 4

### Notes
If this is not a repeat-run check, record `not applicable`.

For repeat-run checks, compare against prior runs on:

- issue vs no-issue stability
- category stability
- scope stability
- evidence-basis stability
- confidence stability

---

## 17. Reviewer summary block

After dimension scoring, record the run-level judgment.

### 17.1 Overall reviewer judgment

Choose one:

- `strong_accept_for_case`
- `acceptable_for_case`
- `borderline`
- `reject_for_case`
- `hard_fail`

### 17.2 Why this judgment

Write 2–6 sentences covering:

- what the model got right
- what it got wrong
- whether the case posture was handled properly
- whether the output would be safe to show a reviewer as a candidate artifact

---

## 18. Expected-posture alignment check

Record the alignment between actual output and case expectations.

- **matched expected review posture:** yes / no / partial
- **matched expected restraint posture:** yes / no / partial
- **finding behavior aligned with case design:** yes / no / partial

### Notes
Explain any mismatch between expected posture and actual model behavior.

---

## 19. Per-case comparison notes

When multiple challengers are reviewed on the same case, add a concise comparison note:

- which challenger was best on this case
- which one was safest
- which one overreached most
- which one had the best evidence discipline

This block is optional per single worksheet, but should be captured somewhere during comparative review.

---

## 20. Repeatability note block

Use this when the case is one of the selected repeat-run anchors.

Record:

- **repeat-run anchor case:** yes / no
- **run number for this case/model:**
- **prior comparable runs reviewed:**
- **material drift observed:** yes / no
- **drift type:**
  - issue/no-issue swing
  - category swing
  - scope swing
  - evidence swing
  - confidence swing
  - schema swing

### Notes
Describe whether the drift is minor wording variation or governance-relevant instability.

---

## 21. Adoption signal block

At the end of each worksheet, record whether this run contributes positively to challenger adoption confidence.

Choose one:

- `positive_signal`
- `mixed_signal`
- `negative_signal`
- `disqualifying_signal`

### Guidance

- **positive_signal** = supports lane suitability
- **mixed_signal** = usable but not yet trustworthy enough
- **negative_signal** = notable weakness for lane use
- **disqualifying_signal** = should weigh heavily against adoption

---

## 22. Lightweight worksheet template

Use this template for each reviewed run.

```md
# Review Worksheet

## Run metadata
- case id:
- run id:
- date:
- challenger model:
- prompt/profile id:
- scope label declared by task:
- scope label declared by output:
- route class:
- output path:
- schema version expected:
- schema version produced:

## Case posture reference
- primary category:
- secondary category:
- expected review posture:
- expected restraint posture:
- finding expected?:
- no-finding acceptable?:
- reviewer notes for case:

## Schema validity
- schema valid:
- top-level structure valid:
- required fields present:
- enum values valid:
- finding objects valid:
- evidence objects valid:
- candidate-language requirement met:
- schema gate result:
- schema notes:

## Hard-fail behavior
- hard-fail checklist items triggered:
- hard-fail result:
- hard-fail notes:

## Dimension scores
- usefulness:
- evidence quality:
- scope honesty:
- restraint:
- label quality:
- review usability:
- confidence calibration:
- canonicality control:
- drift resistance:

## Dimension notes
- usefulness notes:
- evidence quality notes:
- scope honesty notes:
- restraint notes:
- label quality notes:
- review usability notes:
- confidence calibration notes:
- canonicality control notes:
- drift resistance notes:

## Reviewer summary
- overall reviewer judgment:
- why this judgment:

## Expected-posture alignment
- matched expected review posture:
- matched expected restraint posture:
- finding behavior aligned with case design:
- alignment notes:

## Repeatability
- repeat-run anchor case:
- run number for this case/model:
- prior comparable runs reviewed:
- material drift observed:
- drift type:
- repeatability notes:

## Adoption signal
- adoption signal:
- adoption notes:
```

---

## 23. Current recommendation

Use this worksheet as the review spine for the first challenger pass.

Do not compress judgment to a single score only.

The lane’s trust decision depends on:

- hard-fail behavior
- evidence discipline
- scope honesty
- restraint
- schema reliability
- repeatability

This worksheet exists to keep those dimensions visible.

