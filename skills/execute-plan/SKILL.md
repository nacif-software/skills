---
name: execute-plan
description: >-
  Use when an approved or reviewed implementation plan, issue breakdown, or task
  list is ready to be implemented by one or more agents.
license: MIT
metadata:
  author: nacif
  version: "0.2.0"
---

# Execute Plan

## Purpose

Implement an approved or reviewed plan through bounded tasks, minimal context
briefs, review gates, and fresh verification. The main thread coordinates the work;
fresh worker subagents implement planned tasks whenever a delegation mechanism is
available.

## When to use

- Use after an implementation plan, task list, or issue breakdown is approved.
- Prefer a `review-plan` pass first for non-trivial, parallelized, risky, or
  multi-PR work.
- Use when work can be split into task briefs for agents or humans.
- Do not use when requirements or implementation shape are still being discovered.
  Use `design-feature` or `plan-implementation` first.
- Do not use while Critical or Important `review-plan` findings remain unresolved.

## Non-negotiables

- Do not silently implement a reviewed plan in the main thread.
- Create a visible task board before any code edits.
- Dispatch at least one worker subagent for planned implementation when the platform
  supports subagents, even if tasks must run sequentially.
- Dispatch independent tasks in parallel when conflict-safe.
- If no subagent mechanism is available, stop before code edits and say:
  `NO_DELEGATION_AVAILABLE`. Ask whether to continue in single-agent mode or switch
  to an environment that supports subagents.

## Role and model routing

Use the least expensive model that can reliably perform each role, but spend the
strongest model on decisions and review.

In Claude Code, prefer Anthropic models for planning, coordination, implementation,
requirement checks, and verification:

| Role | Default capability | Claude Code preference |
| --- | --- | --- |
| Plan author or architecture decision | strongest available | strongest Anthropic model |
| Mechanical implementer | fast | Claude Sonnet or a faster capable Anthropic model |
| Integration implementer | balanced | Claude Sonnet; escalate to strongest Anthropic model when needed |
| Requirement checker | strongest available | strongest Anthropic model with fresh context |
| Code-quality reviewer | native Codex review | `gpt-5.6-sol` only |

Model rules:

- A good plan makes most worker tasks mechanical or integration-level.
- Do not use the strongest model for a bounded mechanical task merely because it is
  available.
- Do not let a fast worker invent architecture. Return the decision to planning or
  escalate the task.
- For code-quality review, do not silently substitute another GPT model for
  `gpt-5.6-sol`.
- If the requested model is unavailable, report the downgrade before dispatch.

## Procedure

1. Read the implementation plan, test strategy, PR boundary artifact, plan review if
   present, and list the deliverables.
   - For non-trivial, delegated, parallelized, risky, or multi-PR work, stop if the
     test strategy, PR boundary, or plan review is missing and not explicitly marked
     unnecessary.
2. Discover local repo rules before editing. Look for files such as `AGENTS.md`,
   `CLAUDE.md`, `CONTRIBUTING.md`, package scripts, test config, and existing docs.
3. Create the task board from the plan. Use the platform's todo/task-board tool when
   available; otherwise show a Markdown table in the conversation.
4. Split work into tasks with ownership, acceptance criteria, and verification.
   Preserve the selected PR boundary; do not merge separate PR scopes just because
   they are convenient to implement together.
5. Classify tasks:
   - Parallel-safe: disjoint files, stable interfaces, isolated worktrees, or generated
     outputs that merge cleanly.
   - Sequential: shared files, schema/API contracts, migrations, or unclear ownership.
6. For each task, select the worker capability from the plan and create a minimal
   brief using `context-briefing`. Include only the
   relevant source artifact, plan task, test-strategy rows, PR boundary membership,
   plan-review findings, local rules, verification commands, selected model, and
   escalation conditions.
7. Dispatch worker subagents:
   - Independent tasks: dispatch together when conflict-safe.
   - Sequential tasks: dispatch one worker at a time.
   - Single planned task: dispatch one worker instead of implementing in the main
     thread when subagents are available.
8. Require each worker to self-review and report status, changed files, evidence,
   concerns, and any decision it could not safely make.
9. Route the worker status; a worker report never accepts the task by itself.
10. Run the task review state machine below. Do not mark the task done until its
    required gates pass.
11. Continue through ready tasks without asking permission between tasks. Stop only
    for an unresolved blocker, material ambiguity, or user decision.
12. Run `spec-drift-check` after all tasks land and before branch readiness review.
13. Run `review-pr` using the native Codex review policy after unresolved Critical or Important
    drift is fixed or explicitly accepted.
14. Use `verification-gate` before any completion, commit, push, or PR claim.

## Task board contract

The board must exist before edits and stay updated as work progresses.

```markdown
| ID | Task | Worker | Model | Files | Depends on | Mode | Status | Evidence | Review |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T1 | <task name> | <brief path or summary> | <model/tier> | <owned files> | <none/T#> | parallel/sequential | pending/in progress/done/blocked | <command/result> | requirement pending/quality pending/accepted |
```

Board rules:

- Every task from the implementation plan appears on the board.
- Each board row maps to one worker brief.
- Each board row records the chosen worker model or capability tier.
- Main-thread work is limited to coordination, brief writing, integration, review, and
  verification unless `NO_DELEGATION_AVAILABLE` is acknowledged.
- Status changes only after reading worker output and verification evidence.

## Worker status routing

- `DONE`: independently inspect the diff and evidence, then start the requirement gate.
- `DONE_WITH_CONCERNS`: classify each concern before review. Correctness, scope, or
  architecture concerns block acceptance.
- `NEEDS_CONTEXT`: add only the missing context and re-dispatch the same worker tier.
- `BLOCKED`: identify the cause. Supply missing context, upgrade the model when
  reasoning capacity is the problem, split an oversized task, or return a faulty plan
  for revision. Never retry unchanged.

## Task review state machine

```text
worker implementation
  -> independent requirement check
     -> missing, extra, or misunderstood scope: same worker fixes, then re-check
     -> requirement accepted
        -> task-scoped code-quality review when an isolated diff exists
           -> Critical or Important finding: same worker fixes, then re-review
           -> accepted or quality pending for integrated review
```

The requirement checker must inspect the actual code and evidence instead of trusting
the worker summary. All requirement drift blocks task acceptance. Critical and
Important quality findings block acceptance; Minor findings may be recorded for the
final review.

## Native Codex review policy

Use native Codex review for code-quality review, with `gpt-5.6-sol` as the only GPT
review model:

1. In Claude Code, prefer `/codex:review --base <ref> --wait` for the integrated
   branch only after confirming the active Codex configuration selects
   `gpt-5.6-sol`. This command may be user-only; if so, ask the user to invoke it and
   do not pretend the workflow called it. If the model cannot be confirmed, use the
   explicitly pinned CLI path below.
2. For autonomous review, run one of:

   ```bash
   codex review -c 'model="gpt-5.6-sol"' --base <ref>
   codex review -c 'model="gpt-5.6-sol"' --uncommitted
   ```

3. When the platform exposes reviewer subagents but not the command or CLI, dispatch
   a fresh reviewer with `gpt-5.6-sol`.
4. If `gpt-5.6-sol` is unavailable, report `CODEX_REVIEW_UNAVAILABLE`. Do not silently
   downgrade to another GPT model. Use an Anthropic fallback reviewer only after the
   user accepts the downgrade.

Run task-scoped native review only when the task has an isolated diff, commit, or
worktree boundary. Always run one final native Codex review over the integrated change.

## Parallelization rules

Parallelize only when both are true:

- Workers have disjoint write scopes or isolated worktrees.
- The task brief contains enough contract detail that workers do not need to invent
  shared interfaces independently.

Prefer sequential execution when tasks touch the same files, change shared public
interfaces, require migrations, or depend on a decision not yet written down. Sequential
does not mean main-thread implementation; dispatch one worker task at a time.

## Task brief checklist

- Goal and source artifact.
- Implementation plan task or issue ID.
- Owned files or modules.
- Files or areas not to touch.
- Required repo rules.
- Acceptance criteria.
- Verification commands and expected signal.
- Test-strategy rows or expectations for the task.
- PR boundary membership and excluded work.
- Relevant `review-plan` findings or accepted risks.
- Direct dependencies and sibling tasks that must not be changed.
- Worker role, selected model or capability tier, and escalation conditions.
- Report-back format.

## Common mistakes

- Dispatching agents in parallel because tasks look small, not because they are independent.
- Implementing planned tasks in the main thread while subagents are available.
- Starting edits before creating the task board.
- Treating sequential tasks as an excuse to skip worker delegation.
- Giving every task the strongest model instead of using the plan to lower execution cost.
- Retrying a blocked fast worker without adding context, splitting the task, or upgrading capability.
- Passing the entire conversation instead of a brief.
- Omitting the test-strategy rows, PR boundary, or plan-review findings from task
  briefs.
- Accepting a worker report without inspecting diff and evidence.
- Starting quality review before spec review.
- Using another GPT model when `gpt-5.6-sol` was required for native Codex review.
- Claiming `/codex:review` was invoked when the host requires the user to run it.
- Claiming completion before a whole-branch verification gate.
- Executing directly from a broad design when a concrete implementation plan is needed.
- Executing a plan with unresolved Critical or Important plan-review findings.
- Ignoring the PR boundary artifact and producing one oversized mixed branch.
- Ignoring the test strategy and adding only convenient tests.
- Skipping spec drift check because tests pass.

## Success criteria

- Each task has clear ownership, acceptance criteria, and verification.
- The task board was created before implementation and stayed current.
- Planned implementation tasks were dispatched to worker subagents when available.
- Worker models matched task complexity and were escalated only with a recorded reason.
- Parallel tasks are conflict-safe or isolated.
- Every accepted task has review evidence and verification evidence.
- The integrated change has native Codex review evidence from `gpt-5.6-sol`, or an
  explicit accepted downgrade.
- The final branch has a spec drift report.
- The final branch has a `review-pr` whole-branch review.
- The whole change passes a final verification gate.
