# ANVIL and Bloom Reasoning Contract Requirements

## Status
Draft v1.0

## Purpose
Define the module-specific reasoning contract requirements for **ANVIL** and **Bloom** as consumers of NeuronForge Local candidate artifacts.

This document sits on top of the existing NeuronForge control surface:

- Task Contract Taxonomy
- Routing and Model Profile Plan
- Candidate Artifact Doctrine for AuthorForge

Its role is to define what these modules specifically require from candidate artifacts, what they are allowed to consume, what must remain review-only, and where fail-closed behavior is mandatory.

This is a control-surface artifact, not an implementation spec.

---

## 1. Why this artifact exists

The current control surface already defines:

- what NeuronForge task families exist
- how they route across local model capability tiers
- what candidate artifacts are allowed to mean

What remains to define is the **consumer-side contract** for the first major reasoning-driven AuthorForge modules.

Without this layer, the system risks:

- overfeeding ANVIL and Bloom with candidate artifacts that look more certain than they are
- treating all candidate artifacts as equally consumable by both modules
- letting advisory findings drift into module truth surfaces
- failing to distinguish review assistance from canonical structural state

This artifact defines the module-specific consumption and reasoning boundaries.

---

## 2. Core module doctrine

### 2.1 Shared hard rule

ANVIL and Bloom are allowed to consume **candidate artifacts** for review assistance.

They are not allowed to treat candidate artifacts as canonical truth unless those artifacts have passed explicit promotion into authority.

### 2.2 Why this matters

Both modules operate on narrative structure.

That means they are especially vulnerable to:

- confident but weak inference
- malformed structured candidates
- scope confusion
- timeline drift
- arc overinterpretation

### 2.3 Module distinction

ANVIL and Bloom are related but not identical consumers.

- **ANVIL** is primarily a structure / arc / intensity consumer
- **Bloom** is primarily a timeline / scene progression / sequence consumer

Their contract requirements overlap, but they are not interchangeable.

---

## 3. ANVIL reasoning role

### 3.1 ANVIL purpose

ANVIL reasons about story structure through signals such as:

- beats
- intensity changes
- flatlines
- drops
- arc-to-scene relationships
- candidate structural patterns across scenes

### 3.2 ANVIL sensitivity

ANVIL is sensitive to malformed inferred structure because structural mistakes can distort:

- arc interpretation
- intensity visualization
- beat distribution
- review prioritization

### 3.3 ANVIL contract posture

ANVIL requires:

- strongly typed candidate artifacts
- bounded source scope
- evidence-bearing support where text-grounded
- route visibility for reasoning-sensitive tasks
- explicit candidate vs authority separation in the UI and data model

---

## 4. Bloom reasoning role

### 4.1 Bloom purpose

Bloom reasons about narrative sequence and progression through signals such as:

- chapter/scene order
- scene-to-scene progression
- scene-window development
- timeline overlays
- candidate progression hints
- cross-scene narrative movement

### 4.2 Bloom sensitivity

Bloom is sensitive to inference errors that distort:

- sequence interpretation
- progression logic
- timeline continuity
- scene-window narrative reading

### 4.3 Bloom contract posture

Bloom requires:

- scope-aware candidate artifacts
- sequence-safe interpretation rules
- explicit distinction between local scene inference and cross-scene progression inference
- candidate overlays separated from canonical timeline state

---

## 5. Consumer artifact classes

This section defines which candidate artifact classes each module may consume and under what posture.

### 5.1 ANVIL-eligible candidate artifacts

#### Primary

- candidate beat
- candidate integration scene signal
- candidate descriptive scene signal
- candidate analytical finding related to structure, pacing, or continuity

#### Secondary

- candidate entity where entity state materially affects arc interpretation
- candidate arc suggestion (future phase only)

### 5.2 Bloom-eligible candidate artifacts

#### Primary

- candidate descriptive scene signal
- candidate integration scene signal
- candidate beat
- candidate analytical finding related to continuity, pacing, or progression

#### Secondary

- candidate entity where entity movement/state affects progression interpretation
- candidate arc suggestion (future phase only)

### 5.3 Transform results

Candidate transform results are generally **not** first-order ANVIL/Bloom inputs.

They may affect these modules only indirectly if the user accepts revised text and the authoritative manuscript state changes.

