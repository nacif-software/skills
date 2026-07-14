# 0007: Check Spec Drift Before Review Or Readiness Claims

**Date:** 2026-06-30

## Decision

Add `spec-drift-check` as the workflow for comparing implemented work against the
source artifacts, implementation plan, test strategy, PR boundary, and plan review
before PR review or readiness claims.

The execution tail becomes:

```text
execute-plan -> spec-drift-check -> review-pr -> verification-gate
```

## Rationale

Tests can pass while the work drifts from the agreed goal. Agents may add helpful
cleanup, change architecture, miss edge cases, skip promised tests, or violate a PR
boundary without noticing. A drift report turns those differences into explicit
decisions before the branch is reviewed or called ready.

## Consequences

- `execute-plan` should run `spec-drift-check` before whole-branch readiness.
- `review-pr` should read a drift report when present.
- Added scope must be kept, split, reverted, or approved.
- Missing scope must be fixed or explicitly accepted before completion.
