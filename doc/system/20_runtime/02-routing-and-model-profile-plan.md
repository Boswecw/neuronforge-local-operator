# NeuronForge Local Routing and Model Profile Plan

## Status
Draft v1.0

## Purpose
Define the routing and model profile layer for NeuronForge Local.

This document answers the question the task contract taxonomy deliberately left open: **which model class should execute which contract family, under what hardware constraints, with what fallback rules.**

It builds directly on the contract taxonomy (v1) and the current operational reality of NeuronForge's lane-governed evaluation workspace.

This is a control-surface artifact, not an implementation spec.

---

## 1. Why this artifact exists

The task contract taxonomy defines:

- what tasks exist
- what structure they require
- what strictness they enforce
- what degraded modes they honor

It does not define:

- which model class is appropriate for each contract family
- what hardware floor is assumed
- when fallback is acceptable vs unsafe
- when a task must fail closed instead of running on a weaker model

Without this layer, NeuronForge risks:

- running extraction contracts on models that cannot produce reliable structure
- defaulting every task to the heaviest available model
- hiding quality degradation behind successful HTTP 200s
- losing the lane-governed trust discipline that currently works

---

## 2. Route classes

NeuronForge Local defines three route classes. A route class is a capability tier, not a specific model.

### 2.1 `FAST_LOCAL`

Purpose:

- low-latency, low-cost tasks where structural fidelity matters less than speed

Characteristics:

- models in the 3B–7B parameter range
- load time under 5 seconds on target hardware
- inference latency under 10 seconds for typical inputs
- quantized model residency footprint under 2 GiB

Note: residency footprint refers to the quantized model artifact size on disk and approximate GPU/RAM allocation for inference. It does not include Ollama runtime overhead, context window allocation, or system memory pressure from other processes. Real operational memory consumption will be higher.

Typical contract families:

- `ADVISORY_TEXT` tasks
- lightweight formatting normalization
- simple cleanup where precision is non-critical

### 2.2 `WORKHORSE_LOCAL`

Purpose:

- the default route for most governed contract execution

Characteristics:

- models in the 7B–14B parameter range
- load time under 15 seconds on target hardware
- inference latency under 60 seconds for typical inputs
- quantized model residency footprint 2–4 GiB

Typical contract families:

- proofreading (lore-safe, general grammar, minimal edit)
- constrained transformation
- lightweight analysis

This is the route class where current lane baselines operate. `qwen2.5:14b` is the current workhorse baseline across both active lanes.

### 2.3 `HIGH_QUALITY_LOCAL`

Purpose:

- structured extraction and reasoning-intensive analysis where output schema fidelity is critical

Characteristics:

- models in the 14B–32B parameter range, or reasoning-enhanced models at 14B
- load time under 30 seconds on target hardware
- inference latency under 120 seconds for typical inputs
- quantized model residency footprint 4–8 GiB

Typical contract families:

- `STRUCTURED_CANDIDATE` extraction (beats, entities, scene signals)
- `STRUCTURED_ANALYSIS` (continuity, pacing, voice)
- `STRICT_STRUCTURED` tasks for ANVIL/Bloom integration

This is the route class that ANVIL/Bloom's extraction and analysis contracts will require.

---

## 3. Hardware doctrine

### 3.1 Reference target: March 2026 midlevel laptop

The current operational floor:

- 16 GB system RAM
- integrated or entry-level discrete GPU (4–8 GB VRAM)
- NVMe SSD
- single local model loaded at a time via Ollama
- available memory for model: approximately 3–4 GiB typical, with observed failures at 2.5 GiB for 14B models

This is the floor, not the ceiling.

### 3.2 Expected next-quarter norm

By mid-2026, reasonable expectation:

- 32 GB system RAM becoming common on developer-class laptops
- 8–12 GB VRAM on midrange discrete GPUs
- quantized 14B models comfortable
- quantized 32B models feasible but not assumed

### 3.3 Default vs selective doctrine

**Default route must be safe on current hardware.**

This means:

- `WORKHORSE_LOCAL` is the default route class
- `HIGH_QUALITY_LOCAL` is selective, not default
- `FAST_LOCAL` is available for advisory tasks but not trusted for governed lanes
- no contract should silently assume hardware above the March 2026 floor

**Selective escalation:**

- `HIGH_QUALITY_LOCAL` is used only when the contract family requires it
- the runtime must verify model availability before accepting a `HIGH_QUALITY_LOCAL` task
- if the model cannot load, the task must fail with explicit degraded status, not silently downgrade

---

## 4. Contract-to-route mapping

### 4.1 Proofreading family

