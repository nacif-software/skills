---
name: execute-plan
description: >-
  Use when an approved or reviewed implementation plan, issue breakdown, or task
  list is ready to be implemented by one or more agents.
license: MIT
metadata:
  author: nacif
  version: "0.5.0"
---

# Execute Plan

## Purpose

Coordinate an approved or reviewed plan through bounded tasks, minimal context
briefs, review gates, and fresh verification. This skill owns the task board,
task splitting, PR boundary, spec drift, whole-branch review, and the final
verification gate. It does not implement tasks itself and does not run the
per-task implement/review loop directly — that loop is `task-dispatch-loop`.

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
- **REQUIRED SUB-SKILL:** Use `task-dispatch-loop` to run every task's
  implement/spec-review/quality-review/fix loop. Do not re-implement that loop
  inline in this skill's procedure.
- Dispatch at least one worker subagent for planned implementation when the platform
  supports subagents, even if tasks must run sequentially.
- Dispatch independent tasks in parallel when conflict-safe.
- A task board row is not delegation until `task-dispatch-loop` reports back an
  actual dispatch: a fired `Agent` tool call with a named `subagent_type`, not a
  drafted brief. See `context-briefing`'s dispatch contract for the call shape.
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
| Code-quality reviewer | native Codex review via the OpenAI Codex plugin | plugin-managed model — no per-call override exists |

Model rules:

- A good plan makes most worker tasks mechanical or integration-level.
- Do not use the strongest model for a bounded mechanical task merely because it is
  available.
- Do not let a fast worker invent architecture. Return the decision to planning or
  escalate the task.
- For code-quality review, do not substitute a generic Claude reviewer, a raw
  `codex` CLI call, or an invented model-override flag for the installed Codex
  plugin's own review command. See "Codex plugin review policy" below.
- If the plugin is unavailable, report the downgrade before dispatch.

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
7. Run `task-dispatch-loop` for each task:
   - Independent tasks: start their loops together when conflict-safe.
   - Sequential tasks: run one task's loop to completion before starting the next.
   - Single planned task: still run it through `task-dispatch-loop` instead of
     implementing in the main thread when subagents are available.
8. Read what `task-dispatch-loop` reports back for each task: dispatch evidence
   (`subagent_type`, confirmed call), the implementer's final status, and both
   review verdicts. Do not mark a board row done on a status label alone.
9. Continue through ready tasks without asking permission between tasks. Stop only
   for an unresolved blocker, material ambiguity, or user decision that
   `task-dispatch-loop` escalated back.
10. Run `spec-drift-check` after all tasks land and before branch readiness review.
11. Run `review-pr` using the native Codex review policy after unresolved Critical or Important
    drift is fixed or explicitly accepted.
12. Use `verification-gate` before any completion, commit, push, or PR claim.

## Task board contract

The board must exist before edits and stay updated as work progresses.

```markdown
| ID | Task | Worker | Model | Files | Depends on | Mode | Dispatch | Status | Evidence | Review |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T1 | <task name> | <brief path or summary> | <model/tier> | <owned files> | <none/T#> | parallel/sequential | <subagent_type, confirmed fired> | pending/in progress/done/blocked | <command/result> | requirement pending/quality pending/accepted |
```

Board rules:

- Every task from the implementation plan appears on the board.
- Each board row maps to one worker brief.
- Each board row records the chosen worker model or capability tier.
- Each board row's Dispatch column records the `subagent_type` used and confirms an
  actual `Agent` tool call fired for that task. A row cannot move past `pending`
  without this.
- Main-thread work is limited to coordination, brief writing, integration, review, and
  verification unless `NO_DELEGATION_AVAILABLE` is acknowledged.
- Status changes only after reading worker output and verification evidence.

## Worker status and per-task review

`task-dispatch-loop` owns the implementer dispatch, worker status routing
(`DONE` / `DONE_WITH_CONCERNS` / `NEEDS_CONTEXT` / `BLOCKED`), the spec-review-then-
quality-review order, and the fix/re-review loop for each task. This skill's job is
to read back what that loop reports — dispatch evidence and both review verdicts —
and decide whether the task board row can move to done, not to re-run that logic
here. If `task-dispatch-loop` escalates a blocker it could not resolve (a faulty
plan assumption, a missing decision, an unavailable model), treat it the same as
any other blocked task: fix the plan, supply the missing decision, or ask the user.

## Codex plugin review policy

