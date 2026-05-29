# General Grammar Cleanup Lane Plan

## Purpose

Define the Neuronforge lane for general grammar cleanup.

This lane is separate from lore-safe proofreading.

Its goal is to improve grammar, clarity, punctuation, and readability when strict lore-preserving minimal-edit behavior is not the top priority.

---

## Lane name

- general-grammar-cleanup

## Status

- planned

## Core intent

- fix grammar
- improve punctuation
- correct awkward phrasing when helpful
- improve readability
- allow somewhat broader edits than the lore-safe lane

## Non-goals

- do not intentionally rewrite into a different scene
- do not add new facts
- do not delete important meaning
- do not flatten everything into generic prose

## Key difference from lore-safe proofreading

Lore-safe proofreading prioritizes preservation over cleanup.

General grammar cleanup allows broader editing when the result is clearly cleaner and still faithful to the original meaning.

## Initial evaluation questions

- does the model improve grammar and punctuation correctly
- does it preserve the intended meaning
- does it over-rewrite
- does it introduce blandness or generic phrasing
- does it delete important nuance

## Initial outcome classes

- reject
- acceptable
- preferred
- tie

## Initial next build items

- create lane prompt
- create 4 to 6 test inputs
- run anchor comparisons across candidate local models
- lock a baseline for this lane

## Initial model judgment

Current provisional baseline model: `qwen2.5:14b`

Rationale after first three tests:

- test 001: qwen2.5:14b slightly preferred
- test 002: near tie, slight lean to qwen2.5:14b
- test 003: qwen2.5:14b clearly preferred

Working judgment:

`qwen2.5:14b` currently performs better for the general grammar cleanup lane because it improves readability and grammar while staying closer to the intended meaning and avoiding unnecessary stylization.

`phi4:14b` is competent, but in this lane it tends to introduce more literary normalization or heavier phrasing than desired.

This judgment is provisional until more edge cases are tested, but qwen2.5:14b is the current leading baseline candidate for this lane.


## Updated model judgment after test 004

Test 004 strengthened the current lane judgment.

Winner: `qwen2.5:14b`

Reason:

`qwen2.5:14b` continues to make broader cleanup edits while preserving intended meaning more reliably than `phi4:14b`.

In contrast, `phi4:14b` shows repeated tendency toward interpretive normalization and semantic recasting, including wording shifts such as:

- "its implications"
- "all the more unsettling"
- "choose incorrectly on your own"
- "the lesser evil"

These choices read more like rewriting than grammar cleanup and make `phi4:14b` a weaker fit for this lane.

Current lane standing after four tests:

- test 001: qwen2.5:14b slight win
- test 002: near tie, slight lean to qwen2.5:14b
- test 003: qwen2.5:14b clear win
- test 004: qwen2.5:14b clear win

Working conclusion:

`qwen2.5:14b` should now be treated as the working baseline model for the `general-grammar-cleanup` lane unless later edge-case testing overturns that judgment.


## Updated model judgment after test 005

Test 005 further strengthened the lane decision.

Winner: `qwen2.5:14b`

Reason:

`qwen2.5:14b` preserved character nuance more reliably while still performing useful cleanup.

Most importantly, it preserved the distinction between:

- inability to pretend otherwise
- distrust of oneself to pretend otherwise

That nuance matters in this lane because the goal is not only grammatical improvement, but preservation of intended meaning and emotional precision.

By contrast, `phi4:14b` again normalized several lines into flatter constructions, including:

- "part of the problem"
- "Promising something is easy"
- "I cannot pretend otherwise"

These edits are readable, but they reduce specificity and slightly flatten voice and meaning.

Current lane standing after five tests:

- test 001: qwen2.5:14b slight win
- test 002: near tie, slight lean to qwen2.5:14b
- test 003: qwen2.5:14b clear win
- test 004: qwen2.5:14b clear win
- test 005: qwen2.5:14b clear win

Working baseline judgment:

`qwen2.5:14b` should now be treated as the locked baseline candidate for the `general-grammar-cleanup` lane, pending final documentation and lane record alignment.

