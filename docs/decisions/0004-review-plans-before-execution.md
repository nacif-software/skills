# 0004: Review Implementation Plans Before Execution

**Date:** 2026-06-30

## Decision

Add `review-plan` as a workflow gate between `plan-implementation` and
`execute-plan`.

The default non-trivial chain is:

```text
design-feature -> plan-implementation -> test-strategy -> pr-boundary -> review-plan -> execute-plan
```

## Rationale

Implementation plans are durable artifacts, so they should be reviewable before
they become work assignments. A plan review catches requirement gaps, weak tests,
unsafe parallelism, ambiguous task briefs, and poor PR boundaries while the cost of
change is low.

Reviewing the plan also protects context hygiene. If the plan is complete and
reviewed, workers can receive small task briefs instead of the full design
conversation.

## Consequences

- Non-trivial implementation should not move directly from planning to execution.
- `plan-implementation` should include enough structure for review.
- `review-plan` should read an existing `test-strategy` artifact instead of
  inventing test shape from scratch.
- `review-plan` should read an existing `pr-boundary` artifact instead of inventing
  landing shape from scratch.
- `execute-plan` should prefer reviewed plans when work is complex, parallelized, or
  split across agents.
- The suite now treats plan quality as a first-class risk surface, not just code
  quality.
