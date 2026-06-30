---
name: review-plan
description: >-
  Use when an implementation plan, task breakdown, issue sequence, test strategy,
  PR scope, or subagent split needs review before coding, delegation, or execution.
license: MIT
metadata:
  author: nacif
  version: "0.1.0"
---

# Review Plan

## Purpose

Review an implementation plan before code is written. Catch missing requirements,
unsafe task splits, weak tests, false parallelism, and poor PR boundaries while the
artifact is still cheap to change.

## When to use

- Use after `plan-implementation` for non-trivial work.
- Use when the user asks to review a plan, task list, issue breakdown, test plan,
  subagent split, or proposed PR scope.
- Use before `execute-plan` when workers would otherwise inherit ambiguity.
- Do not use after code exists unless the request is still about the plan. Use
  `review-pr` for code review.

## Inputs

- Source artifact: design doc, PRD, issue, or accepted requirements.
- Implementation artifact: plan, task breakdown, issue sequence, or subagent briefs.
- Local repo rules and nearby patterns when needed to judge feasibility.

If either artifact is missing, state the gap and review only what can be verified.

## Procedure

1. Identify the source artifact, implementation artifact, and intended next step.
2. Discover only the repo context needed to judge the plan. Prefer existing docs,
   tests, scripts, interfaces, and nearby examples over broad repository reading.
3. Check source coverage:
   - Every requirement maps to at least one task.
   - Out-of-scope items remain out of scope.
   - Assumptions are explicit and acceptable.
4. Check executability:
   - File paths and ownership are exact.
   - Dependencies and ordering are clear.
   - Shared contracts are specified before dependent tasks.
   - No placeholders or vague steps remain.
5. Check test strategy:
   - Read the `test-strategy` artifact if one exists; otherwise apply test strategy
     checks directly.
   - New behavior has targeted verification.
   - Tests exercise useful interfaces, not fragile internals.
   - Expected red and green signals are specific when tests are added.
   - Manual checks are named only when automation is not practical.
   - Do-not-test decisions have reasons.
6. Check task and subagent safety:
   - Vertical tasks produce reviewable behavior or artifacts.
   - Parallel-safe claims have disjoint write scopes or stable shared contracts.
   - Task briefs can be derived without passing the full conversation.
7. Check risk areas when relevant:
   - Security, auth, privacy, data integrity, migrations, compatibility,
     performance, observability, rollout, rollback, and documentation.
8. Check PR boundary:
   - Read the `pr-boundary` artifact if one exists; otherwise apply the boundary
     checks directly.
   - Recommend one PR, stacked PRs, separate PRs, prep plus feature, migration
     sequence, or follow-up work.
   - Keep changes together only when they share intent, review surface, deployment
     timing, and rollback behavior.
   - Split prep/refactor, risky migrations, unrelated cleanup, and optional polish
     unless they are required for the feature to work.
9. Report findings by severity and provide a verdict.
10. Offer next step:
    - A: revise the plan with `plan-implementation`.
    - B: create or revise `test-strategy`.
    - C: create or revise `pr-boundary`, or split into PRs or issues.
    - D: continue to `execute-plan` only if no Critical or Important findings remain.
11. Use `verification-gate` before claiming the plan review or Ready verdict is
    complete.

## Severity model

- Critical: plan cannot be executed safely or would likely miss the source goal.
- Important: fix before coding, delegation, or issue creation.
- Minor: useful improvement that does not block execution.

## Output format

```markdown
# Implementation Plan Review

## Verdict
Blocked | Needs revisions | Ready

## Findings
- [Critical] <area>: <problem>. Suggested fix: <fix>.
- [Important] <area>: <problem>. Suggested fix: <fix>.
- [Minor] <area>: <problem>. Suggested fix: <fix>.

## Requirement Traceability
- <requirement>: covered by <task> / missing / unclear.

## Test Strategy
- <behavior>: <verification path>.
- Artifact: <path or missing>.
- Gaps: <missing seam, red/green signal, manual reason, or do-not-test decision>.

## Parallelization Review
- <task/group>: safe / sequential / unclear, because <reason>.

## PR Boundary
- Same PR: <changes that belong together>.
- Separate PR, stack, prep, or migration: <work that needs a different landing shape>.
- Follow-up: <non-blocking work>.

## Next Step
Choose A to revise the plan, B to revise tests, C to revise PR shape, or D to execute.
```

## Common mistakes

- Reviewing the plan as prose instead of checking traceability to the source.
- Approving parallel work because tasks look small, not because interfaces and
  write scopes are safe.
- Treating "add tests" as a test strategy.
- Recomputing test strategy from scratch when a `test-strategy` artifact already
  exists.
- Hiding risky migrations, refactors, or cleanup inside the feature PR.
- Recomputing PR shape from scratch when a `pr-boundary` artifact already exists.
- Letting Important findings become "we will notice during implementation".
- Sending work to `execute-plan` while test strategy or PR boundary findings remain
  unresolved.

## Success criteria

- The review creates a durable artifact that can be attached to the plan.
- Critical and Important findings clearly block execution until resolved.
- Test strategy advice separates useful coverage from brittle or low-value tests.
- PR boundary advice separates feature, prep, migration, cleanup, and follow-up work.
- `execute-plan` can start with fewer assumptions and smaller subagent briefs.
- A Ready verdict cites the test strategy and PR boundary artifacts, or explains why
  they are unnecessary.
