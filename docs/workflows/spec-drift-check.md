# Spec Drift Check Workflow

## Purpose

`spec-drift-check` compares implemented work against the agreed artifacts before a
branch is called ready. It protects against the quiet failure mode where tests pass
but the branch no longer matches the design, plan, PR boundary, or test strategy.

## Flow

```text
source artifacts and implementation diff
  -> identify correct base
  -> read durable artifacts
  -> build traceability table
  -> check missing scope
  -> check added scope
  -> check changed decisions
  -> check test and PR boundary drift
  -> report verdict and findings
  -> route to execute-plan, test-strategy, pr-boundary, plan-implementation, or review-pr
```

## Inputs

- Design doc, PRD, issue, acceptance criteria, or task brief.
- Implementation plan.
- Test strategy.
- PR boundary artifact.
- Plan review.
- Diff, changed files, commits, verification logs, and worker reports.

The workflow should use what exists and state what is missing. Missing artifacts are
not an excuse to skip the check.

## Drift Types

### Missing Scope

Required work that did not land:

- Behavior missing.
- Accepted edge case missing.
- Test promised but not added.
- Verification command not run.
- Review finding not addressed.

### Added Scope

Work that landed without being part of the source goal:

- Unrelated cleanup.
- Broad refactor.
- New behavior.
- Optional polish.
- Files outside the chosen PR boundary.

### Changed Decisions

Implementation choices that differ from the accepted artifacts:

- Public contract or API.
- Data model or schema.
- Architecture.
- Test seam.
- Rollout or rollback.
- PR boundary.

## Verdicts

- **Aligned:** no Critical or Important drift remains.
- **Drift found:** Important drift needs fixing, documentation, or user approval.
- **Blocked:** Critical drift makes the branch unsafe to present as ready.

## Next Actions

- Fix missing or incorrect work.
- Update the plan only with explicit approval.
- Split, revert, or move added scope to follow-up.
- Revise `test-strategy` when promised verification changed.
- Revise `pr-boundary` when added scope or split decisions changed.
- Proceed to `review-pr` when no blocking drift remains.

## Success Criteria

- The report maps source items to implementation evidence.
- Added and missing scope are visible.
- Test-strategy and PR-boundary promises are checked.
- Later reviewers can understand whether the branch matches the agreed work without
  replaying the conversation.
- The branch does not proceed to `review-pr` with unresolved Critical or Important
  drift.
