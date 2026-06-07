# Task Contract: analyze.continuity.adjacent_scene.v1

Date: 2026-04-16

## Identity

- **task_id:** `analyze.continuity.adjacent_scene.v1`
- **contract_version:** `1.0`
- **family:** `analysis`
- **lane_id:** `continuity-progression-reasoning`
- **scope:** `adjacent_scene`
- **trust_posture:** `candidate_only`
- **route_class:** `HIGH_QUALITY_LOCAL`
- **strictness:** `STRICT_STRUCTURED`
- **fallback_policy:** `fail_closed`

---

## Purpose

Accept a bounded two-scene packet and return a strict structured candidate artifact containing continuity and progression findings for reviewer consideration.

This task now supports optional first-wave precomputed-context lineage carriage for connected requests.

---

## Non-goals for v1

This contract does not support:

- scene-window or chapter-window execution
- automatic canonical writes
- silent prose fallback on schema failure
- promotion or lifecycle management

---

## Request shape

```json
{
  "task_id": "analyze.continuity.adjacent_scene.v1",
  "scope_label": "adjacent_scene",
  "scene_packet_id": "<string>",
  "scene_a_id": "<string>",
  "scene_b_id": "<string>",
  "scene_a_text": "<string>",
  "scene_b_text": "<string>",
  "task_intent_id": "<string, optional>",
  "context_bundle_id": "<string, optional>",
  "context_bundle_hash": "<string, optional>",
  "context_manifest_ref": "<string, optional>",
  "context_payload_ref": "<string, optional>",
  "packet_metadata": {}
}
```

### Required request fields

| Field | Type | Description |
|-------|------|-------------|
| `task_id` | string | Must be `analyze.continuity.adjacent_scene.v1` |
| `scene_a_id` | string | Identifier for the first (earlier) scene |
| `scene_b_id` | string | Identifier for the second (later) scene |
| `scene_a_text` | string | Full text of scene A |
| `scene_b_text` | string | Full text of scene B |

### Optional request fields

| Field | Type | Description |
|-------|------|-------------|
| `scope_label` | string | Defaults to `adjacent_scene` |
| `scene_packet_id` | string | Identifier for this analysis packet |
| `packet_metadata` | object | Operator notes, chapter context, etc. |
| `task_intent_id` | string | Connected upstream task intent id |
| `context_bundle_id` | string | Connected upstream context bundle id |
| `context_bundle_hash` | string | Connected upstream context bundle content hash |
| `context_manifest_ref` | string | Optional provenance pointer to a context manifest |
| `context_payload_ref` | string | Optional provenance pointer to a context payload |

### Context-lineage completeness rule

The task accepts either:

1. a legacy/local packet with none of `task_intent_id`, `context_bundle_id`, `context_bundle_hash`, or
2. a connected packet with all three present.

Partial presence of those three lineage fields is a hard fail-closed intake error.

If `context_manifest_ref` or `context_payload_ref` is present, the request must also carry all three connected lineage fields.

---

## Candidate artifact envelope shape

On success, the executor returns a candidate artifact envelope:

```json
{
  "task_id": "analyze.continuity.adjacent_scene.v1",
  "contract_version": "1.0",
  "route_class": "HIGH_QUALITY_LOCAL",
  "model_id": "<model-name>",
  "run_id": "<run-id>",
  "timestamp": "<ISO 8601 UTC>",
  "scene_packet_id": "<string>",
  "scope_label": "adjacent_scene",
  "task_intent_id": "<string, optional>",
  "context_bundle_id": "<string, optional>",
  "context_bundle_hash": "<string, optional>",
  "envelope_status": "valid_candidate",
  "candidate_findings": [...],
  "overall_run_note": "<string>",
  "validation_result": {
    "validation_result": "valid",
    "schema_version_checked": "1.0",
    "validated_at": "<ISO 8601 UTC>",
    "findings_count": 0
  },
  "run_metadata": {
    "prompt_file": "prompts/continuity-adjacent-scene-v3.md",
    "request_file": "<path>",
    "raw_output_file": "<path>",
    "context_manifest_ref": "<string, optional>",
    "context_payload_ref": "<string, optional>"
  }
}
```

### Envelope status values

| Value | Meaning |
|-------|---------|
| `valid_candidate` | Schema passed; findings are valid candidates for review |
| `fail_closed` | Intake failed, schema failed, or model failed; no findings promoted |

