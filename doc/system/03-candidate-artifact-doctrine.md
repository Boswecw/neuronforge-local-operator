# Candidate Artifact Doctrine for AuthorForge

## Status
Draft v1.0

## Purpose
Define the doctrine for candidate artifacts produced by NeuronForge Local for AuthorForge.

This document establishes what inferred artifacts are allowed to be, how they must be represented, how they move through review, and what boundaries must exist between candidate inference and canonical authority.

It is the bridge between:

- NeuronForge Local runtime and task contracts
- AuthorForge review and promotion workflows
- ANVIL and Bloom consumption rules

This is a control-surface artifact, not an implementation spec.

---

## 1. Why this artifact exists

The current architecture stack now defines:

- NeuronForge Local as a bounded local inference orchestration service
- task contracts as versioned runtime agreements
- routing/model profiles as hardware-aware execution policy

What remains undefined is the meaning of the outputs.

Without this doctrine, the system risks:

- treating all inferred outputs as interchangeable
- blurring advisory findings and integration-feeding candidates
- silently allowing candidate artifacts to contaminate canonical truth
- overfeeding ANVIL and Bloom with ungoverned inferred structure

This artifact defines what candidate artifacts are allowed to mean.

---

## 2. Core doctrine

### 2.1 Hard rule

**All inferential outputs produced by NeuronForge Local are candidate artifacts by default.**

They are not authoritative.

They are not canonical.

They are not persisted as truth without explicit promotion.

### 2.2 Why this matters

NeuronForge Local is an inference system.

Inference may generate useful structure such as:

- candidate beats
- candidate entities
- candidate scene signals
- candidate continuity findings
- candidate pacing observations

Useful does not mean canonical.

### 2.3 AuthorForge boundary

AuthorForge owns the workflow that determines whether a candidate remains:

- pending
- accepted
- revised
- rejected
- promoted into authority

NeuronForge Local may suggest.

AuthorForge decides what becomes durable truth.

---

## 3. Candidate artifact classes

Candidate artifacts should be classed explicitly.

### 3.1 Candidate beat

Purpose:

- propose a story beat inferred from bounded scene text

Typical use:

- ANVIL candidate ingestion queue
- beat review surface
- arc reasoning assistance

Required posture:

- structured candidate
- evidence-bearing
- confidence-bearing
- never direct authority

### 3.2 Candidate entity

Purpose:

- propose an entity mention, role, or entity-state observation inferred from text

Typical use:

- entity review queue
- scene/entity linkage assistance
- continuity support

Required posture:

- structured candidate
- evidence-bearing
- confidence-bearing
- never direct authority

### 3.3 Candidate scene signal

Purpose:

- propose bounded signals about a scene's narrative properties

Examples:

- tension presence
- conflict presence
- intimacy signal
- turning-point likelihood
- setup/payoff cue

Required posture:

- may be descriptive or integration-feeding
- must be explicitly typed
- confidence-bearing
- evidence-bearing when text-based

### 3.4 Candidate analytical finding

Purpose:

- propose an advisory conclusion from continuity, pacing, voice, or consistency analysis

Required posture:

- advisory by default
- structured if integration-facing
- evidence-linked where feasible
- never auto-promoted

### 3.5 Candidate transform result

Purpose:

- propose revised or transformed text under a bounded contract

Required posture:

- revised text candidate
- risk-marked where applicable
- acceptance required before replacing authoritative user text

---

## 4. Candidate artifact record shape

Every candidate artifact should carry a minimum doctrinal record shape, even if exact schema varies by contract.

### 4.1 Minimum fields

- `candidate_id`
- `artifact_class`
- `source_scope`
- `contract_id`
- `contract_version`
- `lane_id` when applicable
- `route_class_actual`
- `model_id`
- `provenance_class`
- `confidence_class`
- `review_state`
- `created_at`

### 4.2 Conditionally required fields

Required for structure-bearing inference:

- `evidence_spans`
- `schema_validation_status`
- `degraded_mode`
- `degraded_reason` when degraded

Required for beat/entity/signal candidates:

- `candidate_payload`
- `source_scene_ids` or equivalent bounded source refs

Required for transform results:

- `candidate_text`
- `change_risk`

### 4.3 Rule

A candidate artifact without source scope, provenance, and review state is not fit for workflow use.

---

## 5. Evidence span doctrine

### 5.1 Core rule

Any candidate artifact that asserts something about source text should, where feasible, include evidence spans tied to the bounded source scope.

### 5.2 Required for

Evidence spans are required for:

- candidate beats
- candidate entities
- integration-feeding scene signals
- continuity findings that refer to concrete textual signals

### 5.3 Recommended for

Evidence spans are recommended for:

- pacing observations
- voice findings
- descriptive scene signals

### 5.4 Why this matters

Evidence spans make candidates:

- reviewable
- contestable
- auditable
- less likely to be mistaken for magical hidden truth

### 5.5 Hard boundary

A beat or entity candidate with no textual grounding should not be treated as promotion-ready.

---

## 6. Confidence doctrine

### 6.1 Confidence is required, not decorative

Confidence must be present for inferential candidate artifacts.

It exists to support review posture, not to pretend numeric certainty is objective truth.

### 6.2 Recommended confidence classes

Use bounded classes, not fake precision:

- `low`
- `moderate`
- `high`

Optional future extension:

- `very_high` only if separately justified and calibrated

### 6.3 Confidence meaning