---

## 6. Review-grade vs authority-grade consumption

### 6.1 Shared split

Both modules must distinguish between:

- **review-grade consumption**
- **authority-grade consumption**

### 6.2 Review-grade consumption

Allowed inputs:

- `inferred_candidate`
- `human_confirmed` but not yet promoted, if such a transitional state is used later

Allowed use:

- overlays
- review queues
- candidate comparison surfaces
- triage panels
- operator/author inspection views

UI/data rule:

These must remain visibly marked as candidate-derived.

### 6.3 Authority-grade consumption

Allowed inputs:

- `authority_persisted`

Allowed use:

- canonical arc views
- official intensity graphs
- canonical timeline views
- reporting or analytics treated as project truth

### 6.4 Hard boundary

A candidate artifact may appear in a module.

That does not make it eligible to define canonical module state.

---

## 7. Required contract posture by artifact class

### 7.1 Candidate beat

#### ANVIL

Required posture:

- `STRICT_STRUCTURED`
- evidence spans required
- confidence required
- scope required
- fail closed on schema failure

Reason:

Beat candidates directly affect structural interpretation.

#### Bloom

Required posture:

- `STRUCTURED_CANDIDATE`
- evidence spans required
- confidence required
- scope required
- fail closed if used for integration-facing progression overlays

Reason:

Bloom can display beats in review overlays, but timeline logic must not be polluted by malformed beat structure.

### 7.2 Candidate descriptive scene signal

#### ANVIL

Required posture:

- `STRUCTURED_CANDIDATE`
- evidence recommended
- confidence required
- fallback tolerated with degraded flag

Reason:

Descriptive signals may assist review without directly redefining structure.

#### Bloom

Required posture:

- `STRUCTURED_CANDIDATE`
- evidence recommended
- confidence required
- fallback tolerated with degraded flag

Reason:

Descriptive overlays are useful but not canonical by themselves.

### 7.3 Candidate integration scene signal

#### ANVIL

Required posture:

- `STRICT_STRUCTURED`
- evidence required
- confidence required
- fail closed on route downgrade or schema failure

Reason:

These signals feed integration-sensitive structural surfaces.

#### Bloom

Required posture:

- `STRICT_STRUCTURED`
- evidence required
- confidence required
- fail closed on route downgrade or schema failure

Reason:

Integration-facing progression overlays must not consume malformed signals.

### 7.4 Candidate analytical finding

#### ANVIL

Required posture:

- `STRUCTURED_ANALYSIS`
- evidence recommended, required where text-grounded claims are concrete
- degraded fallback allowed for advisory panels

#### Bloom

Required posture:

- `STRUCTURED_ANALYSIS`
- evidence recommended, required where progression claims are text-grounded
- degraded fallback allowed for advisory panels

### 7.5 Candidate entity

#### ANVIL

Required posture:

- `STRICT_STRUCTURED` if entity state affects structural interpretation
- otherwise `STRUCTURED_CANDIDATE`

#### Bloom

Required posture:

- `STRICT_STRUCTURED` if entity movement/state affects progression logic
- otherwise `STRUCTURED_CANDIDATE`

Rule:

Entity candidates should not be treated as first-order structure unless the contract explicitly says they are integration-feeding.

---

## 8. Scope rules

### 8.1 Scope is part of meaning

Both ANVIL and Bloom must treat source scope as part of the artifact meaning.

Examples:

- single scene
- scene window
- chapter window
- selected passage

### 8.2 ANVIL scope rules

#### Single scene

Allowed for:

- beat candidate review
- local intensity hints
- local scene signal overlays

#### Scene window

Allowed for:

- arc relation hints
- continuity-informed beat interpretation
- local structural pattern review

#### Chapter window

Allowed only for:

- higher-order review assistance
- not direct canonical structure unless promotion workflow explicitly supports it

### 8.3 Bloom scope rules

#### Single scene

Allowed for:

- scene-local overlays
- descriptive progression hints

#### Scene window

Allowed for:

- continuity review
- local progression analysis
- transition interpretation

#### Chapter window

Allowed for:

- progression reasoning
- chapter-level review surfaces
- draft timeline assistance

Hard rule:

A chapter-window inference must not be mislabeled as a single-scene fact.

