# Continuity Adjacent-Scene First-Pass Results Ledger

Date created: 2026-03-14

## Purpose

Track every governed execution run against the frozen adjacent-scene case pack.

One row per run. Success and fail-closed runs are both recorded.

This is the operational ledger for the first governed challenger comparison.

---

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
| `worksheet_path` | Path to completed review worksheet, if done |
| `reviewer_outcome` | `pending`, `complete`, or `skipped` |

---

## Runs

| run_id | date | case_id | model | envelope_status | validator_result | findings_count | fail_reason | envelope_file | worksheet_path | reviewer_outcome |
|--------|------|---------|-------|----------------|-----------------|----------------|-------------|---------------|----------------|-----------------|
| run-2026-03-14-001 | 2026-03-14 | cp-001 | phi4:14b | valid_candidate | valid | 1 | — | outputs/phi4-14b-continuity-adj-cp001-sc-a-cp001-sc-b-run-2026-03-14-001.envelope.json | — | complete |
| run-2026-03-14-002 | 2026-03-14 | cp-002 | phi4:14b | valid_candidate | valid | 1 | — | outputs/phi4-14b-continuity-adj-cp002-sc-a-cp002-sc-b-run-2026-03-14-002.envelope.json | — | complete |
| run-2026-03-14-003 | 2026-03-14 | cp-003 | phi4:14b | valid_candidate | valid | 1 | — | outputs/phi4-14b-continuity-adj-cp003-sc-a-cp003-sc-b-run-2026-03-14-003.envelope.json | — | complete |
| run-2026-03-14-004 | 2026-03-14 | cp-004 | phi4:14b | valid_candidate | valid | 1 | — | outputs/phi4-14b-continuity-adj-cp004-sc-a-cp004-sc-b-run-2026-03-14-004.envelope.json | — | complete |
| run-2026-03-14-005 | 2026-03-14 | cp-005 | phi4:14b | valid_candidate | valid | 1 | — | outputs/phi4-14b-continuity-adj-cp005-sc-a-cp005-sc-b-run-2026-03-14-005.envelope.json | — | complete |
| run-2026-03-14-006 | 2026-03-14 | cp-006 | phi4:14b | valid_candidate | valid | 1 | — | outputs/phi4-14b-continuity-adj-cp006-sc-a-cp006-sc-b-run-2026-03-14-006.envelope.json | — | complete |
| run-2026-03-14-007 | 2026-03-14 | cp-007 | phi4:14b | valid_candidate | valid | 1 | — | outputs/phi4-14b-continuity-adj-cp007-sc-a-cp007-sc-b-run-2026-03-14-007.envelope.json | — | complete |
| run-2026-03-14-008 | 2026-03-14 | cp-008 | phi4:14b | valid_candidate | valid | 1 | — | outputs/phi4-14b-continuity-adj-cp008-sc-a-cp008-sc-b-run-2026-03-14-008.envelope.json | — | complete |
| run-2026-03-14-009 | 2026-03-14 | cp-009 | phi4:14b | valid_candidate | valid | 0 | — | outputs/phi4-14b-continuity-adj-cp009-sc-a-cp009-sc-b-run-2026-03-14-009.envelope.json | — | complete |
| run-2026-03-14-010 | 2026-03-14 | cp-010 | phi4:14b | valid_candidate | valid | 1 | — | outputs/phi4-14b-continuity-adj-cp010-sc-a-cp010-sc-b-run-2026-03-14-010.envelope.json | — | complete |
| run-2026-03-14-011 | 2026-03-14 | cp-011 | phi4:14b | valid_candidate | valid | 0 | — | outputs/phi4-14b-continuity-adj-cp011-sc-a-cp011-sc-b-run-2026-03-14-011.envelope.json | — | complete |
| run-2026-03-14-012 | 2026-03-14 | cp-012 | phi4:14b | valid_candidate | valid | 0 | — | outputs/phi4-14b-continuity-adj-cp012-sc-a-cp012-sc-b-run-2026-03-14-012.envelope.json | — | complete |
| run-2026-03-14-013 | 2026-03-14 | cp-001 | qwen2.5:14b | valid_candidate | valid | 1 | — | outputs/qwen2.5-14b-continuity-adj-cp001-sc-a-cp001-sc-b-run-2026-03-14-013.envelope.json | — | complete |
| run-2026-03-14-014 | 2026-03-14 | cp-002 | qwen2.5:14b | valid_candidate | valid | 1 | — | outputs/qwen2.5-14b-continuity-adj-cp002-sc-a-cp002-sc-b-run-2026-03-14-014.envelope.json | — | complete |
| run-2026-03-14-015 | 2026-03-14 | cp-003 | qwen2.5:14b | valid_candidate | valid | 1 | — | outputs/qwen2.5-14b-continuity-adj-cp003-sc-a-cp003-sc-b-run-2026-03-14-015.envelope.json | — | complete |
| run-2026-03-14-016 | 2026-03-14 | cp-004 | qwen2.5:14b | valid_candidate | valid | 0 | — | outputs/qwen2.5-14b-continuity-adj-cp004-sc-a-cp004-sc-b-run-2026-03-14-016.envelope.json | — | complete |
| run-2026-03-14-017 | 2026-03-14 | cp-005 | qwen2.5:14b | valid_candidate | valid | 0 | — | outputs/qwen2.5-14b-continuity-adj-cp005-sc-a-cp005-sc-b-run-2026-03-14-017.envelope.json | — | complete |
| run-2026-03-14-018 | 2026-03-14 | cp-006 | qwen2.5:14b | valid_candidate | valid | 0 | — | outputs/qwen2.5-14b-continuity-adj-cp006-sc-a-cp006-sc-b-run-2026-03-14-018.envelope.json | — | complete |
| run-2026-03-14-019 | 2026-03-14 | cp-007 | qwen2.5:14b | valid_candidate | valid | 1 | — | outputs/qwen2.5-14b-continuity-adj-cp007-sc-a-cp007-sc-b-run-2026-03-14-019.envelope.json | — | complete |
| run-2026-03-14-020 | 2026-03-14 | cp-008 | qwen2.5:14b | valid_candidate | valid | 0 | — | outputs/qwen2.5-14b-continuity-adj-cp008-sc-a-cp008-sc-b-run-2026-03-14-020.envelope.json | — | complete |
| run-2026-03-14-021 | 2026-03-14 | cp-009 | qwen2.5:14b | valid_candidate | valid | 0 | — | outputs/qwen2.5-14b-continuity-adj-cp009-sc-a-cp009-sc-b-run-2026-03-14-021.envelope.json | — | complete |
| run-2026-03-14-022 | 2026-03-14 | cp-010 | qwen2.5:14b | valid_candidate | valid | 0 | — | outputs/qwen2.5-14b-continuity-adj-cp010-sc-a-cp010-sc-b-run-2026-03-14-022.envelope.json | — | complete |
| run-2026-03-14-023 | 2026-03-14 | cp-011 | qwen2.5:14b | valid_candidate | valid | 0 | — | outputs/qwen2.5-14b-continuity-adj-cp011-sc-a-cp011-sc-b-run-2026-03-14-023.envelope.json | — | complete |
| run-2026-03-14-024 | 2026-03-14 | cp-012 | qwen2.5:14b | valid_candidate | valid | 0 | — | outputs/qwen2.5-14b-continuity-adj-cp012-sc-a-cp012-sc-b-run-2026-03-14-024.envelope.json | — | complete |
| run-2026-03-14-025 | 2026-03-14 | cp-001 | phi4-reasoning:latest | valid_candidate | valid | 0 | CORRUPTED: extractor grabbed template JSON from inside think block; superseded by run-026 | outputs/phi4-reasoning-latest-continuity-adj-cp001-sc-a-cp001-sc-b-run-2026-03-14-025.envelope.json | — | skipped |
| run-2026-03-14-026a | 2026-03-14 | cp-001 | phi4-reasoning:latest | fail_closed | fail_closed | 0 | schema_violation: missing required top-level fields (schema_version, lane_id, etc); model output only candidate_findings partial object | outputs/phi4-reasoning-latest-continuity-adj-cp001-sc-a-cp001-sc-b-run-2026-03-14-026.envelope.json | — | skipped |
| run-2026-03-14-026b | 2026-03-14 | cp-002 | phi4-reasoning:latest | fail_closed | fail_closed | 0 | schema_violation: missing required top-level fields; model output partial object with scene_ids + candidate_findings only | outputs/phi4-reasoning-latest-continuity-adj-cp002-sc-a-cp002-sc-b-run-2026-03-14-026.envelope.json | — | skipped |
| run-2026-03-14-026c | 2026-03-14 | cp-003 | phi4-reasoning:latest | fail_closed | fail_closed | 0 | schema_violation: missing overall_run_note and other required top-level fields; same partial-object pattern | outputs/phi4-reasoning-latest-continuity-adj-cp003-sc-a-cp003-sc-b-run-2026-03-14-026.envelope.json | — | skipped |

