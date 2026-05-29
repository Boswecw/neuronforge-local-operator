# Continuity / Progression Review Rubric

Date: 2026-03-14

## Purpose

Define the review instrument for evaluating candidate outputs produced by the `continuity-progression-reasoning` lane.

This rubric exists to judge whether a model and prompt combination is good enough for governed review use in NeuronForge Local.

It does **not** decide canonical story truth.

It decides whether candidate findings are:

- useful
- evidence-grounded
- restrained
- structurally reliable
- scope-honest
- review-friendly
- confidence-calibrated

---

## Rubric posture

This is a **review-grade** rubric.

It is meant for comparing candidate sets produced by:

- different local models
- different prompts
- different route settings within allowed lane policy
- repeated runs for drift observation

This rubric should be used before any increase in lane trust.

---

## Lane under review

- **lane id:** `continuity-progression-reasoning`
- **family:** `analysis`
- **strictness:** `STRICT_STRUCTURED`
- **primary route class:** `HIGH_QUALITY_LOCAL`
- **artifact posture:** candidate-only

---

## Review unit

The review unit is one **candidate set** produced for a defined analysis scope.

Examples:

- one scene-local progression pass
- one adjacent-scene comparison
- one scene-window review

A candidate set may contain zero findings, one finding, or multiple findings.

A zero-finding result may still score well if restraint is correct and the scene set does not warrant findings.

---

## Reviewer instructions

Review the output as a governed operator, not as a co-author trying to rescue the system.

Judge what the model actually produced.

Do not award credit for what the model might have meant.

If the output is vague, inflated, unsupported, or malformed, score that directly.

Prefer disciplined restraint over flashy overreach.

A small number of solid findings is better than a large number of weak ones.

---

## Scoring scale

Each scored dimension uses the following 0–4 scale.

### 4 — Strong

Clear, reliable, review-usable, and governance-aligned.

### 3 — Acceptable

Mostly good, with minor weakness that does not undermine review use.

### 2 — Mixed

Partly useful but materially weakened by inconsistency, vagueness, or overreach.

### 1 — Weak

Limited review value. Problems are substantial.

### 0 — Failed

Not acceptable for governed review use on that dimension.

---

## Core scoring dimensions

### 1. Usefulness

**Question:** Does this candidate set help a reviewer notice something genuinely worth checking?

#### Score guidance

**4**
- Findings are meaningfully helpful
- Reviewer attention is directed to concrete and plausible issues
- No obvious filler findings

**3**
- Mostly helpful
- One or two findings may be weaker, but overall value is real

**2**
- Some useful signal, but diluted by weak, repetitive, or marginal findings

**1**
- Minimal practical value
- Most findings feel generic or unhelpful

**0**
- No meaningful review help provided

---

### 2. Evidence quality

**Question:** Do the cited spans actually support the candidate claims?

#### Score guidance

**4**
- Evidence spans are specific, relevant, and sufficient
- Claims are visibly grounded in the provided text

**3**
- Evidence is mostly good
- Minor gaps exist but claims remain reviewable

**2**
- Evidence partially supports claims, but some findings feel under-backed

**1**
- Evidence is weak, vague, or poorly aligned to the claim

**0**
- Material claims lack usable evidence support

---

### 3. Scope honesty

**Question:** Does the output stay inside the declared analysis window?

#### Score guidance

**4**
- Every finding stays clearly within declared scope
- No cross-scope leakage

**3**
- Mostly scope-disciplined
- Minor phrasing drift but no major overreach

**2**
- Some claims stretch beyond the visible scene set or implied scope

**1**
- Repeated scope confusion or claims unsupported by visible bounds

**0**
- Scope is omitted, violated, or meaningless

---

### 4. Restraint

**Question:** Does the model avoid over-diagnosing, over-claiming, and flattening ambiguity into certainty?

#### Score guidance

**4**
- Strong discipline
- Findings are carefully framed as possible review targets
- Output respects ambiguity

**3**
- Mostly restrained
- Mild inflation present but manageable

**2**
- Noticeable tendency to over-call issues or overstate them

**1**
- Significant overreach or weak issue inflation

**0**
- Output is dominated by unjustified certainty or inflated diagnosis

---

### 5. Label quality

**Question:** Are the labels and finding types clear, stable, and semantically useful?

#### Score guidance

**4**
- Labels are crisp, understandable, and consistent
- Finding types are easy to interpret in review

**3**
- Mostly clear labels with minor inconsistency

**2**
- Labels are understandable but muddy, repetitive, or unstable

**1**
- Labels add confusion or are too generic to help review

**0**
- Labels are missing, malformed, or semantically unusable

---

### 6. Review usability

**Question:** Can a human reviewer act on this output quickly and confidently?

#### Score guidance

**4**
- Fast to scan
- Easy to understand what to inspect and why
- Review notes are actionable

**3**
- Generally usable with minor friction

**2**
- Usable but slowed by verbosity, vagueness, or weak review notes

**1**
- Hard to use efficiently in a real review workflow

**0**
- Not practically reviewable

---

### 7. Confidence calibration

