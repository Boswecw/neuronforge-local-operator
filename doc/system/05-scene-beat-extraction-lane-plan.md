# Scene-Aware Beat Candidate Extraction Lane Plan

## Status
Draft v1.0

## Purpose
Define the first concrete NeuronForge Local reasoning lane for **scene-aware beat candidate extraction**.

This lane is the first major execution bridge from:

**manuscript scenes → candidate beats → review → ANVIL**

It operationalizes the current NeuronForge control surface by defining a bounded extraction lane with explicit inputs, outputs, failure rules, evaluation posture, and adoption gates.

This is a lane/governance artifact, not an implementation spec.

---

## 1. Why this lane exists

The current NeuronForge stack already establishes:

- a local runtime substrate
- task contracts
- routing/model profiles
- candidate artifact doctrine
- ANVIL/Bloom reasoning consumption rules

The first concrete lane should therefore be the one that most directly exercises all of that structure.

That lane is **scene-aware beat candidate extraction** because it:

- directly supports AuthorForge and ANVIL
- forces candidate-not-authority discipline
- requires structured extraction rather than prose-only assistance
- creates a real need for high-quality local reasoning
- remains bounded enough for lane-style evaluation and governance

---

## 2. Lane identity

- **lane id:** `scene-aware-beat-candidate-extraction`
- **lane type:** extraction
- **primary consumer:** ANVIL
- **secondary consumer:** Bloom review surfaces
- **default contract family:** extraction
- **default contract:** `extract.beat_candidates.scene.v1`

### 2.1 Working definition

This lane proposes candidate story beats inferred from bounded scene text and supporting scene/window context.

Its output is:

- structured
- evidence-bearing
- confidence-bearing
- reviewable
- non-authoritative by default

### 2.2 What this lane is not

It is not:

- authoritative beat creation
- full arc inference
- cross-book structural theory generation
- unrestricted literary interpretation
- a substitute for deterministic scene parsing or persistence

---

## 3. Lane goal

The lane should answer a narrow question well:

**Given a bounded scene and allowed supporting context, what plausible candidate beat(s) can be proposed for review, with evidence and confidence, without overstating certainty or silently becoming authority?**

This is the real target.

Not perfect literary omniscience.

Not automatic plot truth.

Useful, bounded, reviewable candidate structure.

---

## 4. Input scope doctrine

### 4.1 Primary scope

The default lane input is a **single scene**.

Required source inputs:

- scene text
- scene id
- chapter id or equivalent local container

### 4.2 Allowed supporting context

Allowed additional context may include:

- immediate prior scene summary or text window
- immediate next scene summary or text window when available
- scene metadata already known deterministically
- confirmed existing beats in nearby scope, if separately authorized by contract

### 4.3 Scope rule

The lane is **scene-aware**, not chapter-global by default.

It may use local supporting context to avoid shallow misreads, but the candidate must still identify its true source scope.

### 4.4 Forbidden scope behavior

Do not:

- imply whole-chapter certainty from one scene
- pretend a scene-window inference is scene-local if it is not
- rely on hidden global context not present in the request contract
- invent continuity support that is not in supplied context

---

## 5. Output doctrine

### 5.1 Output class

This lane produces **candidate beat artifacts**.

These are governed by the Candidate Artifact Doctrine and must remain candidate-only until promoted.

### 5.2 Minimum beat candidate output shape

Each candidate beat should include, at minimum:

- `candidate_id`
- `artifact_class = candidate_beat`
- `scene_id`
- `source_scope`
- `candidate_payload`
- `evidence_spans`
- `confidence_class`
- `review_state = pending_review`
- `route_class_actual`
- `model_id`
- `contract_id`
- `contract_version`
- `provenance_class = inferred_candidate`

### 5.3 Candidate payload expectations

The candidate payload should include, at minimum:

- beat label or beat type
- short beat summary
- optional local rationale summary
- optional local structural role hint

### 5.4 Output strictness

This lane should default to:

- `STRICT_STRUCTURED`

Reason:

Beat candidates directly feed ANVIL review surfaces and structural interpretation.

Malformed structure is worse than no structure.

---

## 6. Evidence span doctrine for this lane

### 6.1 Hard rule

Every beat candidate must include evidence spans.

### 6.2 Evidence requirements

Evidence spans must:

- point to text within bounded supplied scope
- support the claimed beat interpretation
- be specific enough for human review
- avoid hand-wavy “whole scene vibe” references where more concrete grounding exists

### 6.3 Minimum evidence posture

A beat candidate without evidence is not promotion-ready and should generally not be emitted as a valid structured candidate for this lane.

### 6.4 Why this matters

Beat extraction is interpretive.

Evidence spans are the main protection against:

- overreading
- genre-default hallucination
- forced structure imposition
- magical hidden certainty

---

## 7. Confidence doctrine for this lane

### 7.1 Required confidence classes

Use bounded classes:

- `low`
- `moderate`
- `high`

### 7.2 Lane-specific meaning

- `low` = possible beat candidate; substantial review burden
- `moderate` = plausible candidate with decent textual support
- `high` = strong candidate with clear local support; still not authoritative

### 7.3 Hard rule

High confidence does not justify direct promotion.

### 7.4 Emission rule

The lane should prefer emitting fewer higher-quality candidates over many weak speculative candidates.

---

## 8. Candidate count discipline

### 8.1 Default posture

The lane should be conservative in candidate count.

### 8.2 Recommended default

Per scene:

- preferred: 0 to 2 candidate beats
- acceptable upper bound: 3 in unusual complex scenes

### 8.3 Why this matters

Too many beat candidates per scene usually indicates:

- over-interpretation
- weak selection discipline
- taxonomy confusion
- degraded review usability

