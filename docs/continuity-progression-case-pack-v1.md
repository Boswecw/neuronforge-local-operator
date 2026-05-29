# Continuity / Progression Case Pack v1

## Status
Frozen Candidate Pack v1

## Purpose
Define the first frozen eval case pack for the `continuity-progression-reasoning` lane.

This pack is the operational input set for the first governed challenger comparison.

It is intentionally limited, bounded, and reviewable.

This artifact defines:

- the 16 target cases
- scope and category per case
- expected review posture per case
- expected restraint posture per case
- what each case is meant to pressure
- assembly notes for populating the case text packets

This document defines the pack shape and freeze boundary.

It does **not** require that every source text packet be embedded inline here.

---

## 1. Lane and pack identity

- **lane id:** `continuity-progression-reasoning`
- **pack id:** `continuity-progression-case-pack-v1`
- **pass target:** `first-local-challenger-pass-v1`
- **artifact posture:** candidate-only review input
- **route requirement:** `HIGH_QUALITY_LOCAL`
- **fallback:** fail closed

---

## 2. Freeze rule

This pack is considered frozen when:

- all 16 case packets exist
- each case has the required metadata
- each case has an assigned bounded source packet
- reviewer expectations are written before model comparison begins

Once frozen for the first challenger pass:

- do not add new cases casually
- do not rewrite case posture reactively because of model behavior
- do not shift category labels mid-pass unless a case was genuinely misclassified

If a case proves invalid, record the invalidation and replace it explicitly rather than silently mutating the pack.

---

## 3. Pack composition summary

### Total cases

- **16 cases**

### Scope mix

- **12 adjacent-scene cases**
- **4 scene-window cases**
- **0 chapter-window cases**

### Posture mix target

- true-issue pressure
- false-positive resistance pressure
- ambiguous edge pressure
- scope-discipline pressure
- evidence-discipline pressure

---

## 4. Required metadata per case

Each case packet must include at minimum:

- **case id**
- **lane id**
- **pack id**
- **scope label**
- **primary category**
- **secondary category** if applicable
- **expected review posture**
- **expected restraint posture**
- **finding expected**
- **no-finding acceptable**
- **case purpose**
- **assembly note**
- **source packet reference**
- **reviewer note**

---

## 5. Allowed values reference

### Scope labels

- `adjacent_scene`
- `scene_window`

### Expected review posture

- `candidate_issue_expected`
- `restraint_expected`
- `ambiguous_candidate_allowed`

### Expected restraint posture

- `low_restraint`
- `moderate_restraint`
- `high_restraint`

---

## 6. Case list

---

## Case 01

- **case id:** `cp-001`
- **scope label:** `adjacent_scene`
- **primary category:** `true_continuity_tension`
- **secondary category:** `state_carry_forward_issue`
- **expected review posture:** `candidate_issue_expected`
- **expected restraint posture:** `low_restraint`
- **finding expected:** yes
- **no-finding acceptable:** no
- **case purpose:** test whether the model can identify a genuine nearby carry-forward inconsistency without broadening beyond the two bounded scenes
- **assembly note:** choose two adjacent scenes where a concrete state, object condition, wound, location detail, or immediately relevant circumstance appears to shift in a review-worthy way
- **source packet reference:** `TBD`
- **reviewer note:** this should be a relatively clean true-positive anchor, not a subtle maybe-case

---

## Case 02

- **case id:** `cp-002`
- **scope label:** `adjacent_scene`
- **primary category:** `apparent_not_real_continuity_tension`
- **secondary category:** `false_positive_resistance`
- **expected review posture:** `restraint_expected`
- **expected restraint posture:** `high_restraint`
- **finding expected:** no
- **no-finding acceptable:** yes
- **case purpose:** test whether the model can resist inventing a continuity problem when a nearby detail looks suspicious at first glance but remains acceptable on close reading
- **assembly note:** choose adjacent scenes with a surface-level descriptive shift that is explainable within normal narrative compression or staging
- **source packet reference:** `TBD`
- **reviewer note:** over-flagging here is a meaningful safety failure

