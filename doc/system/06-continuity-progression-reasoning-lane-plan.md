# Continuity / Progression Reasoning Lane Plan

Date: 2026-03-14

## Purpose

Define the first governed reasoning lane for cross-scene and scene-window analysis in NeuronForge Local.

This lane exists to produce **candidate continuity and progression findings** that can support Bloom review workflows without allowing inferential output to become canonical truth by default.

This is a planning and governance document.

It is not a declaration that the lane is already trusted.

It defines:

- what this lane is for
- what it is allowed to produce
- what it must never claim
- what route class it requires
- what failure modes matter most
- how review and promotion should work
- what evaluation assets are needed before lane trust can advance

---

## Architectural placement

NeuronForge Local is planned as a **mini local NeuroForge**:

- local-first inference orchestration substrate
- multi-local-LLM runtime
- bounded task-contract service
- candidate-output producer
- lane-governed trust surface

This lane is part of that local reasoning substrate.

It is not an authority engine.

It exists to generate reviewable candidate findings for downstream Forge modules.

---

## Runtime doctrine alignment

### Local baseline

- **DF Local** = baseline local data lane
- **NeuronForge Local** = baseline local AI / LLM orchestration lane

### Cloud remains additive only

- **DataForge** = cloud data services
- **NeuroForge** = cloud intelligence/orchestration services
- **Rake** = cloud research/workflow services
- **ForgeAgents** = cloud agent/process services

This lane must remain meaningful in baseline local operation without assuming cloud services.

---

## Hardware doctrine alignment

This lane must be planned against:

- midlevel writer laptops as of March 14, 2026
- expected normal hardware within the next quarter of 2026
- not workstation or dev-box assumptions

Practical result:

- this lane is not a universal default for all inference tasks
- route selection must prefer reliability over ambition
- heavier reasoning passes must be selective and governance-justified

---

## Lane identity

- **lane id:** `continuity-progression-reasoning`
- **lane family:** `analysis`
- **lane type:** cross-scene / scene-window reasoning
- **primary consumers:** Bloom first, ANVIL second where structure-sensitive review benefits
- **output posture:** candidate findings only
- **canonical truth posture:** prohibited by default

---

## Why this lane exists

The Scene-Aware Beat Candidate Extraction lane covers scene-local candidate beats.

That lane does not fully address:

- cross-scene continuity tension
- progression consistency across adjacent scenes
- scene-window drift in emotional, plot, or causal movement
- descriptive changes that may matter to timeline or sequence review
- review assistance for narrative movement across a bounded span

This lane exists to cover that gap.

It is the first serious reasoning lane that moves beyond extraction into bounded interpretive analysis.

---

## Task contract posture

### Contract family

`analysis`

### Contract strictness

`STRICT_STRUCTURED`

This lane should use strict structured output because freeform reasoning text is too hard to review consistently and too easy to over-interpret.

### Required output discipline

The lane must return structured records with:

- finding id
- finding type
- scope type
- scope bounds
- candidate claim
- evidence spans
- confidence
- uncertainty note
- review note

Malformed structured output is a lane failure.

---

## What the lane is allowed to do

This lane may generate candidate findings such as:

- possible continuity tension between two or more nearby scenes
- possible progression break in character, motivation, tone, injury state, possession state, travel state, or scene consequence
- possible missing bridge between scenes when progression appears abrupt
- possible sequence inconsistency inside a bounded review window
- possible duplicated beat or redundant movement in a bounded sequence
- possible scene-to-scene descriptive mismatch worth review
- possible escalation or de-escalation inconsistency worth review

These are review candidates only.

They are prompts for human review, not declarations of truth.

---

## What the lane must not do

This lane must not:

- declare canonical story truth
- rewrite scenes
- invent missing events as fact
- assert timeline truth beyond available scope
- flatten ambiguity into certainty
- produce legalistic or absolute verdict language when evidence is partial
- upgrade candidate findings into accepted continuity rules
- silently infer off-page events and present them as established story fact
- make project-wide claims from a scene-local or scene-window sample

If the lane cannot support a claim within scope, it must downgrade confidence or fail closed.

---

## Primary analysis scopes

This lane should support bounded scopes only.

### 1. Scene-local progression check