- `low` = useful possibility, high review burden
- `moderate` = plausible candidate, normal review burden
- `high` = strong candidate, still not authority

### 6.4 Rule

High confidence does not change candidate status.

It only changes review posture.

---

## 7. Review state doctrine

Every candidate artifact must move through explicit review states.

### 7.1 Required states

- `pending_review`
- `accepted_as_is`
- `accepted_with_revision`
- `rejected`
- `promoted_to_authority`

### 7.2 Optional future states

- `deferred`
- `needs_more_context`
- `superseded`

### 7.3 Rule

`promoted_to_authority` is not just another acceptance label.

It is a distinct workflow boundary.

### 7.4 Why this matters

A candidate can be useful without being authoritative.

Review states must preserve that distinction.

---

## 8. Promotion doctrine

### 8.1 Hard rule

Promotion into authority requires an explicit workflow transition.

It must not happen implicitly because:

- confidence was high
- the user viewed the candidate
- the route class was high quality
- the model was a trusted baseline

### 8.2 Allowed promotion paths

Promotion may occur through:

- direct author acceptance
- explicit operator review workflow
- future separately approved deterministic promotion policy

### 8.3 Promotion record requirements

When a candidate is promoted, the system should preserve:

- source candidate id
- promotion actor
- promotion timestamp
- whether modified before promotion
- resulting authority artifact id

### 8.4 Promotion consequence

Once promoted, the authoritative artifact lives in the authority layer.

The original candidate remains part of provenance history, not the live truth object itself.

---

## 9. Rejection and discard doctrine

### 9.1 Rejection must be first-class

Rejected candidates are not errors.

They are a normal and healthy outcome of inference review.

### 9.2 Rejection reasons should be capturable

Recommended rejection reasons:

- unsupported by text
- wrong interpretation
- too vague
- duplicative
- structurally malformed
- not useful
- confidence overstated

### 9.3 Discard rule

Rejected candidates must not pollute canonical structure.

They may remain in audit/review history, but not in live authority views.

### 9.4 Supersession rule

A later candidate or a human-authored artifact may supersede an earlier candidate without implying the earlier candidate was promoted.

---

## 10. ANVIL consumption rules

### 10.1 ANVIL sensitivity

ANVIL consumes story-structure signals.

That makes it especially sensitive to malformed or overconfident inferred structure.

### 10.2 Default rule

ANVIL should distinguish between:

- candidate-facing views
- authority-facing views

### 10.3 Candidate-facing allowed consumption

ANVIL may consume candidate beats/signals for:

- review queues
- candidate overlays
- comparison views
- operator triage

These must be visibly marked as candidate-derived.

### 10.4 Authority-facing allowed consumption

ANVIL should consume promoted authoritative beats/signals for:

- canonical arc state
- official intensity and structure views
- cross-scene structural reporting used as truth

### 10.5 Hard rule

Candidate beats may inform review.

They must not silently become canonical ANVIL truth.

---

## 11. Bloom consumption rules

### 11.1 Bloom sensitivity

Bloom presents timeline and chapter/scene progression views.

That makes it sensitive to candidate signals that imply narrative sequence or progression logic.

### 11.2 Default rule

Bloom should distinguish between:

- review-grade candidate overlays
- authoritative narrative timeline state

### 11.3 Candidate-facing allowed consumption

Bloom may consume candidate artifacts for:

- scene-level overlays
- optional progression hints
- review context panels
- draft timeline assistance

### 11.4 Authority-facing allowed consumption

Bloom should consume authoritative state for:

- official scene progression
- canonical structure timelines
- cross-project reporting treated as truth

### 11.5 Hard rule

A candidate scene signal or candidate beat may appear in Bloom as review assistance.

It must not silently define the canonical timeline model.

---

## 12. Candidate scope doctrine

### 12.1 Bounded scope rule

Candidate artifacts must identify bounded source scope.

Examples:

- single scene
- scene window
- chapter window
- selected passage

### 12.2 Why this matters

Scope affects:

- interpretation quality
- route-class requirements
- review difficulty
- confidence meaning

### 12.3 Cross-scope rule

A candidate derived from a scene window must not be mislabeled as if it came from a single scene.

The scope is part of the meaning.

---

## 13. Candidate artifact priorities for AuthorForge v1

### 13.1 First priority

- candidate beat
- candidate entity
- candidate descriptive scene signal
- candidate integration scene signal

These directly support the manuscript → scenes → candidates → review → authority bridge.

### 13.2 Second priority

- candidate continuity finding
- candidate pacing finding
- candidate voice finding

These are useful but can remain more advisory at first.

### 13.3 Third priority

- candidate arc suggestion
- candidate cross-scene thematic linkage

These should wait until the lower-level candidate classes are stable.

---

## 14. Relationship to other artifacts

| Artifact | Relationship |
|---|---|
| Runtime Architecture Spec | Defines where candidate outputs are produced and how provenance is surfaced |
| Task Contract Taxonomy | Defines what contract families exist and which require structured outputs |
| Routing and Model Profile Plan | Defines which route classes can safely produce which candidate classes |
| Future ANVIL/Bloom Reasoning Requirements | Will define module-specific reasoning expectations on top of this doctrine |

---

## 15. Working definition

Use this shorthand going forward:

**A candidate artifact is a bounded, provenance-bearing, review-stateful inferential output produced by NeuronForge Local that may assist AuthorForge workflows and ANVIL/Bloom review surfaces, but does not become canonical truth without explicit promotion.**

