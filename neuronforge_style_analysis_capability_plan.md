# NeuronForge — Style Analysis Capability Plan

## Objective

Enable **style analysis** as a real, contract-backed **NeuronForge capability** that AuthorForge can call safely.

This capability must live in **NeuronForge** as an AI analysis service capability.
It must **not** become AuthorForge business authority.
It must **not** return vague prose as if that were a stable machine contract.
It must remain **advisory/analysis output**, not canonical manuscript truth.

---

## Product and ownership doctrine

### NeuronForge owns
- task contract definition for style analysis
- runtime selection for the analysis task
- prompt/profile execution behind the contract
- schema validation and normalization
- explicit degraded vs failed behavior
- structured analysis output envelope
- route/service implementation for the capability

### AuthorForge owns
- deciding when to invoke style analysis
- supplying the bounded request payload
- rendering and presenting the result to the user
- deciding whether any result is promoted into workflow state
- analytics logging on the proxy side if applicable

### NeuronForge does **not** own
- manuscript truth
- project/workspace truth
- long-term domain authority
- silent promotion of style-analysis output into canonical app data

---

## Recommended first slice

Implement exactly this first:

- **contract id:** `analyze.style.scene.v1`
- **scope:** single scene only
- **task family:** analysis
- **task type:** style_analysis
- **output mode:** `STRUCTURED_ANALYSIS`
- **preferred runtime:** `WORKHORSE_LOCAL`
- **minimum runtime:** `WORKHORSE_LOCAL`
- **status posture:** success, degraded, or failed must be explicit

Why this slice:
- single-scene analysis keeps input bounded and deterministic enough for a first contract
- style analysis is already conceptually within the NeuronForge analysis family
- structured output is more durable and testable than freeform prose
- local runtime keeps the capability aligned with local-first product doctrine

---

## Capability contract

## Request envelope requirements

The request must be explicit and self-contained.
Do not rely on hidden ambient project state as the primary analysis input.

### Minimum request fields
- `request_id`
- `task_family: "analysis"`
- `task_type: "style_analysis"`
- `contract_version: "v1"`
- `source_scope: "scene"`
- `input_payload.scene_text`
- `desired_runtime_mode`
- `output_strictness: "structured"`

### Optional request fields for later
- target tone or style goals
- series voice constraints
- character POV hint
- genre expectation hint
- audience expectation hint

For the first slice, keep optional guidance narrow and bounded.

---

## Response contract

The response must be **structured** and machine-validated.
Do not treat narrative prose as contract success.

### Required envelope fields
- `route_class`
- `model_id`
- `runtime_mode_used`
- `output_payload`
- `provenance_class`
- `warnings`
- `schema_validation_status`

### Required analysis payload fields
- `summary`
- `overall_assessment`
- `dimension_scores`
- `findings`
- `recommendations`
- `confidence`
- `evidence_spans`

### Example dimension candidates
- clarity
- flow
- voice consistency
- sentence variety
- pacing at scene level
- descriptive density
- dialogue balance

These dimensions may evolve, but the first slice should freeze a small v1 set and test against it.

---

## Output truth rules

### Success
Return success only when:
- request schema is valid
- model output can be normalized into the required structure
- required fields are present
- schema validation succeeds or an explicitly allowed normalization path succeeds

### Degraded
Return degraded only when:
- route/runtime succeeds but one or more optional or lower-confidence fields are weak
- evidence spans are partial but still usable under the contract
- normalization succeeds with warnings

### Failed
Return failed when:
- request is malformed
- runtime is unavailable
- model output cannot be normalized into the contract
- output is prose-only and cannot be safely converted into the structured schema

Do not fake success on malformed output.

---

## Runtime policy

### Initial runtime posture
- preferred route class: `WORKHORSE_LOCAL`
- minimum route class: `WORKHORSE_LOCAL`
- no cloud dependency required for the first slice

### Why
Style analysis at scene scope should not require a heavyweight or cloud-only runtime unless proven otherwise.
If larger-scope style analysis is needed later, introduce a separate contract rather than widening `analyze.style.scene.v1`.

---

## Implementation phases

## Phase 0 — Contract freeze
Goal: define the capability before prompt tuning or route wiring.

Tasks:
1. add the task contract id and route policy
2. define request schema
3. define response schema
4. define degraded/failure rules
5. define the frozen v1 dimension set

Exit criteria:
- contract id exists
- schemas exist
- success/degraded/failure rules are explicit

## Phase 1 — Route and adapter implementation
Goal: make the capability callable as a real NeuronForge service.

Tasks:
1. add the style-analysis route
2. bind the route to the style-analysis contract
3. implement the runtime/adapter execution path
4. ensure request validation happens before model execution
5. ensure output normalization happens before response emission

Exit criteria:
- route exists
- route is contract-backed
- malformed requests fail closed

## Phase 2 — Normalization and validation
Goal: make raw model output safe and structured.

