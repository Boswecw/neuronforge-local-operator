# Style Analysis Lane Status — 2026-03-21

## Lane
- lane_id: analyze-style-scene-v1
- lane_name: Style Analysis — Scene (v1)

## Current state
- status: evaluating
- model: qwen2.5:14b
- prompt profile: style-analysis-scene-v1
- anchor input: inputs/style-analysis-eval/scene-01-clean.md
- anchor run id: eval-2026-03-21-001
- calibration doc: evals/style-analysis-calibration-2026-03-21.md

## Eval set summary
- 5 scenes run: run-2026-03-21-001 through run-2026-03-21-005
- all 5 runs returned schema_validation_status: valid
- schema_reliability: 1.00
- false_positive_rate: 0.00 (operator judgment)
- surface_detection_rate: 1.00 (operator judgment, with calibration note on voice_consistency)

## Key calibration note
The voice_consistency dimension may track tonal register consistency rather than POV fidelity. Scene-04 (voice drift) was identified correctly in evidence spans but miscategorized to flow/pacing rather than voice_consistency at the score level. This should be investigated further before baseline adoption.

## Governance state
- first structured evaluation complete
- lane promoted from implementing to evaluating
- calibration doc produced
- schema reliability confirmed at 1.00 for this set
- metrics are operator-judged, not benchmark-derived

## Next likely step
Run 3+ additional POV-shift scenes to probe voice_consistency dimension interpretation. Determine whether the scene-04 miscategorization is a systematic model behavior or an edge case. Assess readiness for candidate_baseline promotion after that investigation.
