# Data Security and Classification

## Default Posture

- local-only;
- least-data;
- enrichment disabled;
- no full-manuscript ingestion;
- graph service bound to loopback;
- no external LLM or embedding transmission without explicit approval.

## Data Classification

| Data Class | Graph Storage | External LLM | External Embeddings |
|---|---|---|---|
| Record IDs | Allowed | Allowed | Allowed |
| Model metadata | Allowed | Allowed | Allowed |
| Prompt IDs/hashes | Allowed | Allowed | Allowed |
| Evaluation scores | Allowed | Allowed | Allowed |
| Failure taxonomy codes | Allowed | Allowed | Allowed |
| Reviewer notes | Restricted | Redacted only | Redacted only |
| Evidence spans | Minimized | Prohibited by default | Prohibited by default |
| Unpublished manuscript excerpts | Restricted | Prohibited by default | Prohibited by default |
| Full manuscript | Prohibited | Prohibited | Prohibited |
| Secrets/API keys | Prohibited | Prohibited | Prohibited |
| Personal customer metadata | Prohibited unless separately governed | Prohibited | Prohibited |

## Required Defaults

```text
NLO_GRAPH_ENRICHMENT_ENABLED=false
NLO_GRAPH_EXTERNAL_CONTENT_ALLOWED=false
NLO_GRAPH_BIND_HOST=127.0.0.1
```

## Ingestion Filter

Reject any episode containing:

- secrets;
- API keys;
- authorization headers;
- full manuscript content;
- prohibited PII;
- unclassified binary attachments;
- external URLs containing tokens;
- fields outside the approved schema.

## Encryption and Storage

- graph volume must remain local;
- host filesystem encryption is recommended;
- backups are disabled during the pilot unless explicitly approved;
- exported canonical graph snapshots must be treated as sensitive artifacts;
- secure deletion must remove containers, volumes, temporary exports, and caches.

## Enrichment Boundary

Core facts are deterministically projected.

Optional semantic enrichment:

- is disabled by default;
- must use separate node/edge types;
- must be marked `derived_enrichment`;
- must preserve exact source references;
- must never change core graph facts;
- must never be consumed by promotion logic;
- requires explicit data-policy approval.
