# Graphiti Pilot Architecture

## Status

Proposed architecture for the NLO Graphiti experiment-memory pilot.

## Decision

Use Graphiti only as a local, rebuildable, non-authoritative temporal graph projection over canonical experiment records.

## Architecture

```text
Git
  ├── task contracts
  ├── prompts
  ├── fixtures
  ├── rubrics
  └── reviewed promotion manifests

DataForge Local
  ├── run records
  ├── evaluation records
  ├── failure observations
  ├── hardware/runtime receipts
  ├── baseline records
  └── operator decisions

Deterministic NLO Projector
  ├── validates canonical records
  ├── maps fields to graph nodes/edges
  ├── attaches exact provenance
  ├── computes projection fingerprints
  └── never relies on LLM extraction for core facts

Graphiti + One Local Graph Backend
  ├── temporal relationship storage
  ├── graph traversal
  ├── hybrid retrieval where justified
  └── optional semantic enrichment, disabled by default

Operator
  ├── inspects canonical evidence
  ├── reviews contradictions
  ├── evaluates advisory context
  └── remains the sole promotion authority
```

## Locked Boundaries

Graphiti:

- is advisory;
- is disposable;
- is rebuildable from canonical records;
- may be stale or unavailable without blocking NLO runs;
- may not write canonical experiment records;
- may not update baselines;
- may not issue promotion decisions;
- may not choose models;
- may not modify public NeuronForge;
- may not be the only copy of any fact.

## Critical Path Rules

NLO execution:

```text
canonical run path
→ succeeds independently of graph state
```

Promotion review:

```text
canonical records
→ baseline comparison
→ optional graph advisory context
→ operator review
→ signed/recorded decision
```

Graphiti must not sit between the operator and canonical evidence.

## Fail-Open and Fail-Closed Doctrine

NLO runs fail open with respect to graph availability.

Promotion-advisory queries fail closed when:

- the graph is stale beyond threshold;
- projection fingerprint is invalid;
- a rebuild is incomplete;
- source references are missing;
- canonical high-watermark exceeds projected high-watermark;
- schema versions are unsupported.

## Pilot Scope

Included:

- one task contract;
- two to five historical runs;
- one accepted baseline path;
- one rejected candidate path;
- one failure-observation path;
- one hardware-constrained path;
- one local graph backend;
- four operator evidence queries;
- deterministic rebuild proof;
- comparison with simpler storage/search methods.

Excluded:

- production deployment;
- automatic incremental ingestion;
- multiple graph backends;
- model routing;
- public NeuronForge integration;
- automatic semantic enrichment;
- full manuscript ingestion;
- automated promotion.