### 8.4 Hard rule

A lane that floods scenes with candidate beats is not behaving usefully, even if the candidates are individually plausible.

---

## 9. Failure taxonomy

This lane needs explicit failure categories for evaluation and adoption.

### 9.1 Under-extraction

The lane misses a clearly useful beat candidate supported by the scene.

### 9.2 Over-extraction

The lane proposes beats where the scene does not strongly justify them.

### 9.3 Beat inflation

The lane extracts too many beats from one scene.

### 9.4 Taxonomy drift

The lane uses beat labels inconsistently or collapses distinct beat types into vague labels.

### 9.5 Evidence weakness

The lane emits candidates with vague, weak, or misaligned evidence spans.

### 9.6 Scope confusion

The lane attributes a chapter-window or scene-window inference to a single scene.

### 9.7 Structural overreach

The lane infers arc significance or structural certainty beyond what bounded scope supports.

### 9.8 Schema failure

The lane output fails contract structure.

### 9.9 Confidence miscalibration

The lane assigns `high` confidence where support is weak or ambiguous.

### 9.10 Review-unfriendly phrasing

The lane emits candidates in language too vague, too literary, or too abstract for reliable review.

---

## 10. Route and model posture

### 10.1 Required route class

This lane requires:

- **preferred route:** `HIGH_QUALITY_LOCAL`
- **minimum acceptable route:** `HIGH_QUALITY_LOCAL`
- **fallback policy:** fail closed

### 10.2 Why fail closed

Beat candidate extraction is a `STRICT_STRUCTURED`, integration-facing task.

A weaker fallback that produces shallow or malformed structure is worse than no output.

### 10.3 Candidate model posture

Initial candidate models should be treated as challengers for this lane, not assumed baselines.

Early likely challengers:

- `phi4-reasoning:latest`
- stronger Qwen variants when hardware allows
- any future reasoning-capable local model that fits hardware doctrine

### 10.4 Current workhorse relation

`qwen2.5:14b` may still be useful for exploratory comparison, but it should not be assumed to be the best fit for this lane simply because it won proofreading lanes.

Different task families may have different trusted baselines.

---

## 11. Evaluation set design

### 11.1 Evaluation purpose

The eval set should determine whether the lane produces review-useful beat candidates under bounded scene conditions.

### 11.2 Starter eval composition

Build a small but diverse starter set of scenes covering:

- clear beat scenes
- ambiguous scenes
- quiet connective scenes
- dialogue-heavy scenes
- action scenes
- emotionally transitional scenes
- scenes with no strong beat candidate

### 11.3 Why negative cases matter

Scenes with **no useful beat candidate** are essential.

Without them, the lane will learn beat inflation.

### 11.4 Evaluation unit

The primary evaluation unit is:

- one bounded scene request
- with known supporting context policy
- producing candidate beat output for review

---

## 12. Human review rubric

Each candidate beat result should be reviewed along at least these axes:

### 12.1 Usefulness

Is the candidate useful enough to help an author/operator review scene structure?

### 12.2 Support

Do the evidence spans actually support the candidate?

### 12.3 Restraint

Did the lane avoid overclaiming certainty or multiplying beats unnecessarily?

### 12.4 Scope honesty

Does the candidate correctly represent what scope it used?

### 12.5 Label quality

Is the beat label/type coherent and operationally understandable?

### 12.6 Review usability

Is the candidate phrased in a way that a reviewer can act on efficiently?

---

## 13. Baseline and challenger adoption posture

### 13.1 Initial posture

This lane begins with:

- no locked baseline yet
- challenger evaluation first
- calibration before adoption

### 13.2 Adoption requirement

A candidate model/profile should only become the lane baseline if it demonstrates:

- strong schema reliability
- evidence quality
- useful restraint
- acceptable confidence calibration
- low beat inflation
- stable review usability across varied scenes

### 13.3 Non-requirement

The lane does not need perfect literary agreement.

It needs trustworthy candidate usefulness.

### 13.4 Rejection conditions

Immediate rejection if the challenger shows repeated:

- schema failure
- over-extraction
- evidence weakness
- scope confusion
- confidence overstatement
- structurally grandiose interpretation

---

## 14. Integration boundary with ANVIL

### 14.1 Allowed use

This lane may feed ANVIL with:

- candidate beats for review queues
- candidate overlays
- comparison/triage panels

### 14.2 Forbidden use

This lane must not directly define:

- canonical beat state
- official intensity curves as truth
- authority arc structure

### 14.3 Promotion rule

Any beat candidate must pass explicit review/promotion before becoming authority-consumable by ANVIL canonical views.

---

## 15. Relationship to Bloom

### 15.1 Bloom posture

Bloom may use beat candidates from this lane as review assistance.

### 15.2 Constraint

Bloom must not treat scene-local beat candidates as full progression truth without additional scope-aware reasoning and promotion workflow.

### 15.3 Future follow-on

A separate progression or cross-scene reasoning lane should be defined before Bloom relies heavily on multi-scene structural inference.

---

## 16. Recommended first artifact set for this lane

When execution planning begins, the lane should produce or require at minimum:

- `docs/scene-aware-beat-candidate-extraction-lane-plan.md`
- `evals/scene-aware-beat-candidate-extraction-status-YYYY-MM-DD.md`
- `evals/scene-aware-beat-candidate-extraction-calibration-YYYY-MM-DD.md`
- starter eval scene set
- review template for candidate beat scoring
- lane registry entry

---

## 17. Working definition

Use this shorthand going forward:

**Scene-aware beat candidate extraction is a high-quality-local, fail-closed, strict-structured NeuronForge lane that proposes bounded, evidence-bearing beat candidates from scene text for review, not authority.**

