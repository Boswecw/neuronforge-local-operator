# Lane Analytics Schema

## Purpose

Define the minimum analytics and governance shape that each Neuronforge lane should expose for operator visibility and future ForgeCommand integration.

This schema is intentionally small and operational.

It is meant to answer:

- what lane is this
- what model is currently trusted
- what challengers have been tested
- what happened in those evaluations
- whether a new model should be adopted

---

## Lane record

Each lane should expose one current lane record.

### Required fields

- `lane_id`
- `lane_name`
- `lane_type`
- `status`
- `current_baseline_model`
- `current_baseline_prompt`
- `anchor_input`
- `anchor_run_id`
- `last_evaluated_date`
- `current_judgment`
- `calibration_doc`
- `status_doc`

### Example

~~~json
{
  "lane_id": "lore-safe-proofreading",
  "lane_name": "Lore Safe Proofreading",
  "lane_type": "proofreading",
  "status": "active",
  "current_baseline_model": "qwen2.5:14b",
  "current_baseline_prompt": "prompts/lore-safe-proofread-003.md",
  "anchor_input": "inputs/lore-safe-test-001.md",
  "anchor_run_id": "run-2026-03-13-005",
  "last_evaluated_date": "2026-03-13",
  "current_judgment": "baseline unchanged",
  "calibration_doc": "docs/lore-safe-calibration-notes.md",
  "status_doc": "evals/lore-safe-lane-status-2026-03-13.md"
}
~~~

---

## Model lane status record

Each tested model should have one current status record per lane.

This is lane-specific.

A model can be trusted in one lane and rejected in another.

### Required fields

- `lane_id`
- `model_id`
- `status`
- `last_eval_date`
- `anchor_result`
- `suite_result`
- `preferred_count`
- `tie_count`
- `acceptable_count`
- `reject_count`
- `weighted_issue_score`
- `last_review_doc`
- `adoption_state`

### Suggested status values

- `baseline`
- `contender`
- `rejected`
- `retired`
- `experimental`

### Suggested adoption state values

- `current`
- `hold`
- `watch`
- `do-not-adopt`
- `retired`

### Example

~~~json
{
  "lane_id": "lore-safe-proofreading",
  "model_id": "phi4:14b",
  "status": "contender",
  "last_eval_date": "2026-03-13",
  "anchor_result": "acceptable",
  "suite_result": "mixed",
  "preferred_count": 1,
  "tie_count": 2,
  "acceptable_count": 1,
  "reject_count": 2,
  "weighted_issue_score": 13,
  "last_review_doc": "evals/run-2026-03-13-024-review.md",
  "adoption_state": "hold"
}
~~~

---

## Case result record

Each evaluated test case should produce one case result record for a given model in a given lane.

This supports drill-down when aggregate counts are not enough.

### Required fields

- `lane_id`
- `model_id`
- `test_input`
- `run_id`
- `outcome_class`
- `weighted_issue_score`
- `preservation_drift`
- `grammar_issue_count`
- `hard_failure`
- `review_doc`
- `notes`

### Outcome class values

- `reject`
- `acceptable`
- `preferred`
- `tie`

### Example

~~~json
{
  "lane_id": "lore-safe-proofreading",
  "model_id": "phi4:14b",
  "test_input": "inputs/lore-safe-test-005.md",
  "run_id": "run-2026-03-13-028",
  "outcome_class": "reject",
  "weighted_issue_score": 5,
  "preservation_drift": true,
  "grammar_issue_count": 0,
  "hard_failure": true,
  "review_doc": "evals/run-2026-03-13-028-review.md",
  "notes": "Meaning drift introduced through content alteration."
}
~~~

---

## Adoption decision record

Each explicit adoption decision should be stored as a separate record.

This includes decisions to keep the baseline unchanged.

### Required fields

- `decision_id`
- `decision_date`
- `lane_id`
- `baseline_model_before`
- `candidate_model`
- `decision`
- `reason_summary`
- `evidence_refs`
- `operator`

### Decision values

- `adopted`
- `baseline unchanged`
- `rejected`
- `retired`

### Example

~~~json
{
  "decision_id": "decision-2026-03-13-lore-safe-001",
  "decision_date": "2026-03-13",
  "lane_id": "lore-safe-proofreading",
  "baseline_model_before": "qwen2.5:14b",
  "candidate_model": "phi4:14b",
  "decision": "baseline unchanged",
  "reason_summary": "Candidate was viable but failed multiple harder cases and did not exceed the locked baseline across the lane.",
  "evidence_refs": [
    "evals/lore-safe-lane-status-2026-03-13.md",
    "docs/lore-safe-calibration-notes.md",
    "evals/run-2026-03-13-024-review.md"
  ],
  "operator": "charlie"
}
~~~

---

## Minimum ForgeCommand view

ForgeCommand does not need full raw evaluation text to show useful lane state.

Minimum lane analytics view should expose:

- lane name
- lane status
- current baseline model
- current baseline prompt
- last evaluated date
- current judgment
- contender models
- rejected models
- preferred/tie/acceptable/reject counts by model
- weighted issue score by model
- last adoption decision
- links to calibration and status docs

### Example operator-facing summary shape

~~~json
{
  "lane_id": "lore-safe-proofreading",
  "lane_name": "Lore Safe Proofreading",
  "status": "active",
  "baseline_model": "qwen2.5:14b",
  "baseline_prompt": "prompts/lore-safe-proofread-003.md",
  "last_evaluated_date": "2026-03-13",
  "current_judgment": "baseline unchanged",
  "models": [
    {
      "model_id": "qwen2.5:14b",
      "status": "baseline",
      "weighted_issue_score": 0
    },
    {
      "model_id": "phi4:14b",
      "status": "contender",
      "preferred_count": 1,
      "tie_count": 2,
      "acceptable_count": 1,
      "reject_count": 2,
      "weighted_issue_score": 13,
      "adoption_state": "hold"
    }
  ],
  "last_decision": "baseline unchanged",
  "calibration_doc": "docs/lore-safe-calibration-notes.md",
  "status_doc": "evals/lore-safe-lane-status-2026-03-13.md"
}
~~~

---

## Working rules for lane-specific model governance

- Model trust is lane-specific, not global.
- A model must not be adopted because it performs well outside the lane.
- Correctness failures outweigh stylistic preference.
- Deletion or omission is a hard failure.
- Preservation drift must be tracked separately from grammar quality.
- Aggregate counts are useful, but adoption decisions must still cite case-level evidence.
- Keeping the baseline unchanged is a valid recorded decision.
- A contender may remain in hold status if it is viable but not yet superior.
- Retired models should remain historically visible in decision records.

---

## Severity guidance

Weighted issue scoring should remain simple and stable.

- `5` = hard failure
- `3` = serious lane damage
- `2` = moderate issue
- `1` = minor issue
- `0` = no issue

This score is not the only adoption signal.

It supports comparison, trend tracking, and operator visibility.

---

## Initial implementation note

This schema is designed to be small enough for:

- markdown-backed manual tracking now
- local Postgres tables later
- ForgeCommand visibility without redesign

It should be treated as the minimum governance shape, not the final analytics ceiling.
