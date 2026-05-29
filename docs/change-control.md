# Change Control

## Purpose

Keep Neuronforge experiments comparable, reviewable, and honest.

Use controlled changes so results can be attributed to a specific cause.

---

## Core rule

Change only one meaningful variable at a time when judging output quality between runs.

---

## Quality-comparison variables

For proofreading-quality comparisons, allowed single-variable changes include:

- prompt wording
- protected terms structure
- style preferences wording
- input passage choice
- model selection

When comparing quality, do not change more than one of these at once.

---

## Operational-change rule

Script, workflow, logging, and documentation changes are allowed, but they should be treated as operational changes rather than quality-comparison changes.

After an operational change:

- verify the workflow still runs correctly
- verify outputs still save correctly
- verify logging still behaves correctly when applicable
- do not treat that run by itself as evidence of a better quality baseline

---

## Do not do

- do not change multiple quality variables at once and then judge the result
- do not swap model and prompt in the same comparison run
- do not rewrite the whole workflow after one bad output
- do not promote a new baseline from a run whose purpose was only operational verification
- do not mix workflow hardening and quality judgment without recording that distinction

---

## Reason

Single-variable changes make results comparable and keep the experiment honest.

Operational hardening is still important, but it answers a different question than output-quality testing.

---

## Practice

For each meaningful run, note:

- what changed
- why it changed
- whether the run was for quality comparison or operational verification

If a run changed more than one meaningful quality variable, do not use it as clean baseline-selection evidence.
