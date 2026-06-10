# Go / No-Go Evaluation

## Mandatory Governance Gates

Graphiti is rejected if any of these fail:

- exact source traceability;
- deterministic provenance-equal rebuild;
- fail-open isolation from NLO execution;
- fail-closed promotion-advisory integrity;
- no canonical-only facts in Graphiti;
- no prohibited data transmission;
- no automatic promotion path;
- bounded decommission path.

## Weighted Comparison

| Criterion | Weight |
|---|---:|
| Source traceability and auditability | 30% |
| Temporal/cross-run answer quality | 25% |
| Deterministic rebuild and idempotency | 15% |
| Operator usefulness | 10% |
| Interactive latency | 10% |
| Setup and maintenance cost | 10% |

## Test Questions

1. Why is the current run the baseline?
2. What changed from the prior baseline?
3. Which failure classes recur?
4. Which model/prompt combinations regress?
5. What evidence supports or opposes promotion?

## Keep Criteria

Graphiti must:

- materially outperform simpler alternatives on at least three questions;
- preserve exact source traceability;
- rebuild deterministically;
- remain operationally optional;
- stay within agreed maintenance cost;
- reduce operator cognitive load.

## Decision Record

The final decision must state:

- evaluator;
- date;
- backend/version;
- fixture set;
- scores;
- mandatory gate results;
- known limitations;
- keep/revise/remove outcome.
