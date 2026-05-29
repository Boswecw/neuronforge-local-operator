# Plan v2 — NeuronForge Lane Metric Semantics and Provenance

## Revision

- Revision: 2
- Status: Proposed
- Scope: NeuronForge lane visibility surface
- Primary concern: metric meaning and evidentiary provenance across lane types

---

## Purpose

This plan formalizes the next governance step for the NeuronForge lane visibility surface.

The current lane fleet is operational and valid, but the fleet now includes more than one kind of lane:

- detection / reasoning style lanes
- editing / cleanup / proofreading style lanes

The current schema requires a common metric shape across all lanes, but those metric fields do not carry the same meaning across all lane types.

This plan exists to prevent semantic drift, false comparability, and future ingest confusion in ForgeCommand.

---

## Current state

The current lane fleet includes:

- `continuity-progression-reasoning`
- `lore-safe-proofreading`
- `general-grammar-cleanup`

### Observed evidence split

#### Continuity lane

The continuity lane has instrument-derived metrics produced against a frozen case pack.

Those values are meaningfully grounded in repeatable evaluation behavior.

#### Editing lanes

The editing lanes currently populate the required metric fields using qualitative approximation based on comparative manual review.

Those values are operationally useful, but they are not equivalent in evidentiary strength to the continuity lane metrics.

This distinction is currently documented in `current_judgment`, but it is not yet surfaced as a first-class governed field in the schema.

---

## Problem statement

The v1 schema currently allows multiple lane types to publish the same metric field names even when:

- the values were produced by different methods
- the values have different semantic meaning
- the values do not support equal-strength comparison

This creates four governance risks:

1. **False comparability**
   Different lane types may appear directly comparable when they are not.

2. **Semantic drift**
   The same metric name can gradually mean different things in different lanes.

3. **Ingest ambiguity**
   ForgeCommand may later consume the values as though they are normalized when they are not.

4. **Governance opacity**
   The lane record does not yet explicitly declare how its metrics were produced.

---

## Goal

Preserve the current operational lane visibility surface while making metric provenance and cross-lane interpretability explicit.

This must be done without breaking the current fleet and without forcing premature metric redesign for every lane.

---

## Non-goals

This plan does not:

- redesign every lane metric immediately
- require benchmark harnesses for all editing lanes right now
- block current approved baselines
- begin ForgeCommand ingest work
- force v1 schema replacement before the fleet is stable

---

## Governance judgment

The current fleet is valid for internal use.

However, the fleet is now large enough that metric provenance must become explicit before broader lane expansion or downstream consumer integration.

The right move is not to halt progress.

The right move is to preserve v1 operability while adding an explicit governance layer for metric meaning.

---

## Proposed policy changes

## 1. Add explicit metric provenance

Each lane record should declare the provenance of its metric values.

### Proposed field

`metric_provenance`

### Initial allowed values

- `instrument_derived`
- `benchmark_derived`
- `operator_judged`
- `mixed`

### Intent

This field answers:

- how were these values produced
- what level of evidentiary confidence should downstream consumers assume

### Expected immediate mapping

- `continuity-progression-reasoning` → `instrument_derived`
- `lore-safe-proofreading` → `operator_judged`
- `general-grammar-cleanup` → `operator_judged`

---

## 2. Preserve current metric fields in the short term

The current required metric fields should remain operational in the near term so the existing fleet does not break.

Current fields:

- `schema_reliability`
- `false_positive_rate`
- `surface_detection_rate`

### Interim rule

These fields may remain populated for all current lanes, but they must not be treated as equally comparable across lane types unless provenance and semantics align.

---

## 3. Add an explicit comparability rule

Future consumers, including ForgeCommand, must not assume cross-lane equivalence from shared numeric field names alone.

### Rule

A lane metric may be compared directly only when all of the following are true:

- lane type is compatible
- metric semantics are aligned
- provenance class is aligned
- evaluation basis is materially comparable

If those conditions are not met, the metric is visibility-only and not comparison-safe.

---

## 4. Require explicit narrative disclosure until schema support lands

Until the schema formally includes provenance and metric semantics support, any lane using qualitative or judgment-derived approximations must say so explicitly in `current_judgment`.

### Required interim disclosure

The lane record must state that the metric values are:

- qualitative, operator-derived, or approximation-based
- not instrument-equivalent to frozen-case-pack detection metrics

This is required for editing lanes until the schema evolves.

---

## 5. Prepare for lane-type-specific metric profiles later

The long-term direction should allow different lane types to carry different primary metrics when necessary.

### Example direction

Detection / reasoning lanes may eventually use metrics such as:

- detection rate
n- suppression success
- schema adherence
- structured output reliability

Editing / proofreading lanes may eventually use metrics such as:

- minimal-edit compliance
- unnecessary rewrite rate
- lore-protection reliability
- operator acceptance rate
- regression incidence

This plan does not require that redesign now.

It only establishes that a later schema revision may need metric profiles by lane type.

---

## Proposed schema evolution path

## Phase 1 — governance clarification without breaking v1

Actions:

- keep the current schema operational
- add governance documentation for provenance and comparability
- require explicit disclosure in `current_judgment` for approximation-backed lanes

Outcome:

- no fleet breakage
- better interpretability
- no false claims of metric equivalence

## Phase 2 — additive schema revision

Actions:

- add `metric_provenance` as a governed field
- optionally add `metric_semantics_note` or equivalent explanatory field
- update validator accordingly

Outcome:

- machine-readable provenance
- safer downstream UI and ingest behavior

## Phase 3 — lane-type metric normalization

Actions:

- define lane-type-aware metric sets or profiles
- decide which metrics are universal and which are lane-specific
- document comparison rules formally

Outcome:

- stable multi-lane analytics surface
- clearer fleet-wide interpretation
- stronger ForgeCommand integration posture

---

## Acceptance criteria

This plan is considered satisfied when:

1. The governance gap is explicitly documented.
2. The fleet remains valid without breaking current records.
3. Editing lanes clearly disclose approximation-based metric origin.
4. A defined path exists for machine-readable provenance.
5. Future consumers are explicitly prevented from assuming direct numeric comparability across incompatible lanes.

---

## Recommended immediate implementation order

1. Lock this governance position in documentation.
2. Ensure editing lane `current_judgment` text explicitly states approximation-based metric origin.
3. Keep current schema and validator unchanged for the immediate term.
4. Draft the additive schema revision for `metric_provenance`.
5. Update validator only after the field contract is approved.

---

## Operator guidance

Until provenance becomes machine-readable, use this interpretation rule:

- continuity lane metrics may be treated as instrument-grounded lane evidence
- editing lane metrics may be treated as operational guidance only, not hard-comparable scoring

Do not present these as equivalent evidence classes in future dashboards, summaries, or ingest consumers.

---

## Compact decision

The lane fleet is valid.

The metric surface is not yet semantically normalized across lane types.

The immediate answer is not to stop using the fleet.

The immediate answer is to make provenance explicit, preserve v1 operability, and evolve toward lane-type-aware metric meaning in a controlled additive way.

---

## Next likely artifact

A natural follow-on artifact after this plan is:

**Schema Change Draft v1 — Add `metric_provenance` to lane analytics records**

