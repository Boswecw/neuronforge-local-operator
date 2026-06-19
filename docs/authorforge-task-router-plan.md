# AuthorForge Task Router Plan

**Status:** active source intake plan; not shipped as a general router.
**Scope:** local-system proving repo.

## Purpose

Move AuthorForge-facing NeuronForge work from one-off endpoints toward governed
task contracts, lane registries, receipts, and candidate-only outputs.

## Current Source Truth

- Drift analysis is exposed at `/api/v1/authorforge/drift-analysis`.
- Style analysis is mounted from the style-analysis app.
- GNAT semantic handoff accepts Cortex-originated handoffs and returns a
  candidate receipt without mutating source receipts.
- Proofreading and style-analysis baselines exist as local experiment records.

## Planned Router Surface

A future general router may expose:

- health/status compatibility
- task envelope validation
- local lane selection
- degraded/unavailable receipts
- optional cloud-assist handoff only after source proof

## Non-Negotiable Rules

- AuthorForge owns writing workflow and manuscript insertion.
- NeuronForge owns model/lane execution only after an admitted contract.
- All generated prose is candidate-only.
- No cloud path may be silent or implicit.
- No baseline promotion without manual validation evidence.

## Next Implementation Gate

Before app-support copies treat the router as promoted source truth, this repo
needs schemas/tests for the chosen envelope and a route that proves degraded and
candidate-only behavior.
