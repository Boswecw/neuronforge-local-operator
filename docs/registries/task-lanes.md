# Task Lane Registry

**Status:** source registry baseline.
**Scope:** local-system proving repo.

## Lifecycle States

| State | Meaning |
| --- | --- |
| `proposed` | Doctrine or planning exists; no admitted runtime route. |
| `experimental` | Source route or runner exists, but baseline promotion is not final. |
| `baseline` | Manually validated baseline and regression evidence exist. |
| `deprecated` | Retained for history; not routed for new work. |

## Lanes

| Lane | Runtime posture | State | Source proof |
| --- | --- | --- | --- |
| `proofread` | local model experiment | `baseline` for lore-safe proofreading records | `registry/models.md`, `registry/prompts.md`, `registry/runs.md`, `docs/manual-validator.md` |
| `style_analysis` | local style-analysis route | `candidate_baseline` | `scripts/style_analysis`, `tests/test-style-analysis.py`, `doc/system/_index.md` |
| `drift_analysis` | deterministic local service route | `experimental` | `service/drift_analysis.py`, `service/main.py` |
| `cortex_gnat_semantic_handoff` | local candidate handoff receipt | `experimental` | `service/cor_gnat_semantic_handoff.py`, `tests/test-cor-gnat-semantic-handoff.py` |
| `scene_candidate` | local/cloud task router | `proposed` | planned support intake only |
| `continuity_check` | local continuity evaluation | `proposed` | continuity docs and eval plans exist; general AuthorForge route not admitted |
| `canon_review` | local first | `proposed` | no admitted source route |

## Lane Invariants

- Outputs are candidate-only unless a separate human/operator review accepts
  them.
- Run logging is evidence, not automatic baseline promotion.
- Protected terms and source authority boundaries must be preserved.
- Cloud lanes require explicit entitlement, degraded-state, and receipt proof
  before promotion.

## Adding A Lane

1. Add or update the lane record here.
2. Define the request/response contract.
3. Add route or runner implementation.
4. Add deterministic tests and manual validation evidence as appropriate.
5. Promote only after source proof, then copy to app-support.