---

## Fail-closed envelope shape

On any failure (intake failure, model failure, or schema validation failure), the executor returns a structured failure envelope:

```json
{
  "task_id": "analyze.continuity.adjacent_scene.v1",
  "contract_version": "1.0",
  "route_class": "HIGH_QUALITY_LOCAL",
  "model_id": "<model-name>",
  "run_id": "<run-id>",
  "timestamp": "<ISO 8601 UTC>",
  "scene_packet_id": "<string>",
  "scope_label": "adjacent_scene",
  "task_intent_id": "<string, optional>",
  "context_bundle_id": "<string, optional>",
  "context_bundle_hash": "<string, optional>",
  "envelope_status": "fail_closed",
  "failure_reason": "<string>",
  "candidate_findings": [],
  "validation_result": null,
  "run_metadata": {
    "prompt_file": "prompts/continuity-adjacent-scene-v3.md",
    "request_file": "<path>",
    "raw_output_file": "<path or null>",
    "context_manifest_ref": "<string, optional>",
    "context_payload_ref": "<string, optional>"
  }
}
```

Zero findings are always returned on failure. No silent coercion.

---

## Schema contract for model output

The model must return a top-level JSON object matching the continuity candidate schema v1.0.

See: `docs/continuity-progression-candidate-schema.md`

### Required top-level fields

| Field | Constraint |
|-------|-----------|
| `schema_version` | Must be `"1.0"` |
| `lane_id` | Must be `"continuity-progression-reasoning"` |
| `analysis_scope_type` | Must be `"adjacent_scene"` for this task |
| `analysis_scope_bounds` | Must include `scene_ids` array |
| `input_unit_ids` | Must be an array |
| `candidate_findings` | Must be an array (may be empty) |
| `overall_run_note` | Must be a non-empty string |
| `run_posture` | Must be `"candidate_only"` |

### Required per-finding fields

| Field | Constraint |
|-------|-----------|
| `finding_id` | Unique string, format `cpf-NNN` |
| `finding_label` | Non-empty, review-friendly string |
| `finding_type` | Approved enum value |
| `claim` | Candidate-framed; no authority language |
| `scope_type` | Approved enum; must not exceed run scope |
| `scope_bounds` | Must include `scene_ids`; must not reference out-of-scope scenes |
| `evidence_spans` | Array of at least 1 evidence object |
| `confidence` | `low`, `moderate`, or `high` |
| `uncertainty_note` | Substantive string; not "None" or empty |
| `review_note` | Actionable string; not "Review this" or empty |
| `candidate_state` | `candidate_unreviewed` for new output |

---

## Validation rules (hard-fail triggers)

The validator rejects output and triggers fail-closed if:

- Any required top-level field is missing
- `lane_id` does not match
- `schema_version` does not match
- `run_posture` is not `candidate_only`
- `analysis_scope_bounds` lacks `scene_ids`
- Any finding is missing a required field
- Any finding uses an unapproved `finding_type`
- Any finding uses an unapproved `confidence` value
- Any finding's `scope_bounds` references scenes outside the run scope
- Any finding has an empty `evidence_spans` array
- Any finding's `claim` contains authority language
- Any finding's `uncertainty_note` is empty or trivial
- Any finding's `review_note` is empty or trivial
- JSON cannot be parsed from model output

---

## Execution path

```text
request packet
  → validate required fields
  → validate context-lineage completeness
  → build model input (prompt + scene texts)
  → run HIGH_QUALITY_LOCAL model via ollama
  → extract JSON from raw output
  → validate against candidate schema v1.0
  → [fail] → fail-closed envelope (exit 1)
  → [pass] → candidate artifact envelope (exit 0)
  → log to registry (success only)
```

---

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/read-context-intake.py` | Request intake normalization and lineage validation |
| `scripts/run-continuity-adjacent-scene.sh` | Main executor |
| `scripts/validate-continuity-candidate.py` | Schema validator |
| `scripts/render-continuity-candidate.sh` | Bloom-facing Markdown renderer |

---

## Governance notes

- This remains a candidate-only contract. Context lineage is provenance, not canonical authority.
- Consumer code must bind to the contract, not prompt internals.
- Changes to required lineage behavior require contract review.
