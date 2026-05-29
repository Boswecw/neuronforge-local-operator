# Run Registry

## Fields
- run id
- date
- model
- prompt file
- input file
- output file
- task
- notes

## Entries
- run id: run-2026-03-13-001
  date: 2026-03-13
  model: deepseek-r1:7b
  prompt file: prompts/proofread-basic-001.md
  input file: inputs/test-proofread-001.md
  output file: outputs/deepseek-r1-7b-proofread-001.md
  task: baseline proofreading test
  notes: produced visible reasoning and violated return-only-text rule; made some correct edits but also introduced a meaning shift
- run id: run-2026-03-13-002
  date: 2026-03-13
  model: deepseek-r1:7b
  prompt file: prompts/lore-safe-proofread-001.md
  input file: inputs/lore-safe-test-001.md
  output file: outputs/deepseek-r1-7b-lore-safe-001.md
  task: lore-safe proofreading baseline
  notes: failed hard; exposed reasoning, added commentary, violated return-only-text rule, altered imagery and meaning
- run id: run-2026-03-13-003
  date: 2026-03-13
  model: deepseek-r1:7b
  prompt file: prompts/lore-safe-proofread-002.md
  input file: inputs/lore-safe-test-001.md
  output file: outputs/deepseek-r1-7b-lore-safe-002.md
  task: lore-safe proofreading prompt revision test
  notes: still failed; reasoning leakage remained, commentary remained, output format failed, and proofreading quality remained unreliable
- run id: run-2026-03-13-004
  date: 2026-03-13
  model: qwen2.5:14b
  prompt file: prompts/lore-safe-proofread-002.md
  input file: inputs/lore-safe-test-001.md
  output file: outputs/qwen2.5-14b-lore-safe-001.md
  task: lore-safe proofreading comparison baseline
  notes: strong improvement over deepseek-r1:7b; no reasoning leakage or commentary; output format passed; still made some non-minimal wording changes; speed somewhat slow
- run id: run-2026-03-13-005
  date: 2026-03-13
  model: qwen2.5:14b
  prompt file: prompts/lore-safe-proofread-003.md
  input file: inputs/lore-safe-test-001.md
  output file: outputs/qwen2.5-14b-lore-safe-002.md
  task: lore-safe proofreading minimal-edit revision test
  notes: best result so far; clean output, no reasoning leakage, protected terms preserved, unnecessary rewrites reduced; still changed "sat badly in him" to "sat badly with him"
- run id: run-2026-03-13-006
  date: 2026-03-13
  model: qwen2.5:14b
  prompt file: prompts/lore-safe-proofread-003.md
  input file: inputs/lore-safe-test-001.md
  output file: outputs/qwen2.5-14b-lore-safe-003.md
  task: lore-safe proofreading repeatability check via script
  notes: script worked; output remained clean and compliant; slight wording drift remained between repeated runs, so behavior is usable but not perfectly deterministic
- run id: run-2026-03-13-007
  date: 2026-03-13
  model: qwen2.5:14b
  prompt file: prompts/lore-safe-proofread-003.md
  input file: inputs/lore-safe-test-001.md
  output file: outputs/qwen2.5-14b-lore-safe-004.md
  task: lore-safe proofreading review-workflow stability check
  notes: review helper script worked correctly; output matched prior run exactly; no diff against outputs/qwen2.5-14b-lore-safe-003.md

- run id: run-2026-03-13-008
  date: 2026-03-13
  model: qwen2.5:14b
  prompt file: prompts/lore-safe-proofread-003.md
  input file: inputs/lore-safe-test-001.md
  output file: outputs/qwen2.5-14b-lore-safe-004.md
  task: helper script logging test
  notes: test entry created by scripts/log-run.sh

- run id: run-2026-03-13-009
  date: 2026-03-13
  model: qwen2.5:14b
  prompt file: prompts/lore-safe-proofread-003.md
  input file: inputs/lore-safe-test-001.md
  output file: outputs/qwen2.5-14b-lore-safe-005.md
  task: wrapper script end-to-end test
  notes: proofread and log completed through wrapper script

- run id: run-2026-03-13-011
  date: 2026-03-13
  model: qwen2.5:14b
  prompt file: prompts/lore-safe-proofread-003.md
  input file: inputs/lore-safe-test-001.md
  output file: outputs/qwen2.5-14b-lore-safe-006.md
  task: wrapper auto-date test
  notes: date omitted intentionally; wrapper should fill with system date

- run id: run-2026-03-13-012
  date: 2026-03-13
  model: qwen2.5:14b
  prompt file: prompts/lore-safe-proofread-003.md
  input file: inputs/lore-safe-test-001.md
  output file: outputs/qwen2.5-14b-lore-safe-007.md
  task: wrapper auto-run-id test
  notes: run id and date omitted intentionally; wrapper should fill both

- run id: run-2026-03-13-013
  date: 2026-03-13
  model: qwen2.5:14b
  prompt file: prompts/lore-safe-proofread-003.md
  input file: inputs/lore-safe-test-001.md
  output file: outputs/qwen2.5-14b-lore-safe-test-001-run-2026-03-13-013.md
  task: wrapper auto-output test
  notes: run id, date, and output omitted intentionally; wrapper should fill all three

