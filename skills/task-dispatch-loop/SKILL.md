---
name: task-dispatch-loop
description: >-
  Use when execute-plan or another coordinator needs to run one plan task, or a
  batch of independent tasks, through fresh-subagent implementation and review:
  dispatch an implementer, run spec review then quality review, route fixes back
  to the same implementer, and mark the task done only once both reviews pass.
  Triggers when a coordinator reaches its per-task dispatch step, or on "implement
  this task", "run the task loop", "dispatch a worker for this task".
license: MIT
metadata:
  author: nacif
  version: "0.1.0"
---

# Task Dispatch Loop

## Purpose

Run one plan task end to end through isolated fresh subagents: implement, spec
review, quality review, fix loop, done. This skill does nothing else, so the rule
"dispatch a fresh subagent per task" never has to compete with board bookkeeping,
drift checks, or PR review for the coordinator's attention.

## When to use

- Use when a coordinator (typically `execute-plan`) has a task board and is ready
  to run one task, or a batch of independent tasks, through implementation and
  review.
- Use once per task. A batch of independent tasks runs this same loop
  concurrently, one instance per task.
- Do not use this skill to decide task splitting, dependencies, or PR boundaries —
  those come from `plan-implementation`, `pr-boundary`, and the task board built by
  the calling workflow.
- Do not use for planning-level judgment calls. If a worker needs one, stop the
  loop and escalate to the coordinator instead of letting a worker invent it.

## Non-negotiables

- The implementer runs as a fresh subagent dispatched through a literal `Agent`
  tool call with a named `subagent_type`. A brief that was drafted but never
  dispatched does not start this loop — see `context-briefing`'s dispatch contract.
- Spec review and quality review each run as their own fresh subagent dispatch,
  never as the implementer's self-report and never as the coordinator's own
  opinion of the diff.
- Spec review always runs before quality review. Do not run quality review on a
  task that has not yet passed spec review.
- A task is not done until both reviews return a passing verdict against the
  current code, not a prior revision.
- Only one implementer dispatch is active per task at a time. Fix passes are
  sequential: same implementer, one fix, then re-review.

## The loop

Run this for one task:

```text
1. Dispatch implementer
   Agent({ subagent_type: <named type>, prompt: <references/implementer-brief.md> })
2. Read implementer status
   -> NEEDS_CONTEXT: add the missing fact, redispatch the same implementer
   -> BLOCKED: change context, model, or task size, or return the task to
      planning; never redispatch unchanged
   -> DONE or DONE_WITH_CONCERNS with no blocking concerns: continue
3. Dispatch spec reviewer (fresh subagent, no access to implementer's reasoning)
   Agent({ subagent_type: <named type>, prompt: <references/spec-reviewer-brief.md> })
4. Read spec reviewer verdict
   -> gaps or extra scope: same implementer fixes only that finding, go to 3
   -> spec compliant: continue
5. Dispatch quality reviewer (fresh subagent, no access to implementer's reasoning)
   Agent({ subagent_type: <named type>, prompt: <references/quality-reviewer-brief.md> })
6. Read quality reviewer verdict
   -> Critical or Important finding: same implementer fixes only that finding, go to 5
   -> Minor only or no findings: continue
7. Record dispatch and review evidence on the coordinator's task board and mark
   the task done
8. Return control to the coordinator for the next task
```

Independent tasks run steps 1-8 concurrently, one loop instance per task. Do not
interleave steps across tasks that share files or an interface that is still
changing — run those tasks' loops one at a time instead.

## Dispatching the implementer

```text
Agent({
  subagent_type: "general-purpose",  // or a project-defined implementer agent
  prompt: "<references/implementer-brief.md, filled in via context-briefing>"
})
```

`context-briefing` owns what goes inside the prompt (role, capability tier, scope,
inputs, constraints, verification, report-back contract). This skill owns the call
itself and the loop around it.

## Dispatching reviewers

Both reviewers are fresh subagents with no access to the implementer's private
reasoning or self-review — they read the diff, the task, and the source artifact
directly, the same way a human reviewer would.

```text
Agent({
  subagent_type: "general-purpose",  // or a project-defined reviewer agent
  prompt: "<references/spec-reviewer-brief.md or references/quality-reviewer-brief.md>"
})
```

- Spec reviewer checks the change against the task's acceptance criteria and
  source artifact only, not general code quality.
- Quality reviewer checks maintainability, idioms, and risk, not spec compliance.
- If the calling workflow also requires an external reviewer for the whole branch
  (for example a `codex-review`-style gate), that requirement is unchanged by this
  skill — this loop's quality reviewer step still runs on the task-scoped diff.

## Templates

- `references/implementer-brief.md`
- `references/spec-reviewer-brief.md`
- `references/quality-reviewer-brief.md`

Fill in every bracketed field before dispatch. Do not send a template with
unresolved placeholders.

## Common mistakes

- Letting the implementer's self-review stand in for spec or quality review.
- Starting quality review before spec review has passed.
- Reviewing a revision that is not the implementer's latest fix.
- Redispatching a `BLOCKED` implementer unchanged instead of changing context,
  model, or task size.
- Running two implementer dispatches for the same task at the same time.
- Marking a task done because "the loop finished" without dispatch and review
  evidence recorded on the board.
- Giving a reviewer the implementer's chat transcript instead of just the diff and
  the task.
- Letting a fix pass touch more than the specific finding it was dispatched to fix.

## Success criteria

- Every task ran through exactly one implementer subagent dispatch, with fresh
  spec and quality review subagent dispatches.
- Every fix loop re-ran the specific review that raised the issue, not both
  reviews, and re-reviewed the latest revision.
- The task board row carries dispatch evidence (subagent_type, confirmed call) and
  both review verdicts, not just a status label.
- Independent tasks ran their loops concurrently without shared write conflicts.
