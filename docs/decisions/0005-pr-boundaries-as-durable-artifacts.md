# 0005: Treat PR Boundaries As Durable Artifacts

**Date:** 2026-06-30

## Decision

Add `pr-boundary` as the workflow for deciding how planned or existing work should
land: one PR, stacked PRs, separate PRs, prep plus feature, migration sequence, or
follow-up work.

The default non-trivial chain becomes:

```text
design-feature -> plan-implementation -> test-strategy -> pr-boundary -> review-plan -> execute-plan
```

## Rationale

PR shape affects review quality, deployment safety, rollback, ownership, and context
size. If the boundary is decided only after implementation, the branch may already
mix feature work, refactors, migrations, cleanup, and polish in ways that are hard
to review or split.

Making the boundary explicit before execution gives agents and humans a stable
artifact for what belongs together and what was intentionally excluded.

## Consequences

- `plan-implementation` should include or call `pr-boundary` for non-trivial work.
- `review-plan` should review the boundary rather than invent it from scratch.
- `execute-plan` should preserve the chosen landing shape while implementing.
- Optional cleanup and polish should become follow-up unless required for safe
  delivery.
