# NeuronForge — Local Operator

> Working training & operator repository for **NeuronForge**, the public-facing applications-support platform.

`neuronforge-local-operator` is the **local-first development and training environment** for NeuronForge. It mirrors the NeuronForge workspace so local LLMs can be run, evaluated, and refined here — and the best-performing, explicitly-reviewed results are **promoted** up to the public-facing NeuronForge applications-support version.

The current project phase is centered on **lore-safe proofreading experiments** with explicit run logging, manual validation, baseline tracking, and controlled operational discipline. It is not currently positioned as a broad general-purpose model lab.

---

## The workflow: local → public

```
┌──────────────────────────┐      run / refine prompts    ┌──────────────────────────┐
│  neuronforge-local-       │  ─────────────────────────▶  │   Local LLM run (output)  │
│  operator  (this repo)    │                              │                           │
└──────────────────────────┘                              └─────────────┬────────────┘
            ▲                                                            │
            │  iterate on prompts, inputs, configs                       │ manual review + eval
            │                                                            ▼
            │                                               ┌──────────────────────────┐
            │                                   promote ◀── │  Beats current baseline?  │
            │                                               └─────────────┬────────────┘
            │                                                             │ yes, reviewed
            ▼                                                             ▼
   (refine & re-run)                                  ┌──────────────────────────────┐
                                                      │  NeuronForge — public-facing  │
                                                      │  applications support         │
                                                      └──────────────────────────────┘
```

1. **Run locally.** Drive local models with controlled prompts against reference inputs.
2. **Capture.** Save every output with a structured run record.
3. **Review & evaluate.** Validate manually against explicit acceptance criteria.
4. **Promote.** Only an explicitly reviewed, better-than-baseline run becomes the new baseline / is promoted to public-facing NeuronForge.
5. **Iterate.** Feed learnings back into prompts and inputs, then repeat.

> Operational success does not by itself replace the current quality baseline. A later run only becomes the new baseline when it is explicitly reviewed and accepted as a better result.

---

## Current focus

The active focus is:

- lore-safe proofreading
- prompt-controlled local model runs
- repeatable output capture
- structured run logging
- manual review against explicit acceptance criteria
- controlled baseline comparison

Current documented baseline:

- model: `qwen2.5:14b`
- prompt: `prompts/lore-safe-proofread-003.md`
- input reference: `inputs/lore-safe-test-001.md`

Current best confirmed quality anchor:

- `run-2026-03-13-005`

Latest successful wrapper-driven operational verification runs:

- `run-2026-03-13-014`
- `run-2026-03-13-015`

---

## Repository layout

- `docs/`
  Control documents for workflow, baseline status, review discipline, drift boundaries, repeatability, and scope.

- `doc/system/`
  Canonical system documentation parts; root `NLOSYSTEM.md` is the build artifact (rebuild with `bash doc/system/BUILD.sh`).

- `inputs/`
  Source texts used for proofreading runs.

- `prompts/`
  Prompt files used to drive controlled model behavior.

- `outputs/`
  Saved model outputs from manual or wrapper-driven runs.

- `registry/`
  Structured registries for runs, prompts, models, protected terms, and style preferences.

- `evals/`
  Per-run review notes and quality assessments.

- `analytics/` · `schemas/` · `service/`
  Supporting analytics surfaces, data/validation schemas, and service code.

- `notes/`
  Supporting working notes and revision logs.

- `scripts/`
  Operator utilities for running, logging, reviewing, and comparing proofreading outputs.

- `tests/`
  Verification and audit surfaces.

---

## Primary documents

Start here for the current control surface:

- `docs/workflow.md`
- `docs/operational-workflow.md`
- `docs/current-baseline.md`
- `docs/manual-validator.md`
- `docs/review-checklist.md`
- `docs/change-control.md`
- `docs/drift-boundary.md`
- `docs/repeatability-note.md`
- `docs/experiment-scope.md`

See also `NLOSYSTEM.md` and `CLAUDE.md` for repo doctrine and assistant working instructions.

---

## Primary scripts

Current core execution path:

- `scripts/run-proofread.sh`
- `scripts/log-run.sh`
- `scripts/next-run-id.sh`
- `scripts/run-and-log-proofread.sh`

Supporting utilities:

- `scripts/review-proofread.sh`
- `scripts/compare-outputs.sh`

Context loading:

```bash
# Show available sections and presets
./scripts/context-bundle.sh --list

# Core / docs / testing bundles
./scripts/context-bundle.sh --preset core
./scripts/context-bundle.sh --preset docs
./scripts/context-bundle.sh --preset testing
```

---

## Current operating posture

NeuronForge is presently run in a manual-first, verification-heavy mode. The current posture emphasizes:

- reproducible runs
- explicit run records
- separation of quality validation from workflow verification
- careful baseline promotion
- documented interpretation of failures

---

## Promotion criteria

A run / model is promoted toward the public-facing applications-support version only when it:

- [ ] Has a complete, reproducible run record (prompt, input, model, output)
- [ ] Passes manual review against the explicit acceptance criteria
- [ ] Is reviewed and accepted as **better than** the current quality anchor
- [ ] Shows no regression in lore-safety or protected-term handling

---

## Boundary note

A real Ollama runtime memory failure has already been observed during testing. That failure is treated as a runtime resource boundary, not as evidence that the wrapper workflow is incorrect. This distinction matters to the current experiment design.

---

## Relationship to NeuronForge

| | **neuronforge-local-operator** (this repo) | **NeuronForge** (public-facing) |
|---|---|---|
| Purpose | Run, train & refine local LLMs | Serve applications support to users |
| Audience | Operators / developers | End users |
| Outputs | Candidate runs & checkpoints | Promoted, baseline-approved results |
| Direction | Source of truth for experiments | Receives promoted results |

---

## Status

The repository has a coherent documentation spine for the current proofreading baseline phase. The next work should continue from one of these paths:

- baseline improvement
- further prompt refinement
- additional model comparison against the current quality anchor
- tighter operational scripting where needed