---

## Model summary table

Update after each model's full pass (all 12 adjacent-scene cases complete).

| model | cases_run | valid_envelopes | fail_closed | hard_fail_count | total_findings | avg_findings_per_case | cases_needing_review |
|-------|-----------|-----------------|------------|----------------|---------------|-----------------------|----------------------|
| phi4:14b | 12 | 12 | 0 | 0 | 9 | 0.75 | 0 (all reviewed) |
| qwen2.5:14b | 12 | 12 | 0 | 0 | 4 | 0.33 | 0 (all reviewed) |
| phi4-reasoning:latest | 3 (stopped at disqualifying threshold) | 0 | 3 | 3 | 0 | 0 | 0 |

---

## Hard-fail tracking

Record any run that produced a hard schema failure (validator exit code 2 or fail_closed).

| run_id | case_id | model | failure_reason |
|--------|---------|-------|----------------|
| run-2026-03-14-026a | cp-001 | phi4-reasoning:latest | schema_violation: model output partial JSON (candidate_findings only); missing schema_version, lane_id, analysis_scope_type, analysis_scope_bounds, input_unit_ids, overall_run_note, run_posture |
| run-2026-03-14-026b | cp-002 | phi4-reasoning:latest | schema_violation: model output partial JSON (scene_ids + candidate_findings only); same missing top-level fields |
| run-2026-03-14-026c | cp-003 | phi4-reasoning:latest | schema_violation: missing overall_run_note and other required top-level fields; consistent partial-object pattern — disqualifying threshold reached at 3/3 |

