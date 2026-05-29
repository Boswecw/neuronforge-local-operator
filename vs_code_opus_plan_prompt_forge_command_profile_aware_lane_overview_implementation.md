# VS Code Opus Plan/Prompt — ForgeCommand Profile-Aware Lane Overview Implementation

## Revision

- Revision: 1
- Status: Implementation Prompt
- Target repo: `/Forge/ecosystem/ForgeCommand`
- Scope: initial lane fleet overview and detail-view governance behavior for profile-aware lane evidence presentation

---

# Part 1 — Implementation Plan

## Objective

Implement the first profile-aware lane evidence surface in ForgeCommand using the governed NeuronForge lane record contract.

This work is specifically for:

- `/Forge/ecosystem/ForgeCommand`

The goal is to create the first real ForgeCommand lane overview that respects:

- `metric_profile`
- `metric_provenance`
- `metrics_gate_eligible`

and does **not** flatten unlike lanes into a misleading generic metrics dashboard.

---

## Why this exists now

NeuronForge lane records now provide enough governed meaning to support a safer control surface.

The lane fleet includes different lane families with different evidence classes and different interpretation models.

ForgeCommand must therefore behave like a profile-aware evidence console rather than a flat dashboard.

This implementation is the first UI slice that makes those distinctions visible to the operator.

---

## Implementation goals

1. Build a lane fleet overview that visibly presents profile, provenance, and gate eligibility.
2. Keep the top-level view scan-friendly and not overloaded with raw metrics.
3. Build a lane detail view or expandable detail surface that exposes deeper context.
4. Prevent naive cross-profile comparison cues in the initial UX.
5. Keep the implementation grounded in current real lane fields and current real fleet records.

---

## Non-goals

This implementation does **not**:

- implement full compare mode yet
- implement fleet-wide rollups or scores
- implement cross-profile ranking
- invent new lane metrics
- redefine NeuronForge schemas
- add speculative future lane families

---

## Required behavior

### 1. Lane overview surface

The initial ForgeCommand lane overview must show, for each lane:

- lane name
- lane id
- status
- current baseline model
- current baseline prompt profile
- metric profile
- metric provenance
- metrics gate eligible state
- concise current judgment summary

The overview should favor quick recognition and governance clarity over metric density.

### 2. Detail surface

Each lane should have a detail surface, whether as a dedicated detail view, side panel, drawer, or expandable row, that shows:

- full lane metadata relevant to operator interpretation
- current metric values
- provenance notes
- current judgment
- calibration doc reference
- status doc reference

### 3. No cross-profile flattening

The initial implementation must not visually imply that all lanes are numerically comparable.

That means:

- no fleet-wide score
- no universal rank ordering by mixed metrics
- no compare affordance that suggests all lanes can be compared interchangeably

### 4. Semantic separation

The UI must keep these distinct:

- `metric_profile` = what kind of lane this is
- `metric_provenance` = how the metric values were produced
- `metrics_gate_eligible` = whether metrics may feed governed automation-facing logic

These should not be merged into one label.

---

## UX/UI intent

The lane overview should feel like an internal governance control surface.

That means:

- clear visual hierarchy
- concise labels
- obvious evidence distinctions
- restrained use of badges
- progressive disclosure for deeper details

This should not look like a generic SaaS analytics dashboard.

---

## Suggested surface model

## Top-level lane row or card

Each lane entry should present three semantic layers in order:

### Layer 1 — identity

- lane name
- lane id
- status

### Layer 2 — interpretation

- metric profile
- metric provenance
- gate eligibility

### Layer 3 — baseline and judgment

- current baseline model
- current baseline prompt profile
- concise current judgment snippet

Raw metrics should not dominate the top-level view.

---

## Detail surface model

The detail surface should contain:

- all current metrics
- provenance notes
- current judgment
- calibration doc path/reference
- status doc path/reference
- anchor input
- anchor run id

The operator should be able to inspect the lane deeply without cluttering the overview.

---

## Current fleet mapping

The current implementation should assume the real active fleet includes:

- `continuity-progression-reasoning`
  - profile: `detection_reasoning`
  - provenance: `benchmark_derived`
  - gate eligible: `true`

- `general-grammar-cleanup`
  - profile: `editing_cleanup`
  - provenance: `operator_judged`
  - gate eligible: `false`

- `lore-safe-proofreading`
  - profile: `lore_protection_editing`
  - provenance: `operator_judged`
  - gate eligible: `false`

The UI should render these distinctions clearly.

---

## Data assumptions

Assume lane data is sourced from the governed NeuronForge lane visibility surface and already validated.

Do not invent fields outside the current lane record contract unless there is a clearly necessary local view-model transformation.

If a local UI mapping/helper is useful, keep it thin and declarative.

---

## Acceptance criteria

The implementation is complete only if all of the following are true:

1. The work is clearly targeted to `/Forge/ecosystem/ForgeCommand`.
2. The overview shows profile, provenance, and gate eligibility for every lane.
3. The overview remains scan-friendly and does not drown in metric detail.
4. A detail surface exposes deeper lane information.
5. The UI does not imply cross-profile comparability.
6. There is no fleet-wide score or universal rank ordering.
7. The implementation uses current real lane semantics, not speculative future abstractions.

---

## Guardrails

- Do not implement cross-profile compare mode in this change.
- Do not add fleet-wide aggregate scoring.
- Do not hide `metric_profile` or `metric_provenance` behind tooltip-only UI.
- Do not merge profile and provenance into one concept in the interface.
- Do not overbuild the component system for hypothetical future views.
- Prefer minimal, high-integrity structure.

---

# Part 2 — Senior Engineer Implementation Review Notes

## Executive engineering posture

This should land as a restrained first slice, not as an attempt to solve the entire ForgeCommand analytics UX in one pass.

That means the implementation should prioritize:

- semantic correctness
- readable structure
- explicit evidence distinctions
- low-friction extensibility

The biggest risk is accidental dashboardification.

Avoid that.

---

## What the implementation should get right

### 1. Thin view-model layer

If the lane records need adaptation for display labels or badge text, use a thin mapping layer rather than scattering logic across multiple components.

Examples of acceptable mapping concerns:

- profile display labels
- provenance display labels
- gate-eligibility label text
- status display text

Do not mutate the underlying semantics.

### 2. Controlled badge use

Badges should communicate governance state, not decorate the UI.

Recommended visible semantic badges/labels:

- status
- profile
- provenance
- gate eligibility

That is enough.

### 3. Judgment must remain visible

Do not build a UI that only shows numbers and badges.

`current_judgment` is part of the governance meaning surface and should remain visible at overview or detail level.

### 4. Do not bury provenance notes

If provenance notes exist, they should be accessible in the detail surface without awkward hunting.

### 5. Build the overview first

Do not jump into compare views, sorting systems, or ranking logic.

The initial slice should stabilize the overview semantics first.

---

## Recommended structure direction

You do not need a large architecture here.

A clean first slice could reasonably consist of:

- one page or route for lane overview
- one lane list component
- one lane card or row component
- one lane detail drawer/panel/expandable section component
- one thin mapping utility for display labels if needed

Keep the shape boring and maintainable.

---

## Risk review

### Risk 1 — generic analytics component drift

A generic analytics table can accidentally erase important meaning boundaries.

#### Mitigation

Keep lane-specific presentation explicit in the first slice.

### Risk 2 — too much metric density

Showing all metrics in the overview will increase noise and make profile/provenance cues less visible.

#### Mitigation

Keep metrics mostly in the detail surface.

### Risk 3 — visual equivalence trap

If all badges and numbers are rendered with identical emphasis, the operator may infer equal comparability.

#### Mitigation

Make profile and provenance visible before raw metrics and avoid summary ranking cues.

### Risk 4 — overengineering for future views

Trying to solve overview, detail, compare, and analytics in one pass will produce unnecessary complexity.

#### Mitigation

Ship only overview + detail semantics now.

---

## Implementation recommendation

Approve a first slice that focuses on:

- lane overview
- lane detail inspection
- profile/provenance/gate visibility
- no compare mode yet
- no aggregation yet

That is the correct senior-engineer scope for this stage.

---

# Part 3 — Final VS Code Opus Prompt

Use the prompt below as the implementation prompt for VS Code Opus.

---

You are implementing the first profile-aware lane evidence overview in the ForgeCommand repository.

Target repo:

- `/Forge/ecosystem/ForgeCommand`

Your task is to create a lane overview and detail surface that correctly presents governed NeuronForge lane records without flattening unlike lanes into a generic metrics dashboard.

## Required context

NeuronForge lane records now include these important semantics:

- `metric_profile`
- `metric_provenance`
- `metrics_gate_eligible`
- `provenance_notes`
- `current_judgment`
- current metric fields
- supporting doc references such as `calibration_doc` and `status_doc`

The current active fleet includes three real lanes:

- `continuity-progression-reasoning`
  - `metric_profile`: `detection_reasoning`
  - `metric_provenance`: `benchmark_derived`
  - `metrics_gate_eligible`: `true`

- `general-grammar-cleanup`
  - `metric_profile`: `editing_cleanup`
  - `metric_provenance`: `operator_judged`
  - `metrics_gate_eligible`: `false`

- `lore-safe-proofreading`
  - `metric_profile`: `lore_protection_editing`
  - `metric_provenance`: `operator_judged`
  - `metrics_gate_eligible`: `false`

These distinctions matter and must remain visible in the UI.

## What to implement

### 1. Lane overview surface

Implement a lane overview surface that shows, for each lane:

- lane name
- lane id
- status
- current baseline model
- current baseline prompt profile
- metric profile
- metric provenance
- metrics gate eligible state
- concise current judgment summary

Important:

The overview should be scan-friendly and governance-oriented.

Do not make raw metrics the visual center of the page.

### 2. Lane detail surface

Implement a detail surface for each lane.

This can be a drawer, expandable section, side panel, or dedicated detail view depending on the current repo structure.

The detail surface should expose:

- current metrics
- provenance notes
- current judgment
- calibration doc reference
- status doc reference
- anchor input
- anchor run id

### 3. Semantic separation

Keep these visibly separate in the UI:

- `metric_profile`
- `metric_provenance`
- `metrics_gate_eligible`

Do not merge them into one badge or one combined label.

### 4. No misleading comparison cues

In this first implementation:

- do not add fleet-wide scoring
- do not add universal metric ranking
- do not add cross-profile compare mode
- do not imply cross-profile comparability through layout or summary widgets

### 5. Keep the implementation restrained

Use a simple, maintainable structure.

A good first slice is likely:

- one overview page/route
- one lane list component
- one lane row/card component
- one detail panel/drawer/expandable component
- one small mapping utility if needed for display labels

Do not overbuild for hypothetical future analytics views.

## UX/UI expectations

This should feel like an internal governance control surface, not a generic SaaS dashboard.

Prioritize:

- clarity
- semantic integrity
- strong visual hierarchy
- progressive disclosure
- recognition over recall

The operator should understand what kind of lane they are looking at, how strong the evidence is, and whether the metrics can feed automation-facing logic before they start reading deeper details.

## Guardrails

- Do not invent new schema fields.
- Do not redefine NeuronForge semantics.
- Do not implement compare mode in this change.
- Do not add fleet-wide aggregates.
- Do not hide profile or provenance in tooltip-only UI.
- Do not collapse profile and provenance into one visual concept.
- Prefer minimal, disciplined code.

## Deliverables

Provide:

1. the new/updated overview UI
2. the detail surface implementation
3. any supporting thin mapping/view-model utility if needed
4. a concise summary of what changed and why

## Quality bar

This should land as a first serious ForgeCommand evidence surface.

It must show senior-engineer judgment:

- small surface area
- explicit semantics
- no dashboard drift
- no speculative overengineering
- maintainable structure

If repo structure forces a choice between multiple reasonable UI implementations, choose the most conservative clean option and explain why.

