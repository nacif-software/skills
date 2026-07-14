---
name: context-briefing
description: >-
  Use when delegating work to subagents, handing work to another agent, splitting
  implementation tasks, or trying to reduce prompt/context bloat.
license: MIT
metadata:
  author: nacif
  version: "0.3.0"
---

# Context Briefing

## Purpose

Keep agents focused by passing the smallest useful packet of context. Prefer durable
artifacts and narrow task briefs over full conversation history.

## When to use

- Use when dispatching a subagent, creating a handoff, splitting implementation work,
  or reviewing whether an agent has too much irrelevant context.
- Do not use when a single agent can finish a tiny task directly without delegation.

## Core rule

A brief should let the receiver succeed without letting unrelated context steer them.

Include:

- Role: implementer, requirement checker, code reviewer, or verifier.
- Capability: mechanical, integration, or judgment; include the selected model when
  the platform exposes model choice.
- Goal: one sentence with the outcome.
- Scope: exact files, modules, issue, PR, branch, or artifact to work on.
- Inputs: source artifact, relevant plan task, relevant test-strategy rows, PR
  boundary membership, accepted plan-review findings, user decisions, and required
  local rules.
- Constraints: what not to change, known risks, style rules, safety rules, sibling
  task boundaries, and PR scope exclusions.
- Verification: commands or manual checks that prove the task is complete.
- Output contract: what the receiver must report back.

Exclude:

- Full chat history.
- Other tasks unless they are direct dependencies.
- Private reasoning, discarded alternatives, and unresolved speculation.
- Large files pasted inline when paths plus search instructions are enough.

## Brief template

```markdown
## Task
<one sentence>

## Role and Capability
- Role: implementer / requirement checker / code reviewer / verifier
- Capability: mechanical / integration / judgment
- Model: <selected model or platform default>
- Escalate when: <conditions that require more context, a stronger model, or replanning>

## Context to read
- `<path-or-url>`: <why it matters>
- Plan task: <task ID or section>
- Test strategy rows: <only rows relevant to this task>
- PR boundary: <same PR / separate PR / excluded work>
- Plan review findings: <only findings relevant to this task>

## Scope
- Owns: <files/modules/artifacts>
- Do not edit: <files/modules/artifacts>

## Requirements
- <observable behavior or deliverable>
- Do not expand scope beyond <boundary or accepted task>

## Constraints
- <repo rules, safety rules, compatibility constraints>

## Verification
- Run: `<command>`
- Expected: <specific signal>

## Report back
- Status: DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT, or BLOCKED
- Changed files
- Verification evidence
- Drift concerns: missing scope, added scope, changed decisions, or none
- Concerns or follow-ups
```

## Dispatch contract

A brief is not delegation until it is delivered through an actual subagent dispatch.
Writing the brief in the conversation and then doing the work in the main thread does
not satisfy any workflow that requires delegation.

In Claude Code, dispatch means a literal `Agent` tool call that names a concrete
`subagent_type` and passes the brief as its prompt:

```text
Agent({
  subagent_type: "general-purpose",  // or a project-defined implementer agent
  prompt: "<the filled-in brief template below>"
})
```

Rules:

- Name the `subagent_type` before dispatch. "Dispatch a worker" without a concrete
  type is not an instruction the coordinator can execute.
- The brief is the entire `prompt` value of that call, not a summary of what the
  prompt will contain.
- Record the call as dispatch evidence: `subagent_type`, task ID, and confirmation
  that the Agent tool actually ran. A brief that was only drafted, not dispatched,
  must not be marked as delegated.
- Other platforms use their own subagent or task-tool primitive; the same rule
  applies: name the concrete mechanism and confirm it fired.

## Common mistakes

- Passing the whole conversation to be "safe" -> pass artifacts and decisions instead.
- Asking a subagent to rediscover known facts -> include the exact source of truth.
- Giving multiple unrelated jobs -> split the work into separate briefs.
- Omitting the output contract -> require status, files changed, evidence, and concerns.
- Omitting PR boundary or test-strategy slices -> workers cannot preserve the plan.
- Choosing a model without recording why its capability fits the task.
- Asking a fast worker to make architecture decisions that belong in the plan.
- Drafting a brief and then implementing it directly instead of making an actual
  subagent dispatch call.
- Treating "I wrote a task brief" as equivalent to "I dispatched a subagent."

## Success criteria

- The receiver can start without asking for broad background.
- The brief names exact scope, constraints, verification, and report-back format.
- Unrelated chat history and unrelated files are excluded.
- The brief carries only the artifact slices needed for the assigned task.
- The receiver knows its role, capability tier, and escalation conditions.
- Every brief has matching dispatch evidence: named `subagent_type` and a confirmed
  tool call, not just drafted text.
