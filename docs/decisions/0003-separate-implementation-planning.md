# 0003: Separate Implementation Planning From Execution

**Date:** 2026-06-30

## Decision

Add `plan-implementation` as a separate workflow between `design-feature` and the
execution path.

The default chain is:

```text
design-feature -> plan-implementation -> test-strategy -> pr-boundary -> review-plan -> execute-plan
```

## Rationale

A design doc answers what should exist and why. Execution needs a different artifact:
exact files, task order, dependencies, test seams, verification commands, and code
snippets where they lock important contracts.

Skipping the implementation plan makes workers invent details during execution,
which increases drift, context use, review ambiguity, and unsafe parallelism.

## Consequences

- `design-feature` should not jump directly to `execute-plan` for non-trivial work.
- `execute-plan` should expect a reviewed implementation plan, task list, or issue
  breakdown when work is non-trivial.
- `plan-implementation` owns the plan contract and self-review checklist.
- `test-strategy` owns the evidence matrix when testing is non-trivial.
- `pr-boundary` owns the landing-shape decision when PR scope is non-trivial.
- `review-plan` owns independent review of the plan before non-trivial execution.
- Code snippets belong in plans when they reduce ambiguity, not as full speculative
  implementations.
