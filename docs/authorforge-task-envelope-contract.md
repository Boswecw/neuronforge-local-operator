# AuthorForge To NeuronForge Task Envelope Contract

**Status:** source intake baseline; not fully implemented as a general task
router.
**Scope:** local-system proving repo.

## Current Source Truth

NeuronForge Local currently exposes these AuthorForge-adjacent surfaces:

- `POST /api/v1/authorforge/drift-analysis`
- mounted style-analysis routes from `scripts/style_analysis.app`
- `POST /api/v1/cortex/gnat-semantic-handoff`
- local experiment registries for proofreading and style-analysis baselines

It does not yet expose the support-copy `POST /api/v1/authorforge/tasks`
general router in this source repo.

## Envelope Doctrine

Every future AuthorForge task envelope must carry:

- request identity
- task type and contract version
- source app identity
- bounded payload
- candidate-only insertion policy
- local/cloud posture if cloud assist is admitted
- receipt requirements
- privacy/body logging policy

## Candidate Rule

Returned text remains candidate output. AuthorForge keeps manuscript insertion
and user workflow authority. NeuronForge Local may produce reviewed candidates,
receipts, and model/run evidence; it does not mutate manuscript truth.

## Promotion Boundary

The support copy's `nf-task-envelope-v1` shape is a candidate support contract
until this source repo adds schemas/tests or an explicit promotion record accepts
the shape.
