# neuronforge-local-operator — Claude Instructions

## Repo Role

This is the **local-first training & operator workspace** for NeuronForge. Work here is about
running local LLMs, capturing reproducible runs, validating them against explicit acceptance
criteria, and **promoting** only baseline-beating, reviewed results toward the public-facing
NeuronForge applications-support version.

- This repo holds a **snapshot** of the NeuronForge workspace (no upstream commit history).
- Current phase: **lore-safe proofreading** experiments — manual-first, verification-heavy.
- This is not a general-purpose model lab; keep changes scoped to the current experiment surface.

## Module Map

| Module | Surface | Current role |
| --- | --- | --- |
| Documentation Stack | `doc/system/`, `SYSTEM.md`, `scripts/context-bundle.sh` | Canonical repo context and build surfaces |
| Run & Operator Path | `scripts/run-proofread.sh`, `scripts/log-run.sh`, `scripts/run-and-log-proofread.sh`, `scripts/next-run-id.sh` | Drive, log, and identify local model runs |
| Review & Compare | `scripts/review-proofread.sh`, `scripts/compare-outputs.sh`, `evals/` | Manual validation and baseline comparison |
| Experiment Inputs | `prompts/`, `inputs/` | Controlled prompts and reference source texts |
| Run Records | `outputs/`, `registry/` | Saved outputs and structured run/model/term registries |
| Data and Schemas | `schemas/`, `analytics/`, `service/` | Validation surfaces, analytics, and service code |
| Governance and Specs | `docs/`, the root `*plan*.md` / `schema_change*.md` design docs | Repo doctrine, experiment design, and supporting material |
| Verification | `tests/` | Test and audit surfaces |

## Baseline (current)

- model: `qwen2.5:14b`
- prompt: `prompts/lore-safe-proofread-003.md`
- input reference: `inputs/lore-safe-test-001.md`
- best confirmed quality anchor: `run-2026-03-13-005`

A later run only becomes the new baseline when it is **explicitly reviewed and accepted** as a
better result. Operational success (the wrapper runs cleanly) does not by itself replace the
quality baseline.

## Coding Standards

- Treat `doc/system/` part files as canonical; rebuild root `SYSTEM.md` with `bash doc/system/BUILD.sh`
- Keep documentation in present tense and aligned to implemented reality
- Prefer bounded patches over broad rewrites unless a file is clearly scaffold-only
- Do not bypass repo-local authority boundaries documented in `SYSTEM.md`

## File Conventions

- Canonical system docs live under `doc/system/`; root `SYSTEM.md` is a build artifact
- Supporting design material lives under `docs/`
- Repo automation scripts live under `scripts/`
- Tests live under `tests/` when present
- Every model run should produce a complete, reproducible record (prompt + input + model + output) in `outputs/` and `registry/`

## Context Loading

```bash
# Show available sections and presets
./scripts/context-bundle.sh --list

# Core bundle
./scripts/context-bundle.sh --preset core

# Documentation or testing-focused bundles
./scripts/context-bundle.sh --preset docs
./scripts/context-bundle.sh --preset testing
```

## Run & Promotion Protocol

- Use the existing operator scripts to run and log; do not hand-roll one-off run flows
- Keep runs reproducible: pin the prompt, input, and model for every recorded run
- Validate manually against the explicit acceptance criteria in `docs/` and `evals/` before claiming a result
- Treat a run as **promotable** only when it is reviewed, beats the current quality anchor, and shows no regression in lore-safety / protected-term handling
- A known Ollama runtime memory failure is a resource boundary, not a workflow defect — don't redesign the wrapper around it

## Ecosystem Rules

- Keep cross-repo integrations explicit and documented
- Do not invent undocumented APIs, tables, routes, or environment variables
- If a runtime contract changes, update `doc/system/`, rebuild `SYSTEM.md`, and keep `CLAUDE.md` current

## Testing Expectations

- Run the repo's existing tests when available before claiming a change is complete
- Keep documentation build and context-bundle scripts working
- Expand test documentation in `SYSTEM.md` as exact suites and commands are cataloged

## Change Protocol

- Edit `doc/system/` part files, not the generated root `SYSTEM.md`
- Rebuild `SYSTEM.md` after documentation changes
- Keep new docs honest about current implementation state
