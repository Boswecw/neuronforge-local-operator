# Neuronforge Operational Workflow

## Purpose

This document defines the operator workflow for running proofreading experiments in a controlled, repeatable, manual-first way.

The workflow is designed to support:

- one change at a time
- explicit verification after each run
- clean run logging
- repeatable command usage
- low-friction preflight checks before execution

---

## Manual-first execution rule

Neuronforge runs are executed manually by the operator.

This workflow is intentionally manual-first.

That means:

- the operator chooses the model
- the operator chooses the prompt file
- the operator chooses the input file
- the operator reviews output artifacts directly
- the operator verifies run logging directly
- failures are inspected before another run is attempted

Do not treat this workflow as unattended automation.

---

## Core scripts

### `scripts/run-proofread.sh`

Runs a proofreading job from:

- model
- prompt file
- input file
- output file

It writes the model output to the requested output path.

Execution behavior:

- reads the full prompt file first
- inserts a literal `PASSAGE:` separator
- appends the full input file after that separator
- sends the combined payload to `ollama run`

Effective input structure:

    <prompt file contents>

    PASSAGE:

    <input file contents>

This separator is part of the current proofreading contract and should be treated as intentional unless the runner design is changed.

Current hardening includes:

- checks that `ollama` exists on `PATH`
- captures stderr from `ollama run`
- prints a cleaner operator-facing failure message
- detects insufficient memory errors more clearly
- removes partial output files on failure
- exits nonzero on failure

Because it exits nonzero on failure, wrapper-driven logging does not occur for failed runs.

### `scripts/log-run.sh`

Appends a formatted run record to:

- `registry/runs.md`

### `scripts/next-run-id.sh`

Scans `registry/runs.md` for the current date and prints the next available run id in this format:

- `run-YYYY-MM-DD-NNN`

### `scripts/run-and-log-proofread.sh`

Primary operator wrapper.

This script can:

- run proofreading
- write output
- log the run
- auto-fill missing metadata depending on argument form
- perform dry-run validation without executing the model

Additional wrapper behavior:

- resolves and runs from the repository root automatically
- requires these helper scripts to exist and be executable:
  - `scripts/run-proofread.sh`
  - `scripts/log-run.sh`
  - `scripts/next-run-id.sh`

Dry-run behavior:

- does not execute proofreading
- does not write a log entry
- prints the fully resolved run metadata for operator review

Dry-run output fields:

- `run id`
- `date`
- `model`
- `prompt file`
- `input file`
- `output file`
- `task`
- `notes`

---

## Wrapper argument forms

The wrapper currently supports the following forms.

### 5 arguments

Auto-generates:

- `RUN_ID`
- `DATE`
- `OUTPUT_FILE`

Form:

    scripts/run-and-log-proofread.sh \
      MODEL \
      PROMPT_FILE \
      INPUT_FILE \
      TASK \
      NOTES

### 6 arguments

Auto-generates:

- `RUN_ID`
- `DATE`

Form:

    scripts/run-and-log-proofread.sh \
      MODEL \
      PROMPT_FILE \
      INPUT_FILE \
      OUTPUT_FILE \
      TASK \
      NOTES

### 7 arguments

Auto-generates:

- `DATE`

Form:

    scripts/run-and-log-proofread.sh \
      RUN_ID \
      MODEL \
      PROMPT_FILE \
      INPUT_FILE \
      OUTPUT_FILE \
      TASK \
      NOTES

### 8 arguments

Uses all provided values exactly as passed.

Form:

    scripts/run-and-log-proofread.sh \
      RUN_ID \
      DATE \
      MODEL \
      PROMPT_FILE \
      INPUT_FILE \
      OUTPUT_FILE \
      TASK \
      NOTES

---

## Dry-run preflight procedure

Use dry-run mode before a live run when testing argument shape, output naming, or logging metadata.

Verified example:

    scripts/run-and-log-proofread.sh --dry-run \
      qwen2.5:14b \
      prompts/lore-safe-proofread-003.md \
      inputs/lore-safe-test-001.md \
      proofread \
      "dry run verification"

This verified behavior should confirm the resolved values for:

- `RUN_ID`
- `DATE`
- `OUTPUT_FILE`

