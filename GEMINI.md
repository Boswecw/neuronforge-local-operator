# GEMINI.md
Date: 2026-04-17
Time: 03:14 AM America/New_York

## Repo Identity
neuronforge is part of the BDS / Forge ecosystem.
Treat it as a governed intelligence / inference / connectivity system, not as a toy AI repo.
Do not frame this repo as an MVP.

## Primary Working Rules
- Prefer bounded, explicit changes.
- Prefer minimal edits over broad refactors.
- Do not invent commands, routes, task formats, receipts, or runtime seams.
- Preserve provenance, contract integrity, and bounded behavior.
- Keep responses copy/paste friendly.
- If a command or seam is uncertain, inspect the repo first.

## Output Contract
- Show the exact file path first when changing files.
- Prefer full-file replacement output when practical.
- Provide exact commands only.
- Do not provide pseudo-commands.
- State root cause before or with the fix when debugging.
- If verification was not run, say so explicitly.

## Repo Shape
At minimum, expect these major concerns:
- prompts
- inputs
- run scripts
- model/runtime invocation
- logging / receipts / outputs
- connectivity or intake seams to adjacent systems

Do not assume a successful model run proves contract correctness.
Do not assume a prompt change is harmless.

## Commands to Prefer
When relevant, inspect available scripts and repo docs first.
Known useful commands:

### Dry-run proofread path
- `bash scripts/run-and-log-proofread.sh --dry-run qwen2.5:14b prompts/lore-safe-proofread-003.md inputs/lore-safe-test-001.md "lore-safe-proofread" "vscode-manual-connectivity-check"`

### Live proofread path
- `bash scripts/run-and-log-proofread.sh qwen2.5:14b prompts/lore-safe-proofread-003.md inputs/lore-safe-test-001.md "lore-safe-proofread" "vscode-manual-connectivity-check"`

Use the narrowest relevant verification first.

## Verification Rules
Before calling a task done:
1. Prefer dry-run validation first when available.
2. If changing connectivity, receipts, or contract carriage, verify the relevant seam explicitly.
3. If changing prompt/run behavior, distinguish prompt success from contract success.
4. Report exactly what command was run and what passed or failed.
5. Do not claim end-to-end success without evidence.

## Architecture Boundaries
Preserve boundaries between:
- prompt content
- task/intake semantics
- model/runtime invocation
- logging / receipt / evidence surfaces
- adjacent system connectivity

Do not casually blur those layers.

## Connectivity and Provenance Rules
When working on connectivity seams, preserve lineage and provenance fields.
Important fields to preserve when relevant:
- `task_intent_id`
- `context_bundle_id`
- `context_bundle_hash`

Do not casually rename, drop, or synthesize these fields.
Do not treat missing provenance as acceptable unless the task explicitly changes the contract.

## Prompt and Lane Rules
When touching prompts or lane behavior:
- preserve lane intent
- preserve evaluation meaning
- do not weaken guardrails casually
- do not change prompt semantics without calling out the effect on outputs and verification
- distinguish content changes from runtime or seam changes

## Logging / Receipt Rules
If the repo produces logs, receipts, or artifacts:
- treat them as evidence surfaces
- preserve field stability unless the task explicitly changes schema
- do not remove high-value provenance just to simplify output
- verify whether downstream consumers rely on the current artifact shape

## Model / Runtime Rules
- Do not assume model changes are interchangeable.
- Do not silently change model identifiers, invocation shape, or runtime assumptions.
- If a task involves a different model or runtime path, call it out explicitly.
- Preserve bounded behavior around inference and task handling.

## Cross-System Rules
When neuronforge is connected to another system:
- identify ownership on both sides
- verify contract fields explicitly
- separate transport issues from task semantics issues
- separate runtime/model issues from connectivity issues
- do not claim the seam is correct because one side appears green

## Documentation Rules
When creating or updating docs in this repo:
- keep docs aligned to implementation
- do not write aspirational behavior as if it is already live
- include date and time
- use direct, operational language

## Context Priorities
When reasoning about neuronforge, inspect in this order when relevant:
1. target file(s)
2. scripts involved in the current path
3. prompts and inputs used by the current task
4. log / receipt / artifact structures
5. connectivity or intake code
6. repo docs or system docs

## Do Not
- do not invent a seam command
- do not assume dry-run proves live behavior
- do not assume live model output proves contract correctness
- do not weaken provenance
- do not broaden scope silently

## Preferred Default Work Pattern
1. Identify whether the task is prompt, runtime, receipt, or connectivity related.
2. Identify the exact files and scripts.
3. State the narrow verification target.
4. Make the bounded change.
5. Run or recommend the narrow verification.
6. Report exact results and next step.