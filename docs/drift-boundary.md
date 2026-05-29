# Drift Boundary

## Purpose

Define the current acceptable drift boundary for the lore-safe proofreading baseline.

This document explains what variation is tolerable and what crosses into rejection territory.

---

## Current baseline

- model: qwen2.5:14b
- prompt: prompts/lore-safe-proofread-003.md
- quality anchor: run-2026-03-13-005
- latest successful verification runs:
  - run-2026-03-13-014
  - run-2026-03-13-015

---

## Observed repeatability

Repeated runs remain stable in:

- output format
- protected term preservation
- absence of reasoning leakage
- absence of extra commentary
- core proofreading behavior

They are not perfectly deterministic at phrase level.

---

## Observed acceptable drift

Small phrase-level variation can still occur between runs.

### Confirmed example

- `her silence said enough`
- `her silence spoke enough`

This kind of variation is currently acceptable when all of the following remain true:

- meaning remains effectively unchanged
- canon terms remain stable
- tone remains materially consistent
- output format remains correct
- proofreading restraint remains acceptable

---

## Unacceptable drift

Drift crosses the current boundary if it causes any of the following:

- protected names changed
- invented terms changed without explicit justification
- titles or ranks normalized incorrectly
- obvious canon drift introduced
- visible reasoning leakage
- extra commentary outside the required format
- overly aggressive rewriting for a proofread task
- literary tone or meaning materially degraded

---

## Current boundary judgment

The current baseline is acceptable for manual proofreading assistance because phrase-level drift has remained minor while the output contract and canon safety have remained stable.

---

## Operational rule

Treat the current baseline as suitable for assisted proofreading, not as fully deterministic text correction.

Continue manual review for final acceptance.
