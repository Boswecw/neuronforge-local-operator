# phi4-reasoning:latest Evaluation Results — Adjacent-Scene Cases

Date: 2026-03-14
Model: phi4-reasoning:latest
Case pack: continuity-progression-case-pack-v1
Cases attempted: cp-001 through cp-003 (stopped at disqualifying threshold)
Runs: run-2026-03-14-025 (corrupted), run-2026-03-14-026a/b/c (fail-closed)

---

## Summary

phi4-reasoning:latest failed schema validation on every legitimate run. The pass was stopped at 3 consecutive hard fails, which meets the disqualifying threshold defined in the execution plan (3+/12).

The model is **disqualified from first-pass lane adoption** for `continuity-progression-reasoning`.

---

## What happened

### Run-025: extractor bug

The first run (cp-001) produced a correct JSON response, but the executor's `extract_json()` function grabbed the wrong JSON. phi4-reasoning wraps all output in `<think>...</think>` before producing the final response. The prompt includes the full output schema as an example. The model echoed that example schema verbatim inside its think block — with the template placeholder `"<short summary of what you found or did not find>"` intact.

The extractor searched for the first JSON-in-code-fence match in the full raw output. The think block came first and contained the example schema. The extractor found that schema, not the actual model output after `</think>`.

The resulting envelope: valid schema structure, 0 findings, template literal in `overall_run_note`. The validator passed it because the structure was formally correct. The content was the prompt's own example, not the model's analysis.

Fix applied: `strip_think_blocks()` added to both the executor and validator. The function strips `<think>.*</think>` before extraction.

### Runs 026a/b/c: consistent schema structure failure

After the extractor fix, phi4-reasoning produced three consecutive outputs that failed schema validation:

| case | model output structure | missing fields |
|------|----------------------|----------------|
| cp-001 | `{candidate_findings: [...]}` | schema_version, lane_id, analysis_scope_type, analysis_scope_bounds, input_unit_ids, overall_run_note, run_posture |
| cp-002 | `{scene_ids: [...], candidate_findings: [...]}` | schema_version, lane_id, analysis_scope_type, overall_run_note, run_posture |
| cp-003 | `{...candidate_findings: [...]}` | overall_run_note and other required top-level fields |

The model consistently generates a custom partial JSON object that includes the findings content but omits the required envelope-level fields. The structure varies between runs but is never the full required schema.

---

## What the model's reasoning shows

The `<think>` blocks for all three cases show substantive analysis:

- **cp-001**: The model correctly identified the injured-hand carry-forward issue, selected `state_carry_forward_issue` as the appropriate type, and cited specific evidence spans. The reasoning is sound.
- **cp-002**: The model identified what it called an "inconsistency in Amicae's belongings" — a misread, but it attempted substantive analysis.
- **cp-003**: The model reasoned through the warden meeting progression break.

The quality of reasoning inside the think block is not the problem. The model can analyze manuscript scenes. It cannot reliably translate that analysis into the required JSON schema structure.

---

## Root cause

phi4-reasoning:latest is a reasoning-first model. Its training optimizes for chain-of-thought reasoning quality. Schema compliance is a secondary concern. When the model generates its final output, it appears to produce what it considers the "essential" response — the findings — without consistently including the surrounding envelope fields.

This is not a prompt issue in the sense that other models handle the same prompt correctly. phi4:14b and qwen2.5:14b both produced valid full-schema output on all 12 cases. The schema requirement is clear in the prompt. phi4-reasoning simply doesn't prioritize the wrapper fields.

The model may be more amenable to a different prompt strategy — for example, providing the schema fields one at a time as a fill-in exercise, or using a structured output mode if Ollama supports it for this model. But neither of those paths is available in the current executor design.

---

## Infrastructure finding: extractor vulnerability

The run-025 extractor bug is significant beyond phi4-reasoning. Any reasoning model that:
1. Wraps output in `<think>...</think>`
2. Contains the example schema in its think block (because the schema is in the prompt)

...will hit this same extraction failure.

The fix (`strip_think_blocks()`) is now in both the executor and validator. This makes the pipeline robust to all future reasoning-model candidates that use the standard `<think>` format.

---

## Infrastructure finding: run ID collision

Fail-closed runs do not log to `registry/runs.md`. The `next-run-id.sh` script reads from that file to determine the next sequential ID. When multiple fail-closed runs occur on the same day, they all receive the same run ID from the script's perspective.

This was worked around by manual suffix notation (026a/b/c) in the ledger. It is a design gap that should be addressed before any future high-volume testing session with models expected to produce fail-closed output.

---

## Disposition

phi4-reasoning:latest is not a candidate for this lane in its current form.

The model has genuine analytical capability — its reasoning traces show it can identify manuscript continuity issues. That capability is inaccessible under the current contract because the model cannot reliably produce the required schema output.

Possible future paths:
1. Structured output mode (if Ollama adds native JSON schema enforcement for this model)
2. A two-stage pipeline: phi4-reasoning produces reasoning in any format, a post-processor extracts and structures it into the required schema
3. A different prompt strategy that builds the schema fields incrementally

None of these are in scope for the current first-pass evaluation.

---

## Effect on first-pass comparison

The first-pass comparison (phi4:14b vs qwen2.5:14b) is complete and documented in:

`docs/continuity-adjacent-scene-first-pass-results.md`

phi4-reasoning:latest is an additional evaluated challenger, stopped early due to disqualifying schema failure rate. It does not change the first-pass recommendation, which stands as written.