| Contract | Preferred route | Minimum acceptable | Fallback policy |
|----------|----------------|-------------------|-----------------|
| `proofread.lore_safe.v1` | `WORKHORSE_LOCAL` | `WORKHORSE_LOCAL` | fail closed |
| `proofread.minimal_edit.v1` | `WORKHORSE_LOCAL` | `WORKHORSE_LOCAL` | fail closed |
| `cleanup.general_grammar.v1` | `WORKHORSE_LOCAL` | `FAST_LOCAL` | degraded allowed |

Proofreading contracts are the current operational core. They run on the workhorse route because they require enough model capability to preserve meaning, tone, and protected terms. Lore-safe and minimal-edit have no gap between preferred and minimum — the workhorse route is both preferred and required, because precision is the contract obligation. Grammar cleanup tolerates a lower minimum because its broader edit tolerance absorbs reduced model capability.

### 4.2 Extraction family

| Contract | Preferred route | Minimum acceptable | Fallback policy |
|----------|----------------|-------------------|-----------------|
| `extract.beat_candidates.scene.v1` | `HIGH_QUALITY_LOCAL` | `HIGH_QUALITY_LOCAL` | fail closed |
| `extract.entity_candidates.scene.v1` | `HIGH_QUALITY_LOCAL` | `HIGH_QUALITY_LOCAL` | fail closed |
| `extract.scene_signals.descriptive.v1` | `HIGH_QUALITY_LOCAL` | `WORKHORSE_LOCAL` | degraded allowed |
| `extract.scene_signals.integration.v1` | `HIGH_QUALITY_LOCAL` | `HIGH_QUALITY_LOCAL` | fail closed |

Extraction contracts exist to feed ANVIL and Bloom with structured candidate artifacts. A model that cannot reliably produce schema-conformant output with evidence spans is worse than no output at all. Beat and entity extraction must fail closed because a malformed candidate is more dangerous than an absent one.

Scene signals are split into two levels:

- **Descriptive scene signals** (mood, tension, conflict presence, POV cues) are advisory observations. They tolerate fallback to workhorse with degraded flag because downstream consumers treat them as soft input.
- **Integration-feeding scene signals** (signals directly consumed by ANVIL/Bloom structural logic) must fail closed. These signals become structural inputs, and a malformed signal corrupts downstream state the same way a malformed beat candidate would.

### 4.3 Analysis family

| Contract | Preferred route | Minimum acceptable | Fallback policy |
|----------|----------------|-------------------|-----------------|
| `analyze.continuity.scene_window.v1` | `HIGH_QUALITY_LOCAL` | `WORKHORSE_LOCAL` | degraded allowed |
| `analyze.pacing.scene_window.v1` | `WORKHORSE_LOCAL` | `FAST_LOCAL` | degraded allowed |
| `analyze.voice.scene.v1` | `HIGH_QUALITY_LOCAL` | `WORKHORSE_LOCAL` | degraded allowed |

Analysis contracts are advisory by default. This means fallback is generally acceptable as long as the degraded mode is explicit. Continuity and voice analysis benefit from reasoning-capable models but can return useful lower-confidence results from workhorse models.

### 4.3.1 Scope-width escalation rule

Route class requirements for analysis contracts are not fixed — they escalate with scope width.

| Scope | Route class floor |
|-------|-------------------|
| single scene | contract default (see table above) |
| multi-scene window (2–5 scenes) | `WORKHORSE_LOCAL` minimum |
| chapter-window or cross-chapter | `HIGH_QUALITY_LOCAL` minimum |

This matters because continuity, pacing, and Bloom-style reasoning across wider windows demand more context handling and multi-step inference than single-scene analysis. A workhorse model can produce useful single-scene pacing observations, but chapter-window continuity analysis on a fast model will produce noise, not signal.

The runtime must check scope width at task acceptance and escalate the minimum acceptable route accordingly. If the escalated route is unavailable, the task must follow its fallback policy at the escalated level, not the base level.

### 4.4 Transformation family

| Contract | Preferred route | Minimum acceptable | Fallback policy |
|----------|----------------|-------------------|-----------------|
| `transform.rewrite_constrained.v1` | `WORKHORSE_LOCAL` | `WORKHORSE_LOCAL` | fail closed |
| `transform.normalize_formatting.v1` | `FAST_LOCAL` | deterministic | deterministic fallback |

Formatting normalization may be achievable deterministically. If so, it should not consume an inference route at all.

### 4.5 Deterministic-first gate

**If a task can be solved deterministically with equal or better reliability, it must not consume an inference route.**

This is a general rule, not specific to formatting normalization. Before routing any task to inference, the runtime should check whether a deterministic path exists that satisfies the contract. Examples:

- formatting normalization (regex, AST transforms)
- whitespace cleanup
- encoding normalization
- known-pattern substitution from a governed dictionary

A deterministic path that meets the contract is always preferred over an inferential path, because it is faster, cheaper, reproducible, and does not consume model residency. The deterministic path should still return a valid response envelope with `route_class: DETERMINISTIC` and appropriate provenance (`deterministic_derived`).

