# NeuronForge System Documentation

**Document version:** 1.1 (2026-03-22) — analyze.style.scene.v1 promoted to candidate_baseline
**Protocol:** Forge Documentation Protocol v1

This `doc/system/` tree defines the NeuronForge Local control surface:
- Task contract taxonomy and contract doctrine
- Routing and model profile plan
- Candidate artifact doctrine
- Module-specific reasoning contract requirements
- Concrete lane plans

Assembly contract:
- Command: `bash doc/system/BUILD.sh`
- Output: `doc/nfSYSTEM.md`

| Part | File | Contents |
|------|------|----------|
| §1 | [01-task-contract-taxonomy.md](01-task-contract-taxonomy.md) | Task families, contract layering, strictness classes, degraded-mode doctrine |
| §2 | [02-routing-and-model-profile-plan.md](02-routing-and-model-profile-plan.md) | Route classes, hardware doctrine, contract-to-route mapping, fallback rules |
| §3 | [03-candidate-artifact-doctrine.md](03-candidate-artifact-doctrine.md) | Candidate artifact classes, evidence/confidence doctrine, review states, promotion rules |
| §4 | [04-anvil-bloom-reasoning-contracts.md](04-anvil-bloom-reasoning-contracts.md) | ANVIL/Bloom consumption rules, required contract posture, scope rules, failure doctrine |
| §5 | [05-scene-beat-extraction-lane-plan.md](05-scene-beat-extraction-lane-plan.md) | First concrete extraction lane: input scope, output doctrine, failure taxonomy, eval design |
| §6 | [06-continuity-progression-reasoning-lane-plan.md](06-continuity-progression-reasoning-lane-plan.md) | Cross-scene reasoning lane: scope doctrine, finding types, risk taxonomy, review rubric direction |

## Task contracts

| Contract                               | Status                              |
| -------------------------------------- | ----------------------------------- |
| `analyze.continuity.adjacent_scene.v1` | live                                |
| `analyze.style.scene.v1`               | **candidate_baseline** (2026-03-22) |

## Quick Assembly

```bash
bash doc/system/BUILD.sh   # Assembles all parts into doc/nfSYSTEM.md
```

*Last updated: 2026-03-22*

---

# NeuronForge Local Task Contract Taxonomy

## Status
Draft v1.0

## Purpose
Define the first version of NeuronForge Local task contracts.

This document translates the runtime architecture into a bounded contract taxonomy so NeuronForge does not collapse back into ad hoc prompt calls or a narrow AuthorForge-only helper.

It defines:

- contract doctrine
- shared request/response envelope rules
- task family taxonomy
- contract strictness levels
- candidate vs authority handling
- first AuthorForge-facing contract priorities
- Forge-wide reuse posture

This is a control-surface artifact, not an implementation spec.

---

## 1. Why this artifact exists

The current runtime architecture already requires:

- versioned request/response contracts
- task-family boundaries
- structured outputs for extraction and analysis
- candidate-not-authority discipline
- explicit degraded-mode signaling

That means a contract taxonomy is now the next required layer between architecture and implementation. fileciteturn5file10 fileciteturn5file11

Without this layer, NeuronForge risks sliding back into:

- prompt-per-feature drift
- app-specific one-offs
- prose-only AI outputs where structure is required
- hidden contract inconsistency across Forge apps

---

## 2. Contract doctrine

### 2.1 Core doctrine

Every NeuronForge Local task must execute through a **versioned contract**.

A contract is the bounded agreement for:

- what task is being requested
- what inputs are valid
- what outputs are allowed
- what provenance must be emitted
- what degraded behavior is acceptable

### 2.2 Why contracts matter

NeuronForge Local is now planned as a bounded local orchestration sidecar/service rather than a freeform prompt runner. Its runtime spec already requires explicit request/response envelopes, route visibility, degraded-mode signaling, and structured outputs for extraction/analysis. fileciteturn5file11 fileciteturn5file12

### 2.3 Contract first, prompt second

Prompts and profiles are implementation details behind the contract boundary.

The caller should depend on:

- the contract family
- contract version
- task type
- runtime guarantees

not on a specific hidden prompt.

---

## 3. Contract layering model

NeuronForge contracts should be understood in three layers.

### 3.1 Layer A — shared envelope layer

