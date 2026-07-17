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

Per-task review and checkpoint review are two different loops at two different
granularities — do not collapse them back into one.

**Per task**, inside `task-dispatch-loop`:

1. Spec review.
2. Fix gaps or extra scope — same implementer, one fix at a time.
3. Re-review with a fresh spec reviewer dispatch.
4. Mark spec-approved; code-quality review is deferred to the task's PR-boundary
   group checkpoint, not run here.

**Per PR-boundary group**, at `execute-plan`'s checkpoint (see decision 0008 for
why this is batched instead of per-task):

1. Confirm every task in the group is spec-approved.
2. One Codex plugin review over the group's whole accumulated diff — skip this
   step entirely for mechanical-only, low-risk groups; rely on the final
   whole-branch pass instead.
3. Collect every finding from that single pass; fix all of them, then one
   re-review of the group — not one review per finding.
4. Mark complete only after verification evidence is read.

## Dispatch graph

```text
reviewed plan
  -> execute-plan coordinator
     -> visible task board
     -> context-briefing for each task
        -> task-dispatch-loop, parallel-safe tasks together
        -> task-dispatch-loop, sequential tasks one at a time
     -> board update from task-dispatch-loop's dispatch and spec-review evidence
     -> checkpoint Codex review, once per PR-boundary group
     -> spec-drift-check
     -> review-pr
     -> verification-gate
```

Workers do not choose the graph. The coordinator owns dispatch order, cross-task
integration, drift handling, review, and final verification. `task-dispatch-loop`
owns what happens inside one task: implementer dispatch, spec review, and the fix
loop between them — see "Review loop" above. `execute-plan` owns the checkpoint:
when it runs, whether it is tier-gated away, and how its findings route back to
the owning tasks' implementers.

## Model routing

In Claude Code, prefer Anthropic models for coordinator and worker roles:

- Strongest available Anthropic model for planning, architecture, and plan review.
- Claude Sonnet for bounded implementation and integration work, and for the
  per-task spec reviewer — it is a narrow compliance check, not a judgment call.
- Faster Anthropic models only for narrow mechanical work with cheap verification.
- Native Codex review through the OpenAI Codex plugin's companion script,
  dispatched as a fresh subagent, for code-quality review — once per PR-boundary
  group, not once per task. The dispatching subagent does no reasoning of its own
  (it runs one command and relays the output), so give it the fastest/cheapest
  available model regardless of the task's own tier.

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
