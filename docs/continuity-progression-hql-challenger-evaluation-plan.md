# High-Quality-Local Challenger Evaluation Plan — Continuity / Progression Reasoning

## Status
Draft v1.0

## Purpose
Define the first governed challenger-evaluation plan for the `continuity-progression-reasoning` lane.

This artifact assumes the lane identity, candidate-only posture, bounded-scope doctrine, schema direction, and review-grade trust posture are already stable.

This plan does **not** promote any model to baseline.

It defines:

- what should be tested first
- how local challengers should be compared
- what counts as acceptance vs rejection
- how drift and repeatability should be judged
- what evidence must exist before any baseline adoption decision

---

## 1. Lane under evaluation

- **lane id:** `continuity-progression-reasoning`
- **family:** `analysis`
- **role:** bounded cross-scene / scene-window reasoning
- **primary consumer:** Bloom
- **secondary consumer:** ANVIL
- **artifact posture:** candidate-only
- **required route class:** `HIGH_QUALITY_LOCAL`
- **minimum acceptable route:** `HIGH_QUALITY_LOCAL`
- **fallback:** fail closed

---

## 2. Evaluation objective

Identify which local reasoning-capable model is most trustworthy for producing:

- bounded candidate findings
- evidence-grounded reasoning
- scope-honest outputs
- restrained review aids
- valid structured outputs

The winning model is **not** the one that sounds smartest.

The winning model is the one that most reliably produces:

- review-usable findings
- low hallucination pressure
- strong scope discipline
- valid schema output
- candidate-framed language
- acceptable repeatability for governed use

---

## 3. Initial challenger posture

## 3.1 Baseline posture today

There is **no locked baseline model yet** for this lane.

That is intentional.

Proofreading-lane success with `qwen2.5:14b` does not automatically qualify it for this reasoning-sensitive lane.

## 3.2 First natural challengers

Recommended first-pass challenger pool:

1. **`phi4-reasoning:latest`**
   - first natural reasoning-heavy challenger
   - likely strong early candidate for bounded cross-scene reasoning

2. **`qwen2.5:14b`**
   - include as workhorse comparison point
   - not assumed to be good enough just because it performs well in proofreading lanes

3. **one additional local high-quality challenger if available**
   - only if it is runnable on the target laptop class without distorting the baseline hardware doctrine
   - should be reasoning-capable and structurally disciplined

## 3.3 Challenger count rule

For the first pass, prefer **2–3 challengers maximum**.

Do not widen into a large model bakeoff yet.

The current need is lane trust discovery, not broad benchmark theater.

---

## 4. Evaluation set posture

## 4.1 First-pass eval size

Target approximately **16 eval cases**.

## 4.2 Scope mix

Recommended distribution:

- **10–12 adjacent-scene** cases
- **4–6 scene-window** cases
- **0 chapter-window** cases in the first pass unless a case cannot be represented otherwise

## 4.3 Core category mix

The initial eval set should include at least these categories:

- true continuity tension
- apparent but not real continuity tension
- true progression break
- abrupt but acceptable transition
- repeated movement worth flagging
- repeated movement not worth flagging
- descriptive mismatch worth review
- ambiguous edge case
- state carry-forward issue
- unclear causal link

## 4.4 Eval-case metadata

Each case should record at minimum:

- case id
- scope label
- category
- source scenes or scene window
- expected review posture
- whether a meaningful finding is expected
- whether restraint is the correct behavior
- notes on why the case exists

---

## 5. Required output contract posture

All challengers must be judged against the same candidate schema and lane rubric.

At minimum, outputs must show:

- explicit bounded scope
- candidate framing
- finding labels from the approved taxonomy
- evidence references tied to actual text spans or scene references
- no canonicality leakage
- no unsupported certainty language

Malformed or weak structured output is a lane failure, not a style preference.

---

## 6. Review dimensions

Use the already-defined lane rubric as the scoring spine.

Primary review dimensions:

1. **usefulness**
2. **evidence quality**
3. **scope honesty**
4. **restraint**
5. **label quality**
6. **review usability**
7. **confidence calibration**
8. **schema reliability**
9. **canonicality control**
10. **drift resistance**

## 6.1 Heaviest dimensions for first-pass selection

Weight these most heavily:

- evidence quality
- scope honesty
- restraint
- schema reliability
- canonicality control
- drift resistance

Reason:

A flashy but unstable reviewer is more dangerous here than a slightly conservative one.

---

## 7. Hard-fail conditions

A run should be judged as hard fail if it does any of the following:

- asserts unsupported claims as fact
- invents events, transitions, or causal bridges
- omits material evidence while making a strong claim
- violates the declared scope boundary
- outputs malformed schema where structured output is required
- uses authority language instead of candidate language
- fabricates continuity violations from weak pattern resemblance alone
- inflates harmless repetition into review-hostile noise

A model with repeated hard fails should not be adopted even if some outputs are impressive.

---

## 8. Acceptance posture

## 8.1 Case-level acceptance

A single case is acceptable when the output is:

- structurally valid
- bounded to the declared scope
- candidate-framed
- evidence-grounded
- restrained enough for review use
- free of hard-fail behavior

## 8.2 Model-level acceptance

A challenger is acceptable for lane consideration only if it shows:

- strong schema reliability across the set
- low rate of hard-fail behavior
- consistent scope honesty
- acceptable restraint on no-issue and edge cases
- evidence quality high enough for review trust
- repeatability that stays within lane drift tolerance

## 8.3 Rejection posture

Reject or defer a challenger if it shows any of these patterns:

- repeated unsupported reasoning
- repeated over-flagging on acceptable transitions
- weak evidence anchoring
- frequent schema breakage
- unstable taxonomy usage
- confidence inflation
- large repeated-run behavioral drift on the same case

---

## 9. Repeatability and drift judgment

## 9.1 Core principle

This lane does **not** require exact wording determinism.

It does require **review-grade behavioral stability**.

## 9.2 What should remain stable across repeated runs

Across repeated runs of the same case, the model should remain reasonably stable in:

- whether it flags a finding at all
- the category/label family of the finding
- the bounded scope used
- the main evidence basis
- the overall severity/review posture

## 9.3 What may vary without immediate rejection

Acceptable minor drift may include:

- wording differences
- minor phrasing of candidate language
- small confidence variation
- slightly different evidence span choices when equally valid

## 9.4 Drift rejection conditions

Repeatability should be judged weak if repeated runs swing materially between:

- issue vs no issue
- continuity vs progression taxonomy without textual basis
- cautious candidate language vs confident authority claims
- grounded evidence vs speculative bridging
- valid structured output vs malformed output

## 9.5 Suggested repeat-run posture

For first-pass challenger evaluation:

- run each anchor case once for all challengers
- choose **4–6 representative cases** for repeat-run checks
- run those repeatability cases at least **3 times per challenger**

That is enough to detect dangerous instability without overbuilding the first pass.

---

## 10. Comparison workflow

## 10.1 Per-case comparison

For each eval case:

1. run each challenger under the same task contract
2. review structured output validity first
3. review hard-fail conditions second
4. review evidence quality and restraint third
5. record comparative notes

## 10.2 Cross-model judgment

At the model level, compare:

- hard-fail count
- schema failure count
- false-positive tendency
- false-negative tendency
- evidence usefulness
- candidate-language discipline
- repeatability behavior

## 10.3 Winner selection rule

Prefer the challenger that is most trustworthy under governance, not the one that produces the most findings.

Conservative, review-usable, evidence-anchored performance beats aggressive pseudo-insight.

---

## 11. Recommended evidence bundle for adoption consideration

Before any baseline decision, the lane should have:

- a defined eval set
- saved outputs for all challengers
- per-case review notes
- repeat-run notes on selected anchor cases
- a challenger summary table
- a lane status document
- an adoption recommendation note

No baseline should be declared from vibe alone.

---

## 12. First-pass success criteria

The first challenger pass is successful if it answers these questions clearly:

1. Is `phi4-reasoning:latest` materially better than `qwen2.5:14b` for this lane?
2. Does any challenger produce review-grade candidate outputs with acceptable restraint?
3. Are schema reliability and scope honesty strong enough to move into lane anchoring?
4. Is repeated-run drift small enough for governed use?
5. Do current labels and schema hold up under real case pressure?

If the answer to those questions is still unclear, the correct result is:

- no baseline yet
- refine evals
- refine prompt/profile
- continue governed testing

That is a valid outcome.

---

## 13. Immediate next artifacts after this plan

Recommended next order:

1. **Continuity / Progression Eval Set Assembly v1**
2. **Continuity / Progression Candidate Schema v1** if not already pocketed in durable form
3. **Continuity / Progression Review Worksheet v1**
4. **First Challenger Run Sheet** for the selected local models

---

## 14. Current recommendation

Proceed with a first-pass local challenger comparison using:

- `phi4-reasoning:latest`
- `qwen2.5:14b`
- optional third challenger only if it fits the laptop-doctrine budget cleanly

Do **not** assign a baseline yet.

The lane is ready for governed challenger evaluation, not baseline declaration.