Used when analyzing one scene for internal progression signals such as:

- escalation flow
- emotional movement
- action continuity within the scene
- immediate consequence clarity

### 2. Adjacent-scene comparison

Used when analyzing scene N and scene N+1 for:

- carry-forward continuity
- abrupt state changes
- handoff clarity
- transition integrity

### 3. Scene-window review

Used for a small bounded sequence such as 3 to 6 scenes to inspect:

- progression consistency
- repeated movement
- missing bridge signals
- drift across a short arc

### 4. Chapter-window review

This is optional later, not a first-trust default.

It should only be added after smaller bounded scopes show stable performance.

---

## Scope discipline

Every finding must declare scope explicitly.

Allowed scope labels:

- `scene_local`
- `adjacent_scene`
- `scene_window`
- `chapter_window`

Every finding must also declare scope bounds, such as:

- scene ids
- chapter ids when applicable
- ordered scene positions when available

A finding without explicit scope is malformed.

A finding that speaks beyond its declared scope is governance-failed.

---

## Candidate artifact doctrine for this lane

All outputs from this lane are **candidate artifacts**.

That means:

- they may be useful
- they may be insightful
- they may influence review
- they may support downstream triage
- they are not authority by default

### Required candidate fields

Each candidate finding should include:

- **finding label** — short reviewable label
- **finding type** — continuity / progression / transition / redundancy / bridge-gap / descriptive mismatch / escalation mismatch
- **claim** — concise statement of the possible issue
- **evidence spans** — bounded supporting text references
- **scope** — explicit analysis boundary
- **confidence** — calibrated, not inflated
- **uncertainty note** — why the system may be wrong
- **review note** — what the reviewer should inspect

### Candidate confidence classes

Use restrained classes such as:

- `low`
- `moderate`
- `high`

No `certain` or equivalent class should be allowed for this lane.

---

## Review-state doctrine

This lane should support review states like:

- `candidate_unreviewed`
- `candidate_review_in_progress`
- `candidate_retained`
- `candidate_rejected`
- `candidate_promoted`

### Promotion doctrine

Promotion is explicit and external to inference.

NeuronForge Local may propose.

A governed review layer decides whether any finding is promoted into a trusted project artifact or accepted working note.

No automatic promotion.

---

## Route policy

### Preferred route

`HIGH_QUALITY_LOCAL`

### Minimum acceptable route

`HIGH_QUALITY_LOCAL`

### Default fallback posture

Fail closed.

### Why

This lane depends on bounded reasoning, evidence discipline, scope honesty, and structured restraint.

A weaker workhorse route may be acceptable for future experiments, but it should not be treated as acceptable baseline trust for the first governed version of this lane.

This lane is reasoning-sensitive enough that “usable-looking” output from a weaker route may still be governance-poor.

---

## Model posture

### Current posture

- `qwen2.5:14b` remains relevant as a workhorse local model for active proofreading and grammar lanes
- that does not make it the default model for this reasoning lane

### Challenger posture

As of 2026-03-14, three challengers have been evaluated against the frozen adjacent-scene case pack (cp-001 through cp-012):

**phi4:14b** — 12/12 valid schema envelopes. 75% false positive rate on restraint cases (transition inflation). 0/2 hard true positives detected. Default `moderate` confidence on all findings. Not suitable as baseline without prompt revision.

**qwen2.5:14b** — 12/12 valid schema envelopes. 25% false positive rate on restraint cases (better restraint). 60% surface true positive detection rate. 0/2 hard true positives detected. Default `moderate` confidence on all findings. Stronger starting point for prompt iteration than phi4:14b.

**phi4-reasoning:latest** — Disqualified at 3/3 hard schema failures. The model produces partial JSON objects (candidate findings content without required envelope fields). The `<think>` reasoning traces show substantive analysis quality, but the model cannot reliably emit the required schema structure. An extractor bug (think-block template capture) was discovered and fixed during this run, making the pipeline more robust to future reasoning-model candidates.

Current recommendation: **qwen2.5:14b with prompt v3 is the first baseline candidate.** Zero false positives on all four restraint cases. 80% surface detection rate (up from 60%). Schema reliability 100%. Hard case detection remains 0/2 — a shared ceiling across all tested configurations.

