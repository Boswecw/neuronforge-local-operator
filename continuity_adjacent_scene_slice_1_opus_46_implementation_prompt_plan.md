# Continuity Adjacent-Scene Slice 1 — Opus 4.6 Implementation Prompt / Plan

## Artifact Type
Implementation prompt and execution plan

## Status
Draft v1.0

## Purpose
Define the first implementation slice for the `continuity-progression-reasoning` lane.

This artifact is intended to be handed to Opus 4.6 to implement the first thin end-to-end governed path.

The goal is **not** to build the whole lane.

The goal is to implement one narrow, fully governed vertical slice:

**`analyze.continuity.adjacent_scene.v1`**

This slice must prove:

- contract-first execution
- strict structured output validation
- candidate-only posture
- fail-closed behavior
- bounded adjacent-scene reasoning only
- reviewer-facing utility for Bloom

---

# 1. Build objective

Implement the first live continuity/progression reasoning slice for NeuronForge.

That slice is:

- **task id:** `analyze.continuity.adjacent_scene.v1`
- **family:** `analysis`
- **scope:** adjacent scene only
- **trust posture:** candidate-only
- **route class:** `HIGH_QUALITY_LOCAL`
- **strictness:** strict structured output required

This slice must accept a bounded adjacent-scene packet, run through the NeuronForge contract path, validate structured output, fail closed when output is malformed or out of scope, and return a reviewer-usable candidate artifact.

---

# 2. Non-goals

Do **not** implement any of the following in this slice:

- scene-window execution
- chapter-window execution
- automatic canonical truth updates
- Bloom-side ranking sophistication beyond basic rendering
- ANVIL-side integration beyond preserving compatibility
- generalized continuity analysis across arbitrary document spans
- prompt experimentation framework
- model bakeoff automation
- silent fallback to unstructured text on schema failure

If a requested change expands beyond the first thin slice, stop and note it explicitly.

---

# 3. Required outcome

At the end of this slice, the system must be able to:

1. accept a bounded adjacent-scene input packet
2. execute the task under `HIGH_QUALITY_LOCAL`
3. call one configured local model profile
4. require strict structured candidate output
5. validate the output against the continuity candidate schema
6. fail closed if output is malformed, missing evidence, violates candidate posture, or exceeds scope
7. return a candidate artifact envelope usable by Bloom
8. preserve run metadata needed for later worksheet-based review

---

# 4. Implementation doctrine

## 4.1 Contract first

The implementation must be driven by the task contract, not by ad hoc prompt wiring.

UI or consumer code must depend on the task contract and structured response shape, not on prompt details.

## 4.2 Candidate-only posture

All findings are candidates for review.

The implementation must not use authority language, canonical write paths, or silent promotion behavior.

## 4.3 Fail closed

Malformed, weak, missing, or out-of-scope structured output must fail closed.

Do not silently downgrade to prose.
Do not silently coerce bad output into success.

## 4.4 Bounded scope only

This slice is adjacent-scene only.

The model must not be allowed to reason beyond the provided packet.

## 4.5 Thin vertical slice

Implement the minimum coherent path end to end.

Do not broaden horizontally before the slice works and is testable.

---

# 5. Deliverables

Implement the following concrete deliverables.

## 5.1 Task contract

Add the first live task contract for:

- `analyze.continuity.adjacent_scene.v1`

Define request and response structures clearly and version them.

## 5.2 Schema validator

Implement strict validation for the response object.

Validation must reject:

- malformed top-level objects
- missing required fields
- invalid enums
- missing evidence objects
- authority-language leakage where candidate framing is required
- invalid scope declarations
- unsupported confidence fields

## 5.3 Lane executor path

Add the backend execution path for this task.

It should:

- accept the request packet
- route through the configured local model profile
- bind the hidden prompt/profile behind the contract
- parse the returned structured output
- validate it
- produce either a valid candidate artifact envelope or a fail-closed result

## 5.4 Candidate artifact envelope

Return a clean envelope that includes at minimum:

- task id
- contract version
- route class
- model/profile id
- scope label
- candidate findings
- validation result
- run metadata
- failure reason if fail-closed

## 5.5 Bloom-facing rendering surface

Expose the result in the simplest useful reviewer-facing form.

Minimum display should show:

- finding label/type
- candidate claim
- scope
- evidence basis
- confidence
- uncertainty note
- review note

No canonicality language.
No “this is true” framing.

## 5.6 Test coverage

Add tests for:

- valid structured success
- malformed response hard fail
- missing evidence hard fail
- out-of-scope claim rejection
- authority-language rejection if applicable in schema rules
- fail-closed envelope behavior
- minimal Bloom rendering compatibility

---

# 6. Suggested implementation order

## Step 1 — inspect and anchor existing control surfaces

Before changing code, inspect the existing repo surfaces for:

- contract/type definitions
- task routing
- model profile binding
- structured parsing/validation
- candidate artifact envelope patterns
- Bloom consumer rendering path

Do not invent parallel infrastructure if an existing contract/runtime path already exists.

## Step 2 — add contract types

Implement the typed request/response structures for `analyze.continuity.adjacent_scene.v1`.

The request should capture only what is needed for bounded adjacent-scene reasoning.

