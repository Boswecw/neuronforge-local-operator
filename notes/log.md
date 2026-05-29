# Working Log

## Entry Template

### Date
YYYY-MM-DD

### Context
What you were testing

### Action
What you ran or changed

### Result
What happened

### Notes
What matters next
---

### Date
2026-03-13

### Context
Initial sanity test of deepseek-r1:7b in Ollama for proofreading behavior.

### Action
Ran:
ollama run deepseek-r1:7b

Prompt used:
Correct the grammar in this sentence: He go to the road and dont look back.

### Result
Model exposed reasoning, did not follow the instruction to return only corrected text, and produced an incorrect correction:
"He goes to the road and don't look back."

### Notes
This model may not be suitable as a strict proofreading model in default interactive mode. Need to test controlled prompt-file workflow and possibly use a non-reasoning model for proofreading tasks.
