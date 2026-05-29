# Manual Validator Rules

## Purpose

Define the manual acceptance gate for proofreading outputs.

Use these rules to decide whether a run result is acceptable for the current task.

---

## Validation order

Review outputs in this order:

1. required output shape
2. protected terms and canon safety
3. proofreading restraint
4. overall output acceptability

---

## Hard rejection conditions

Reject output if any of the following occur:

- protected names changed
- invented terms changed without explicit justification
- titles or ranks normalized incorrectly
- obvious canon drift introduced
- prose rewritten too aggressively for a proofread task
- required output sections missing
- reasoning leakage appears in the output
- extra commentary appears outside the expected output format

---

## Acceptable minor issues

The following may still be acceptable if they do not damage canon, compliance, or task fit:

- small phrasing differences
- minor wording drift
- light sentence smoothing
- small punctuation cleanup differences

These should still be noted when relevant.

---

## Judgment labels

Use one of these labels:

- `accept`
- `accept with notes`
- `reject`

---

## Label guidance

### `accept`

Use when the output satisfies the task cleanly and no meaningful issues need to be recorded.

### `accept with notes`

Use when the output is usable, but minor issues, caveats, or small drift should be recorded.

### `reject`

Use when the output violates canon safety, output contract, or proofreading restraint.

---

## Rule

Always record why.

For `accept with notes` and `reject`, record the specific issue that drove the judgment.

For `accept`, a short confirmation note is still preferred when the run is important enough to compare later.