- run id: run-2026-03-13-014
  date: 2026-03-13
  model: qwen2.5:14b
  prompt file: prompts/lore-safe-proofread-003.md
  input file: inputs/lore-safe-test-001.md
  output file: outputs/qwen2.5-14b-lore-safe-test-001-run-2026-03-13-014.md
  task: proofread
  notes: live run verification

- run id: run-2026-03-13-015
  date: 2026-03-13
  model: qwen2.5:14b
  prompt file: prompts/lore-safe-proofread-003.md
  input file: inputs/lore-safe-test-001.md
  output file: outputs/qwen2.5-14b-lore-safe-test-001-run-2026-03-13-015.md
  task: proofread
  notes: post-hardening live run

- run id: run-2026-03-13-016
  date: 2026-03-13
  model: gemma3:4b
  prompt file: prompts/lore-safe-proofread-003.md
  input file: inputs/lore-safe-test-001.md
  output file: outputs/gemma3-4b-lore-safe-test-001-run-2026-03-13-016.md
  task: lore-safe proofreading challenger test
  notes: stayed inside output contract and preserved terms and tone, but failed challenger review due to core grammar errors


- run id: run-2026-03-13-017
  date: 2026-03-13
  model: qwen2.5:7b
  prompt file: prompts/lore-safe-proofread-003.md
  input file: inputs/lore-safe-test-001.md
  output file: outputs/qwen2.5-7b-lore-safe-test-001-run-2026-03-13-017.md
  task: lore-safe proofreading challenger test
  notes: qwen2.5:7b challenger run against current qwen2.5:14b baseline

- run id: run-2026-03-13-018
  date: 2026-03-13
  model: gemma3:12b
  prompt file: prompts/lore-safe-proofread-003.md
  input file: inputs/lore-safe-test-001.md
  output file: outputs/gemma3-12b-lore-safe-test-001-run-2026-03-13-018.md
  task: lore-safe proofreading challenger test
  notes: gemma3:12b challenger run against current qwen2.5:14b baseline

- run id: run-2026-03-13-019
  date: 2026-03-13
  model: qwen2.5:14b
  prompt file: prompts/lore-safe-proofread-004.md
  input file: inputs/lore-safe-test-001.md
  output file: outputs/qwen2.5-14b-lore-safe-test-001-run-2026-03-13-019.md
  task: lore-safe proofreading prompt challenger test
  notes: qwen2.5:14b test of prompt 004 against current prompt 003 baseline

- run id: run-2026-03-13-020
  date: 2026-03-13
  model: llama3.1:8b
  prompt file: prompts/lore-safe-proofread-003.md
  input file: inputs/lore-safe-test-001.md
  output file: outputs/run-2026-03-13-020-lore-safe-test-001-llama3.1-8b.md
  task: lore-safe-proofreading
  notes: challenger run for llama3.1:8b against current qwen2.5:14b baseline

- run id: run-2026-03-13-021
  date: 2026-03-13
  model: mistral:7b-instruct
  prompt file: prompts/lore-safe-proofread-003.md
  input file: inputs/lore-safe-test-001.md
  output file: outputs/run-2026-03-13-021-lore-safe-test-001-mistral-7b-instruct.md
  task: lore-safe-proofreading
  notes: challenger run for mistral:7b-instruct against current qwen2.5:14b baseline

- run id: run-2026-03-13-022
  date: 2026-03-13
  model: olmo2:13b
  prompt file: prompts/lore-safe-proofread-003.md
  input file: inputs/lore-safe-test-001.md
  output file: outputs/run-2026-03-13-022-lore-safe-test-001-olmo2-13b.md
  task: lore-safe-proofreading
  notes: challenger run for olmo2:13b against current qwen2.5:14b baseline

- run id: run-2026-03-13-023
  date: 2026-03-13
  model: cogito:14b
  prompt file: prompts/lore-safe-proofread-003.md
  input file: inputs/lore-safe-test-001.md
  output file: outputs/run-2026-03-13-023-lore-safe-test-001-cogito-14b.md
  task: lore-safe-proofreading
  notes: challenger run for cogito:14b against current qwen2.5:14b baseline

- run id: run-2026-03-13-024
  date: 2026-03-13
  model: phi4:14b
  prompt file: prompts/lore-safe-proofread-003.md
  input file: inputs/lore-safe-test-001.md
  output file: outputs/run-2026-03-13-024-lore-safe-test-001-phi4-14b.md
  task: lore-safe-proofreading
  notes: challenger run for phi4:14b against current qwen2.5:14b baseline

- run id: run-2026-03-13-025
  date: 2026-03-13
  model: qwen2.5:14b
  prompt file: prompts/lore-safe-proofread-003.md
  input file: inputs/lore-safe-test-002.md
  output file: outputs/run-2026-03-13-025-lore-safe-test-002-qwen2.5-14b.md
  task: lore-safe-proofreading
  notes: baseline suite expansion test 002 with locked qwen baseline

