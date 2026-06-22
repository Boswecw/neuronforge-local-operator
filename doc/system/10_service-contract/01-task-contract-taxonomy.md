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

