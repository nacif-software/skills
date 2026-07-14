# Subagents and Context Control

## Principle

Subagents reduce context bloat only when the coordinator gives them bounded work.
Parallelism is useful when tasks are independent; it is dangerous when workers must
invent shared contracts at the same time.

## Coordinator responsibilities

The coordinator keeps:

- Full user conversation.
- Design doc and decision map.
- Implementation plan and task graph.
- Visible task board.
- Test strategy, PR boundary, plan review, and spec drift state.
- Integration responsibility.

Workers receive:

- One task.
- Required source artifacts.
- Relevant test-strategy rows, PR boundary membership, and plan-review findings.
- Local rules relevant to that task.
- Exact scope.
- Acceptance criteria.
- Verification commands.
- Output contract.
- Selected model or capability tier and escalation conditions.

The coordinator should not implement planned tasks in the main thread while subagents
are available. Main-thread work is coordination, brief writing, integration, review,
and final verification.

## Parallelization checklist

Parallelize a task only when all are true:

- The write scope is disjoint or the worker has an isolated worktree.
- Shared interfaces are already designed.
- The task has clear acceptance criteria.
- The worker can verify its slice without relying on unfinished sibling tasks.
- Merge conflict risk is low and understood.

Run sequentially when any are true:

- Two tasks edit the same file or same generated artifact.
- A schema, API, or public interface is still changing.
- One task depends on another task's implementation details.
- The correct behavior is still being decided.

## Worker statuses

Workers must report one of:

- `DONE`: completed as requested.
- `DONE_WITH_CONCERNS`: completed, but with risks or doubts.
- `NEEDS_CONTEXT`: cannot proceed without a missing fact or artifact.
- `BLOCKED`: cannot complete with current scope or environment.

The coordinator must not ignore `NEEDS_CONTEXT` or `BLOCKED`. Change the brief,
scope, model, or task split before retrying.

## Review loop

Every implementation task needs review before acceptance:

1. Spec review first.
2. Quality review second.
3. Fix Critical and Important findings.
4. Re-review changed areas.
5. Mark complete only after verification evidence is read.

## Dispatch graph

```text
reviewed plan
  -> execute-plan coordinator
     -> visible task board
     -> context-briefing for each task
        -> parallel-safe worker tasks
        -> sequential worker tasks, one at a time
     -> task review and integration
     -> spec-drift-check
     -> review-pr
     -> verification-gate
```

Workers do not choose the graph. The coordinator owns dispatch order, cross-task
integration, drift handling, review, and final verification.

## Model routing

In Claude Code, prefer Anthropic models for coordinator and worker roles:

- Strongest available Anthropic model for planning, architecture, and plan review.
- Claude Sonnet for bounded implementation and integration work.
- Faster Anthropic models only for narrow mechanical work with cheap verification.
- Native Codex review with `gpt-5.6-sol` for code-quality review.

Upgrade a worker only when reasoning capacity is the blocker. Add missing context when
context is the blocker, and split the task when size is the blocker.

## Dispatch call contract

A worker brief is not delegation until an actual subagent dispatch call fires with
that brief as its input. Drafting the brief, updating the task board, or reasoning
about what a worker would do are not substitutes.

In Claude Code, dispatch means a literal `Agent` tool call with a named
`subagent_type`:

```text
Agent({
  subagent_type: "general-purpose",  // or a project-defined implementer agent
  prompt: "<the minimal task brief below>"
})
```

Record, per task: the `subagent_type` used and confirmation that the call fired.
A task cannot be marked in progress or done without this evidence. Other platforms
use their own subagent primitive; the same rule applies — name the concrete
mechanism and confirm it fired.

## Minimal task brief

```markdown
## Task
<one sentence>

## Source artifact
- `<path>`: <design, plan, issue, or PR>
- Plan task: <task ID or section>
- Test strategy rows: <only rows relevant to this task>
- PR boundary: <same PR / separate PR / excluded work>
- Plan review findings: <only relevant findings or accepted risks>

## Scope
- Owns: <files/modules>
- Do not touch: <files/modules>

## Requirements
- <acceptance criteria>
- Do not expand beyond <task or PR boundary>

## Local rules
- <repo instructions that matter>

## Verification
- `<command>` should <expected result>

## Report back
- Status
- Changed files
- Verification evidence
- Drift concerns
- Concerns
```

## Anti-patterns

- Passing a full transcript to every worker.
- Dispatching parallel tasks before shared contracts are stable.
- Implementing plan tasks in the coordinator thread while worker delegation is
  available.
- Marking a task dispatched because a brief was written, without an actual subagent
  dispatch call firing.
- Asking workers to "figure out the architecture."
- Treating worker self-review as the only review.
- Letting a worker silently expand scope.
- Dispatching without the relevant test-strategy rows, PR boundary, or plan-review
  findings.
