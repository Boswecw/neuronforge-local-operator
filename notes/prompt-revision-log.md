# Prompt Revision Log

## Entry Template

### Date
YYYY-MM-DD

### Prompt File
prompts/example.md

### Revision ID
rev-001

### What Changed
Describe the exact wording change

### Why
Describe the reason for the change

### Expected Effect
Describe what you expect to improve

### Related Run
run-YYYY-MM-DD-###
---

### Date
2026-03-13

### Prompt File
prompts/lore-safe-proofread-002.md

### Revision ID
rev-001

### What Changed
Rewrote the prompt into a shorter and stricter format. Added an explicit do-not list and a fallback instruction to return the original passage unchanged if the model cannot comply.

### Why
The prior prompt still allowed deepseek-r1:7b to leak reasoning, add commentary, and rewrite beyond proofreading scope.

### Expected Effect
Improve instruction compliance, reduce reasoning leakage, reduce commentary, and reduce overediting.

### Related Run
run-2026-03-13-002
---

### Date
2026-03-13

### Prompt File
prompts/lore-safe-proofread-003.md

### Revision ID
rev-002

### What Changed
Added stronger minimal-edit instructions: preserve wording and sentence structure whenever possible, do not replace correct phrases with different phrases, keep unusual but valid phrasing, and make the fewest possible changes.

### Why
Run 004 was compliant and usable, but it still made non-minimal editorial substitutions.

### Expected Effect
Reduce unnecessary rewrites while keeping grammar correction quality and clean output compliance.

### Related Run
run-2026-03-13-004

### Date
2026-03-13

### Prompt File
prompts/lore-safe-proofread-004.md

### Revision ID
rev-003

### What Changed
Forked the accepted baseline prompt into a new challenger prompt and added explicit preservation of tense and aspect. Added explicit instructions not to normalize tense or aspect when the original is already acceptable, and not to replace unusual but valid literary phrasing with more common phrasing.

### Why
Several challenger outputs and the current accepted baseline still showed optional editorial substitutions around tense, aspect, and literary phrasing. This revision is intended to pressure the model further toward minimal-edit behavior without changing the accepted baseline prompt.

### Expected Effect
Reduce optional phrasing drift such as tense/aspect normalization and preserve unusual but valid literary constructions more consistently.

### Related Run
run-2026-03-13-005
