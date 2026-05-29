# Model Registry

## Purpose

Track models that have actually been used in Neuronforge experiments.

This registry should record current status cleanly without duplicating entries for the same runtime model unless there is a real reason to distinguish them.

---

## Fields

- model name
- source
- size
- quant
- runtime
- status
- confirmed use case
- best confirmed run
- latest successful verification runs
- notes

---

## Entries

- model name: deepseek-r1:7b
  source: Ollama
  size: 7b
  quant: unknown
  runtime: local
  status: rejected for current baseline
  confirmed use case: initial proofreading comparison only
  best confirmed run: run-2026-03-13-001
  latest successful verification runs: none
  notes: failed current proofreading baseline requirements; exposed reasoning, added commentary, violated return-only-text constraints, and altered meaning too aggressively

- model name: qwen2.5:14b
  source: Ollama
  size: 14b
  quant: unknown
  runtime: local
  status: current baseline
  confirmed use case: lore-safe proofreading
  best confirmed run: run-2026-03-13-005
  latest successful verification runs: run-2026-03-13-014, run-2026-03-13-015
  notes: current best confirmed lore-safe proofreading model; clean output, no reasoning leakage observed in confirmed baseline runs, preserves protected terms and literary tone better than the prior baseline model, still shows occasional non-minimal phrasing drift, somewhat slow, and may hit runtime memory limits depending on available free memory

- model name: gemma3:4b
  source: Ollama
  size: 4b
  quant: unknown
  runtime: local
  status: rejected for current baseline
  confirmed use case: lore-safe proofreading challenger
  best confirmed run: run-2026-03-13-016
  latest successful verification runs: run-2026-03-13-016
  notes: stayed inside the return-only-text contract and preserved protected terms and literary tone, but failed basic proofreading quality with clear grammar errors; not strong enough to challenge the current qwen2.5:14b baseline


- model name: qwen2.5:7b
  source: Ollama
  size: 7b
  quant: unknown
  runtime: local
  status: rejected for current baseline
  confirmed use case: lore-safe proofreading challenger
  best confirmed run: run-2026-03-13-017
  latest successful verification runs: run-2026-03-13-017
  notes: stayed inside the return-only-text contract and preserved protected terms and meaning, but showed more editorial phrasing drift than the current qwen2.5:14b baseline and did not clearly improve proofreading quality

- model name: gemma3:12b
  source: Ollama
  size: 12b
  quant: unknown
  runtime: local
  status: rejected for current baseline
  confirmed use case: lore-safe proofreading challenger
  best confirmed run: run-2026-03-13-018
  latest successful verification runs: run-2026-03-13-018
  notes: returned clean contract-compliant output and was notably fast, but failed baseline challenge due to clear grammar errors and additional editorial drift relative to the current qwen2.5:14b winner

- model name: llama3.1:8b
  source: Ollama
  size: 8b
  quant: unknown
  runtime: local
  status: rejected for current baseline
  confirmed use case: lore-safe proofreading challenger
  best confirmed run: run-2026-03-13-020
  latest successful verification runs: run-2026-03-13-020
  notes: returned clean and fast output, but failed the baseline challenge due to a clear grammar error (`were`) and an inferior optional phrasing substitution (`sat badly in him`); not strong enough to replace the current qwen2.5:14b baseline

- model name: mistral:7b-instruct
  source: Ollama
  size: 7b
  quant: unknown
  runtime: local
  status: rejected for current baseline
  confirmed use case: lore-safe proofreading challenger
  best confirmed run: run-2026-03-13-021
  latest successful verification runs: run-2026-03-13-021
  notes: returned grammatically clean output, but failed the baseline challenge due to substantial editorial drift and normalized too many acceptable literary phrasings instead of performing minimal correction

- model name: olmo2:13b
  source: Ollama
  size: 13b
  quant: unknown
  runtime: local
  status: rejected for current baseline
  confirmed use case: lore-safe proofreading challenger
  best confirmed run: run-2026-03-13-022
  latest successful verification runs: run-2026-03-13-022
  notes: relatively strong and restrained challenger that correctly fixed the core grammar error and preserved several desirable literary phrasings, but still failed the baseline challenge due to an unnecessary optional substitution (`said enough` → `spoke enough`)

- model name: cogito:14b
  source: Ollama
  size: 14b
  quant: unknown
  runtime: local
  status: rejected for current baseline
  confirmed use case: lore-safe proofreading challenger
  best confirmed run: run-2026-03-13-023
  latest successful verification runs: run-2026-03-13-023
  notes: produced generally clean output and fixed the core grammar error, but failed the baseline challenge due to unnecessary literary normalization and phrasing drift (`as if it were` → `as if it was`, `said enough` → `spoke enough`, and `had seen` → `saw` kept it below the qwen2.5:14b baseline)