Applies to all tasks.

Defines:

- request id / trace id
- task family
- task type
- contract version
- lane binding if governed
- runtime mode requested / actual
- route class
- degraded mode
- provenance class
- warnings / soft-fail notes

### 3.2 Layer B — family contract layer

Defines the common semantics for a task family.

Examples:

- proofreading family rules
- extraction family rules
- analysis family rules
- transformation family rules

### 3.3 Layer C — task-specific contract layer

Defines the exact task contract for a concrete operation.

Examples:

- `proofread.lore_safe.v1`
- `cleanup.general_grammar.v1`
- `extract.beat_candidates.scene.v1`
- `analyze.continuity.scene_window.v1`

This keeps the runtime reusable across Forge apps while still allowing app-specific task contracts.

---

## 4. Shared request envelope doctrine

The runtime spec already defines the minimum request envelope shape. This taxonomy adopts that as mandatory baseline. fileciteturn5file11

### 4.1 Required request envelope fields

Every request must identify:

- `request_id` or trace id
- `task_family`
- `task_type`
- `contract_version`
- `lane_id` when governed
- `source_scope`
- `input_payload` or source references
- `desired_runtime_mode`
- `output_strictness`

### 4.2 Optional request envelope fields

Allowed optional fields:

- `quality_target`
- `latency_target`
- `privacy_locality_requirement`
- `resource_budget_class`
- `context_hints`
- `caller_app`
- `caller_module`

### 4.3 Request rule

No task may rely on hidden ambient state as its primary contract input.

If something matters for interpretation, it belongs either in:

- the payload
- the source scope
- the context metadata

---

## 5. Shared response envelope doctrine

The runtime spec already defines the minimum response envelope shape. This taxonomy adopts that as mandatory baseline. fileciteturn5file11

### 5.1 Required response envelope fields

Every response must identify:

- `request_id`
- `task_family`
- `task_type`
- `contract_version`
- `lane_id` if applicable
- `route_class`
- `model_id`
- `profile_or_prompt_id` when applicable
- `runtime_mode_used`
- `degraded_mode` if any
- `output_payload`
- `provenance_class`
- `warnings`

### 5.2 Conditionally required response fields

Required when inference-based or structure-bearing:

- `confidence`
- `evidence_spans`
- `schema_validation_status`
- `soft_fail_reasons`

### 5.3 Response rule

If the contract requires structure and the model returns unusable prose, the runtime must not pretend success.

It must either:

- normalize successfully into schema
- return degraded/soft-fail status
- or hard-fail the contract

---

## 6. Contract strictness classes

Not all tasks need the same output rigidity.

### 6.1 `ADVISORY_TEXT`

Used for:

- lightweight style suggestions
- small prose observations
- low-risk assistance

Characteristics:

- prose output allowed
- structure optional
- never authoritative

### 6.2 `TEXT_PLUS_METADATA`

Used for:

- proofreading
- cleanup
- constrained transforms

Characteristics:

- main text candidate plus bounded metadata
- issue list optional but recommended
- no direct authority promotion

### 6.3 `STRUCTURED_CANDIDATE`

Used for:

- entity extraction
- beat candidate extraction
- arc candidate extraction
- scene signal extraction

Characteristics:

- structured schema required
- evidence spans expected
- confidence required
- candidate-only by default

### 6.4 `STRUCTURED_ANALYSIS`

Used for:

- continuity checks
- pacing analysis
- style scoring
- consistency review

Characteristics:

- structured findings object required
- evidence references expected
- advisory only unless separately promoted

### 6.5 `STRICT_STRUCTURED`

Used for the most integration-sensitive tasks.

Characteristics:

- schema conformance mandatory
- unusable freeform output counts as failure
- best fit for ANVIL/Bloom-facing extraction and reasoning tasks

This matches the architecture rule that extraction and analysis contracts must be structured for app integration. fileciteturn5file11 fileciteturn5file13

---

## 7. Top-level task family taxonomy

This taxonomy adopts the four primary runtime families already defined in the architecture and planning docs. fileciteturn5file13 fileciteturn5file15

### 7.1 Proofreading family

Purpose:

- detect and correct text-quality issues with restrained edits

Typical output strictness:

- `TEXT_PLUS_METADATA`

Typical provenance:

- `inferred_candidate`

