# Graph Identity and Fingerprint Contract

## Purpose

Define deterministic node, edge, and graph identity so rebuilds are comparable and duplicates cannot silently accumulate.

## Canonical Node Identity

```text
node_id = SHA256(
  graph_schema_version
  + ":"
  + entity_type
  + ":"
  + canonical_business_key
)
```

Examples:

```text
ModelVersion:qwen2.5:14b@digest-sha256-abc
Run:run-2026-03-13-005
PromptVersion:lore-safe-proofread-003@sha256-def
TaskContractVersion:analyze.style.scene.v1
Evaluation:eval-run-005-review-01
```

## Canonical Edge Identity

```text
edge_id = SHA256(
  graph_schema_version
  + ":"
  + relationship_type
  + ":"
  + source_node_id
  + ":"
  + target_node_id
  + ":"
  + source_record_id
  + ":"
  + effective_at
)
```

This permits historically distinct edges while preventing duplicate replay of the same canonical fact.

## Property Normalization

Before hashing:

- encode UTF-8;
- normalize Unicode to NFC;
- trim prohibited insignificant whitespace;
- sort object keys;
- sort set-like arrays;
- preserve ordered arrays where order is semantic;
- normalize timestamps to UTC RFC3339 with `Z`;
- represent absent optional fields as omission, not empty strings;
- never include backend-generated IDs;
- never include projection runtime timestamps in semantic fingerprints.

## Graph Fingerprint

The graph fingerprint is computed from a canonical export containing:

- canonical node IDs;
- canonical edge IDs;
- entity/relationship types;
- normalized semantic properties;
- temporal validity fields;
- exact source references.

Exclude:

- database internal IDs;
- storage page order;
- query-plan metadata;
- projected-at timestamps;
- runtime metrics;
- connection metadata.

## Equality Levels

### Structural Equality

Same node IDs, edge IDs, entity types, and relationship types.

### Semantic Equality

Structural equality plus identical normalized semantic properties and temporal fields.

### Provenance Equality

Semantic equality plus identical source references and content hashes.

Pilot rebuild acceptance requires provenance equality.

## Rebuild Proof

Run two clean rebuilds:

```text
rebuild A
→ canonical export A
→ fingerprint A

rebuild B
→ canonical export B
→ fingerprint B
```

Acceptance:

```text
fingerprint A == fingerprint B
```

and zero duplicate canonical identities.