### 8.4 Scope-width escalation

When source scope widens:

- minimum acceptable route class may increase
- confidence interpretation should become more conservative
- review burden should increase

This rule must remain aligned with the routing plan's scope-width escalation logic.

---

## 9. Required route posture for module reasoning

### 9.1 ANVIL

#### Must use `HIGH_QUALITY_LOCAL`

- beat candidate extraction
- integration scene signal extraction
- structure-sensitive continuity findings

#### May use `WORKHORSE_LOCAL` with degraded flag

- descriptive scene signals
- pacing observations in advisory panels

#### Must fail closed

- any `STRICT_STRUCTURED` candidate with schema failure
- route downgrade below minimum acceptable class
- missing scope or missing confidence on required contracts

### 9.2 Bloom

#### Must use `HIGH_QUALITY_LOCAL`

- integration scene signal extraction
- progression-sensitive continuity reasoning
- chapter-window progression reasoning

#### May use `WORKHORSE_LOCAL` with degraded flag

- descriptive scene signals
- single-scene pacing observations
- advisory scene-local findings

#### Must fail closed

- any candidate used for integration-facing timeline/progression surfaces if schema fails
- route downgrade below minimum acceptable class
- scope mismatch for cross-scene claims

---

## 10. Failure doctrine

### 10.1 Hard rule

A malformed structured candidate is worse than no candidate.

### 10.2 Fail-closed conditions for both modules

Fail closed when:

- schema validation fails on `STRICT_STRUCTURED` input
- evidence is required but absent
- confidence is required but absent
- scope is missing or mismatched
- route class actual is below minimum acceptable route
- degraded fallback is not allowed by the contract

### 10.3 Degraded-but-valid conditions

Degraded output may still be consumable for review assistance when:

- contract allows fallback
- structure remains valid
- confidence remains present
- scope remains correct
- UI/data surface clearly marks the result as degraded candidate output

### 10.4 Forbidden behavior

Do not:

- silently coerce malformed candidate input into canonical module state
- display candidate-derived structure as if it were authoritative
- merge cross-scope inferences into one undifferentiated timeline/arc truth
- treat high confidence as permission to skip review

---

## 11. Module-specific contract priorities

### 11.1 ANVIL first-priority contracts

- `extract.beat_candidates.scene.v1`
- `extract.scene_signals.integration.v1`
- `extract.scene_signals.descriptive.v1`
- `analyze.continuity.scene_window.v1`
- `analyze.pacing.scene_window.v1`

### 11.2 Bloom first-priority contracts

- `extract.scene_signals.descriptive.v1`
- `extract.scene_signals.integration.v1`
- `extract.beat_candidates.scene.v1`
- `analyze.continuity.scene_window.v1`
- `analyze.pacing.scene_window.v1`

### 11.3 Shared future-phase contracts

- `extract.arc_candidates.scene_window.v1`
- `analyze.progression.chapter_window.v1`
- `analyze.voice.scene_window.v1`

These should wait until lower-level candidate classes are stable.

---

## 12. Review surface requirements

### 12.1 Required review metadata in ANVIL/Bloom surfaces

When showing candidate-derived artifacts, the surface should be able to show:

- artifact class
- candidate status
- confidence class
- source scope
- evidence availability
- route quality/degraded status

### 12.2 Why this matters

A reasoning module that hides candidate status will train users to mistake inference for truth.

### 12.3 Hard rule

Review surfaces must preserve candidate visibility.

Authority surfaces must preserve canonical visibility.

Do not blur them.

---

## 13. Relationship to other artifacts

| Artifact | Relationship |
|---|---|
| Task Contract Taxonomy | Defines the families and strictness classes this module layer consumes |
| Routing and Model Profile Plan | Defines the route minimums and fail-closed policy this module layer relies on |
| Candidate Artifact Doctrine | Defines what candidate artifacts mean before modules consume them |
| Future lane plans | Will define baseline/challenger trust decisions per reasoning task |

---

## 14. Working definition

Use this shorthand going forward:

**ANVIL and Bloom are reasoning-sensitive consumers of NeuronForge candidate artifacts that may use structured candidate outputs for review assistance, but must reserve canonical structural and timeline truth for authority-persisted artifacts under explicit fail-closed and scope-aware contract rules.**

