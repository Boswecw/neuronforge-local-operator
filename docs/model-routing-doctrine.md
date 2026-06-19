# Model Routing Doctrine

**Status:** source doctrine baseline; support-side router claims require
reconciliation.
**Scope:** local-system proving repo.

## What NeuronForge Owns

When a task contract is admitted, NeuronForge owns:

- lane execution posture
- model/profile/prompt selection behind the contract
- validation and review evidence
- degraded-state classification
- candidate receipts

AuthorForge supplies task context and keeps writer-facing workflow authority.

## Current Source Truth

- Local experiment docs and registries identify local proofreading and
  style-analysis baselines.
- `scripts/style_analysis` provides a concrete AuthorForge style-analysis route.
- `service/drift_analysis.py` provides deterministic drift analysis.
- `service/cor_gnat_semantic_handoff.py` accepts GNAT handoffs as non-canonical
  candidate work and keeps source receipts immutable.

## Planned / Not Yet Proven

The app-support copy claims local-first execution with cloud escalation. This
source repo does not yet prove a full cost-aware provider/model router for
AuthorForge task envelopes. Until source implementation and tests land, cloud
provider selection remains planned doctrine, not promoted source truth.

## Prohibited

- AuthorForge choosing provider/model ids.
- Treating a configured URL as entitlement.
- Returning unreviewed output as final manuscript truth.
- Promoting a model/lane baseline without manual validation evidence.
