# General Grammar Cleanup Calibration
Date: 2026-03-13

## Lane
- lane id: general-grammar-cleanup
- lane name: General Grammar Cleanup
- lane type: grammar / readability cleanup

## Purpose
This lane is for broader grammar cleanup than lore-safe proofreading.

It should improve:

- grammar
- punctuation
- sentence clarity
- readability
- light awkwardness

It should still preserve:

- intended meaning
- important nuance
- scene logic
- authorial intent

It should not drift into heavy rewriting, interpretive normalization, or semantic recasting when straightforward cleanup is sufficient.

## Adopted baseline
- model: qwen2.5:14b
- prompt: prompts/general-grammar-cleanup-001.md
- anchor input: inputs/general-grammar-test-001.md

## Evaluation set
- inputs/general-grammar-test-001.md
- inputs/general-grammar-test-002.md
- inputs/general-grammar-test-003.md
- inputs/general-grammar-test-004.md
- inputs/general-grammar-test-005.md

## Compared models
- qwen2.5:14b
- phi4:14b

## Output files reviewed

### Qwen
- outputs/qwen2.5-14b-general-grammar-test-001.md
- outputs/qwen2.5-14b-general-grammar-test-002.md
- outputs/qwen2.5-14b-general-grammar-test-003.md
- outputs/qwen2.5-14b-general-grammar-test-004.md
- outputs/qwen2.5-14b-general-grammar-test-005.md

### Phi4
- outputs/phi4-14b-general-grammar-test-001.md
- outputs/phi4-14b-general-grammar-test-002.md
- outputs/phi4-14b-general-grammar-test-003.md
- outputs/phi4-14b-general-grammar-test-004.md
- outputs/phi4-14b-general-grammar-test-005.md

## Test judgments
- test 001: qwen slight win
- test 002: near tie, slight lean to qwen
- test 003: qwen clear win
- test 004: qwen clear win
- test 005: qwen clear win

## Calibration judgment

### qwen2.5:14b
qwen2.5:14b best fits the lane.

Observed strengths:

- cleans grammar without overreaching
- preserves meaning more reliably
- tends to keep sentence intent intact
- improves readability without flattening voice as often
- stays closer to cleanup than rewrite

### phi4:14b
phi4:14b is readable, but it is not the better calibration fit for this lane.

Observed weaknesses:

- interpretive normalization
- semantic recasting
- flatter phrasing
- broader rewrite tendency than the lane calls for

This makes phi4 less reliable for a cleanup lane whose purpose is improvement without unnecessary authorship drift.

## Adoption decision
Adopt `qwen2.5:14b` as the working baseline model for `general-grammar-cleanup`.

## Why this baseline was adopted
The lane requires a model that can make broader edits than lore-safe proofreading while still remaining disciplined.

qwen2.5:14b showed the best balance of:

- correctness
- restraint
- readability improvement
- meaning preservation

## Confidence and limits
Confidence is moderate and sufficient for a working lane baseline.

Current limits:

- evaluation set is still small
- judgment is based on manual comparative review, not scored rubric analytics
- more challenger testing may still improve the lane later

## Current operator guidance
Use this lane when the goal is cleanup, not lore-safe minimal intervention and not stylistic rewriting.

Prefer lore-safe proofreading when preservation pressure is highest.

Prefer general grammar cleanup when broader mechanical and readability correction is desired but meaning must still remain stable.

## Next recommended work
- add a lane-specific status / calibration cross-link from analytics docs if needed
- test another challenger model against the same five-input set
- define a lightweight judgment rubric for future adoption decisions

## Operator decision
As of 2026-03-13, `qwen2.5:14b` is the adopted working baseline for the `general-grammar-cleanup` lane.