Example task types:

- lore-safe proofreading
- minimal-edit proofreading
- proofreading with issue annotations

### 7.2 Extraction family

Purpose:

- derive candidate structured artifacts from bounded source material

Typical output strictness:

- `STRUCTURED_CANDIDATE`
- `STRICT_STRUCTURED` for integration-sensitive tasks

Typical provenance:

- `inferred_candidate`

Example task types:

- entity extraction
- candidate beat extraction
- candidate arc extraction
- scene signal extraction

### 7.3 Analysis family

Purpose:

- evaluate source material and produce bounded analytical findings

Typical output strictness:

- `STRUCTURED_ANALYSIS`
- occasionally `ADVISORY_TEXT` for low-risk lightweight analysis

Typical provenance:

- `inferred_candidate`

Example task types:

- continuity review
- pacing observations
- style analysis
- voice analysis
- consistency scan

### 7.4 Transformation family

Purpose:

- produce bounded text transformation under explicit rules

Typical output strictness:

- `TEXT_PLUS_METADATA`

Typical provenance:

- `inferred_candidate`

Example task types:

- constrained rewrite
- formatting normalization
- cleanup under policy

---

## 8. Family-specific contract rules

### 8.1 Proofreading family rules

Proofreading contracts must:

- preserve intended meaning where possible
- identify whether edits are minimal or broader cleanup
- avoid silent semantic recast as acceptable default behavior
- return the revised text candidate as non-authoritative output

Recommended response sections:

- revised text
- issue summary
- risk notes
- optional changed-span metadata

### 8.2 Extraction family rules

Extraction contracts must:

- return structured candidate artifacts only
- include evidence spans for extracted claims where possible
- include confidence metadata
- refuse to imply authority persistence
- fail clearly if schema conformance cannot be achieved

This is especially important because the architecture explicitly frames beat/entity extraction as candidate generation feeding review/promotion workflows. fileciteturn5file11 fileciteturn5file13

### 8.3 Analysis family rules

Analysis contracts must:

- produce findings, not hidden decisions
- distinguish observation from recommendation
- include evidence references where feasible
- avoid overstating certainty
- remain advisory unless separately promoted by app workflow

### 8.4 Transformation family rules

Transformation contracts must:

- state the transformation policy or mode
- return transformed text candidate
- signal if transformation pressure exceeded safe bounds
- avoid pretending deterministic equivalence when the result is inferential

---

## 9. Candidate vs authority rule inside contracts

### 9.1 Hard rule

Any inferential output produced by NeuronForge Local remains candidate output by default.

This rule is already locked in the planning and runtime docs. fileciteturn5file13 fileciteturn5file15

### 9.2 Contract consequence

No contract may imply that NeuronForge Local directly writes canonical truth.

Contracts may support:

- `candidate_items`
- `review_hints`
- `promotion_recommendations`

Contracts must not imply:

- automatic canonical persistence
- automatic authority promotion
- background mutation of app truth

### 9.3 Provenance classes

Minimum provenance classes remain:

- `deterministic_derived`
- `inferred_candidate`
- `human_confirmed`
- `authority_persisted`

NeuronForge Local primarily emits the first two, while app workflows own promotion into the latter states. fileciteturn5file13

---

## 10. Degraded-mode contract doctrine

The runtime already defines explicit degraded modes, and contracts must honor them instead of masking them. fileciteturn5file10 fileciteturn5file15

### 10.1 Contract behavior in `FULL_LOCAL`

Expected:

- full contract execution
- preferred route class available
- normal output strictness enforced

### 10.2 Contract behavior in `LIMITED_LOCAL`

Expected:

- fallback route may execute
- lower confidence allowed where safe
- degraded metadata required

### 10.3 Contract behavior in `NO_EXTRACTION`

Expected:

- extraction contracts return explicit degraded response
- analysis may be limited
- cleanup/proofreading may remain available

### 10.4 Contract behavior in `NO_LOCAL_AI`

Expected:

- no inferential output
- explicit unavailable status
- deterministic app workflows unaffected

### 10.5 Rule

Degraded mode must be part of the response truth, not hidden in logs only.

---

## 11. First-priority contract families for AuthorForge