- run id: run-2026-03-13-026
  date: 2026-03-13
  model: phi4:14b
  prompt file: prompts/lore-safe-proofread-003.md
  input file: inputs/lore-safe-test-002.md
  output file: outputs/run-2026-03-13-026-lore-safe-test-002-phi4-14b.md
  task: lore-safe-proofreading
  notes: challenger suite expansion test 002 with phi4 contender

- run id: run-2026-03-13-027
  date: 2026-03-13
  model: qwen2.5:14b
  prompt file: prompts/lore-safe-proofread-003.md
  input file: inputs/lore-safe-test-003.md
  output file: outputs/run-2026-03-13-027-lore-safe-test-003-qwen2.5-14b.md
  task: lore-safe-proofreading
  notes: baseline suite expansion test 003 with locked qwen baseline

- run id: run-2026-03-13-028
  date: 2026-03-13
  model: phi4:14b
  prompt file: prompts/lore-safe-proofread-003.md
  input file: inputs/lore-safe-test-003.md
  output file: outputs/run-2026-03-13-028-lore-safe-test-003-phi4-14b.md
  task: lore-safe-proofreading
  notes: challenger suite expansion test 003 with phi4 contender

- run id: run-2026-03-13-029
  date: 2026-03-13
  model: qwen2.5:14b
  prompt file: prompts/lore-safe-proofread-003.md
  input file: inputs/lore-safe-test-004.md
  output file: outputs/run-2026-03-13-029-lore-safe-test-004-qwen2.5-14b.md
  task: lore-safe-proofreading
  notes: baseline suite expansion test 004 with locked qwen baseline

- run id: run-2026-03-13-030
  date: 2026-03-13
  model: phi4:14b
  prompt file: prompts/lore-safe-proofread-003.md
  input file: inputs/lore-safe-test-004.md
  output file: outputs/run-2026-03-13-030-lore-safe-test-004-phi4-14b.md
  task: lore-safe-proofreading
  notes: challenger suite expansion test 004 with phi4 contender

- run id: run-2026-03-13-031
  date: 2026-03-13
  model: qwen2.5:14b
  prompt file: prompts/lore-safe-proofread-003.md
  input file: inputs/lore-safe-test-005.md
  output file: outputs/run-2026-03-13-031-lore-safe-test-005-qwen2.5-14b.md
  task: lore-safe-proofreading
  notes: baseline suite expansion test 005 with locked qwen baseline

- run id: run-2026-03-13-032
  date: 2026-03-13
  model: phi4:14b
  prompt file: prompts/lore-safe-proofread-003.md
  input file: inputs/lore-safe-test-005.md
  output file: outputs/run-2026-03-13-032-lore-safe-test-005-phi4-14b.md
  task: lore-safe-proofreading
  notes: challenger suite expansion test 005 with phi4 contender

- run id: run-2026-03-13-033
  date: 2026-03-13
  model: qwen2.5:14b
  prompt file: prompts/lore-safe-proofread-003.md
  input file: inputs/lore-safe-test-006.md
  output file: outputs/run-2026-03-13-033-lore-safe-test-006-qwen2.5-14b.md
  task: lore-safe-proofreading
  notes: baseline suite expansion test 006 with locked qwen baseline

- run id: run-2026-03-13-034
  date: 2026-03-13
  model: phi4:14b
  prompt file: prompts/lore-safe-proofread-003.md
  input file: inputs/lore-safe-test-006.md
  output file: outputs/run-2026-03-13-034-lore-safe-test-006-phi4-14b.md
  task: lore-safe-proofreading
  notes: challenger suite expansion test 006 with phi4 contender

- run id: run-2026-03-13-035
  date: 2026-03-13
  model: qwen2.5:14b
  prompt file: prompts/general-grammar-cleanup-001.md
  input file: inputs/general-grammar-test-001.md
  output file: outputs/qwen2.5-14b-general-grammar-test-001.md
  task: general-grammar-cleanup
  notes: anchor run for general grammar lane

- run id: run-2026-03-13-036
  date: 2026-03-13
  model: phi4:14b
  prompt file: prompts/general-grammar-cleanup-001.md
  input file: inputs/general-grammar-test-001.md
  output file: outputs/phi4-14b-general-grammar-test-001.md
  task: general-grammar-cleanup
  notes: anchor run for general grammar lane

- run id: run-2026-03-13-037
  date: 2026-03-13
  model: qwen2.5:14b
  prompt file: prompts/general-grammar-cleanup-001.md
  input file: inputs/general-grammar-test-002.md
  output file: outputs/qwen2.5-14b-general-grammar-test-002.md
  task: general-grammar-cleanup
  notes: test 002 for general grammar lane

- run id: run-2026-03-13-038
  date: 2026-03-13
  model: phi4:14b
  prompt file: prompts/general-grammar-cleanup-001.md
  input file: inputs/general-grammar-test-002.md
  output file: outputs/phi4-14b-general-grammar-test-002.md
  task: general-grammar-cleanup
  notes: test 002 for general grammar lane

- run id: run-2026-03-13-039
  date: 2026-03-13
  model: qwen2.5:14b
  prompt file: prompts/general-grammar-cleanup-001.md
  input file: inputs/general-grammar-test-003.md
  output file: outputs/qwen2.5-14b-general-grammar-test-003.md
  task: general-grammar-cleanup
  notes: test 003 for general grammar lane