phi4:14b with v3 improved (cp-012 now caught; cp-002, cp-006 now correctly suppressed) but still produces false positives on cp-004 and cp-011. Not recommended for baseline.

phi4-reasoning:latest is disqualified from first-pass consideration under the current schema contract.

Other high-quality-local models may also be evaluated if they fit the hardware doctrine.

### Important separation

Route class is not model identity.

Keep separate:

- task contract
- route policy
- active model selection
- lane trust judgment

---

## Primary consumers

### Bloom

Bloom is the main initial consumer.

Bloom may use this lane for:

- review overlays
- scene-window progression review
- continuity triage
- descriptive mismatch review assistance
- progression-sensitive queues

Bloom must not treat lane findings as canonical timeline truth without explicit promotion.

### ANVIL

ANVIL is a secondary consumer where structure-sensitive review may benefit from progression and continuity signals.

Examples:

- possible repeated movement
- abrupt bridge gaps across scene transitions
- candidate escalation pattern issues affecting structural review

ANVIL must not treat these findings as canonical beat or structure truth without promotion.

---

## Primary risks

This lane is vulnerable to the following failure classes.

### 1. False continuity violations

The model flags an issue where the text is actually consistent.

### 2. Progression overreach

The model claims narrative or emotional inconsistency where ambiguity is intentional or acceptable.

### 3. Scope confusion

The model draws claims beyond the scenes it actually inspected.

### 4. Evidence weakness

The evidence spans do not support the claim strongly enough.

### 5. Causal hallucination

The model invents causal connections that the text does not establish.

### 6. Transition inflation

The model over-diagnoses missing bridges in places where concise narrative motion is acceptable.

### 7. Redundancy inflation

The model over-calls repeated beats or repeated scene function.

### 8. Taxonomy drift

Labels become inconsistent or semantically muddy across evaluations.

### 9. Confidence miscalibration

The model assigns moderate or high confidence to weakly supported claims.

### 10. Review-hostile phrasing

The output is technically structured but hard for a human reviewer to act on quickly.

### 11. Schema failure

The output breaks structure, omits required fields, or blurs evidence and claim.

### 12. Canonicality leakage

The output language implies authority rather than candidate review posture.

---

## Fail-closed doctrine

This lane should fail closed when:

- structured output is malformed
- evidence spans are missing
- scope cannot be stated clearly
- confidence is given without support
- the model tries to make project-wide claims from insufficient context
- the review note is unusable
- output looks polished but cannot be audited

No output is better than deceptive output.

Structured failure is better than fake success.

---

## Review rubric direction

A review rubric should score each candidate set across at least the following dimensions:

### 1. Usefulness

Does the finding help a reviewer notice something worth checking?

### 2. Evidence quality

Are the cited spans actually relevant and sufficient?

### 3. Scope honesty

Does the claim stay inside the declared analysis window?

### 4. Restraint

Does the model avoid over-claiming and over-diagnosing?

### 5. Label quality

Are the finding labels clear, stable, and review-friendly?

### 6. Review usability

Can a human reviewer act on the output quickly?

### 7. Confidence calibration

Does confidence track the real strength of evidence?

### 8. Schema reliability

Does the output remain structurally valid and consistent?

### 9. Canonicality control

Does the output maintain candidate posture rather than truth posture?

### 10. Drift resistance

Do repeated runs stay semantically close enough for governed review usage?

---

## Hard-fail conditions

A candidate set should be hard-failed if any of the following occur:

- unsupported claim framed as truth
- evidence missing for a material claim
- scope omitted or violated
- malformed structured output
- confidence materially higher than evidence supports
- invented event or invented causal bridge presented as fact
- project-wide statement made from bounded local evidence
- review note too vague to support operator action

---

## Evaluation assets needed

Before this lane can advance beyond planning posture, it should have:

### 1. Candidate evaluation set

A bounded set of scene pairs and scene windows containing examples of:

- true continuity tension
- apparent but not real continuity tension
- real progression issue
- acceptable abrupt transition
- repeated movement worth flagging
- repeated movement that should not be flagged
- descriptive mismatch worth review
- ambiguous cases that test restraint

### 2. Structured output schema

A stable output shape for candidate findings.

### 3. Review template

A reviewer-facing scoring form that allows consistent comparison across models and prompt revisions.

