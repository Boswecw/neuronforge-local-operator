# Prompt Registry

## Purpose

Track prompt files that have actually been used in Neuronforge experiments.

This registry should record prompt role, status, and known outcome clearly enough to support baseline tracking and later comparison.

---

## Fields

- prompt id
- file name
- purpose
- target model
- status
- best confirmed run
- notes

---

## Entries

- prompt id: proofread-basic-001
  file name: prompts/proofread-basic-001.md
  purpose: initial basic proofreading sanity check
  target model: deepseek-r1:7b
  status: superseded
  best confirmed run: run-2026-03-13-001
  notes: useful only as an early sanity-check prompt; not suitable for current lore-safe proofreading baseline work

- prompt id: lore-safe-proofread-001
  file name: prompts/lore-safe-proofread-001.md
  purpose: initial lore-safe proofreading baseline attempt
  target model: deepseek-r1:7b
  status: failed baseline attempt
  best confirmed run: run-2026-03-13-002
  notes: did not sufficiently constrain reasoning leakage, commentary, or meaning drift

- prompt id: lore-safe-proofread-002
  file name: prompts/lore-safe-proofread-002.md
  purpose: revised lore-safe proofreading prompt
  target model: deepseek-r1:7b, qwen2.5:14b
  status: superseded
  best confirmed run: run-2026-03-13-004
  notes: improved behavior substantially with qwen2.5:14b but was later replaced by a stronger minimal-edit revision

- prompt id: lore-safe-proofread-003
  file name: prompts/lore-safe-proofread-003.md
  purpose: current lore-safe proofreading baseline prompt
  target model: qwen2.5:14b
  status: current baseline prompt
  best confirmed run: run-2026-03-13-005
  notes: current best confirmed proofreading prompt; produces clean output with no confirmed reasoning leakage in baseline use and reduces unnecessary rewrites relative to the prior revision

- prompt id: lore-safe-proofread-004
  file name: prompts/lore-safe-proofread-004.md
  purpose: tense/aspect preservation challenger prompt
  target model: qwen2.5:14b
  status: rejected prompt challenger
  best confirmed run: run-2026-03-13-019
  notes: added explicit tense/aspect preservation and anti-normalization guardrails, but did not beat the accepted prompt 003 baseline; remained clean and compliant while introducing worse optional substitutions
