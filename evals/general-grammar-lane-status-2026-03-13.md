# General Grammar Lane Status — 2026-03-13

## Working baseline

- model: `qwen2.5:14b`
- prompt: `prompts/general-grammar-cleanup-001.md`
- anchor input: `inputs/general-grammar-test-001.md`
- direct compare baseline file: `outputs/qwen2.5-14b-general-grammar-test-001.md`
- calibration doc: `evals/general-grammar-calibration-2026-03-13.md`

## Phi4 contender summary

- broader suite result:
  - test 001: slight loss to qwen
  - test 002: near tie, slight lean to qwen
  - test 003: clear loss to qwen
  - test 004: clear loss to qwen
  - test 005: clear loss to qwen

## Current lane judgment

- `qwen2.5:14b` is the working baseline for this lane
- `phi4:14b` is readable but tends toward interpretive normalization
- this lane favors cleanup with meaning preservation over semantic recasting
- model ranking is by lane, not global

## Governance state

- baseline established
- calibration/adoption decision documented
- lane status and calibration are now aligned

## Next likely step

- cross-link this calibration doc from any analytics or baseline index docs if still missing
- optionally add a dedicated adoption-history section if this lane gains future challengers
