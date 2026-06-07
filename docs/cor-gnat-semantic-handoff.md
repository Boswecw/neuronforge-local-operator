# COR GNAT Semantic Handoff

Endpoint: `POST /api/v1/cortex/gnat-semantic-handoff`

This endpoint accepts Cortex `GnatSemanticHandoff.v1` requests for optional
NeuronForge semantic candidate generation from reconciled GNAT syntax artifacts.

The request must carry:

- a referenced Cortex retrieval package artifact;
- an explicit user or app request;
- the candidate contract family;
- model and resource disclosure;
- transfer guardrails proving COR receipts remain immutable.

NeuronForge Local responds with
`NeuronForgeGnatSemanticHandoffReceipt.v1`, an acceptance receipt only. It does
not run the model in this route, rewrite COR receipts, promote truth, or create
canonical semantic output.

Required boundary:

- `semantic_result_posture` remains `non_canonical_candidate`.
- `cor_receipts_mutation_allowed` remains `false`.
- `raw_content_included` remains `false`.
- source artifact state must be `ready`/`complete` or
  `partial_success`/`incomplete`.

Malformed handoffs fail closed through FastAPI/Pydantic validation.