---

## Case 03

- **case id:** `cp-003`
- **scope label:** `adjacent_scene`
- **primary category:** `true_progression_break`
- **secondary category:** `transition_gap`
- **expected review posture:** `candidate_issue_expected`
- **expected restraint posture:** `low_restraint`
- **finding expected:** yes
- **no-finding acceptable:** no
- **case purpose:** test whether the model can flag a real nearby progression break where a state advance, action bridge, or narrative step feels missing
- **assembly note:** choose two adjacent scenes where the reader is asked to accept a meaningful change without enough bounded connective support
- **source packet reference:** `TBD`
- **reviewer note:** this should pressure causal and transition reasoning, not long-range memory

---

## Case 04

- **case id:** `cp-004`
- **scope label:** `adjacent_scene`
- **primary category:** `acceptable_abrupt_transition`
- **secondary category:** `false_positive_resistance`
- **expected review posture:** `restraint_expected`
- **expected restraint posture:** `high_restraint`
- **finding expected:** no
- **no-finding acceptable:** yes
- **case purpose:** test whether the model can distinguish sharp but acceptable pacing from a true progression defect
- **assembly note:** choose adjacent scenes with a deliberately brisk transition that still reads as stylistically valid
- **source packet reference:** `TBD`
- **reviewer note:** a good model should avoid polishing the manuscript into sameness

---

## Case 05

- **case id:** `cp-005`
- **scope label:** `adjacent_scene`
- **primary category:** `repeated_movement_worth_flagging`
- **secondary category:** `progression_redundancy`
- **expected review posture:** `candidate_issue_expected`
- **expected restraint posture:** `moderate_restraint`
- **finding expected:** yes
- **no-finding acceptable:** partial
- **case purpose:** test whether the model can identify duplicated motion or re-staging that plausibly deserves review
- **assembly note:** choose adjacent scenes where a character appears to stand, turn, cross, approach, reach, sit, or otherwise complete a movement beat twice in a way that muddies progression
- **source packet reference:** `TBD`
- **reviewer note:** a cautious candidate finding is fine; exaggerated certainty is not required

---

## Case 06

- **case id:** `cp-006`
- **scope label:** `adjacent_scene`
- **primary category:** `repeated_movement_not_worth_flagging`
- **secondary category:** `false_positive_resistance`
- **expected review posture:** `restraint_expected`
- **expected restraint posture:** `high_restraint`
- **finding expected:** no
- **no-finding acceptable:** yes
- **case purpose:** test whether the model can tolerate natural reiteration of motion or staging without turning it into review noise
- **assembly note:** choose adjacent scenes where repeated movement language exists but remains functional, natural, or below intervention threshold
- **source packet reference:** `TBD`
- **reviewer note:** this case helps detect review-hostile sensitivity

---

## Case 07

- **case id:** `cp-007`
- **scope label:** `adjacent_scene`
- **primary category:** `descriptive_mismatch_worth_review`
- **secondary category:** `continuity_tension`
- **expected review posture:** `candidate_issue_expected`
- **expected restraint posture:** `moderate_restraint`
- **finding expected:** yes
- **no-finding acceptable:** partial
- **case purpose:** test whether the model can flag a plausible descriptive mismatch without overstating certainty
- **assembly note:** choose adjacent scenes where a described environmental, physical, positional, or immediate visual detail changes in a way that may deserve review
- **source packet reference:** `TBD`
- **reviewer note:** this is candidate territory, not authority territory

---

## Case 08

- **case id:** `cp-008`
- **scope label:** `adjacent_scene`
- **primary category:** `ambiguous_edge_case`
- **secondary category:** `confidence_calibration`
- **expected review posture:** `ambiguous_candidate_allowed`
- **expected restraint posture:** `high_restraint`
- **finding expected:** partial
- **no-finding acceptable:** yes
- **case purpose:** test whether the model can stay honest in a legitimately debatable case
- **assembly note:** choose adjacent scenes where a bounded concern could be raised, but only with cautious language and clear ambiguity handling
- **source packet reference:** `TBD`
- **reviewer note:** this case is mainly about restraint and calibration rather than raw detection