- run id: run-2026-03-13-040
  date: 2026-03-13
  model: phi4:14b
  prompt file: prompts/general-grammar-cleanup-001.md
  input file: inputs/general-grammar-test-003.md
  output file: outputs/phi4-14b-general-grammar-test-003.md
  task: general-grammar-cleanup
  notes: test 003 for general grammar lane

- run id: run-2026-03-13-041
  date: 2026-03-13
  model: qwen2.5:14b
  prompt file: prompts/general-grammar-cleanup-001.md
  input file: inputs/general-grammar-test-004.md
  output file: outputs/qwen2.5-14b-general-grammar-test-004.md
  task: general-grammar-cleanup
  notes: test 004 for general grammar lane

- run id: run-2026-03-13-042
  date: 2026-03-13
  model: phi4:14b
  prompt file: prompts/general-grammar-cleanup-001.md
  input file: inputs/general-grammar-test-004.md
  output file: outputs/phi4-14b-general-grammar-test-004.md
  task: general-grammar-cleanup
  notes: test 004 for general grammar lane

- run id: run-2026-03-13-043
  date: 2026-03-13
  model: qwen2.5:14b
  prompt file: prompts/general-grammar-cleanup-001.md
  input file: inputs/general-grammar-test-005.md
  output file: outputs/qwen2.5-14b-general-grammar-test-005.md
  task: general-grammar-cleanup
  notes: test 005 for general grammar lane

- run id: run-2026-03-13-044
  date: 2026-03-13
  model: phi4:14b
  prompt file: prompts/general-grammar-cleanup-001.md
  input file: inputs/general-grammar-test-005.md
  output file: outputs/phi4-14b-general-grammar-test-005.md
  task: general-grammar-cleanup
  notes: test 005 for general grammar lane

- run id: run-2026-03-14-001
  date: 2026-03-14
  model: phi4:14b
  prompt file: prompts/continuity-adjacent-scene-v1.md
  input file: inputs/case-packets/cp-001.json
  output file: outputs/phi4-14b-continuity-adj-cp001-sc-a-cp001-sc-b-run-2026-03-14-001.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp001-sc-a+cp001-sc-b, findings: 1

- run id: run-2026-03-14-002
  date: 2026-03-14
  model: phi4:14b
  prompt file: prompts/continuity-adjacent-scene-v1.md
  input file: inputs/case-packets/cp-002.json
  output file: outputs/phi4-14b-continuity-adj-cp002-sc-a-cp002-sc-b-run-2026-03-14-002.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp002-sc-a+cp002-sc-b, findings: 1

- run id: run-2026-03-14-003
  date: 2026-03-14
  model: phi4:14b
  prompt file: prompts/continuity-adjacent-scene-v1.md
  input file: inputs/case-packets/cp-003.json
  output file: outputs/phi4-14b-continuity-adj-cp003-sc-a-cp003-sc-b-run-2026-03-14-003.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp003-sc-a+cp003-sc-b, findings: 1

- run id: run-2026-03-14-004
  date: 2026-03-14
  model: phi4:14b
  prompt file: prompts/continuity-adjacent-scene-v1.md
  input file: inputs/case-packets/cp-004.json
  output file: outputs/phi4-14b-continuity-adj-cp004-sc-a-cp004-sc-b-run-2026-03-14-004.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp004-sc-a+cp004-sc-b, findings: 1

- run id: run-2026-03-14-005
  date: 2026-03-14
  model: phi4:14b
  prompt file: prompts/continuity-adjacent-scene-v1.md
  input file: inputs/case-packets/cp-005.json
  output file: outputs/phi4-14b-continuity-adj-cp005-sc-a-cp005-sc-b-run-2026-03-14-005.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp005-sc-a+cp005-sc-b, findings: 1

- run id: run-2026-03-14-006
  date: 2026-03-14
  model: phi4:14b
  prompt file: prompts/continuity-adjacent-scene-v1.md
  input file: inputs/case-packets/cp-006.json
  output file: outputs/phi4-14b-continuity-adj-cp006-sc-a-cp006-sc-b-run-2026-03-14-006.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp006-sc-a+cp006-sc-b, findings: 1

- run id: run-2026-03-14-007
  date: 2026-03-14
  model: phi4:14b
  prompt file: prompts/continuity-adjacent-scene-v1.md
  input file: inputs/case-packets/cp-007.json
  output file: outputs/phi4-14b-continuity-adj-cp007-sc-a-cp007-sc-b-run-2026-03-14-007.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp007-sc-a+cp007-sc-b, findings: 1

- run id: run-2026-03-14-008
  date: 2026-03-14
  model: phi4:14b
  prompt file: prompts/continuity-adjacent-scene-v1.md
  input file: inputs/case-packets/cp-008.json
  output file: outputs/phi4-14b-continuity-adj-cp008-sc-a-cp008-sc-b-run-2026-03-14-008.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp008-sc-a+cp008-sc-b, findings: 1

- run id: run-2026-03-14-009
  date: 2026-03-14
  model: phi4:14b
  prompt file: prompts/continuity-adjacent-scene-v1.md
  input file: inputs/case-packets/cp-009.json
  output file: outputs/phi4-14b-continuity-adj-cp009-sc-a-cp009-sc-b-run-2026-03-14-009.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp009-sc-a+cp009-sc-b, findings: 0

