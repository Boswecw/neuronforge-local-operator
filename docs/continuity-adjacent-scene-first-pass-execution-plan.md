# Continuity Adjacent-Scene First-Pass Execution Plan

Date: 2026-03-14

## Purpose

Define the controlled execution sequence for the first governed challenger comparison on the `continuity-progression-reasoning` lane.

This plan covers the adjacent-scene subset only (cp-001 through cp-012).

---

## What this plan governs

- Which cases to run
- Which models to run them against
- In what order
- How to record results
- What constitutes a complete pass
- What to do with a hard failure
- What happens after both challengers have run

---

## Lane state going in

- **Task contract:** `analyze.continuity.adjacent_scene.v1` — implemented
- **Executor:** `scripts/run-continuity-adjacent-scene.sh` — implemented
- **Schema validator:** `scripts/validate-continuity-candidate.py` — implemented
- **Renderer:** `scripts/render-continuity-candidate.sh` — implemented
- **Case packets:** `inputs/case-packets/cp-001.json` through `cp-012.json` — all populated
- **Results ledger:** `evals/continuity-adjacent-scene-first-pass-ledger.md` — initialized
- **Review worksheet:** `docs/continuity-progression-review-worksheet-v1.md` — available

---

## Frozen case set

Run exactly these 12 cases in this order:

| Order | Case ID | Primary category | Finding expected |
|-------|---------|-----------------|-----------------|
| 1 | `cp-001` | true_continuity_tension | yes |
| 2 | `cp-002` | apparent_not_real | no (restraint) |
| 3 | `cp-003` | true_progression_break | yes |
| 4 | `cp-004` | acceptable_abrupt_transition | no (restraint) |
| 5 | `cp-005` | repeated_movement_worth_flagging | yes |
| 6 | `cp-006` | repeated_movement_not_worth_flagging | no (restraint) |
| 7 | `cp-007` | descriptive_mismatch | yes |
| 8 | `cp-008` | ambiguous_edge | partial |
| 9 | `cp-009` | state_carry_forward_issue | yes |
| 10 | `cp-010` | unclear_causal_link | yes |
| 11 | `cp-011` | apparent_not_real (v2) | no (restraint) |
| 12 | `cp-012` | true_progression_break (v2) | yes |

Do not add, remove, or reorder cases between challengers.

---

## Challenger sequence

### Pass 1 — phi4-reasoning:latest

Run all 12 cases with `phi4-reasoning:latest`.

```bash
# Run a single case
scripts/run-continuity-adjacent-scene.sh phi4-reasoning:latest inputs/case-packets/cp-001.json

# Repeat for cp-002 through cp-012
```

After each run:
- Note the run ID from the registry
- Note the envelope status and findings count
- Add a row to the ledger

After all 12 runs for this model:
- Review each valid envelope using the worksheet
- Record worksheet outcome in the ledger

### Pass 2 — qwen2.5:14b

Run the identical 12 cases with `qwen2.5:14b`.

```bash
scripts/run-continuity-adjacent-scene.sh qwen2.5:14b inputs/case-packets/cp-001.json

# Repeat for cp-002 through cp-012
```

Same post-run procedure as pass 1.

---

## Per-run procedure

For each case run:

1. Execute the run script
2. Check the terminal output for envelope status
3. If `valid_candidate`:
   - Render the envelope for review: `scripts/render-continuity-candidate.sh <envelope_file>`
   - Note findings count and overall_run_note
4. If `fail_closed`:
   - Record failure reason in the ledger and hard-fail tracking table
   - Do not score the run; treat as schema failure
5. Add ledger row (all runs, regardless of status)

---

## Review procedure (valid envelopes only)

After a model's full pass, review each valid envelope:

1. Open the rendered Markdown
2. Complete a review worksheet entry for each case
3. Score across dimensions per the rubric in `docs/continuity-progression-review-rubric.md`
4. Mark ledger `reviewer_outcome` as `complete`

Do not score fail-closed envelopes. They have already failed.

---

## Hard-fail handling

If any run produces a fail-closed envelope:

- Record it in the ledger hard-fail table
- Do not re-run immediately
- Note whether the failure is schema failure (validator exit 1) or parse failure (exit 2)
- After all 12 cases: assess whether hard-fail rate is a disqualifying signal for the model

Hard-fail rate thresholds:

| Hard-fail count | Signal |
|----------------|--------|
| 0 of 12 | Clean pass — continue to review |
| 1–2 of 12 | Notable — review failure reasons before scoring |
| 3+ of 12 | Disqualifying for first-pass adoption — still review remainder |

---

## What constitutes a complete pass

A model's pass is complete when:

- All 12 cases have been run (not necessarily all valid)
- All valid envelopes have been reviewed with the worksheet
- The ledger model summary row is filled in
- Any hard fails are noted with failure reasons

---

## Post-pass synthesis

After both models have completed their passes:

Write `docs/continuity-adjacent-scene-first-pass-results.md` covering:

- Per-case outcome comparison (phi4 vs qwen2.5)
- Schema reliability (fail-closed count per model)
- Hard-fail pattern analysis
- Evidence quality trend per model
- Restraint performance per model (false-positive cases)
- Overall recommendation: which model is the stronger starting point for lane trust

---

## Do not do

- Do not run only partial cases and claim a pass is complete
- Do not adjust case packets between models
- Do not score fail-closed envelopes as if they were findings
- Do not re-run a case to get a better result without documenting the re-run
- Do not promote any model to lane baseline before the worksheet review is complete

---

## What success looks like for this lane at this stage

This first pass is not about finding a perfect model.

It is about establishing:

- which model can reliably produce schema-valid output for adjacent-scene cases
- which model can flag genuine issues without over-flagging restraint cases
- whether the contract path works end-to-end under real execution

A model that produces mostly valid envelopes with moderate evidence quality and acceptable restraint is good enough to anchor a first-pass baseline.

Perfection is not the bar. Governed, reviewable, fail-closed behavior is the bar.

---

## Sequence summary

```
1. Run phi4-reasoning:latest against cp-001 through cp-012
2. Record all results in ledger
3. Render and review valid envelopes with worksheet
4. Run qwen2.5:14b against cp-001 through cp-012
5. Record all results in ledger
6. Render and review valid envelopes with worksheet
7. Write first-pass results summary doc
8. Update lane status
```
