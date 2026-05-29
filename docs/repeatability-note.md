# Repeatability Note

## Purpose

Record the current repeatability judgment for the lore-safe proofreading baseline.

This note distinguishes workflow repeatability from exact phrase-level output determinism.

---

## Workflow repeatability

The reusable wrapper-driven workflow works correctly and reduces manual command assembly errors.

The current operator path has been verified for:

- dry-run resolution
- live execution
- output file creation
- run logging
- run id generation

This means the operational workflow is repeatable as a process.

---

## Model output repeatability

`qwen2.5:14b` remains clean and compliant for the current lore-safe proofreading baseline, but repeated runs can still produce small wording differences.

The current baseline combination remains:

- model: `qwen2.5:14b`
- prompt: `prompts/lore-safe-proofread-003.md`
- input reference: `inputs/lore-safe-test-001.md`

Quality anchor:

- `run-2026-03-13-005`

Latest successful verification runs:

- `run-2026-03-13-014`
- `run-2026-03-13-015`

---

## Current interpretation

- output format is stable
- reasoning leakage is absent
- extra commentary is absent
- protected terms are stable
- proofreading quality is strong
- minimal-edit behavior is good but not perfectly repeatable at phrase level

---

## Practical conclusion

This baseline is usable for manual proofreading workflows, but outputs should still be reviewed rather than treated as perfectly deterministic text correction.
