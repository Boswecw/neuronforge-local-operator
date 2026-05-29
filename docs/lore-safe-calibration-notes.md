# Lore Safe Calibration Notes

## Purpose

Calibrate judgment rules for the lore-safe proofreading lane before additional challenger testing.

## Core lane goal

The lane is not trying to find the most creative rewrite.

The lane is trying to identify proofreading behavior that:
- fixes real errors
- preserves valid prose
- protects lore terms
- avoids unnecessary rewrites
- makes the fewest possible changes

## Error classes

### 1. Hard correctness failure
A clear grammar, spelling, punctuation, or usage error introduced by the model.

Examples:
- singular changed to plural incorrectly
- wrong verb agreement introduced
- punctuation broken
- misspelling introduced

Default result:
- reject

### 2. Omission or deletion failure
The model removes content that should have been preserved.

Examples:
- drops a title/header line that is part of the input
- removes a sentence
- removes canon wording without justification

Default result:
- reject

### 3. Preservation failure
The model changes wording that was already acceptable, even if the new wording is also acceptable.

Examples:
- swaps one valid phrase for another
- changes literary phrasing without need
- softens or strengthens tone
- alters rhythm where no correction was needed

Default result:
- usually acceptable loss or reject depending on severity
- if paired with another failure, strengthens reject judgment

### 4. Acceptable variation
The model makes a different choice that remains grammatically valid and does not materially damage tone, meaning, or preservation expectations.

Examples:
- minor punctuation normalization
- equally valid wording where preservation is not materially harmed

Default result:
- acceptable or tie

### 5. Useful correction
The model fixes a real issue while preserving the rest of the passage.

Examples:
- fixes obvious agreement error
- corrects clear usage issue
- repairs punctuation without rewriting surrounding prose

Default result:
- preferred if the competing output misses the same issue

## Outcome classes

### Reject
Use when the model:
- introduces a hard correctness error
- deletes protected content
- shows major unnecessary rewriting
- damages preservation badly enough to break lane intent

### Acceptable
Use when the model:
- is safe overall
- may miss some fix opportunities
- may make small non-ideal changes
- still remains usable for the lane

### Preferred
Use when the model:
- fixes real issues correctly
- preserves acceptable prose
- makes fewer unnecessary changes than the alternative

### Tie
Use when:
- outputs are identical
- or both are equally acceptable with no meaningful preference

## Decision priority order

1. introduced correctness errors
2. deletions/omissions
3. preservation damage
4. missed useful fixes
5. stylistic preference

## Severity weighting

Use weighted severity to avoid treating all mistakes as equal.

### Weight 5 — hard failure
- introduced grammar/correctness error
- deleted or omitted protected content

Default impact:
- usually reject

### Weight 3 — serious lane damage
- unnecessary rewrite that changes meaning, tone, or literary force
- strong preservation failure

Default impact:
- often reject or strong acceptable loss

### Weight 2 — moderate issue
- missed obvious useful correction
- noticeable but limited preservation drift

Default impact:
- acceptable loss unless paired with worse issues

### Weight 1 — minor issue
- harmless but unnecessary tweak
- weak preference loss

Default impact:
- usually acceptable

### Weight 0 — no issue
- no meaningful problem detected

## Weighted decision use

Use weights as judgment support, not as fake mathematical certainty.

Working rule:
- any weight-5 issue is presumptive reject
- lower total weighted damage is better
- a model that fixes a real issue with no new damage can be preferred
- preservation-only drift should score lower than correctness failure
- deletion should score as a hard failure

## Case reminders from current suite

### Test 002
- phi4 preferred because it fixed `open it careful` to `open it carefully`

### Test 003
- phi4 reject because it introduced `was still` -> `were still`
- `behind` -> `beyond` is not a grammar error
- that wording shift is a preservation issue, not a correctness issue

### Test 004
- tie

### Test 005
- phi4 reject because it dropped the title line from the input

### Test 006
- tie

## Current suite examples

- test 002:
  - qwen: 2
  - phi4: 0

- test 003:
  - qwen: 0
  - phi4: 5 + 1/2

- test 005:
  - qwen: 0
  - phi4: 5

## Current calibration direction

Working rule:
- correctness and preservation both matter
- correctness errors are weighted more heavily than stylistic preference
- deletion is a hard failure
- valid but unnecessary rewording should be tracked separately from grammar failure

## Next use

Use these rules when writing future review files and lane summaries.