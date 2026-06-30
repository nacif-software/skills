# Plan Implementation Workflow

## Purpose

`plan-implementation` is the precision layer between design and execution. A design
explains what should exist and why; an implementation plan explains how to build it,
in what order, with what tests, and with what evidence.

## Flow

```text
approved design, PRD, or issue
  -> extract requirements and decisions
  -> discover repo rules and nearby patterns
  -> choose or call test-strategy
  -> map files and responsibilities
  -> split vertical tasks
  -> mark dependencies and parallel safety
  -> propose PR boundary or call pr-boundary
  -> write task steps with verification
  -> self-review for gaps and placeholders
  -> test-strategy and pr-boundary ready or unnecessary
  -> review-plan
  -> stop, split to issues, or execute a reviewed plan
```

## What belongs in the plan

The plan should be concrete enough to delegate without extra conversation:

- Goal and source artifact.
- Architecture summary.
- Test seam.
- Test strategy artifact or summary.
- File map.
- Task graph.
- Task-by-task acceptance criteria.
- PR shape recommendation or `pr-boundary` artifact.
- Exact verification commands and expected signals.
- Code snippets where they lock important contracts.
- Final verification.

## Code snippet policy

Use code snippets when they prevent ambiguity:

- Public interfaces.
- Schema changes.
- Test skeletons.
- State machines.
- Command shapes.
- Algorithms where prose is weaker than code.

Avoid filling the plan with large obvious implementation bodies. Too much code in
the plan freezes details prematurely and makes review harder.

## Vertical task policy

Prefer tasks that create a narrow, verifiable path through the system. A useful task
should end with a behavior, interface, or artifact that can be reviewed.

Avoid plans that batch by layer:

- All models.
- All services.
- All UI.
- All tests.

Layered tasks create late integration risk and are hard to parallelize safely.

## Parallel safety

A task is parallel-safe only when:

- Its write scope is disjoint or isolated.
- Shared interfaces are already specified.
- It can verify its own slice.
- It has no hidden dependency on a sibling task's implementation choices.

If any of those are false, mark it sequential.

## Self-review

Before handoff, check:

- Every requirement maps to a task.
- Every task has exact files.
- Every new behavior has a verification path.
- Test strategy is explicit when risk or behavior is non-trivial.
- Every placeholder is removed.
- Every parallel task has a reason.
- PR shape is explicit: one PR, stacked PRs, separate PRs, prep plus feature,
  migration sequence, or follow-up work.
- The plan can feed `review-plan` without the full design conversation.
- The plan can feed `execute-plan` without the full chat history.
- For non-trivial work, `test-strategy`, `pr-boundary`, and `review-plan` are ready
  or explicitly unnecessary before execution.

## Success criteria

- The plan is decision-complete.
- Execution tasks are bounded and reviewable.
- Subagent briefs can be derived directly from tasks.
- `test-strategy` can evaluate or provide the verification matrix.
- `review-plan` can evaluate the plan without the full design conversation.
- The final verification proves the original goal, not just individual steps.