- run id: run-2026-03-14-010
  date: 2026-03-14
  model: phi4:14b
  prompt file: prompts/continuity-adjacent-scene-v1.md
  input file: inputs/case-packets/cp-010.json
  output file: outputs/phi4-14b-continuity-adj-cp010-sc-a-cp010-sc-b-run-2026-03-14-010.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp010-sc-a+cp010-sc-b, findings: 1

- run id: run-2026-03-14-011
  date: 2026-03-14
  model: phi4:14b
  prompt file: prompts/continuity-adjacent-scene-v1.md
  input file: inputs/case-packets/cp-011.json
  output file: outputs/phi4-14b-continuity-adj-cp011-sc-a-cp011-sc-b-run-2026-03-14-011.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp011-sc-a+cp011-sc-b, findings: 0

- run id: run-2026-03-14-012
  date: 2026-03-14
  model: phi4:14b
  prompt file: prompts/continuity-adjacent-scene-v1.md
  input file: inputs/case-packets/cp-012.json
  output file: outputs/phi4-14b-continuity-adj-cp012-sc-a-cp012-sc-b-run-2026-03-14-012.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp012-sc-a+cp012-sc-b, findings: 0

- run id: run-2026-03-14-013
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v1.md
  input file: inputs/case-packets/cp-001.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp001-sc-a-cp001-sc-b-run-2026-03-14-013.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp001-sc-a+cp001-sc-b, findings: 1

- run id: run-2026-03-14-014
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v1.md
  input file: inputs/case-packets/cp-002.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp002-sc-a-cp002-sc-b-run-2026-03-14-014.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp002-sc-a+cp002-sc-b, findings: 1

- run id: run-2026-03-14-015
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v1.md
  input file: inputs/case-packets/cp-003.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp003-sc-a-cp003-sc-b-run-2026-03-14-015.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp003-sc-a+cp003-sc-b, findings: 1

- run id: run-2026-03-14-016
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v1.md
  input file: inputs/case-packets/cp-004.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp004-sc-a-cp004-sc-b-run-2026-03-14-016.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp004-sc-a+cp004-sc-b, findings: 0

- run id: run-2026-03-14-017
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v1.md
  input file: inputs/case-packets/cp-005.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp005-sc-a-cp005-sc-b-run-2026-03-14-017.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp005-sc-a+cp005-sc-b, findings: 0

- run id: run-2026-03-14-018
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v1.md
  input file: inputs/case-packets/cp-006.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp006-sc-a-cp006-sc-b-run-2026-03-14-018.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp006-sc-a+cp006-sc-b, findings: 0

- run id: run-2026-03-14-019
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v1.md
  input file: inputs/case-packets/cp-007.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp007-sc-a-cp007-sc-b-run-2026-03-14-019.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp007-sc-a+cp007-sc-b, findings: 1

- run id: run-2026-03-14-020
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v1.md
  input file: inputs/case-packets/cp-008.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp008-sc-a-cp008-sc-b-run-2026-03-14-020.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp008-sc-a+cp008-sc-b, findings: 0

- run id: run-2026-03-14-021
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v1.md
  input file: inputs/case-packets/cp-009.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp009-sc-a-cp009-sc-b-run-2026-03-14-021.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp009-sc-a+cp009-sc-b, findings: 0

- run id: run-2026-03-14-022
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v1.md
  input file: inputs/case-packets/cp-010.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp010-sc-a-cp010-sc-b-run-2026-03-14-022.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp010-sc-a+cp010-sc-b, findings: 0

- run id: run-2026-03-14-023
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v1.md
  input file: inputs/case-packets/cp-011.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp011-sc-a-cp011-sc-b-run-2026-03-14-023.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp011-sc-a+cp011-sc-b, findings: 0

- run id: run-2026-03-14-024
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v1.md
  input file: inputs/case-packets/cp-012.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp012-sc-a-cp012-sc-b-run-2026-03-14-024.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp012-sc-a+cp012-sc-b, findings: 0

- run id: run-2026-03-14-025
  date: 2026-03-14
  model: phi4-reasoning:latest
  prompt file: prompts/continuity-adjacent-scene-v1.md
  input file: inputs/case-packets/cp-001.json
  output file: outputs/phi4-reasoning-latest-continuity-adj-cp001-sc-a-cp001-sc-b-run-2026-03-14-025.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp001-sc-a+cp001-sc-b, findings: 0

- run id: run-2026-03-14-026
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v2.md
  input file: inputs/case-packets/cp-001.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp001-sc-a-cp001-sc-b-run-2026-03-14-026.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp001-sc-a+cp001-sc-b, findings: 0

- run id: run-2026-03-14-027
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v2.md
  input file: inputs/case-packets/cp-002.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp002-sc-a-cp002-sc-b-run-2026-03-14-027.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp002-sc-a+cp002-sc-b, findings: 0

- run id: run-2026-03-14-028
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v2.md
  input file: inputs/case-packets/cp-003.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp003-sc-a-cp003-sc-b-run-2026-03-14-028.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp003-sc-a+cp003-sc-b, findings: 0

