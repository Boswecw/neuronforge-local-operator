# Experiment-Memory Canonical Record Fixtures (G-04)

These are the pilot's canonical experiment records, converted from the real
markdown registries and reviews (`registry/runs.md`, `evals/run-*.md`,
`docs/current-baseline.md`, `docs/operational-workflow.md`). Each record names
its source in `converted_from`. Artifact hashes are real SHA256 digests of the
committed prompt/input/output files and are verified by the integrity checker.

Honesty notes:

- `registry/runs.md` records dates, not times. Times of day on 2026-03-13 are
  ordering placeholders only (run < review < decision), following the plan's
  own example anchor (19:00Z for the run-005 baseline decision). The dates and
  all substantive facts are real.
- `run-fixture-oom-001`, `failure-fixture-oom-001`, and
  `hw-fixture-constrained-001` are explicitly fixture-namespaced: they
  reconstruct the **documented** Ollama memory-failure boundary from
  `docs/operational-workflow.md` (error string verbatim). The source doc does
  not record which model or run hit the boundary, so these ids cannot collide
  with real registry runs.
- Failure observations map reviewer language onto `failure-taxonomy-v1`
  classes; each `reviewer_note` quotes or closely paraphrases the source
  review so the mapping is auditable.

Paths:

- `records/` — the canonical record set (the pilot's record source; Git is the
  authority per the authority matrix until DataForge Local exists).
- `invalid/` — deliberately broken records for contract tests. Never loaded as
  canonical data.
- `golden/` — frozen expected `OperatorQueryEvidence.v1` objects for the five
  operator queries (plan 08).
