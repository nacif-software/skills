# Execute Plan Workflow

## Purpose

`execute-plan` turns an approved implementation plan, task list, or issue breakdown
into implemented work. It should not replace `plan-implementation` or `review-plan`
for non-trivial work; execution depends on a concrete, reviewed plan.

## Flow

```text
reviewed implementation plan
  -> read test strategy artifact when present
  -> read PR boundary artifact when present
  -> discover repository rules
  -> split tasks
  -> classify parallel safety
  -> create minimal task briefs
  -> run parallel-safe work where possible
  -> review each task
  -> fix or reassign findings
  -> spec-drift-check
  -> review-pr whole-branch review
  -> verification gate
```

## Task splitting

Each task from the plan needs:

- Owned scope.
- Acceptance criteria.
- Dependencies.
- PR boundary membership when the plan spans multiple PRs.
- Test-strategy expectations.
- Verification command or check.
- Report-back contract.

Prefer vertical slices that can be verified independently. Avoid horizontal tasks
that force several workers to invent or coordinate the same interface.

## Parallel safety

Run tasks in parallel when:

- Write scopes are disjoint or isolated by worktree.
- Shared interfaces are already documented.
- Each worker can verify its own task.
- Merge conflict risk is low.

Run tasks sequentially when:

- Files overlap.
- A schema, API, or shared interface is changing.
- One task depends on another task's implementation.
- Requirements are still ambiguous.
- The plan has unresolved Critical or Important `review-plan` findings.
- The work would violate an explicit `pr-boundary` artifact.
- The task would skip or weaken the agreed `test-strategy` artifact.

## Review gates

Every task must pass two checks before acceptance:

1. Spec review: the task matches the source artifact and does not expand scope.
2. Quality review: the task is maintainable, idiomatic, and verified.

Critical and Important findings must be fixed or explicitly rejected with a reason.

## Completion

The workflow ends only after:

- All accepted tasks have review and verification evidence.
- The selected PR boundary is preserved or any change to it is explained.
- `spec-drift-check` reports no unresolved Critical or Important drift.
- The integrated branch receives a whole-branch review.
- Any plan-review findings are addressed or explicitly accepted as remaining risk.
- `verification-gate` confirms the final completion claim.

## Success criteria

- The plan is implemented through bounded tasks.
- Independent tasks are parallelized when safe.
- Subagents receive minimal briefs instead of full chat history.
- The final branch has a spec drift report before PR review.
- The final branch has a `review-pr` whole-branch review before readiness claims.
- The final report names changed areas, verification evidence, and remaining risks.
