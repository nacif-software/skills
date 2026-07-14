# Execute Plan Workflow

## Purpose

`execute-plan` turns an approved implementation plan, task list, or issue breakdown
into implemented work. It should not replace `plan-implementation` or `review-plan`
for non-trivial work; execution depends on a concrete, reviewed plan.

The coordinator should not silently implement the plan in the main thread. A visible
task board comes first, then worker subagents receive focused task briefs whenever
the platform supports delegation. The per-task implement/review/fix loop is not
re-implemented here — `task-dispatch-loop` owns it, so that rule never has to
compete with board bookkeeping, drift checks, or PR review for the coordinator's
attention.

In Claude Code, prefer Anthropic models for planning and implementation. Use the
strongest available Anthropic model for plan-level judgment, Claude Sonnet for most
bounded workers, and native Codex review with `gpt-5.6-sol` for code-quality review.

## Flow

```text
reviewed implementation plan
  -> read test strategy artifact when present
  -> read PR boundary artifact when present
  -> discover repository rules
  -> create task board
  -> split tasks
  -> classify parallel safety
  -> create minimal task briefs
  -> task-dispatch-loop, in parallel or sequentially per task
  -> read back dispatch evidence and review verdicts
  -> fix or reassign findings that task-dispatch-loop escalated
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

## Task board

Before edits, create a visible task board with:

- Task ID and task name.
- Worker brief summary or path.
- Owned files.
- Dependencies.
- Parallel or sequential mode.
- Dispatch evidence: the concrete subagent mechanism used and confirmation it fired.
- Worker status.
- Verification evidence.
- Review status.
- Worker model or capability tier.

Every implementation-plan task should map to one board row and one worker brief.
Sequential tasks still use workers when subagents are available; they just run one at
a time. A brief that was drafted but never sent through an actual dispatch call is not
delegation — see `docs/subagents.md` for the dispatch call contract.

## Worker and review loop

`task-dispatch-loop` runs each task through implementer dispatch, spec review,
quality review, and the fix/re-review loop between them. Worker status routes the
next action inside that loop; it never accepts the task by itself. That loop adds
context for `NEEDS_CONTEXT`, upgrades only when capability is the blocker, splits
oversized tasks, and escalates faulty plan decisions back to this coordinator
instead of guessing.

The integrated change always receives native Codex review with `gpt-5.6-sol`; in
Claude Code, prefer `/codex:review --base <ref> --wait` only when the active Codex
configuration confirms that model, and use the explicitly pinned `codex review` CLI
fallback otherwise.

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

If no subagent mechanism exists, the coordinator should stop before edits, report
`NO_DELEGATION_AVAILABLE`, and ask whether to continue in single-agent mode.

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
- The task board is visible before code edits.
- Independent tasks are parallelized when safe.
- Sequential tasks still receive focused worker briefs when subagents are available.
- Subagents receive minimal briefs instead of full chat history.
- The final branch has a spec drift report before PR review.
- The final branch has a `review-pr` whole-branch review before readiness claims.
- The final report names changed areas, verification evidence, and remaining risks.