---

## Case 09

- **case id:** `cp-009`
- **scope label:** `adjacent_scene`
- **primary category:** `state_carry_forward_issue`
- **secondary category:** `true_continuity_tension`
- **expected review posture:** `candidate_issue_expected`
- **expected restraint posture:** `moderate_restraint`
- **finding expected:** yes
- **no-finding acceptable:** no
- **case purpose:** test whether the model can track immediate state persistence across a small bounded handoff
- **assembly note:** choose adjacent scenes where a nearby emotional, tactical, physical, or situational state is inadequately carried forward
- **source packet reference:** `TBD`
- **reviewer note:** this should be distinct from the cleaner material-object case in cp-001

---

## Case 10

- **case id:** `cp-010`
- **scope label:** `adjacent_scene`
- **primary category:** `unclear_causal_link`
- **secondary category:** `progression_break`
- **expected review posture:** `candidate_issue_expected`
- **expected restraint posture:** `moderate_restraint`
- **finding expected:** yes
- **no-finding acceptable:** partial
- **case purpose:** test whether the model can identify when an action, reaction, or outcome lacks enough nearby causal support
- **assembly note:** choose adjacent scenes where a meaningful reaction, realization, or change happens with insufficient bounded explanation
- **source packet reference:** `TBD`
- **reviewer note:** this should remain tightly local; do not use cases that rely on broad hidden context

---

## Case 11

- **case id:** `cp-011`
- **scope label:** `adjacent_scene`
- **primary category:** `apparent_not_real_continuity_tension`
- **secondary category:** `acceptable_variation`
- **expected review posture:** `restraint_expected`
- **expected restraint posture:** `high_restraint`
- **finding expected:** no
- **no-finding acceptable:** yes
- **case purpose:** add a second false-positive resistance case so the pack does not over-reward aggressive flagging
- **assembly note:** choose adjacent scenes where wording or attention focus changes, but not in a way that creates a genuine bounded continuity problem
- **source packet reference:** `TBD`
- **reviewer note:** this should feel tempting to a weak over-eager reviewer

---

## Case 12

- **case id:** `cp-012`
- **scope label:** `adjacent_scene`
- **primary category:** `true_progression_break`
- **secondary category:** `state_transition_gap`
- **expected review posture:** `candidate_issue_expected`
- **expected restraint posture:** `low_restraint`
- **finding expected:** yes
- **no-finding acceptable:** no
- **case purpose:** provide a second strong true-positive progression case for stability and challenger differentiation
- **assembly note:** choose adjacent scenes where the reader is asked to accept a meaningful step change in scene logic or character action without enough local bridge
- **source packet reference:** `TBD`
- **reviewer note:** this should be different in flavor from cp-003 so the model cannot succeed via one narrow trick

---

## Case 13

- **case id:** `cp-013`
- **scope label:** `scene_window`
- **primary category:** `state_carry_forward_issue`
- **secondary category:** `scene_window_reasoning`
- **expected review posture:** `candidate_issue_expected`
- **expected restraint posture:** `moderate_restraint`
- **finding expected:** yes
- **no-finding acceptable:** no
- **case purpose:** test whether the model can maintain bounded reasoning across a small multi-scene window without inflating to chapter-scale claims
- **assembly note:** choose a 3-scene packet where an important nearby state should carry across the window and appears to degrade or disappear improperly
- **source packet reference:** `TBD`
- **reviewer note:** this is the first wider-memory pressure case, but still tightly bounded

---

## Case 14