---

## Notes

Add any operational notes about run conditions, model availability, or anomalies.

**phi4-reasoning:latest — extraction bug and schema compliance failure (2026-03-14)**

Run-025: corrupted extraction. The executor's JSON extractor grabbed the example schema template from inside the model's `<think>` block rather than the actual output after `</think>`. The template contained the literal placeholder string `"<short summary of what you found or did not find>"` as `overall_run_note` and empty `candidate_findings`. Envelope was marked valid by the schema validator because the template structure is schema-conformant. Envelope is invalid as a content artifact. Superseded by run-026a.

Extractor fix applied after run-025: added `strip_think_blocks()` to both `run-continuity-adjacent-scene.sh` and `validate-continuity-candidate.py`. The regex now strips `<think>...</think>` before attempting JSON extraction.

Runs 026a/b/c: After the extractor fix, phi4-reasoning:latest consistently produced partial JSON objects — subsets of the required fields, not the full schema. The model generates its own custom structure (e.g. `{candidate_findings: [...]}` or `{scene_ids: [...], candidate_findings: [...]}`) rather than the full top-level schema. Three consecutive hard fails triggered the disqualifying threshold. Pass stopped at 3/12.

Run ID collision: fail-closed runs do not log to `registry/runs.md`, so `next-run-id.sh` did not advance past run-025 for any of the failed phi4-reasoning runs. Runs 026a/b/c share the ID space manually suffixed for ledger disambiguation. This is a known design gap — the registry only tracks successful runs.

---

## Freeze note

This ledger covers the **first-pass challenger runs** only.

Once the first pass is complete for both `phi4-reasoning:latest` and `qwen2.5:14b`, close this ledger and write:

`continuity-adjacent-scene-first-pass-results.md`

That document should synthesize ledger data into reviewer judgments and lane recommendations.
