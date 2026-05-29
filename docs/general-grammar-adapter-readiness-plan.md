# General Grammar Adapter Readiness Plan

Date: 2026-03-14

## Purpose

Define the readiness path for a first adapter experiment for the `general-grammar-cleanup` lane.

This is not an approval to train yet.

This document exists to answer:

- whether prompt-only control has plateaued for this lane
- whether a QLoRA experiment is justified
- what evidence must exist before training begins
- how adapter adoption should be governed if training later succeeds

---

## Lane

- lane id: `general-grammar-cleanup`
- current baseline model: `qwen2.5:14b`
- current baseline prompt: `prompts/general-grammar-cleanup-001.md`
- current lane status doc: `evals/general-grammar-lane-status-2026-03-13.md`
- current calibration doc: `evals/general-grammar-calibration-2026-03-13.md`

---

## Current judgment

This lane is a plausible first adapter candidate.

Why:

- the lane has a stable purpose
- the lane is broader and less brittle than lore-safe proofreading
- the lane is easier to encode as before/after supervision pairs
- the lane is specifically about controlled cleanup behavior rather than unrestricted rewriting

This lane is not yet approved for training.

Current evidence supports adapter planning, not adapter execution.

---

## Why this lane is the best first candidate

Compared with `lore-safe proofreading`, this lane is safer for first adapter work.

Reasons:

- broader cleanup behavior is easier to teach than highly restrained lore-safe behavior
- training mistakes are less likely to corrupt protected-term handling
- dataset examples are easier to author and review consistently
- success criteria are easier to define and measure

`lore-safe proofreading` remains a higher-risk lane for first training because it is easier to damage restraint, tone preservation, and protected-language behavior with imperfect examples.

---

## Adapter strategy direction

If training becomes justified, preferred direction is:

- base model retained separately
- adapter trained per lane
- no merged model as the primary operational artifact
- adapter adoption evaluated per lane, not globally

This preserves a clean operational shape:

- base model
- lane prompt
- lane adapter
- evaluation set
- adoption decision
- rollback path

---

## Readiness gates

Training is only justified when all gates below are satisfied.

### Gate 1 - Stable lane doctrine

The lane must remain stable enough that examples are teaching one coherent behavior.

Required:

- lane purpose is documented
- inclusion behavior is clear
- exclusion behavior is clear
- operator can explain what counts as cleanup vs rewrite

Current status:

- mostly satisfied

### Gate 2 - Prompt plateau evidence

We must show that prompt refinement alone is no longer solving the important residual failures well enough.

Required:

- at least one additional prompt revision tested against the lane
- explicit notes on what failures remain after prompt revision
- repeated failure categories across multiple samples

Current status:

- not yet satisfied

### Gate 3 - Gold dataset readiness

We must have curated before/after examples that teach the intended lane behavior.

Required:

- minimum starter target: 50 curated pairs
- preferred first serious target: 100 to 150 curated pairs
- each pair reviewed for meaning preservation
- each pair reviewed for overreach risk
- no pairs that teach interpretive normalization as desired behavior

Current status:

- not yet satisfied

### Gate 4 - Held-out evaluation set

Training data and evaluation data must be separated.

Required:

- held-out eval set not used in training
- lane-specific review criteria defined before training
- side-by-side comparison against prompt-only baseline

Current status:

- not yet satisfied

### Gate 5 - Governance readiness

We must be able to track adapter lineage and adoption cleanly.

Required:

- adapter naming convention
- dataset version record
- training config record
- adoption decision template
- rollback rule

Current status:

- not yet satisfied

---

## Dataset plan

### Dataset purpose

Teach controlled grammar cleanup behavior that improves:

- grammar
- punctuation
- readability
- sentence clarity
- light awkwardness

while preserving:

- intended meaning
- important nuance
- voice where possible
- scene logic

and avoiding:

- semantic recasting
- interpretive normalization
- flattening for convenience
- deletion of meaningful ambiguity
- insertion of facts not present in source

### Example source classes

Collect examples from several buckets:

- obvious grammar error cleanup
- punctuation cleanup
- clarity improvement without semantic recast
- awkward sentence smoothing
- paragraph flow cleanup
- dialogue punctuation and mechanics
- minor repetition cleanup where meaning remains intact

### Exclusion classes

Do not include training pairs whose edits primarily reflect:

- stylistic rewriting
- tone homogenization
- lore interpretation
- plot clarification not justified by the source
- omission of purposeful ambiguity
- forced simplification that changes the feel of the prose

### Dataset review fields

Each candidate pair should be reviewed with these fields:

- pair id
- source text
- edited text
- category
- meaning preserved: yes/no
- overreach risk: low/medium/high
- notes
- approved for training: yes/no

---

## Failure taxonomy to collect before training

Before any adapter work, collect recurring prompt-only failures for this lane.

Track at least these categories:

- under-correction
- over-correction
- interpretive normalization
- semantic recasting
- voice flattening
- nuance deletion
- punctuation miss
- readability improvement success
- readability improvement with overreach

This taxonomy should be used during both dataset creation and later evaluation.

---

## Experimental sequence

### Phase 1 - Prompt plateau check

Goal:

verify whether prompt-only control is actually plateauing

Required work:

- create at least one challenger prompt revision for this lane
- test against the current five-input set
- add 10 to 20 additional lane samples if needed
- record the residual failure patterns

Exit condition:

- repeated residual failures remain that a better prompt does not resolve well enough

### Phase 2 - Gold dataset assembly

Goal:

build the first approved supervised dataset for this lane

Required work:

- assemble 50 curated before/after pairs
- review every pair manually
- reject anything that teaches rewrite drift
- split training and held-out evaluation sets

Exit condition:

- dataset is coherent enough that two independent review passes would likely agree on intent

### Phase 3 - QLoRA pilot

Goal:

run one small adapter experiment only after the earlier gates are met

Pilot posture:

- one base model only
- one lane only
- one adapter only
- no merged artifact as the baseline deployment shape

Exit condition:

- adapter clearly outperforms prompt-only baseline on held-out eval without introducing unacceptable drift

### Phase 4 - Adoption decision

Goal:

determine whether the adapter becomes an accepted lane artifact

Required comparison:

- prompt-only current baseline
- prompt-only best challenger
- qlora adapter candidate

Adoption only if:

- the adapter delivers a clear quality gain
- meaning preservation remains strong
- rewrite drift does not materially increase
- governance records are complete

---

## Evaluation criteria for adapter adoption

An adapter candidate should be judged on:

- grammar correctness
- punctuation correctness
- readability improvement
- meaning preservation
- nuance preservation
- rewrite restraint
- consistency across samples

Immediate rejection conditions:

- repeated semantic recasting
- new factual insertions
- flattening of prose beyond lane intent
- unstable behavior across similar samples
- inability to outperform prompt-only baseline in meaningful ways

---

## Proposed artifact set if training begins later

Recommended future artifact shape:

- `datasets/general-grammar-adapter-train-v001.*`
- `datasets/general-grammar-adapter-eval-v001.*`
- `docs/general-grammar-adapter-readiness-plan.md`
- `docs/general-grammar-adapter-training-spec-v001.md`
- `evals/general-grammar-adapter-pilot-001.md`
- `registry/adapters.md`

---

## Suggested registry fields for future adapter tracking

When adapter work starts, record at minimum:

- adapter id
- lane id
- base model
- adapter method
- dataset version
- training config version
- train date
- eval doc
- adoption status
- rollback target
- notes

---

## Current decision

As of 2026-03-14:

- `general-grammar-cleanup` is the first plausible adapter candidate lane
- adapter planning is justified
- QLoRA training is not yet approved
- next work should prove prompt plateau and build the first gold dataset

---

## Next logical steps

1. create a prompt challenger for `general-grammar-cleanup`
2. define the lane failure taxonomy in a dedicated review doc
3. begin collecting curated before/after pairs
4. draft a small dataset review template
5. only then decide whether a pilot QLoRA run is justified
