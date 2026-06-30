# PR Boundary Workflow

## Purpose

`pr-boundary` decides how work should land. It creates a durable artifact that
answers whether a change belongs in one PR, stacked PRs, separate PRs, a prep plus
feature sequence, a migration sequence, or follow-up work.

## Flow

```text
source intent and work inventory
  -> discover landing constraints
  -> group changes by intent
  -> map dependencies
  -> choose landing shape
  -> justify review, deploy, rollback, and ownership trade-offs
  -> name verification per boundary
  -> produce PR boundary artifact
  -> feed boundary membership to plan tasks, execute-plan, or review-pr
```

## Inputs

The workflow can run from either planned or existing work:

- Design doc, PRD, issue, or stated goal.
- Implementation plan, task breakdown, issue list, or current diff.
- Contribution rules, release notes, deployment docs, ownership boundaries, and
  existing PR patterns when available.

If the agent cannot identify source intent or work inventory, it should state the
gap and mark the recommendation uncertain.

## Landing Shapes

### One PR

Use one PR when the changes share:

- One intent.
- One coherent review surface.
- One deploy moment.
- One rollback story.
- One verification path.

### Stacked PRs

Use stacked PRs when each step depends on the previous step but can still be
reviewed, verified, and merged in order. Each PR in the stack should leave the
project in a healthy state.

### Separate PRs

Use separate PRs when changes are independently valuable, independently risky,
owned by different reviewers, or deployable on different schedules.

### Prep Plus Feature

Use a prep/refactor PR when enabling work can land without behavior change. The
feature PR should then be smaller and easier to review.

### Migration Sequence

Use a migration sequence when schema, data, API, or infrastructure changes need
compatibility windows, backfills, staged deploy, or rollback planning.

### Follow-Up

Use follow-up work for optional polish, cleanup, documentation, observability, or
future hardening that is not required for the source goal.

## Boundary Questions

- Would a reviewer understand this PR in one sitting?
- Does this change need to deploy atomically?
- Can this PR be reverted without breaking later work?
- Is a refactor required for the feature, or only adjacent cleanup?
- Can tests prove this PR independently?
- Are different owners or reviewers responsible for different parts?
- Would splitting lower risk without creating fake dependencies?
- Would keeping it together make rollback or review harder?

## Anti-Patterns

- A feature PR that also contains broad cleanup.
- A migration hidden inside unrelated feature work.
- A stack where PR 2 is the first one that actually passes tests.
- Separate PRs that cannot be understood without each other.
- A "follow-up" that is actually required for safe delivery.
- A giant PR justified only by "the files were nearby."

## Artifact Contract

The PR boundary artifact should include:

- Recommendation.
- Change inventory.
- Proposed PR list.
- Included and excluded work.
- Dependencies.
- Verification per PR.
- Rollback notes.
- Follow-ups.
- Risks and mitigations.

## Success Criteria

- The landing shape is explicit and justified.
- Each PR has one purpose, review surface, and verification path.
- Splits reduce real risk instead of creating ceremony.
- Future agents can use the artifact without replaying the conversation.
- Delegated tasks preserve the selected PR boundary instead of silently expanding
  scope.