**Question:** Does stated confidence match the actual support strength?

#### Score guidance

**4**
- Confidence tracks evidence well
- Uncertainty is acknowledged where needed

**3**
- Mostly calibrated
- Minor over- or under-confidence only

**2**
- Confidence is uneven or somewhat inflated

**1**
- Confidence often misstates support strength

**0**
- Confidence is materially misleading or absent where required

---

### 8. Schema reliability

**Question:** Is the structured output valid, complete, and internally consistent?

#### Score guidance

**4**
- Schema is clean and complete
- Required fields are present and coherent

**3**
- Minor structural issues that do not block review

**2**
- Noticeable inconsistencies or omissions, but output remains partly usable

**1**
- Structure is fragile or materially incomplete

**0**
- Malformed structured output

---

### 9. Canonicality control

**Question:** Does the output maintain candidate posture rather than presenting findings as established truth?

#### Score guidance

**4**
- Output consistently signals candidate posture
- No truth-language leakage

**3**
- Mostly controlled with minor phrasing slips

**2**
- Some statements read too definitively for a candidate lane

**1**
- Repeated authority leakage in wording or framing

**0**
- Output materially presents candidate findings as truth

---

### 10. Drift resistance

**Question:** Across repeated runs, does the output remain semantically stable enough for governed review use?

#### Score guidance

**4**
- Repeated runs are meaningfully stable in findings, tone, and structure

**3**
- Some variation, but review conclusions would stay mostly the same

**2**
- Variation is noticeable enough to reduce operator trust

**1**
- Drift is substantial and undermines comparison reliability

**0**
- Output is too unstable for governed evaluation use

---

## Hard-fail conditions

A candidate set should be marked **hard fail** if any of the following occur:

- unsupported claim framed as fact
- material claim without evidence span
- scope omitted or materially violated
- malformed structured output
- invented event presented as story truth
- invented causal bridge presented as established fact
- project-wide claim made from bounded local context
- confidence materially higher than evidence supports
- candidate posture replaced by authority posture
- review notes too vague to support operator action

A hard fail should override a high aggregate score.

---

## Optional secondary observations

These do not replace the main score but may be recorded as notes:

- under-extraction
- over-extraction
- redundancy inflation
- bridge-gap inflation
- descriptive mismatch sensitivity
- ambiguity handling quality
- reviewer cognitive load
- repeated wording artifacts
- taxonomy drift across runs

---

## Recommended scoring summary

For each candidate set, record:

- model
- prompt id
- route class
- input scope id
- per-dimension scores
- hard fail yes/no
- short operator judgment
- keep / reject / compare further

---

## Suggested score interpretation

### Strong review-grade candidate set

Typical shape:

- no hard fail
- mostly 3s and 4s
- evidence quality, scope honesty, restraint, and schema reliability all strong

### Borderline candidate set

Typical shape:

- no hard fail
- several 2s
- useful in places, but not strong enough for lane trust advancement

### Reject candidate set

Typical shape:

- hard fail present
- or multiple 0/1 scores in evidence, scope, schema, restraint, or canonicality control

---

## Comparison guidance

When comparing two candidate sets, prefer the one that is:

1. more evidence-grounded
2. more scope-honest
3. more restrained
4. more structurally reliable
5. easier to review

Do not prefer a model just because it produces more findings.

More findings only help if they remain well-supported and review-worthy.

---

## Zero-finding guidance

A zero-finding output is not automatically weak.

It may score well when:

- the analysis scope genuinely contains no strong review-worthy issue
- the model clearly preserves structure and candidate posture
- restraint is appropriate
- the result is auditably empty rather than evasive

A zero-finding output should score poorly when:

- obvious issues were missed
- evidence handling is absent
- the system avoids findings by being vague or under-responsive

---

## Reviewer judgment labels

Use one of these overall labels after scoring:

- `strong_accept_for_further_lane_testing`
- `usable_but_not_yet_trustworthy`
- `borderline_compare_against_challenger`
- `reject_for_current_lane_purpose`
- `hard_fail`

---

## Initial adoption bar

For early lane advancement, the minimum practical bar should likely be:

- no hard fail
- evidence quality >= 3
- scope honesty >= 3
- restraint >= 3
- schema reliability >= 3
- canonicality control >= 3

This should be treated as a starting bar, not final policy.

---

## Current judgment

This rubric is the first review-grade scoring instrument for the `continuity-progression-reasoning` lane.

It is strict by design because this lane is reasoning-sensitive, review-facing, and vulnerable to polished but unsafe inference.

The rubric deliberately rewards:

- bounded reasoning
- evidence discipline
- reviewer usefulness
- structural reliability
- candidate-not-authority behavior

And it deliberately penalizes:

- overreach
- invented continuity claims
- weak evidence
- authority leakage
- schema failure

---

## Restart note

If resuming later, this rubric is ready to be used with:

- a continuity/progression candidate schema
- a bounded eval set
- challenger model comparisons for `HIGH_QUALITY_LOCAL`

Most natural next artifact:

**Continuity / Progression Candidate Schema**