Code-quality review runs through the official OpenAI Codex plugin for Claude Code
([openai/codex-plugin-cc](https://github.com/openai/codex-plugin-cc)) — the same
plugin `review-and-wrap-up-pr` uses. Not a bare `codex` CLI call, not an invented
`-c 'model="..."'` override (no such flag exists on this transport), and not a
generic Claude reviewer's own opinion standing in for it.

**Prerequisite:** the plugin is installed and authenticated. Locate its runtime
once per session:

```bash
companion="$(ls -d "$HOME"/.claude/plugins/cache/openai-codex/codex/*/scripts/codex-companion.mjs 2>/dev/null | sort -V | tail -1)"
```

If nothing is found, report `CODEX_PLUGIN_UNAVAILABLE` and stop before a readiness
claim. Have the user install it (`/plugin marketplace add openai/codex-plugin-cc`,
then `/plugin install codex@openai-codex`) rather than falling back to a raw
`codex` CLI call or a generic reviewer. Setup or auth errors route to
`/codex:setup` — don't improvise an alternate auth flow.

**Dispatch, never run inline.** A fresh `Agent` subagent's only job is to locate
the companion script and run it — this is what makes "dispatch a subagent" and
"use the Codex harness" the same instruction, not competing ones:

```bash
node "$companion" adversarial-review --wait --base <ref> "<review brief / focus text>"
# or, for uncommitted work:
node "$companion" adversarial-review --wait --scope working-tree "<review brief>"
```

Use `adversarial-review`, not plain `review` — only `adversarial-review` accepts
focus text, and every review dispatched from this workflow carries a brief (task
acceptance criteria, source intent, or PR context). The dispatched subagent
returns the report verbatim as the verdict; it does not summarize or edit it.

There is no model-pinning flag on `review`/`adversarial-review` — only the
companion's separate `task` command exposes `--model`. The plugin's configured
backend model is the review engine for every call on this transport; do not
invent a per-call override.

If the plugin is unavailable, report `CODEX_PLUGIN_UNAVAILABLE`. Use an
Anthropic fallback reviewer only after the user accepts that downgrade.

Run task-scoped review only when the task has an isolated diff, commit, or
worktree boundary. `task-dispatch-loop` is what actually invokes this policy per
task, as its quality-review step — it must dispatch the review this way whenever
this policy applies; it must not substitute a generic reviewer that skips the
Codex harness, and it must not run the command directly instead of dispatching
it. Always run one final Codex plugin review over the integrated change via
`review-pr`.

## Parallelization rules

Parallelize only when both are true:

- Workers have disjoint write scopes or isolated worktrees.
- The task brief contains enough contract detail that workers do not need to invent
  shared interfaces independently.

Prefer sequential execution when tasks touch the same files, change shared public
interfaces, require migrations, or depend on a decision not yet written down. Sequential
does not mean main-thread implementation; run one task's `task-dispatch-loop` at a
time instead.

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
- Re-implementing the dispatch/review/fix loop inline instead of using
  `task-dispatch-loop`.
- Marking a board row done because `task-dispatch-loop` returned, without reading
  its dispatch evidence and review verdicts.
- Starting edits before creating the task board.
- Treating sequential tasks as an excuse to skip worker delegation.
- Giving every task the strongest model instead of using the plan to lower execution cost.
- Passing the entire conversation instead of a brief.
- Omitting the test-strategy rows, PR boundary, or plan-review findings from task
  briefs.
- Using a raw `codex` CLI call or an invented model-override flag instead of the
  installed Codex plugin's companion script.
- Claiming a Codex plugin review ran without an actual dispatched subagent call
  that located and ran the companion script.
- Claiming completion before a whole-branch verification gate.
- Executing directly from a broad design when a concrete implementation plan is needed.
- Executing a plan with unresolved Critical or Important plan-review findings.
- Ignoring the PR boundary artifact and producing one oversized mixed branch.
- Ignoring the test strategy and adding only convenient tests.
- Skipping spec drift check because tests pass.

## Success criteria

- Each task has clear ownership, acceptance criteria, and verification.
- The task board was created before implementation and stayed current.
- Every planned task ran through `task-dispatch-loop` rather than being
  implemented inline.
- Every board row carries the `subagent_type` and confirmation that the `Agent`
  tool call actually fired, plus both review verdicts from `task-dispatch-loop`.
- Worker models matched task complexity and were escalated only with a recorded reason.
- Parallel tasks are conflict-safe or isolated.
- The integrated change has Codex plugin review evidence (dispatched subagent,
  companion script transport, target, verdict), or an explicit accepted downgrade.
- The final branch has a spec drift report.
- The final branch has a `review-pr` whole-branch review.
- The whole change passes a final verification gate.
