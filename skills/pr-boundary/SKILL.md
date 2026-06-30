---
name: pr-boundary
description: >-
  Use when deciding whether work should be one PR, stacked PRs, separate PRs, or
  follow-up work; triggers on PR scope, PR split, stacked PR, branch too large,
  reviewability, rollout, rollback, or separating refactors from feature work.
license: MIT
metadata:
  author: nacif
  version: "0.1.0"
---

# PR Boundary

## Purpose

Decide how work should land. Produce a durable boundary artifact that separates
feature work, prep work, migrations, refactors, cleanup, risky changes, and
follow-ups before review or execution becomes harder.

## When to use

- Use during `plan-implementation` when work might span multiple review or deploy
  units.
- Use during `review-plan` when PR shape is missing, vague, or risky.
- Use before opening a PR when a branch feels too large or mixed.
- Use when the user asks what belongs in the same PR, what should split, what can be
  stacked, or what should become follow-up work.
- Do not use to review code quality. Use `review-pr` for code review.

## Inputs

- Source intent: design doc, issue, PRD, or stated goal.
- Work inventory: implementation plan, task list, issue list, current diff, or
  proposed change list.
- Constraints: release timing, migration order, deployment coupling, rollback needs,
  reviewer ownership, and repo contribution rules if available.

If the source intent or work inventory is incomplete, state the assumption and mark
the affected boundary as uncertain.

## Procedure

1. Identify the source goal and the current work inventory.
2. Discover only the repo context needed for landing decisions:
   - contribution or PR rules,
   - deployment or migration docs,
   - ownership boundaries,
   - nearby examples of similar changes.
3. Group changes by intent:
   - feature behavior,
   - enabling refactor,
   - schema or migration,
   - contract/API change,
   - tests or fixtures,
   - documentation,
   - cleanup or polish,
   - observability or operational work.
4. Map dependencies:
   - What must land first?
   - What can merge independently?
   - What must deploy atomically?
   - What can be hidden behind compatibility or feature flags?
5. Choose a landing shape:
   - One PR.
   - Stacked PRs.
   - Separate independent PRs.
   - Prep/refactor PR plus feature PR.
   - Migration/backfill/cleanup sequence.
   - Follow-up work.
6. Justify the boundary using reviewability, deployability, rollback, risk, and
   reviewer ownership.
7. Move unrelated cleanup, broad refactors, optional polish, and speculative work out
   of the feature PR unless they are required for safe delivery.
8. Name the verification expected at each PR boundary.
9. If work will be delegated, name which PR boundary each task belongs to so
   `context-briefing` can include the boundary without the full discussion.
10. Produce the boundary artifact and next action.

## Boundary rules

- Same PR when changes share one intent, one review surface, one deploy moment, and
  one rollback story.
- Stack PRs when each step depends on the previous step but can be reviewed and
  verified independently.
- Separate PRs when changes are independently valuable, independently risky, owned by
  different reviewers, or deployable on different schedules.
- Split prep/refactor work when it can land without changing behavior.
- Split migrations or backfills when they need staged deploy, compatibility, or
  rollback planning.
- Mark follow-up work when it is useful but not required for the source goal.

## Output format

```markdown
# PR Boundary

## Recommendation
One PR | Stacked PRs | Separate PRs | Prep + feature | Migration sequence | Follow-up

## Change Inventory
- <change>: <intent, files or area, dependency>

## Proposed PRs
### PR 1: <title>
- Purpose: <why this PR exists>
- Includes: <changes>
- Excludes: <changes>
- Depends on: <none or PR>
- Verification: <checks>
- Rollback: <what happens if this must revert>

## Follow-ups
- <work not required now>: <why later is safe>

## Risks
- <risk>: <mitigation or owner>

## Next Action
Proceed as planned | revise plan | split branch | create stacked issues
```

## Common mistakes

- Keeping unrelated cleanup because it was discovered nearby.
- Hiding risky migrations inside a large feature PR.
- Splitting by code layer instead of reviewable intent.
- Creating stacks where every PR is impossible to verify independently.
- Calling optional polish "required" because it would be nice to have.
- Ignoring rollback until after the PR is open.
- Dispatching task work without telling workers what must stay inside or outside the
  selected PR boundary.

## Success criteria

- Each proposed PR has one clear purpose and review surface.
- Dependencies, verification, and rollback are explicit.
- Reviewers can see what belongs together and what was intentionally excluded.
- `plan-implementation`, `review-plan`, or `review-pr` can use the artifact without
  the full conversation.
- `execute-plan` can preserve PR boundaries while splitting or parallelizing tasks.
