# Risks, Anti-Patterns, and Locked Decisions

## Highest Risks

1. unstable identity;
2. ambiguous authority;
3. bad temporal semantics;
4. misleading query narratives;
5. stale graph advice;
6. sensitive-content leakage;
7. over-scoped backend abstraction;
8. Graphiti concepts leaking into canonical contracts;
9. expensive removal;
10. building a platform before proving value.

## Prohibited Anti-Patterns

- using graph output to select models;
- using graph output to promote baselines;
- treating graph confidence as evaluation confidence;
- generating source IDs with an LLM;
- letting Graphiti create canonical records;
- blocking NLO runs when Graphiti is down;
- using graph state as the only copy of a decision;
- feeding full manuscripts;
- mixing inferred enrichment with core deterministic facts;
- allowing learned ontology to redefine core types;
- supporting multiple production backends during the pilot;
- showing narrative before evidence;
- hiding contradictory records;
- using backend insertion order as event order.

## Locked Decisions Before Graph Code

- one backend;
- one authority per artifact type;
- one timestamp doctrine;
- one deterministic ID scheme;
- one projection freshness model;
- one query evidence contract;
- enrichment disabled by default;
- one bounded decommission path.

## Open Decisions

- final backend choice;
- acceptable projection lag for advisory queries;
- whether DataForge Local adapter is available in the first pilot;
- whether optional semantic enrichment is ever tested;
- final operator CLI naming.
