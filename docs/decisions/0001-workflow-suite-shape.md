# 0001: Start With A Curated Workflow Suite

**Date:** 2026-06-30

## Decision

Start Nacif Skills as a curated workflow suite, not as a loose collection of
unrelated skills.

V1 includes:

- `design-feature`
- `plan-implementation`
- `test-strategy`
- `pr-boundary`
- `review-plan`
- `review-pr`
- `execute-plan`
- `spec-drift-check`
- `context-briefing`
- `verification-gate`

## Rationale

The first public value should be a recommended path that teams can use immediately.
Feature design and PR review cover two common development moments: deciding what to
build and deciding whether a change is good enough to merge.

The implementation flow intentionally separates planning from execution so workers
can act from a decision-complete artifact instead of a broad design. Smaller
discipline skills still exist, but they support the workflows instead of competing
with them.

Plan review is part of the happy path because the implementation artifact is also a
quality surface. Reviewing it before execution reduces ambiguous work, unsafe
parallelism, and oversized PRs.

PR boundary is separate because landing shape affects execution, review, deploy, and
rollback. It should be decided before work is spread across agents or branches.

Test strategy and spec drift are separate because test confidence and requirement
alignment are different risks. A branch can have tests but still miss the spec, and
it can match the spec while still needing better evidence.

## Consequences

- New workflows must document their gates and artifacts.
- README should emphasize the recommended path.
- Standalone skills can be added later without weakening the happy path.