Tasks:
1. implement model-output normalization
2. validate against the response schema
3. emit warnings/degraded state when allowed
4. fail honestly when output cannot satisfy the contract

Exit criteria:
- prose-only output cannot silently pass as success
- degraded vs failed boundaries are explicit

## Phase 3 — Tests
Goal: prove contract truth.

Tasks:
1. schema acceptance tests for valid requests
2. rejection tests for malformed requests
3. success tests for schema-valid structured responses
4. degraded tests for partial-but-acceptable normalization
5. failure tests for unusable raw output
6. route tests proving bounded runtime behavior

Exit criteria:
- the capability is proven by contract-level tests, not just manual spot checks

## Phase 4 — AuthorForge integration readiness
Goal: make the capability safely consumable by AuthorForge.

Tasks:
1. document the endpoint and request shape clearly
2. confirm AuthorForge proxy expectations match the NeuronForge contract
3. only after capability truth exists, wire proxy-side analytics logging if desired

Exit criteria:
- AuthorForge can call a stable NeuronForge contract
- integration does not reinterpret analysis semantics on the proxy side

---

## P0 requirements

1. create `analyze.style.scene.v1`
2. freeze request schema
3. freeze response schema
4. add route binding
5. implement normalization + schema validation
6. add success/degraded/failure tests

## P1 requirements

1. refine score dimensions
2. add optional user-supplied style goals
3. improve evidence span quality
4. add richer warnings taxonomy
5. document future expansion paths such as chapter-level analysis under a separate contract

---

## Non-goals for the first slice

Do not do these yet:
- chapter or manuscript scope
- hidden project-context ingestion
- automatic manuscript rewriting
- automatic state promotion into app truth
- cloud-only implementation
- freeform essay output as the only response mode
- multi-step orchestration with unrelated capabilities

---

## Suggested route surface

Use a bounded route such as:
- `POST /api/v1/authorforge/style-analysis`

The route should:
- validate the contract envelope
- call the style-analysis adapter/runtime path
- return a structured response envelope
- never claim stronger authority than analysis/advisory output

---

## Suggested v1 response shape

```json
{
  "route_class": "WORKHORSE_LOCAL",
  "runtime_mode_used": "local",
  "model_id": "...",
  "provenance_class": "model_analysis",
  "schema_validation_status": "valid",
  "warnings": [],
  "output_payload": {
    "summary": "...",
    "overall_assessment": "...",
    "dimension_scores": {
      "clarity": 0,
      "flow": 0,
      "voice_consistency": 0,
      "sentence_variety": 0,
      "pacing": 0
    },
    "findings": [
      {
        "type": "strength",
        "label": "...",
        "detail": "..."
      }
    ],
    "recommendations": [
      {
        "priority": "medium",
        "label": "...",
        "detail": "..."
      }
    ],
    "confidence": 0.0,
    "evidence_spans": [
      {
        "start": 0,
        "end": 0,
        "reason": "..."
      }
    ]
  }
}
```

The exact schema can vary, but it must remain structured, bounded, and testable.

---

## Exact implementation prompt for Opus

Act as a senior repo-aware engineer working inside **NeuronForge**.

Your job is to implement a bounded new capability:

> **Style analysis as a contract-backed NeuronForge analysis task**

This is **not** a greenfield redesign.
This is **not** permission to turn analysis output into app business truth.
This is **not** permission to ship vague prose as if it were a stable machine contract.

## Primary objective

Implement the first safe slice of style analysis as:
- contract id: `analyze.style.scene.v1`
- scope: single scene only
- output mode: `STRUCTURED_ANALYSIS`
- runtime posture: `WORKHORSE_LOCAL`

## Required method

1. inspect current NeuronForge task taxonomy, request/response envelope rules, and analysis-family capabilities
2. add a style-analysis contract entry consistent with existing analysis-family doctrine
3. define the request schema for a bounded single-scene style-analysis request
4. define the response schema for structured analysis output
5. implement the route/service/adapter path for the capability
6. normalize raw model output into the structured schema
7. implement explicit success/degraded/failed behavior
8. add contract-level and route-level tests proving the capability truth
9. document only the specific surfaces needed to make the capability legible and stable

## Required output

Produce:
1. contract id and route policy added
2. request schema
3. response schema
4. route and adapter patch points
5. normalization behavior
6. degraded/failure rules
7. tests added/updated
8. residual risks or future expansions explicitly deferred

## Hard rules

- do not broaden this into chapter/manuscript scope
- do not rely on hidden project context as primary input
- do not emit freeform prose as the only contract output
- do not fake success when schema validation fails
- do not make the capability cloud-required for the first slice
- keep the patch small, bounded, and reviewable

## Completion standard

This task is complete only when you can prove:
- style analysis exists as a real NeuronForge capability
- it is contract-backed and schema-validated
- it returns structured analysis output rather than unstable prose
- AuthorForge can safely consume it as advisory AI output

