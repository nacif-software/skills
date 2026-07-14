---
name: test-strategy
description: >-
  Use when planning, reviewing, or improving tests for a feature, bugfix, PR,
  implementation plan, test matrix, verification plan, regression risk, edge cases,
  manual checks, or deciding what not to test.
license: MIT
metadata:
  author: nacif
  version: "0.1.0"
---

# Test Strategy

## Purpose

Create the smallest useful test plan for the risk being changed. The output is a
durable test matrix that maps behavior, risk, and verification commands before code
is written or before a PR is judged.

## When to use

- Use during `plan-implementation` before task steps are finalized.
- Use during `review-plan` when the plan says only "add tests" or verification is
  vague.
- Use during `review-pr` when tests are missing, too broad, too brittle, or not tied
  to the changed behavior.
- Use for bug fixes, regressions, permission logic, migrations, API contracts,
  UI flows, integration boundaries, and manual verification choices.
- Do not use to execute tests. Use `verification-gate` for evidence before claims.

## Inputs

- Source intent: design doc, PRD, issue, bug report, or stated behavior.
- Change shape: implementation plan, task list, current diff, or proposed files.
- Existing test patterns and commands when available.
- Risk notes: security, permissions, data integrity, migrations, compatibility,
  performance, concurrency, observability, and rollback.

If inputs are incomplete, write the strategy with explicit assumptions and mark
unknowns.

## Procedure

1. Identify the behaviors and risks that need confidence.
2. Discover local test conventions and commands:
   - test directory structure,
   - naming patterns,
   - fixtures, factories, helpers, mocks,
   - unit, integration, end-to-end, contract, typecheck, lint, and build commands.
3. Choose the highest useful test seam for each behavior:
   - Unit for pure logic and edge cases.
   - Integration for module boundaries, persistence, APIs, queues, and workflows.
   - Contract for public APIs, schemas, events, or generated clients.
   - End-to-end for user-critical flows where lower seams miss wiring risk.
   - Manual only when automation is impractical or too brittle.
4. Build a risk-based matrix:
   - happy path,
   - boundary and invalid input,
   - permissions and tenancy,
   - failure and rollback,
   - regression case,
   - compatibility or migration behavior,
   - "do not test" items with reasons.
5. For new automated tests, name the expected red failure and green signal.
6. Prefer fewer high-signal tests over broad low-value coverage.
7. Avoid brittle internals unless the internal contract is the behavior being changed.
8. If the strategy will feed delegated work, name which matrix rows belong in each
   task brief and pass only those rows through `context-briefing`.
9. Produce the test strategy artifact and next action.

## Output format

```markdown
# Test Strategy

## Scope
- Source: <design, issue, bug, plan, or PR>
- Goal: <behavior or risk being verified>

## Existing Test Surface
- Patterns: <nearby examples>
- Commands: <targeted and broad commands>

## Test Matrix
| Behavior or risk | Seam | Test or check | Red signal | Green signal |
| --- | --- | --- | --- | --- |
| <behavior> | unit/integration/contract/e2e/manual | <test/check> | <expected failure> | <expected pass> |

## Do Not Test
- <case>: <why not useful now>

## Manual Verification
- <check>: <why automation is not practical>

## Coverage Gaps
- <gap>: <risk or follow-up>

## Next Action
Add to implementation plan | feed task briefs | revise plan | review PR | run verification
```

## Common mistakes

- Treating "add tests" as a strategy.
- Testing private implementation instead of observable behavior.
- Writing too many low-value tests while missing the risky edge.
- Skipping the regression that proves the bug is fixed.
- Using manual verification because it is faster, not because automation is poor.
- Forgetting to state what should fail before implementation.
- Expanding scope to test unrelated legacy behavior.
- Handing workers the whole strategy when a task needs only a few relevant rows.
- Claiming tests pass from the strategy alone instead of using `verification-gate`.

## Success criteria

- Each important behavior or risk has an appropriate verification seam.
- The matrix names exact tests or checks and expected signals.
- The strategy says what not to test and why.
- `plan-implementation`, `review-plan`, `execute-plan`, or `review-pr` can use the
  artifact without the full conversation.
- Subagent briefs can reference the relevant rows without carrying unrelated test
  discussion.