### 4. Challenger run protocol

A controlled process for comparing:

- model A vs model B
- prompt revision vs prompt revision
- route stability across bounded tasks

### 5. Lane status document

A living status note tracking:

- current trusted posture
- last reviewed challenger
- known strengths
- known weaknesses
- current recommendation

---

## Initial adoption posture

Initial posture for this lane should be conservative.

### Recommended initial status

`planned`

### First live usage posture

If the lane performs acceptably, first live usage should likely be:

- review assist only
- no silent automation
- no canonical writes
- explicit operator visibility
- explicit candidate labeling in UI

### Promotion posture

Promotion should be manual, explicit, and governed by downstream review logic rather than by NeuronForge Local itself.

---

## Relationship to deterministic methods

This lane should not consume inference where deterministic logic can solve the problem with equal or better reliability.

Examples of deterministic-first candidates include:

- exact metadata mismatch detection
- scene ordering checks
- reference integrity checks
- explicit schema validation
- duplicate id or broken link detection

Inference should be reserved for problems that actually require bounded judgment.

---

## Open implementation questions

These remain open and should be resolved before trust advancement:

1. What exact schema shape best balances strictness and reviewer speed?
2. Should confidence be categorical only, or categorical plus rationale?
3. How much evidence is minimally required for a cross-scene claim?
4. Should scene-window size be fixed at first to reduce drift?
5. Should adjacent-scene review become the first trusted sub-mode before broader scene-window review?
6. Which output labels are stable enough to standardize now?
7. What degree of repeatability is acceptable for a reasoning lane that is candidate-only but review-facing?

---

## Recommended next artifacts

Most natural immediate follow-ons:

### 1. Continuity / Progression Review Rubric

A formal scoring document for reviewing candidate outputs from this lane.

### 2. Continuity / Progression Candidate Schema

The strict structured output contract for this lane.

### 3. Continuity / Progression Eval Set Plan

Defines the first bounded evaluation dataset and edge-case coverage.

### 4. High-Quality-Local Challenger Evaluation Plan

Defines how `phi4-reasoning:latest` and other local reasoning-capable challengers should be compared for this lane.

---

## Current planning judgment

This lane is the correct next governed reasoning lane for NeuronForge Local because it:

- extends beyond scene-local extraction
- directly supports Bloom’s review needs
- pressure-tests candidate-vs-authority doctrine
- exercises strict structured reasoning under bounded scope
- helps prove that NeuronForge Local is a real local reasoning substrate rather than only a proofreading or extraction workspace

The lane should proceed conservatively, with strict structure, bounded scope, high-quality-local routing, and explicit fail-closed behavior.

---

## Restart note

If resuming later, the state of this lane is:

- concept defined
- governance posture defined
- route posture defined
- consumer posture defined
- risks defined
- evaluation needs defined
- **task contract implemented:** `doc/system/tasks/analyze.continuity.adjacent_scene.v1.md`
- **model prompt written:** `prompts/continuity-adjacent-scene-v1.md`
- **schema validator implemented:** `scripts/validate-continuity-candidate.py`
- **executor implemented:** `scripts/run-continuity-adjacent-scene.sh`
- **renderer implemented:** `scripts/render-continuity-candidate.sh`
- **case pack complete:** `inputs/case-packets/cp-001.json` through `cp-012.json` (12 frozen adjacent-scene cases)
- **first-pass challenger comparison complete:** phi4:14b and qwen2.5:14b against all 12 cases; phi4-reasoning:latest stopped at disqualifying schema failure rate
- **first-pass results documented:** `docs/continuity-adjacent-scene-first-pass-results.md`
- **first baseline candidate identified:** `qwen2.5:14b` with `prompts/continuity-adjacent-scene-v3.md`
- baseline candidacy evidence: 0% false positive rate on restraint cases, 80% surface detection, 100% schema reliability
- known ceiling: hard interpretive cases (cp-009, cp-012) remain undetected across all tested models
- trust not yet granted — pending governed promotion

Most natural next step:

**Governed promotion decision** for qwen2.5:14b as lane baseline, or continued evaluation if hard-case detection is required before promotion. Scene-window scope should not expand until adjacent-scene baseline is formally promoted.

