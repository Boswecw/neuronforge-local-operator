# Handoff: Wire Forge_Command's local-LLM training system to NLO + approval-gated promotion

**Status:** Pending — to be implemented in a session opened on the `Forge_Command` repo.
**Created from:** `neuronforge-local-operator` (NLO) session, 2026-05-29.

This document is the briefing for work that must happen **in Forge_Command**, not here.
NLO (`neuronforge-local-operator`) is the operator/training workspace; Forge_Command is the
control app that should orchestrate it. This file is committed in NLO so the Forge_Command
session can read it from a local checkout.

---

## Ecosystem (local, rooted at `/home/charlie/Forge/`)

| Piece | Location | Role |
| --- | --- | --- |
| **Forge_Command** | `/home/charlie/Forge/ecosystem/Forge_Command` | Tauri + SvelteKit control app. Holds the "train local LLMs" system. **← repo to edit.** |
| **NLO** | `/home/charlie/Forge/ecosystem/neuronforge` (this `neuronforge-local-operator` workspace) | Local-first training/operator workspace. Source of truth for runs. |
| **Public neuronforge** | `/home/charlie/Forge/apps/public-app-local-support/neuronforge` | Public-facing applications-support version. **← promotion target.** |

### Relevant Forge_Command surfaces (from settings)

- `orchestrator/app`, `orchestrator/tests`
- `src/routes/neuroforge`, `src/routes/operations`, `src/routes/fleet`, `src/routes/connectivity`, `src/routes/forge-keys`
- `src/lib/stores`, `src/lib/data`, `src/lib/types`, `src/lib/components`, `src/lib/utils`
- `src-tauri/src`, `src-tauri/migrations`

### Relevant NLO surfaces

- Operator/training scripts in `scripts/`:
  - `run-proofread.sh`, `run-and-log-proofread.sh`
  - `run-style-analysis.sh`, `run-continuity-adjacent-scene.sh`
  - `log-run.sh`, `next-run-id.sh`
  - `review-proofread.sh`, `compare-outputs.sh`
- Run records: `outputs/` + `registry/`
- Canonical doc: `NLOSYSTEM.md` (built from `doc/system/` via `bash doc/system/BUILD.sh`)

---

## Goal

Forge_Command's training system should:

1. **Train/run via NLO** — invoke NLO's operator scripts and read back its run records /
   registry, rather than reimplementing the training flow inside Forge_Command.
2. **Approval gate** — surface candidate runs for **explicit user approval** in the
   Forge_Command UI. The `neuroforge` / `operations` routes are the natural home.
3. **Promote on approval** — only after approval, push the approved result to the public-facing
   neuronforge at `/Forge/apps/public-app-local-support/neuronforge`.

Flow: **train via NLO → user approves → promote to `/Forge/apps/.../neuronforge`.**

---

## Promotion rule (from NLO doctrine)

A run is promotable only when it:

- is explicitly reviewed,
- beats the current quality anchor (`run-2026-03-13-005`, baseline model `qwen2.5:14b`),
- and shows no lore-safety / protected-term regression.

Operational success (the wrapper runs cleanly) does **not** by itself replace the baseline.

---

## First steps in the Forge_Command session

1. Read `Forge_Command/orchestrator/app` and `src/routes/neuroforge` to locate the existing
   "train local LLMs" system.
2. Map how it currently triggers runs and where results are stored.
3. Design the integration against the real code:
   - **NLO invocation** layer (call the `scripts/` entry points; ingest `outputs/` + `registry/`).
   - **Approval** UI/state (candidate list → approve/reject, gated promotion).
   - **Promotion** action targeting `/Forge/apps/public-app-local-support/neuronforge`, executed
     only after approval.
4. Confirm the session can see `/home/charlie/Forge/` (all three checkouts present).

---

## Notes / open questions for the implementer

- How should promotion physically move artifacts into the public app (copy, git push, packaging)?
  Decide with the user before writing the promote step.
- Where does approval state persist (Tauri SQLite migration in `src-tauri/migrations`?).
- Keep the promotion irreversible-action guardrails: never promote without explicit approval.