This rule protects NeuronForge from becoming a lazy AI wrapper around things that should just be code.

### 4.6 Mapping summary

| Route class | Contract families | Fail-closed contracts |
|-------------|-------------------|----------------------|
| `FAST_LOCAL` | advisory text, formatting, grammar cleanup fallback | none |
| `WORKHORSE_LOCAL` | proofreading, pacing analysis, constrained transforms | lore-safe, minimal-edit, constrained rewrite |
| `HIGH_QUALITY_LOCAL` | extraction (beats, entities), continuity, voice | beat extraction, entity extraction |

---

## 5. Model candidate posture

### 5.1 Current operational baseline

`qwen2.5:14b` via Ollama is the confirmed baseline for both active lanes (lore-safe proofreading, general grammar cleanup). It occupies the `WORKHORSE_LOCAL` route class.

This is not a global endorsement. It is a lane-specific, evaluation-backed judgment. The model won its position through structured challenger evaluation, not assumption.

### 5.2 Where `qwen2.5:14b` fits

- `WORKHORSE_LOCAL` route class
- proofreading and cleanup contracts
- lightweight analysis contracts (pacing)
- constrained transformation contracts

It is the right default for tasks where text preservation and grammatical precision matter more than deep structural reasoning.

### 5.3 Where `phi4-reasoning:latest` fits

- `HIGH_QUALITY_LOCAL` route class candidate
- extraction contracts requiring structured schema output
- analysis contracts requiring multi-step reasoning (continuity, voice)
- any `STRICT_STRUCTURED` task where schema conformance is mandatory

`phi4:14b` was evaluated as a challenger in proofreading lanes and rejected — it showed more literary normalization than `qwen2.5:14b` and failed harder test cases. However, proofreading is not where reasoning models justify their cost. Extraction and analysis contracts are.

`phi4-reasoning:latest` should be evaluated as a `HIGH_QUALITY_LOCAL` candidate specifically for:

- beat candidate extraction
- entity candidate extraction
- continuity analysis

It should not be evaluated as a proofreading replacement. Different contract families may have different baselines.

### 5.4 Where Qwen fits beyond current use

`qwen2.5:14b` is the current workhorse. Larger Qwen variants (32B) could serve as `HIGH_QUALITY_LOCAL` candidates when hardware allows, but they are not assumed safe on current hardware.

Smaller Qwen variants (`qwen2.5:7b`) were evaluated and showed more phrasing drift than the 14B baseline. They fit the `FAST_LOCAL` route class for advisory tasks but should not be trusted for governed lanes.

### 5.5 Where smaller/faster models fit

Models in the 3B–7B range (`gemma3:4b`, `qwen2.5:7b`, `llama3.1:8b`) occupy the `FAST_LOCAL` route class.

They are appropriate for:

- `ADVISORY_TEXT` strictness tasks
- formatting normalization where inference is optional
- grammar cleanup fallback with explicit degraded flag

They are not appropriate for:

- any governed lane baseline
- any extraction contract
- any analysis contract beyond trivial observations

### 5.6 Adapter-enhanced routes

The general grammar adapter readiness plan already defines gates for QLoRA experimentation:

- prompt plateau proof required first
- 50–150 gold dataset pairs minimum
- held-out evaluation set mandatory

Adapter-enhanced routes should be treated as a future extension of the `WORKHORSE_LOCAL` route class, not as a separate route class. An adapted model is still a workhorse model — it just has lane-specific tuning.

Adapter readiness should be considered per-lane, not globally. A lane that has proven prompt plateau and has sufficient gold data may justify adapter experimentation. A lane that is still improving through prompt iteration should not.

No extraction or analysis lane should pursue adapters before proving the base model route is insufficient.

---

## 6. Fallback and rejection rules

### 6.1 When fallback is acceptable

Fallback from a higher route class to a lower one is acceptable when:

- the contract strictness is `ADVISORY_TEXT` or `TEXT_PLUS_METADATA`
- the task is advisory, not integration-feeding
- the response envelope includes explicit degraded mode metadata
- the caller can interpret degraded results safely

### 6.2 When fallback is unsafe

Fallback is unsafe and the task must fail closed when:

- the contract strictness is `STRICT_STRUCTURED` and the fallback model cannot reliably produce schema-conformant output
- the contract is lane-governed with a locked baseline and the fallback model is not the baseline
- the extraction output feeds ANVIL or Bloom integration where malformed candidates corrupt downstream state
- the task has `fail_closed` fallback policy in its contract definition

### 6.3 When structured tasks must return degraded instead of fake success

A structured task must return degraded status rather than attempt execution when:

- the required model is unavailable (not loaded, insufficient memory)
- the loaded model is a lower route class than the contract requires
- the model produces output that fails schema validation
- the model produces output with confidence below the contract minimum threshold

