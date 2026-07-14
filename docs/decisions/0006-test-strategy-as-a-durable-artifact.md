# 0006: Treat Test Strategy As A Durable Artifact

**Date:** 2026-06-30

## Decision

Add `test-strategy` as the workflow for deciding what tests and verification checks
are useful before execution or PR review.

The non-trivial path becomes:

```text
design-feature -> plan-implementation -> test-strategy -> pr-boundary -> review-plan
```

## Rationale

"Add tests" is too vague for reliable implementation. Agents need to know which
behavior, risk, seam, command, red signal, and green signal matter. A durable test
matrix lets planning, execution, review, and verification share the same evidence
expectations without carrying the full conversation.

## Consequences

- `plan-implementation` should include or call `test-strategy` for non-trivial work.
- `review-plan` should review an existing test strategy instead of inventing one
  from scratch.
- `execute-plan` should preserve the promised test matrix or explain deviations.
- `review-pr` should compare the final tests to the strategy when one exists.