- run id: run-2026-03-14-029
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v2.md
  input file: inputs/case-packets/cp-004.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp004-sc-a-cp004-sc-b-run-2026-03-14-029.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp004-sc-a+cp004-sc-b, findings: 0

- run id: run-2026-03-14-030
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v2.md
  input file: inputs/case-packets/cp-005.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp005-sc-a-cp005-sc-b-run-2026-03-14-030.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp005-sc-a+cp005-sc-b, findings: 0

- run id: run-2026-03-14-031
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v2.md
  input file: inputs/case-packets/cp-006.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp006-sc-a-cp006-sc-b-run-2026-03-14-031.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp006-sc-a+cp006-sc-b, findings: 0

- run id: run-2026-03-14-032
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v2.md
  input file: inputs/case-packets/cp-007.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp007-sc-a-cp007-sc-b-run-2026-03-14-032.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp007-sc-a+cp007-sc-b, findings: 0

- run id: run-2026-03-14-033
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v2.md
  input file: inputs/case-packets/cp-008.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp008-sc-a-cp008-sc-b-run-2026-03-14-033.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp008-sc-a+cp008-sc-b, findings: 0

- run id: run-2026-03-14-034
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v2.md
  input file: inputs/case-packets/cp-009.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp009-sc-a-cp009-sc-b-run-2026-03-14-034.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp009-sc-a+cp009-sc-b, findings: 0

- run id: run-2026-03-14-035
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v2.md
  input file: inputs/case-packets/cp-010.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp010-sc-a-cp010-sc-b-run-2026-03-14-035.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp010-sc-a+cp010-sc-b, findings: 0

- run id: run-2026-03-14-036
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v2.md
  input file: inputs/case-packets/cp-011.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp011-sc-a-cp011-sc-b-run-2026-03-14-036.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp011-sc-a+cp011-sc-b, findings: 0

- run id: run-2026-03-14-037
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v2.md
  input file: inputs/case-packets/cp-012.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp012-sc-a-cp012-sc-b-run-2026-03-14-037.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp012-sc-a+cp012-sc-b, findings: 0

- run id: run-2026-03-14-038
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-001.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp001-sc-a-cp001-sc-b-run-2026-03-14-038.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp001-sc-a+cp001-sc-b, findings: 1

- run id: run-2026-03-14-039
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-002.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp002-sc-a-cp002-sc-b-run-2026-03-14-039.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp002-sc-a+cp002-sc-b, findings: 0

- run id: run-2026-03-14-040
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-004.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp004-sc-a-cp004-sc-b-run-2026-03-14-040.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp004-sc-a+cp004-sc-b, findings: 0

- run id: run-2026-03-14-041
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-005.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp005-sc-a-cp005-sc-b-run-2026-03-14-041.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp005-sc-a+cp005-sc-b, findings: 1

- run id: run-2026-03-14-042
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-006.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp006-sc-a-cp006-sc-b-run-2026-03-14-042.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp006-sc-a+cp006-sc-b, findings: 0

- run id: run-2026-03-14-043
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-007.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp007-sc-a-cp007-sc-b-run-2026-03-14-043.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp007-sc-a+cp007-sc-b, findings: 1

- run id: run-2026-03-14-044
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-008.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp008-sc-a-cp008-sc-b-run-2026-03-14-044.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp008-sc-a+cp008-sc-b, findings: 0

- run id: run-2026-03-14-045
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-009.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp009-sc-a-cp009-sc-b-run-2026-03-14-045.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp009-sc-a+cp009-sc-b, findings: 0

- run id: run-2026-03-14-046
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-010.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp010-sc-a-cp010-sc-b-run-2026-03-14-046.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp010-sc-a+cp010-sc-b, findings: 0

- run id: run-2026-03-14-047
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-011.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp011-sc-a-cp011-sc-b-run-2026-03-14-047.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp011-sc-a+cp011-sc-b, findings: 0

- run id: run-2026-03-14-048
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-012.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp012-sc-a-cp012-sc-b-run-2026-03-14-048.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp012-sc-a+cp012-sc-b, findings: 0

- run id: run-2026-03-14-049
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-003.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp003-sc-a-cp003-sc-b-run-2026-03-14-049.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp003-sc-a+cp003-sc-b, findings: 1

- run id: run-2026-03-14-050
  date: 2026-03-14
  model: phi4:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-001.json
  output file: outputs/phi4-14b-continuity-adj-cp001-sc-a-cp001-sc-b-run-2026-03-14-050.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp001-sc-a+cp001-sc-b, findings: 1

- run id: run-2026-03-14-051
  date: 2026-03-14
  model: phi4:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-002.json
  output file: outputs/phi4-14b-continuity-adj-cp002-sc-a-cp002-sc-b-run-2026-03-14-051.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp002-sc-a+cp002-sc-b, findings: 0

- run id: run-2026-03-14-052
  date: 2026-03-14
  model: phi4:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-004.json
  output file: outputs/phi4-14b-continuity-adj-cp004-sc-a-cp004-sc-b-run-2026-03-14-052.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp004-sc-a+cp004-sc-b, findings: 1

