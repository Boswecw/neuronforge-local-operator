# Experiment Record Authority Matrix

## Purpose

Prevent authority duplication between Git, DataForge Local, and Graphiti.

## Authority Matrix

| Artifact | Git | DataForge Local | Graphiti |
|---|---|---|---|
| Task contract source | Authority | Version reference | Projection |
| Prompt source | Authority | Version reference | Projection |
| Evaluation rubric | Authority | Version reference | Projection |
| Test fixture source | Authority | Optional hash/reference | Projection |
| Run receipt | Optional historical fixture | Authority | Projection |
| Hardware profile | Optional fixture | Authority | Projection |
| Evaluation record | Optional reviewed fixture | Authority | Projection |
| Failure observation | Optional fixture | Authority | Projection |
| Baseline decision | Reviewed manifest | Authority receipt | Projection |
| Promotion candidate | Reviewed manifest or proposal | Authority receipt | Projection |
| Promotion decision | Authority manifest | Authority receipt | Projection |
| Graph projection report | Optional committed proof fixture | Runtime record | Not authority |
| Graph node/edge | No | No | Derived only |
| Graph narrative summary | No | No | Derived only |

## Conflict Doctrine

If Git and DataForge Local disagree:

1. identify artifact type;
2. consult this matrix;
3. use the designated authority;
4. quarantine the conflicting record;
5. do not project disputed facts;
6. create a reconciliation record;
7. rebuild after resolution.

Graphiti never resolves authority conflicts.

## Canonical References

Every projected fact must include:

- `source_record_id`;
- `source_record_type`;
- `source_schema_version`;
- `source_content_hash`;
- `source_commit` when Git-backed;
- `source_store`;
- `recorded_at`.

## Recovery Doctrine

A full graph rebuild must require only:

- canonical Git artifacts;
- canonical DataForge Local records;
- deterministic mapping code;
- pinned graph schema version.

No hidden graph-only state may be required.