- **case id:** `cp-014`
- **scope label:** `scene_window`
- **primary category:** `true_progression_break`
- **secondary category:** `scene_window_transition_gap`
- **expected review posture:** `candidate_issue_expected`
- **expected restraint posture:** `moderate_restraint`
- **finding expected:** yes
- **no-finding acceptable:** partial
- **case purpose:** test multi-scene progression reasoning where a missing bridge becomes visible only across a short window
- **assembly note:** choose a 3-scene packet where progression feels incomplete when the scenes are read together, even if each individual handoff looks superficially acceptable
- **source packet reference:** `TBD`
- **reviewer note:** this should not require external lore knowledge beyond the packet

---

## Case 15

- **case id:** `cp-015`
- **scope label:** `scene_window`
- **primary category:** `acceptable_abrupt_transition`
- **secondary category:** `false_positive_resistance`
- **expected review posture:** `restraint_expected`
- **expected restraint posture:** `high_restraint`
- **finding expected:** no
- **no-finding acceptable:** yes
- **case purpose:** test whether the model can remain calm when a compressed multi-scene handoff is brisk but still narratively acceptable
- **assembly note:** choose a short scene window with fast movement or compression that may look under-bridged to a weak reviewer but works in context
- **source packet reference:** `TBD`
- **reviewer note:** scene-window reasoning must not become automatic inflation

---

## Case 16

- **case id:** `cp-016`
- **scope label:** `scene_window`
- **primary category:** `ambiguous_edge_case`
- **secondary category:** `taxonomy_stability`
- **expected review posture:** `ambiguous_candidate_allowed`
- **expected restraint posture:** `high_restraint`
- **finding expected:** partial
- **no-finding acceptable:** yes
- **case purpose:** test whether the model can stay structurally disciplined and taxonomically stable in a short-window ambiguous case
- **assembly note:** choose a 3-scene packet that supports cautious concern but does not justify strong declarative claims
- **source packet reference:** `TBD`
- **reviewer note:** this is a drift-sensitive anchor candidate for repeatability checks

---

## 7. Recommended repeatability subset

When the first-pass runs are complete, the initial repeatability subset should preferably include:

- `cp-001` — clean true continuity anchor
- `cp-003` — clean progression-break anchor
- `cp-008` — adjacent-scene ambiguity anchor
- `cp-015` — scene-window restraint anchor
- `cp-016` — scene-window ambiguity / taxonomy-stability anchor

Optional sixth anchor:

- `cp-005` if repeated-movement behavior looks especially unstable across challengers

---

## 8. Case packet assembly instructions

For each case, create a packet file containing:

1. **case header**
   - case id
   - scope label
   - primary category
   - secondary category

2. **bounded manuscript text**
   - only the scenes or scene window required
   - no hidden extra context

3. **task framing metadata**
   - state clearly that this is candidate-only review
   - require bounded reasoning within the provided scope only

4. **operator notes block**
   - optional internal-only note about why the case exists

Do not embed expected answers in the case packet shown to the model.

---

## 9. Pack acceptance criteria

This pack is ready for first-pass challenger use when:

- all 16 case packet files exist
- each case packet is bounded and readable
- each case has a linked source packet reference
- reviewer expectations are written in advance
- the pack includes both true issues and restraint traps
- no case depends on hidden long-range context to be scored fairly

---

## 10. Pack invalidation triggers

A case should be revised or replaced if it is found to be:

- dependent on unseen long-range context
- too ambiguous to score even with the worksheet
- too trivial to differentiate challengers
- mislabeled in a way that breaks fair review
- so synthetic that it no longer resembles manuscript reality

If a case is replaced, record:

- old case id
- invalidation reason
- replacement case id
- date of replacement

---

## 11. Immediate next operational step

Populate the 16 packet files and assign concrete source passages to each `source packet reference` field.

Once that is done, freeze the pack and begin the first local challenger pass.

---

## 12. Current recommendation

Treat this case pack as the execution boundary for the lane.

Do not widen to chapter-window reasoning yet.

Get the first 16 cases assembled, frozen, and run under disciplined review before expanding the lane further.