- run id: run-2026-03-14-053
  date: 2026-03-14
  model: phi4:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-005.json
  output file: outputs/phi4-14b-continuity-adj-cp005-sc-a-cp005-sc-b-run-2026-03-14-053.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp005-sc-a+cp005-sc-b, findings: 0

- run id: run-2026-03-14-054
  date: 2026-03-14
  model: phi4:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-006.json
  output file: outputs/phi4-14b-continuity-adj-cp006-sc-a-cp006-sc-b-run-2026-03-14-054.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp006-sc-a+cp006-sc-b, findings: 0

- run id: run-2026-03-14-055
  date: 2026-03-14
  model: phi4:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-007.json
  output file: outputs/phi4-14b-continuity-adj-cp007-sc-a-cp007-sc-b-run-2026-03-14-055.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp007-sc-a+cp007-sc-b, findings: 1

- run id: run-2026-03-14-056
  date: 2026-03-14
  model: phi4:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-008.json
  output file: outputs/phi4-14b-continuity-adj-cp008-sc-a-cp008-sc-b-run-2026-03-14-056.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp008-sc-a+cp008-sc-b, findings: 0

- run id: run-2026-03-14-057
  date: 2026-03-14
  model: phi4:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-009.json
  output file: outputs/phi4-14b-continuity-adj-cp009-sc-a-cp009-sc-b-run-2026-03-14-057.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp009-sc-a+cp009-sc-b, findings: 0

- run id: run-2026-03-14-058
  date: 2026-03-14
  model: phi4:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-010.json
  output file: outputs/phi4-14b-continuity-adj-cp010-sc-a-cp010-sc-b-run-2026-03-14-058.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp010-sc-a+cp010-sc-b, findings: 0

- run id: run-2026-03-14-059
  date: 2026-03-14
  model: phi4:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-011.json
  output file: outputs/phi4-14b-continuity-adj-cp011-sc-a-cp011-sc-b-run-2026-03-14-059.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp011-sc-a+cp011-sc-b, findings: 0

- run id: run-2026-03-14-060
  date: 2026-03-14
  model: phi4:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-012.json
  output file: outputs/phi4-14b-continuity-adj-cp012-sc-a-cp012-sc-b-run-2026-03-14-060.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp012-sc-a+cp012-sc-b, findings: 1

- run id: run-2026-03-14-061
  date: 2026-03-14
  model: phi4:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-003.json
  output file: outputs/phi4-14b-continuity-adj-cp003-sc-a-cp003-sc-b-run-2026-03-14-061.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp003-sc-a+cp003-sc-b, findings: 1

- run id: run-2026-03-14-062
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-004.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp004-sc-a-cp004-sc-b-run-2026-03-14-062.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp004-sc-a+cp004-sc-b, findings: 0

- run id: run-2026-03-14-063
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-005.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp005-sc-a-cp005-sc-b-run-2026-03-14-063.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp005-sc-a+cp005-sc-b, findings: 1

- run id: run-2026-03-14-064
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-006.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp006-sc-a-cp006-sc-b-run-2026-03-14-064.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp006-sc-a+cp006-sc-b, findings: 0

- run id: run-2026-03-14-065
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-007.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp007-sc-a-cp007-sc-b-run-2026-03-14-065.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp007-sc-a+cp007-sc-b, findings: 1

- run id: run-2026-03-14-066
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-008.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp008-sc-a-cp008-sc-b-run-2026-03-14-066.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp008-sc-a+cp008-sc-b, findings: 0

- run id: run-2026-03-14-067
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-009.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp009-sc-a-cp009-sc-b-run-2026-03-14-067.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp009-sc-a+cp009-sc-b, findings: 0

- run id: run-2026-03-14-068
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-010.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp010-sc-a-cp010-sc-b-run-2026-03-14-068.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp010-sc-a+cp010-sc-b, findings: 0

- run id: run-2026-03-14-069
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-011.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp011-sc-a-cp011-sc-b-run-2026-03-14-069.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp011-sc-a+cp011-sc-b, findings: 0

- run id: run-2026-03-14-070
  date: 2026-03-14
  model: qwen2.5:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-012.json
  output file: outputs/qwen2.5-14b-continuity-adj-cp012-sc-a-cp012-sc-b-run-2026-03-14-070.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp012-sc-a+cp012-sc-b, findings: 0

- run id: run-2026-03-14-071
  date: 2026-03-14
  model: phi4:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-001.json
  output file: outputs/phi4-14b-continuity-adj-cp001-sc-a-cp001-sc-b-run-2026-03-14-071.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp001-sc-a+cp001-sc-b, findings: 1

- run id: run-2026-03-14-072
  date: 2026-03-14
  model: phi4:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-002.json
  output file: outputs/phi4-14b-continuity-adj-cp002-sc-a-cp002-sc-b-run-2026-03-14-072.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp002-sc-a+cp002-sc-b, findings: 0

- run id: run-2026-03-14-073
  date: 2026-03-14
  model: phi4:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-003.json
  output file: outputs/phi4-14b-continuity-adj-cp003-sc-a-cp003-sc-b-run-2026-03-14-073.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp003-sc-a+cp003-sc-b, findings: 1

