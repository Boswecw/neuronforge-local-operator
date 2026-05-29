# Model Notes

## Purpose

Track verified observations about local models used in Neuronforge experiments.

Record only observations that were actually tested or directly observed.

---

## qwen2.5:14b

### Status
Current baseline model for lore-safe proofreading.

### Confirmed use case
- lore-safe proofreading
- minimal-edit proofreading experiments
- wrapper-driven operational verification runs

### Prompt pairing currently in baseline use
- `prompts/lore-safe-proofread-003.md`

### Input reference used in current baseline testing
- `inputs/lore-safe-test-001.md`

### Quality impressions
- clean output format
- no reasoning leakage observed in the confirmed baseline runs
- no extra commentary observed in the confirmed baseline runs
- preserves protected terms better than the prior baseline model
- preserves literary tone better than the prior baseline model
- still shows occasional non-minimal phrasing drift

### Speed impression
- somewhat slow

This should be treated as an operator impression, not a benchmark result.

### Repeatability note
Outputs are stable in structure and compliance, but not perfectly deterministic at phrase level.

Repeated runs may still produce small wording differences.

### Best confirmed quality anchor
- `run-2026-03-13-005`

### Latest successful operational verification runs
- `run-2026-03-13-014`
- `run-2026-03-13-015`

### Weak points
- occasional unnecessary wording changes
- not perfectly repeatable at phrase level
- may hit available-memory limits depending on system state

### Runtime boundary observed
A real Ollama runtime failure was observed:

- `Error: 500 Internal Server Error: model requires more system memory (3.3 GiB) than is available (2.5 GiB)`

Interpretation:

- this is a runtime resource limit
- this is not evidence of a wrapper logic failure
- successful use may depend on available free memory at run time

---

## Note discipline

When adding future model notes:

- separate verified observations from guesses
- record the exact model name used at runtime
- prefer run-linked observations when possible
- do not promote a model to baseline status without a confirmed quality reason
