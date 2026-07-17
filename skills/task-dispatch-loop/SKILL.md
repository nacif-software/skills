---
name: task-dispatch-loop
description: >-
  Use when execute-plan or another coordinator needs to run one plan task, or a
  batch of independent tasks, through fresh-subagent implementation and spec
  review: dispatch an implementer, verify it against the task's acceptance
  criteria, route fixes back to the same implementer, and mark the task done once
  spec review passes. Triggers when a coordinator reaches its per-task dispatch
  step, or on "implement this task", "run the task loop", "dispatch a worker for
  this task".
license: MIT
metadata:
  author: nacif
  version: "0.3.0"
---

# Task Dispatch Loop

## Purpose

Run one plan task end to end through isolated fresh subagents: implement, verify
against spec, fix loop, done. This skill does nothing else, so the rule "dispatch a
fresh subagent per task" never has to compete with board bookkeeping, drift
checks, or PR review for the coordinator's attention.

This loop does not run code-quality review (Codex or otherwise). Code-quality
review runs once per PR-boundary group, via `execute-plan`'s checkpoint step and
`review-pr` — not once per task. Running Codex after every single task is what
turns an 18-task feature into 60-80 review calls and days of latency; see
`execute-plan`'s "Quality-review cadence" section for why this loop stops at spec
review.

## When to use

- Use when a coordinator (typically `execute-plan`) has a task board and is ready
  to run one task, or a batch of independent tasks, through implementation and
  spec verification.
- Use once per task. A batch of independent tasks runs this same loop
  concurrently, one instance per task.
- Do not use this skill to decide task splitting, dependencies, or PR boundaries —
  those come from `plan-implementation`, `pr-boundary`, and the task board built by
  the calling workflow.
- Do not use this skill to run code-quality review. That is a checkpoint-level
  concern owned by `execute-plan` and `review-pr`, not a per-task one.
- Do not use for planning-level judgment calls. If a worker needs one, stop the
  loop and escalate to the coordinator instead of letting a worker invent it.

## Non-negotiables

- The implementer runs as a fresh subagent dispatched through a literal `Agent`
  tool call with a named `subagent_type`. A brief that was drafted but never
  dispatched does not start this loop — see `context-briefing`'s dispatch contract.
- Spec review runs as its own fresh reviewer dispatch, never as the implementer's
  self-report and never as the coordinator's own opinion of the diff.
- A task is not done until spec review returns a passing verdict against the
  current code, not a prior revision.
- Only one implementer dispatch is active per task at a time. Fix passes are
  sequential: same implementer, one fix, then re-review.
- Do not add a code-quality or Codex dispatch back into this loop. That
  reintroduces the exact per-task review cost this design exists to avoid — see
  `execute-plan`'s checkpoint step instead.

## Model guidance

Neither dispatch in this loop needs the strongest available model:

- The implementer's model comes from the plan's worker-tier classification
  (mechanical/integration/judgment) — use the tier the plan assigned, not
  automatically the strongest model. See `execute-plan`'s Role and model routing
  table.
- The spec reviewer is a narrow, mechanical check — "does this diff satisfy these
  acceptance criteria, yes or no, what's missing or extra." Use a fast, cheap
  capable model (e.g. Claude Sonnet or faster) for it. Escalate to a stronger model
  only if the reviewer reports it cannot judge compliance from the brief alone.

## The loop

Run this for one task:

```text
1. Dispatch implementer
   Agent({ subagent_type: <named type>, prompt: <references/implementer-brief.md> })
2. Read implementer status
   -> NEEDS_CONTEXT: add the missing fact, redispatch the same implementer
   -> BLOCKED: change context, model, or task size, or return the task to
      planning; never redispatch unchanged
   -> DONE_WITH_CONCERNS: classify each concern first.
      -> correctness, scope, or architecture concern: treat as a fix pass —
         same implementer resolves it, then re-read status
      -> observation only (e.g. "this file is getting large"): note it and
         continue
   -> DONE, or DONE_WITH_CONCERNS with only non-blocking observations: continue
3. Dispatch spec reviewer (fresh subagent, no access to implementer's reasoning,
   fast/cheap model — see Model guidance)
   Agent({ subagent_type: <named type>, prompt: <references/spec-reviewer-brief.md> })
4. Read spec reviewer verdict
   -> gaps or extra scope: same implementer fixes only that finding, go to 3
   -> spec compliant: continue
5. Record dispatch and review evidence on the coordinator's task board. Mark the
   task's code-quality status "deferred to PR checkpoint" and mark the task done.
6. Return control to the coordinator for the next task
```

Independent tasks run steps 1-6 concurrently, one loop instance per task. Do not
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

## Dispatching the spec reviewer

Always a fresh subagent with no access to the implementer's private reasoning or
self-review — it reads the diff, the task, and the source artifact directly, the
same way a human reviewer would.

```text
Agent({
  subagent_type: "general-purpose",  // or a project-defined reviewer agent
  prompt: "<references/spec-reviewer-brief.md>"
})
```

Spec reviewer checks the change against the task's acceptance criteria and source
artifact only, not general code quality — code quality is checked once per PR at
the checkpoint, not here.

## Templates

- `references/implementer-brief.md`
- `references/spec-reviewer-brief.md`

Fill in every bracketed field before dispatch. Do not send a template with
unresolved placeholders. `references/quality-reviewer-brief.md` moved to
`execute-plan`'s checkpoint step — it is no longer used here.

## Common mistakes

- Proceeding past a `DONE_WITH_CONCERNS` report without first classifying whether
  the concern is blocking (correctness, scope, architecture) or just an
  observation.
- Letting the implementer's self-review stand in for spec review.
- Reviewing a revision that is not the implementer's latest fix.
- Redispatching a `BLOCKED` implementer unchanged instead of changing context,
  model, or task size.
- Running two implementer dispatches for the same task at the same time.
- Marking a task done because "the loop finished" without dispatch and review
  evidence recorded on the board.
- Giving the spec reviewer the implementer's chat transcript instead of just the
  diff and the task.
- Letting a fix pass touch more than the specific finding it was dispatched to fix.
- Adding a per-task Codex or code-quality dispatch back into this loop — that
  reintroduces the review-volume problem checkpoint-level review exists to solve.
- Using the strongest available model for the spec reviewer when a fast, cheap
  model can judge compliance from the brief.

## Success criteria

- Every task ran through exactly one implementer subagent dispatch and a fresh
  spec reviewer dispatch — two dispatches, not three.
- The spec reviewer ran on a fast/cheap model unless it explicitly needed
  escalation.
- Every fix loop re-reviewed the latest revision, not a prior one.
- The task board row carries dispatch evidence (`subagent_type` for each
  dispatch, confirmed calls), the spec-review verdict, and a code-quality status
  of "deferred to PR checkpoint."
- Independent tasks ran their loops concurrently without shared write conflicts.
- No Codex or code-quality dispatch happened inside this loop.