- run id: run-2026-03-14-074
  date: 2026-03-14
  model: phi4:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-004.json
  output file: outputs/phi4-14b-continuity-adj-cp004-sc-a-cp004-sc-b-run-2026-03-14-074.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp004-sc-a+cp004-sc-b, findings: 1

- run id: run-2026-03-14-075
  date: 2026-03-14
  model: phi4:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-005.json
  output file: outputs/phi4-14b-continuity-adj-cp005-sc-a-cp005-sc-b-run-2026-03-14-075.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp005-sc-a+cp005-sc-b, findings: 0

- run id: run-2026-03-14-076
  date: 2026-03-14
  model: phi4:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-006.json
  output file: outputs/phi4-14b-continuity-adj-cp006-sc-a-cp006-sc-b-run-2026-03-14-076.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp006-sc-a+cp006-sc-b, findings: 0

- run id: run-2026-03-14-077
  date: 2026-03-14
  model: phi4:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-007.json
  output file: outputs/phi4-14b-continuity-adj-cp007-sc-a-cp007-sc-b-run-2026-03-14-077.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp007-sc-a+cp007-sc-b, findings: 1

- run id: run-2026-03-14-078
  date: 2026-03-14
  model: phi4:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-008.json
  output file: outputs/phi4-14b-continuity-adj-cp008-sc-a-cp008-sc-b-run-2026-03-14-078.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp008-sc-a+cp008-sc-b, findings: 1

- run id: run-2026-03-14-079
  date: 2026-03-14
  model: phi4:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-009.json
  output file: outputs/phi4-14b-continuity-adj-cp009-sc-a-cp009-sc-b-run-2026-03-14-079.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp009-sc-a+cp009-sc-b, findings: 0

- run id: run-2026-03-14-080
  date: 2026-03-14
  model: phi4:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-010.json
  output file: outputs/phi4-14b-continuity-adj-cp010-sc-a-cp010-sc-b-run-2026-03-14-080.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp010-sc-a+cp010-sc-b, findings: 1

- run id: run-2026-03-14-081
  date: 2026-03-14
  model: phi4:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-011.json
  output file: outputs/phi4-14b-continuity-adj-cp011-sc-a-cp011-sc-b-run-2026-03-14-081.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp011-sc-a+cp011-sc-b, findings: 1

- run id: run-2026-03-14-082
  date: 2026-03-14
  model: phi4:14b
  prompt file: prompts/continuity-adjacent-scene-v3.md
  input file: inputs/case-packets/cp-012.json
  output file: outputs/phi4-14b-continuity-adj-cp012-sc-a-cp012-sc-b-run-2026-03-14-082.envelope.json
  task: analyze.continuity.adjacent_scene.v1
  notes: adjacent_scene: cp012-sc-a+cp012-sc-b, findings: 1

- run id: run-2026-03-21-001
  date: 2026-03-21
  model: qwen2.5:14b
  prompt file: prompts/style-analysis-scene-v1.md
  input file: inputs/style-analysis-eval/scene-01-clean.md
  output file: evals/style-analysis-eval-2026-03-21/raw/qwen2.5-14b-style-scene-01-clean.md-run-2026-03-21-001.envelope.json
  task: analyze.style.scene.v1
  notes: style analysis, status: failed

- run id: run-2026-03-21-002
  date: 2026-03-21
  model: qwen2.5:14b
  prompt file: prompts/style-analysis-scene-v1.md
  input file: inputs/style-analysis-eval/scene-02-dense.md
  output file: evals/style-analysis-eval-2026-03-21/raw/qwen2.5-14b-style-scene-02-dense.md-run-2026-03-21-002.envelope.json
  task: analyze.style.scene.v1
  notes: style analysis, status: failed

- run id: run-2026-03-21-003
  date: 2026-03-21
  model: qwen2.5:14b
  prompt file: prompts/style-analysis-scene-v1.md
  input file: inputs/style-analysis-eval/scene-03-flat.md
  output file: evals/style-analysis-eval-2026-03-21/raw/qwen2.5-14b-style-scene-03-flat.md-run-2026-03-21-003.envelope.json
  task: analyze.style.scene.v1
  notes: style analysis, status: failed

- run id: run-2026-03-21-004
  date: 2026-03-21
  model: qwen2.5:14b
  prompt file: prompts/style-analysis-scene-v1.md
  input file: inputs/style-analysis-eval/scene-04-voice-drift.md
  output file: evals/style-analysis-eval-2026-03-21/raw/qwen2.5-14b-style-scene-04-voice-drift.md-run-2026-03-21-004.envelope.json
  task: analyze.style.scene.v1
  notes: style analysis, status: failed

- run id: run-2026-03-21-005
  date: 2026-03-21
  model: qwen2.5:14b
  prompt file: prompts/style-analysis-scene-v1.md
  input file: inputs/style-analysis-eval/scene-05-dialogue-heavy.md
  output file: evals/style-analysis-eval-2026-03-21/raw/qwen2.5-14b-style-scene-05-dialogue-heavy.md-run-2026-03-21-005.envelope.json
  task: analyze.style.scene.v1
  notes: style analysis, status: failed