Recommended request fields:

- task id
- scope label
- scene packet id
- adjacent scene A text
- adjacent scene B text
- optional packet metadata
- candidate-only mode flag if your architecture uses explicit posture flags

Recommended response fields:

- task id
- scope label
- findings array
- validation metadata
- route metadata
- model/profile metadata
- run metadata

Each finding should include at minimum:

- finding id
- finding type
- scope type
- candidate claim
- evidence array
- confidence
- uncertainty note
- review note

## Step 3 — bind schema validator

Add strict validation for the full response and each finding.

Validator should reject:

- empty findings when the overall result shape requires explanatory no-finding handling
- evidence objects with missing anchors
- unknown finding types
- scope mismatches
- bad confidence representation
- prohibited language or fields where required

## Step 4 — implement executor path

Build the first real execution path for this task.

That path should:

- receive request
- resolve route class
- resolve local model/profile
- construct bounded model input
- request structured output
- parse output
- validate output
- return validated candidate artifact or fail-closed response

## Step 5 — implement fail-closed behavior

Make failure explicit and traceable.

Failure response should still be structured.

It should include:

- task id
- run id
- route class
- validation failure state
- failure reason
- zero promoted findings

## Step 6 — implement minimal Bloom rendering

Render valid candidate findings in Bloom with emphasis on:

- bounded scope
- evidence visibility
n- candidate framing
- uncertainty visibility

Avoid adding ranking, automation, or complex workflow behavior in this slice.

## Step 7 — add tests

Add unit and slice-level tests covering success and hard-fail behavior.

Prefer tests that mirror the lane doctrine, not generic parse tests only.

---

# 7. Acceptance criteria

This slice is complete only when all of the following are true.

## 7.1 Contract criteria

- a versioned task contract exists for `analyze.continuity.adjacent_scene.v1`
- the contract is typed and discoverable in the runtime path
- consumer code uses the contract, not prompt assumptions

## 7.2 Validation criteria

- structured output is validated strictly
- invalid schema fails closed
- missing evidence fails closed
- out-of-scope output fails closed
- bad candidate posture fails closed if detectable by rules

## 7.3 Runtime criteria

- the executor route works end to end for one configured local model profile
- valid output produces a candidate artifact envelope
- invalid output produces a fail-closed structured failure envelope

## 7.4 Consumer criteria

- Bloom can render the candidate artifact without implying canonical truth
- rendering exposes scope, evidence, and uncertainty clearly

## 7.5 Test criteria

- tests cover both valid and invalid paths
- tests confirm fail-closed behavior
- tests confirm no silent prose fallback

---

# 8. Engineering constraints

Follow these constraints during implementation.

## 8.1 Respect existing architecture

Prefer extending existing paths over inventing duplicate systems.

## 8.2 Keep prompt/profile behind the contract

Do not let UI or consumer code couple to prompt text.

## 8.3 Keep it small

Do not implement scene-window or generalized lane orchestration in this slice.

## 8.4 Make failure legible

A structured failure is better than a fake success.

## 8.5 Preserve future comparability

Record enough metadata so first-pass challenger evaluation can later use this path with the frozen case pack and worksheet.

---

# 9. Recommended file/work areas to inspect first

Inspect repo areas related to:

- task contract definitions
- schema/type validators
- model profile / route resolution
- NeuronForge execution handlers
- Bloom candidate artifact rendering
- run metadata / logging surfaces

Use the repo’s existing naming and architecture patterns where possible.

---

# 10. Expected implementation output format

When completing the work, report back in this structure:

## A. Files changed
List each file and why it changed.

## B. Contract path implemented
Describe the concrete runtime path from request to validated response.

## C. Validation behavior
List what fails closed and how.

## D. Bloom rendering behavior
Describe what a reviewer now sees.

## E. Tests added
List tests and what each one proves.

## F. Remaining gaps
List what is intentionally deferred to later slices.

---

# 11. Suggested slice name

Use a name like:

**Slice 1 — Adjacent-Scene Continuity Contract Path**

That keeps the scope explicit and the implementation burden bounded.

---

# 12. Direct build prompt for Opus 4.6

Implement **Slice 1 — Adjacent-Scene Continuity Contract Path** for NeuronForge.

Build the first thin end-to-end governed path for the `continuity-progression-reasoning` lane using the task contract:

- `analyze.continuity.adjacent_scene.v1`

Requirements:

- contract-first implementation
- strict structured response validation
- candidate-only findings
- adjacent-scene scope only
- `HIGH_QUALITY_LOCAL` route only
- fail closed on malformed, weak, or out-of-scope output
- minimal Bloom reviewer rendering for valid candidate findings
- tests for valid success and fail-closed behavior

Do not implement scene-window, chapter-window, canonical writes, silent fallbacks, or broad lane orchestration.

Use existing repo architecture patterns wherever possible.

At completion, report:

- files changed
- runtime path implemented
- validation behavior
- rendering behavior
- tests added
- deferred items

---

# 13. Operator note

This slice is successful if it proves the lane can exist as a real governed runtime path.

It does **not** need to prove the best model yet.

Model evaluation comes after the slice is live enough to execute against the frozen case pack.

