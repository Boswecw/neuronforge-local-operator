# Lore Safe Lane Status — 2026-03-13

## Locked baseline

- model: `qwen2.5:14b`
- prompt: `prompts/lore-safe-proofread-003.md`
- anchor input: `inputs/lore-safe-test-001.md`
- best confirmed anchor run: `run-2026-03-13-005`
- direct compare baseline file: `outputs/qwen2.5-14b-lore-safe-005.md`

## Phi4 contender summary

- anchor run: `run-2026-03-13-024`
- review: provisional accept
- broader harder-suite result:
  - test 002: preferred over qwen
  - test 003: reject
  - test 004: tie
  - test 005: reject
  - test 006: tie

## Current lane judgment

- baseline remains unchanged
- `phi4:14b` remains a viable contender
- `phi4:14b` did not overtake `qwen2.5:14b` across the harder suite
- model ranking is by lane, not global

## Next likely step

- test the next challenger model across the same harder suite