AuthorForge is the first concrete consumer, but not the long-term only consumer. The runtime must remain Forge-wide reusable while prioritizing the contracts AuthorForge needs first. fileciteturn5file12 fileciteturn5file16

### 11.1 Priority A — proofreading / cleanup

Early contracts:

- `proofread.lore_safe.v1`
- `cleanup.general_grammar.v1`
- `proofread.minimal_edit.v1`

Why first:

- current lane-governed maturity already exists
- easiest carry-forward from the current repo reality

### 11.2 Priority B — scene extraction for ANVIL/Bloom

Early contracts:

- `extract.beat_candidates.scene.v1`
- `extract.scene_signals.v1`
- `extract.entity_candidates.scene.v1`

Why second:

- directly supports the near-term bridge from manuscript scenes to candidate beats and ANVIL authority
- Bloom and ANVIL both depend on structured narrative signals, not just prose output

AuthorForge docs already define Bloom as a narrative timeline over chapters/scenes and ANVIL as story arc/intensity visualization with beat points and change signals. fileciteturn5file17 fileciteturn5file19

### 11.3 Priority C — bounded narrative analysis

Early contracts:

- `analyze.style.scene.v1` — **live, candidate_baseline** (2026-03-22)
- `analyze.continuity.scene_window.v1`
- `analyze.pacing.scene_window.v1`
- `analyze.voice.scene.v1`

Why third:

- useful across Smithy, Bloom, ANVIL, and Crucible-style experiences
- pushes structured analysis without yet demanding automatic authority promotion

---

## 12. Forge-wide reuse rule

NeuronForge must not be reduced to “AuthorForge’s local LLM manager.”

The contract taxonomy should therefore separate:

- **generic family semantics**
- **task-specific contracts**
- **app-specific integration meanings**

### 12.1 What stays generic

- envelope structure
- degraded-mode doctrine
- provenance classes
- family semantics
- strictness levels
- routing compatibility

### 12.2 What can be app-specific

- task-specific schemas
- module-specific evidence expectations
- promotion workflows
- UI-facing labels and review flows

This preserves Forge-wide runtime reuse while still serving AuthorForge first.

---

## 13. Governance binding rule

Contracts are runtime artifacts.

Lanes are trust/governance artifacts.

They must link, but they are not the same thing.

### 13.1 When lane binding is required

Lane binding should be explicit for:

- proofreading tasks already governed by lanes
- any extraction or analysis task that will undergo baseline/challenger adoption decisions
- future ANVIL/Bloom reasoning lanes

### 13.2 What lane binding contributes

- trusted baseline model/profile
- challenger history
- calibration notes
- adoption judgment
- rejection conditions

That preserves the current evaluation spine as the trust layer for future substrate growth. fileciteturn5file14 fileciteturn5file16

---

## 14. Recommended first concrete contract set

Start with a small, disciplined set.

### 14.1 Proofreading / cleanup starter set

- `proofread.lore_safe.v1`
- `cleanup.general_grammar.v1`
- `proofread.minimal_edit.v1`

### 14.2 Extraction starter set

- `extract.beat_candidates.scene.v1`
- `extract.entity_candidates.scene.v1`
- `extract.scene_signals.v1`

### 14.3 Analysis starter set

- `analyze.style.scene.v1` — **live, candidate_baseline** (qwen2.5:14b, experimental_only)
- `analyze.continuity.scene_window.v1`
- `analyze.pacing.scene_window.v1`

### 14.4 Transformation starter set

- `transform.rewrite_constrained.v1`
- `transform.normalize_formatting.v1`

This is enough to prove the substrate without letting the contract surface sprawl too early.

---

## 15. Immediate follow-on artifact

After this taxonomy, the next best artifact is:

**NeuronForge Local Routing and Model Profile Plan**

because the contracts now define what tasks exist, and the routing/model profile plan should define:

- which route class each contract family prefers
- where high-quality reasoning models are justified
- how midlevel-laptop reality constrains default selection
- when fallback is acceptable vs blocked

---

## 16. Working definition

Use this shorthand going forward:

**NeuronForge task contracts are versioned, family-bounded runtime agreements that enforce structured, provenance-aware, degraded-mode-truthful local AI behavior across Forge apps, with AuthorForge as the first concrete consumer and candidate-not-authority discipline as a hard boundary.**


---

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

---

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


---

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


---

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


---

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

