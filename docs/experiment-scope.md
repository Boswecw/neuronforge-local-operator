# Experiment Scope

## Purpose

Define the current controlled scope of Neuronforge as it exists now.

This document records what the experiment is presently trying to prove, what is inside scope, and what is outside scope for the current phase.

---

## Current scope

Neuronforge is currently being used as a controlled local-first experimentation environment for lore-safe proofreading.

The present scope is not general multi-task model evaluation.

The present scope is narrower and more operational:

- test local proofreading behavior against a defined prompt and input
- capture outputs in a repeatable way
- log meaningful runs in a structured registry
- manually review output quality against explicit acceptance criteria
- distinguish quality validation from workflow verification
- preserve a current baseline until a better quality winner is actually confirmed

---

## Active baseline focus

The current baseline focus is:

- task: lore-safe proofreading
- baseline model: `qwen2.5:14b`
- baseline prompt: `prompts/lore-safe-proofread-003.md`
- baseline input reference: `inputs/lore-safe-test-001.md`

The current best confirmed quality anchor is:

- `run-2026-03-13-005`

Later successful runs may verify operational repeatability without replacing the quality anchor unless they are explicitly reviewed and accepted as a better result.

---

## What this phase is trying to establish

This phase is intended to establish the following:

- a repeatable operator workflow for local proofreading runs
- a clean separation between prompts, inputs, outputs, and run records
- a usable manual validation gate for output acceptance
- a stable current baseline for comparison against future candidates
- a clear drift boundary between acceptable variation and unacceptable change
- documented distinction between workflow repeatability and exact output determinism

---

## In scope

The following are in scope for the current phase:

- local model proofreading experiments
- prompt iteration for lore-safe proofreading
- wrapper-driven execution and logging
- manual run validation
- baseline comparison
- drift evaluation
- documentation that clarifies the operational contract

---

## Out of scope for the current phase

The following are not the main focus of the current phase:

- broad multi-model benchmarking
- generalized task expansion beyond proofreading
- automated scoring as the primary acceptance authority
- cloud-first orchestration
- large-scale pipeline automation
- promotion of a new baseline without confirmed quality review

These may become future work, but they are not the present control target.

---

## Operating rules

The current experiment should continue to follow these rules:

- keep runs reproducible
- log each meaningful run
- save prompts separately from outputs
- evaluate outputs against explicit review criteria
- treat runtime resource failures separately from workflow logic failures
- do not treat later successful runs as a new baseline without a quality reason

---

## Current boundary note

A real Ollama runtime memory failure has already been observed during this phase.

That failure is currently treated as a runtime resource boundary, not as evidence that the wrapper workflow is incorrect.

This distinction is part of the present experiment scope because operational interpretation matters as much as raw execution success.

---

## Scope change rule

If Neuronforge expands beyond this current proofreading baseline phase, this document should be updated intentionally.

Scope changes should be documented when the project moves into a materially different activity such as:

- new proofreading task classes
- a different baseline model family
- a different evaluation authority
- broader model comparison work
- automation beyond the current manual-first control path
