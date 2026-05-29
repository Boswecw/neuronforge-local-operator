# Continuity / Progression First Challenger Run Sheet

## Status
Draft v1.0

## Purpose
Provide the operational run sheet for the first governed challenger comparison in the `continuity-progression-reasoning` lane.

This artifact bridges planning into execution.

It defines:

- which challengers are in scope for the first pass
- what must be frozen before runs begin
- the required run order
- what must be recorded for each run
- how repeatability checks should be scheduled
- what evidence package should exist when the pass is complete

This is an execution control surface, not a lane-policy document.

---

## 1. Lane and pass identity

- **lane id:** `continuity-progression-reasoning`
- **pass id:** `first-local-challenger-pass-v1`
- **family:** `analysis`
- **trust posture:** candidate-only
- **required route class:** `HIGH_QUALITY_LOCAL`
- **fallback:** fail closed

---

## 2. First-pass challengers

## Locked initial pool

1. **`phi4-reasoning:latest`**
2. **`qwen2.5:14b`**

## Optional third challenger

A third challenger may be included only if all of the following are true:

- it is genuinely runnable within the target laptop-doctrine hardware budget
- it is reasoning-capable enough to justify comparison
- adding it does not slow the first pass into benchmark sprawl
- the case pack can still be reviewed manually with discipline

If no such challenger is clearly available, do not add one yet.

---

## 3. Frozen prerequisites before execution

Do not begin the comparative pass until the following are frozen.

### 3.1 Required frozen artifacts

- eval-set assembly plan approved for v1 use
- actual v1 case pack assembled
- candidate schema version selected
- review worksheet version selected
- task contract wording selected for the lane
- route class fixed to `HIGH_QUALITY_LOCAL`

### 3.2 Freeze rule

Once the first comparative pass begins:

- do not rewrite the case pack casually
- do not swap schema versions mid-pass
- do not materially change prompt/profile wording mid-pass
- do not change scoring criteria mid-pass

Only invalidate and rerun if something is clearly broken.

---

## 4. Run inputs to lock

For each challenger, lock the following before the first run:

- **model name**
- **model tag/version if available**
- **prompt/profile id**
- **candidate schema version**
- **task contract text**
- **route class**
- **temperature or equivalent stability controls** if exposed
- **output directory convention**
- **run id convention**

This prevents post hoc ambiguity during review.

---

## 5. Recommended run order

## Phase 1 — full single-pass comparison

Run every frozen eval case once for each challenger.

Recommended order:

1. run all cases for `phi4-reasoning:latest`
2. run all cases for `qwen2.5:14b`
3. run optional third challenger only if approved before pass start

Alternative ordering is acceptable if operationally easier, but keep it consistent and recorded.

## Phase 2 — repeatability subset

After the single-pass comparison, choose the frozen repeatability subset and run repeat checks.

Recommended repeatability subset size:

- **4–6 cases**

Recommended repeat-run count per model per selected case:

- **3 total runs per case/model**

That means if one initial run already exists, add **2 more runs** for each repeatability case per challenger.

---

## 6. Recommended repeatability subset composition

The repeatability subset should include a mix of:

1. one strong true-issue case
2. one false-positive resistance case
3. one ambiguous edge case
4. one scene-window case
5. optional additional high-risk instability case
6. optional additional taxonomy-sensitive case

Reason:

Drift matters most where governance pressure is highest, not only on easy cases.

---

## 7. Per-run record requirements

For every executed run, record at minimum:

- **run id**
- **date**
- **challenger model**
- **prompt/profile id**
- **case id**
- **scope label expected**
- **route class used**
- **output file path**
- **schema version expected**
- **schema pass/fail at review time**
- **hard-fail presence at review time**
- **worksheet path or review reference**

This should be enough to reconstruct the pass without memory.

---

## 8. Proposed run matrix

Assuming **16 cases** and **2 challengers**:

### Base comparison

- 16 cases × 2 challengers = **32 runs**

### Repeatability layer

If **5 repeatability cases** are selected and each needs **2 additional runs** per challenger:

- 5 cases × 2 extra runs × 2 challengers = **20 additional runs**

### Total expected first-pass run count

- **52 runs** for a 2-challenger pass with a 5-case repeatability subset

This is substantial but still manageable if review discipline is maintained.

---

## 9. Run naming posture

Each run should be identifiable without ambiguity.

Recommended naming elements:

- lane id
- case id
n- model name
- pass id
- run sequence number

Example shape:

`run-YYYY-MM-DD-<seq>-continuity-progression-<case-id>-<model>`

The exact format can follow existing NeuronForge run conventions if those already exist and remain unambiguous.

---

## 10. Output storage posture

Store outputs so comparison is easy and future audit is simple.

Recommended minimum organization:

- outputs grouped by lane
- clearly labeled by challenger model
- filenames including case id
- repeatability runs clearly distinguished from first-pass runs

Avoid burying outputs in mixed directories where comparative review becomes manual archaeology.

---

## 11. Review sequencing

Recommended review sequence after generation:

1. validate schema first
2. check hard-fail conditions second
3. complete review worksheet for each run
4. compare challengers case-by-case
5. complete repeatability review notes
6. write model-level summary

Do not jump straight to “which model feels best.”

---

## 12. Case-by-case comparison table shape

When the pass is complete, each case should have a compact comparative record.

Suggested fields:

- **case id**
- **case category**
- **expected posture**
- **best challenger**
- **safest challenger**
- **overreach note**
- **schema issues observed**
- **hard-fail issues observed**
- **reviewer winner note**

This table becomes the backbone of the final adoption recommendation.

---

## 13. Model-level summary table shape

At pass completion, create a model-level summary using fields like:

- **challenger model**
- **cases reviewed**
- **schema hard fails**
- **schema soft issues**
- **hard-fail behavior count**
- **average evidence quality judgment**
- **average restraint judgment**
- **average scope honesty judgment**
- **average canonicality control judgment**
- **repeatability confidence**
- **adoption posture**

This does not replace detailed notes, but it makes the decision legible.

---

## 14. Adoption posture labels

For the first pass, recommended model-level outcome labels are:

- `candidate_for_baseline_consideration`
- `promising_but_not_ready`
- `needs_prompt_or_schema_revision`
- `not_suitable_for_lane`

These labels are better than vague “good/bad” conclusions.

---

## 15. Pass-complete evidence bundle

When the first challenger pass is complete, the evidence bundle should include:

- frozen v1 case pack
- frozen schema version
- frozen task contract/prompt profile version
- all challenger outputs
- completed review worksheets
- repeatability notes
- case-by-case comparison table
- model-level summary table
- lane status update
- adoption recommendation note

No model should be proposed for baseline status without this bundle.

---

## 16. Abort and rerun conditions

Abort or partially rerun only if one of these occurs:

- schema contract was wrong or incomplete
- task contract materially changed mid-pass
- outputs were saved incorrectly or not traceably
- case packet was invalid or mis-scoped
- route class was not actually `HIGH_QUALITY_LOCAL`
- a challenger configuration was inconsistent across runs

Do not rerun simply because one model produced disappointing results.

---

## 17. Immediate operational next step

Before any runs are executed, create the actual frozen **v1 case pack** for the 16 target cases.

That pack should be the last missing execution prerequisite.

---

## 18. Current recommendation

Proceed with a **2-challenger first pass** using:

- `phi4-reasoning:latest`
- `qwen2.5:14b`

Keep the first pass narrow, disciplined, and reviewable.

The goal is not benchmark spectacle.

The goal is to determine whether any local challenger is trustworthy enough for bounded continuity/progression candidate review.