The response must include:

- `degraded_mode: true`
- `degraded_reason` (model unavailable, schema validation failed, confidence below threshold)
- `route_class_requested` vs `route_class_actual`

### 6.4 Schema validation failure is contract failure

For contracts with `STRUCTURED_CANDIDATE`, `STRUCTURED_ANALYSIS`, or `STRICT_STRUCTURED` strictness:

- schema validation failure after inference is a **contract failure**, not a soft warning
- it must never be normalized into a successful response with reduced confidence
- the response must carry `contract_status: FAILED` with `failure_reason: schema_validation`
- for `STRICT_STRUCTURED` contracts specifically, schema failure is equivalent to task non-execution — there is no partial credit

This is distinct from low confidence, which is a valid degraded result. A low-confidence structured response that conforms to schema is degraded. A response that does not conform to schema is failed. The distinction matters because consumers may tolerate degraded results but must never silently ingest structurally invalid ones.

### 6.5 Hard rule

**A successful response with wrong structure is worse than an explicit failure.**

No contract should return HTTP 200 with prose where schema was required. No contract should silently substitute a lower-capability model and pretend the output has the same trust level.

This is the routing equivalent of the candidate-not-authority rule: the system must not lie about what it did.

---

## 7. Route selection at runtime

### 7.1 Selection sequence

When a task request arrives:

1. Identify the contract family and task type
2. Look up the required route class from the contract-to-route mapping
3. Check whether the required model is available and loaded
4. If available: execute on the required route
5. If unavailable: check the fallback policy
   - if fallback allowed: execute on fallback route with degraded flag
   - if fail closed: return explicit failure with `model_unavailable` reason
6. After execution: validate output against contract schema
7. If validation fails: return degraded status regardless of model used

### 7.2 Model loading policy

Current reality is single-model-at-a-time via Ollama. This means:

- route class transitions require model swap
- model swap has real latency cost (5–30 seconds)
- a batch of tasks should be grouped by route class where possible
- the runtime should not swap models mid-task

Future multi-model capability (more RAM, GPU offload) would relax this constraint but should not be assumed.

### 7.3 Route visibility

The response envelope already requires `route_class` and `model_id`. This plan adds:

- `route_class_requested` — what the contract mapping specified
- `route_class_actual` — what actually executed
- `model_swap_occurred` — whether a model load was required

This supports operational observability without requiring the caller to know internal model details.

---

## 8. Forge-wide route-layer rule

AuthorForge is the first contract consumer, but route classes are defined at the Forge-runtime level and must remain app-agnostic.

This means:

- route class definitions (`FAST_LOCAL`, `WORKHORSE_LOCAL`, `HIGH_QUALITY_LOCAL`, `DETERMINISTIC`) belong to NeuronForge, not to AuthorForge
- contract-to-route mappings may be app-specific (AuthorForge may map `extract.beat_candidates` differently than a future DataForge consumer would), but the route classes themselves are shared
- no route class definition should encode assumptions about literary content, narrative structure, or AuthorForge-specific semantics
- app-specific routing preferences should be expressed as contract metadata, not as route-class modifications

When other Forge apps begin consuming NeuronForge contracts, they should find the route-class layer ready without requiring architectural changes. The task contracts may differ, but the routing substrate should not.

---

## 9. What this plan does not cover

This plan deliberately excludes:

- **Specific model version pinning** — that is a lane governance decision, not a routing decision
- **Prompt selection** — prompts are behind the contract boundary, managed by lane baselines
- **Remote/cloud routing** — NeuronForge Local is local-first; cloud fallback is a separate architectural decision
- **Multi-GPU orchestration** — out of scope for midlevel laptop doctrine
- **Model training or fine-tuning execution** — the adapter readiness plan covers gates; this plan covers routing

---

## 10. Relationship to other artifacts

| Artifact | Relationship |
|----------|-------------|
| Task Contract Taxonomy v1 | This plan maps contracts to routes. The taxonomy defines what; this plan defines how. |
| Lane governance (lore-safe, general grammar) | Lanes own baseline model selection. This plan defines the route class envelope lanes operate within. |
| Adapter readiness plan | Adapters extend the workhorse route class. This plan defines when adapter pursuit is justified. |
| Lane analytics schema | Analytics track per-lane model outcomes. Route class adds a grouping dimension to analytics. |
| Runtime architecture | This plan feeds the routing logic the runtime must implement. |

---

## 11. Working definition

Use this shorthand going forward:

**NeuronForge route classes are hardware-aware capability tiers that map contract families to model classes, enforce fail-closed discipline for structured tasks, and preserve lane-governed baseline trust — with workhorse local as the safe default and high-quality local as selective escalation for extraction and reasoning contracts.**
