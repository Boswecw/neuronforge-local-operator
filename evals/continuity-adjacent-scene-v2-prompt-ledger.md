# Continuity Adjacent-Scene v2 Prompt Revision Ledger

Date created: 2026-03-14

## Purpose

Track every run against the frozen adjacent-scene case pack using the revised prompt (`prompts/continuity-adjacent-scene-v2.md`).

This ledger covers the post-revision challenger comparison only. The first-pass results (v1 prompt) are in:

`evals/continuity-adjacent-scene-first-pass-ledger.md`

---

## Prompt reference

- **prompt:** `prompts/continuity-adjacent-scene-v2.md`
- **changes from v1:** structural parsing check before flagging; compression tolerance guidance; confidence calibration rules; explicit restraint bias section

## Pack reference

- **pack id:** `continuity-progression-case-pack-v1`
- **scope:** adjacent-scene cases only (cp-001 through cp-012)
- **task contract:** `analyze.continuity.adjacent_scene.v1`
- **route class:** `HIGH_QUALITY_LOCAL`
- **executor:** `scripts/run-continuity-adjacent-scene.sh`

---

## Ledger columns

| Column | Meaning |
|--------|---------|
| `run_id` | From `registry/runs.md` |
| `date` | Execution date |
| `case_id` | Which case packet was run |
| `model` | Ollama model name |
| `envelope_status` | `valid_candidate` or `fail_closed` |
| `validator_result` | `valid` or `fail_closed` |
| `findings_count` | Number of candidate findings in envelope |
| `fail_reason` | Failure reason if fail-closed, else `—` |
| `envelope_file` | Path to `.envelope.json` output |
| `reviewer_outcome` | `pending`, `complete`, or `skipped` |

---

## Runs

| run_id | date | case_id | model | envelope_status | validator_result | findings_count | fail_reason | envelope_file | reviewer_outcome |
|--------|------|---------|-------|----------------|-----------------|----------------|-------------|---------------|-----------------|

---

## Model summary table

Update after each model's full pass (all 12 adjacent-scene cases complete).

| model | prompt | cases_run | valid_envelopes | fail_closed | total_findings | avg_findings | fp_restraint_cases | fn_tp_cases |
|-------|--------|-----------|-----------------|-------------|---------------|--------------|-------------------|-------------|
| _(none yet)_ | | | | | | | | |

---

## Hard-fail tracking

| run_id | case_id | model | failure_reason |
|--------|---------|-------|----------------|
| _(none yet)_ | | | |

---

## Notes

_(none yet)_