Dry run should be used to confirm that the wrapper is constructing the run correctly before spending model runtime.

---

## Live-run procedure

After dry-run verification, execute the live run.

Example pattern:

    scripts/run-and-log-proofread.sh \
      qwen2.5:14b \
      prompts/lore-safe-proofread-003.md \
      inputs/lore-safe-test-001.md \
      proofread \
      "live run verification"

Expected live-run behavior:

1. resolve run metadata
2. call the proofread runner
3. write the output file
4. append a run record to `registry/runs.md`

---

## Standard verification after runs

After a successful live run, verify both output creation and logging.

    wc -l outputs/<output-file>.md
    tail -n 20 registry/runs.md

Confirm:

- the output file exists
- the output file is non-empty
- the expected run id appears in `registry/runs.md`
- the logged metadata matches the executed run

---

## Expected registry record shape

Successful runs logged in `registry/runs.md` should include these fields:

- `run id`
- `date`
- `model`
- `prompt file`
- `input file`
- `output file`
- `task`
- `notes`

Example shape:

    - run id: run-YYYY-MM-DD-NNN
      date: YYYY-MM-DD
      model: <model-name>
      prompt file: prompts/<prompt-file>.md
      input file: inputs/<input-file>.md
      output file: outputs/<output-file>.md
      task: <task-name>
      notes: <operator-notes>

This record format is the expected verification target after successful wrapper-driven runs.

The log writer currently appends a blank line before each new run record, so entries are visually separated in `registry/runs.md`.

---

## Output filename behavior

Output filenames may come from either of two paths.

### Auto-generated output filename

When the wrapper is used in the 5-argument form, it auto-generates `OUTPUT_FILE`.

Verified pattern:

    outputs/<sanitized-model>-<input-stem>-<run-id>.md

Example:

    outputs/qwen2.5-14b-lore-safe-test-001-run-2026-03-13-015.md

Where `<sanitized-model>` is produced by replacing `:` and `/` in the model name with `-`.

### Manually supplied output filename

When the wrapper is used in a form that explicitly provides `OUTPUT_FILE`, the operator-supplied filename is used as-is.

Examples:

    outputs/qwen2.5-14b-lore-safe-006.md
    outputs/qwen2.5-14b-lore-safe-007.md

This means output naming in the repository may include both:

- wrapper-generated filenames
- manually assigned filenames

Both are valid if the run record correctly reflects the file actually written.

---
## Verified operator chain

The following operator path has already been verified end to end:

1. dry run via `scripts/run-and-log-proofread.sh --dry-run`
2. live run via `scripts/run-and-log-proofread.sh`
3. output file creation
4. run logging into `registry/runs.md`
5. run-id generation through `scripts/next-run-id.sh`

Verified successful live runs included:

- `run-2026-03-13-014`
- `run-2026-03-13-015`

Verified output files included:

- `outputs/qwen2.5-14b-lore-safe-test-001-run-2026-03-13-014.md`
- `outputs/qwen2.5-14b-lore-safe-test-001-run-2026-03-13-015.md`

Both outputs were verified with `wc -l`, and both log entries were confirmed in `registry/runs.md`.

---

## Observed failure boundary

A real runtime failure was observed during a live run due to Ollama memory availability.

Observed error:

    Error: 500 Internal Server Error: model requires more system memory (3.3 GiB) than is available (2.5 GiB)

This is treated as a runtime resource failure, not a wrapper logic bug.

Operational meaning:

- the wrapper may be valid
- the runner may be valid
- the model may still fail if system memory is insufficient at runtime

Because `scripts/run-proofread.sh` exits nonzero and removes partial outputs on failure, failed runs should not be logged as successful runs.

---

## Failure handling rule

If a run fails:

1. do not log it manually as a successful run
2. inspect the operator-facing error message
3. confirm no partial output file remains
4. correct the runtime condition or reduce model pressure
5. rerun only after the failure cause is understood

---

## Recommended operator rhythm

Use this sequence for repeatable manual execution:

1. confirm repo root
2. verify prompt and input paths
3. run dry-run preflight
4. review resolved metadata
5. execute live run
6. verify output file with `wc -l`
7. verify log entry in `registry/runs.md`
8. inspect output quality before changing anything else

This keeps the workflow controlled, auditable, and easy to debu