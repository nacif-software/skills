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
  version: "0.2.0"
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
- Spec review and quality review each run as their own fresh reviewer dispatch,
  never as the implementer's self-report and never as the coordinator's own
  opinion of the diff.
- Quality review is always a fresh `Agent` dispatch, same as the implementer and
  spec reviewer. What differs is which agent it targets. If `execute-plan`
  designates native Codex review, the dispatched subagent's job is to locate and
  run the OpenAI Codex plugin's companion script (`execute-plan`'s Codex plugin
  review policy) and return the findings unedited — not a generic reviewer that
  skips the plugin, and not the coordinator running the review command itself
  instead of dispatching it. Only use a generic reviewer subagent when the calling
  workflow names no code-quality reviewer at all.
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
   -> DONE_WITH_CONCERNS: classify each concern first.
      -> correctness, scope, or architecture concern: treat as a fix pass —
         same implementer resolves it, then re-read status
      -> observation only (e.g. "this file is getting large"): note it and
         continue
   -> DONE, or DONE_WITH_CONCERNS with only non-blocking observations: continue
3. Dispatch spec reviewer (fresh subagent, no access to implementer's reasoning)
   Agent({ subagent_type: <named type>, prompt: <references/spec-reviewer-brief.md> })
4. Read spec reviewer verdict
   -> gaps or extra scope: same implementer fixes only that finding, go to 3
   -> spec compliant: continue
5. Dispatch quality reviewer over this task's isolated diff: a fresh `Agent`
   subagent that internally runs native Codex review per `execute-plan`'s policy
   (or a generic reviewer subagent only if the calling workflow designates none),
   passing <references/quality-reviewer-brief.md>
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
artifact only, not general code quality.

## Dispatching the quality reviewer

Like the implementer and spec reviewer, the quality reviewer is always dispatched
through a fresh `Agent` tool call. What changes is which agent it targets and what
that agent does internally — not whether it is a dispatch at all. Ask what the
calling workflow's code-quality review policy is before dispatching; do not
default to a generic reviewer when the calling workflow names a specific one.

**When the calling workflow designates native Codex review** (this is
`execute-plan`'s default in Claude Code): dispatch a fresh, Bash-capable subagent
whose only instructions are to locate the OpenAI Codex plugin's companion script
and run it against this task's isolated diff, per `execute-plan`'s Codex plugin
review policy, and return its output unedited:

```text
Agent({
  subagent_type: "general-purpose",  // Bash-capable; the review engine is the
                                     // dispatched command below, not this agent
  prompt: "Locate the OpenAI Codex plugin's companion script:\n" +
          "companion=\"$(ls -d \"$HOME\"/.claude/plugins/cache/openai-codex/codex/*/scripts/codex-companion.mjs 2>/dev/null | sort -V | tail -1)\"\n" +
          "If empty, report CODEX_PLUGIN_UNAVAILABLE and stop.\n" +
          "Otherwise run exactly:\n" +
          "node \"$companion\" adversarial-review --wait --scope working-tree \"<task acceptance criteria>\"\n" +
          "(or --base <ref-before-this-task> instead of --scope working-tree once the task's change is committed)\n" +
          "Return the command's full output verbatim as the verdict. Do not " +
          "summarize or edit it. Do not edit files.\n\n<references/quality-reviewer-brief.md>"
})
```

This is what makes "dispatch a subagent" and "use the Codex harness" the same
instruction rather than competing choices: the subagent's entire job is to run the
real review engine and hand back what it says, while still giving the review a
fresh, isolated dispatch with the same board-evidence contract as every other step
in this loop. There is no model-pinning flag on this command — the plugin's
configured backend model is the review engine.

**Only when the calling workflow designates no code-quality reviewer**, dispatch a
generic reviewer subagent instead, whose own judgment is the review:

```text
Agent({
  subagent_type: "general-purpose",  // or a project-defined reviewer agent
  prompt: "<references/quality-reviewer-brief.md>"
})
```

Quality reviewer checks maintainability, idioms, and risk, not spec compliance,
regardless of which agent performed it.

If the calling workflow also requires a separate whole-branch review after all
tasks land (for example `review-pr`'s native Codex review over the integrated
change), that requirement is unchanged by this skill — this loop's quality
reviewer step covers only the task-scoped diff.

## Templates

- `references/implementer-brief.md`
- `references/spec-reviewer-brief.md`
- `references/quality-reviewer-brief.md`

Fill in every bracketed field before dispatch. Do not send a template with
unresolved placeholders.

## Common mistakes

- Proceeding to spec review on a `DONE_WITH_CONCERNS` report without first
  classifying whether the concern is blocking (correctness, scope, architecture)
  or just an observation.
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
- Defaulting quality review to a generic reviewer subagent when the calling
  workflow designates native Codex review, silently downgrading the review engine.
- Running the native Codex review command directly in the coordinator's own shell
  instead of dispatching a fresh subagent to run it — losing the fresh-context
  isolation and board evidence every other step gets.
- Letting the dispatched Codex-review subagent summarize or edit the harness's
  output instead of returning it verbatim as the verdict.
- Skipping the task-scoped quality review because a whole-branch review will run
  later.

## Success criteria

- Every task ran through exactly one implementer subagent dispatch and a fresh
  spec reviewer dispatch.
- The quality reviewer was a fresh `Agent` dispatch; when `execute-plan` requires
  native Codex review, that subagent's job was to locate and run the OpenAI Codex
  plugin's companion script and return its findings unedited.
- Every fix loop re-ran the specific review that raised the issue, not both
  reviews, and re-reviewed the latest revision.
- The task board row carries dispatch evidence (`subagent_type` for each of the
  three dispatches, confirmed calls) and both review verdicts, not just a status
  label.
- Independent tasks ran their loops concurrently without shared write conflicts.
