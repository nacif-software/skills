---
name: execute-plan
description: >-
  Use when an approved or reviewed implementation plan, issue breakdown, or task
  list is ready to be implemented by one or more agents.
license: MIT
metadata:
  author: nacif
  version: "0.6.0"
---

# Execute Plan

## Purpose

Coordinate an approved or reviewed plan through bounded tasks, minimal context
briefs, review gates, and fresh verification. This skill owns the task board,
task splitting, PR boundary, spec drift, checkpoint and whole-branch code-quality
review, and the final verification gate. It does not implement tasks itself and
does not run the per-task implement/spec-review loop directly — that loop is
`task-dispatch-loop`.

Code-quality review (native Codex review) runs **once per PR-boundary group**, not
once per task. Running it after every task turns an 18-task plan into 60-80 review
calls and days of latency for no proportional safety gain; see "Quality-review
cadence" below.

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
  implement/spec-review/fix loop. Do not re-implement that loop inline in this
  skill's procedure, and do not add code-quality review back into it — that
  belongs to this skill's checkpoint step, not the per-task loop.
- Run one code-quality (Codex plugin) review per PR-boundary group, at the point
  that group's tasks all pass spec review — not once per task.
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
| Spec reviewer (per task, via `task-dispatch-loop`) | fast | Claude Sonnet or a faster capable Anthropic model |
| Requirement checker | strongest available | strongest Anthropic model with fresh context |
| Codex-dispatch subagent (per checkpoint) | no reasoning needed | fastest/cheapest available model — its only job is to run one command and relay output verbatim |
| Code-quality reviewer (once per PR-boundary group) | native Codex review via the OpenAI Codex plugin | plugin-managed model — no per-call override exists |

Model rules:

- A good plan makes most worker tasks mechanical or integration-level.
- Do not use the strongest model for a bounded mechanical task merely because it is
  available.
- Do not let a fast worker invent architecture. Return the decision to planning or
  escalate the task.
- Do not use the strongest model for the spec reviewer or the Codex-dispatch
  subagent. Neither makes an architecture decision: the spec reviewer checks a
  diff against acceptance criteria, and the Codex-dispatch subagent only shells
  out to a command and returns its output — spend tokens on the plan and the
  requirement checker, not on these two.
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
   - `task-dispatch-loop` covers implementation and spec review only. It does not
     run code-quality review.
8. Read what `task-dispatch-loop` reports back for each task: dispatch evidence
   (`subagent_type`, confirmed call) and the spec-review verdict. Do not mark a
   board row done on a status label alone.
9. Continue through ready tasks without asking permission between tasks. Stop only
   for an unresolved blocker, material ambiguity, or user decision that
   `task-dispatch-loop` escalated back.
10. When every task in a PR-boundary group has passed spec review, run that
    group's checkpoint under "Quality-review cadence" below before moving to the
    next group or, for the last group, before branch readiness review.
11. Run `spec-drift-check` for each group's scope once its checkpoint clears, and
    again for the whole branch before the final `review-pr` pass.
12. Run `review-pr` using the native Codex review policy for each PR-boundary
    group's own PR when that group is ready, and once more for the whole branch
    after unresolved Critical or Important drift is fixed or explicitly accepted.
13. Use `verification-gate` before any completion, commit, push, or PR claim.

## Task board contract

The board must exist before edits and stay updated as work progresses.

```markdown
| ID | Task | Worker | Model | Files | Depends on | PR group | Mode | Dispatch | Status | Spec review | Quality review |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T1 | <task name> | <brief path or summary> | <model/tier> | <owned files> | <none/T#> | <group id> | parallel/sequential | <subagent_type, confirmed fired> | pending/in progress/done/blocked | pending/passed | deferred to checkpoint / <checkpoint id> passed / skipped, low-risk |
```

Board rules:

- Every task from the implementation plan appears on the board.
- Each board row maps to one worker brief.
- Each board row records the chosen worker model or capability tier and its
  PR-boundary group.
- Each board row's Dispatch column records the `subagent_type` used and confirms an
  actual `Agent` tool call fired for that task. A row cannot move past `pending`
  without this.
- The Quality review column starts as "deferred to checkpoint" for every task and
  only changes once that task's PR-boundary group's checkpoint runs (see
  "Quality-review cadence"). It never gets Codex evidence from a per-task dispatch.
- Main-thread work is limited to coordination, brief writing, integration, review, and
  verification unless `NO_DELEGATION_AVAILABLE` is acknowledged.
- Status changes only after reading worker output and verification evidence.

## Worker status and per-task review

`task-dispatch-loop` owns the implementer dispatch, worker status routing
(`DONE` / `DONE_WITH_CONCERNS` / `NEEDS_CONTEXT` / `BLOCKED`), and the spec-review
fix/re-review loop for each task. This skill's job is to read back what that loop
reports — dispatch evidence and the spec-review verdict — and decide whether the
task board row can move to done, not to re-run that logic here. If
`task-dispatch-loop` escalates a blocker it could not resolve (a faulty plan
assumption, a missing decision, an unavailable model), treat it the same as any
other blocked task: fix the plan, supply the missing decision, or ask the user.

## Quality-review cadence

Code-quality review is a checkpoint concern, not a per-task one. Run it once per
PR-boundary group, when every task in that group has passed spec review — never
inside `task-dispatch-loop`, and never once per task.

**Why:** a task-scoped Codex dispatch per task, with a fix-and-re-review cycle per
individual finding, turns a plan with N tasks into roughly 2-4×N Codex calls. For
an 18-task feature that is 40-80 calls, and each one takes real wall-clock minutes
— the difference between a same-day feature and one that spans days. Batching to
one pass per PR-boundary group, with all findings from that pass fixed together
before a single re-review, cuts this to roughly 1-2 calls per group.

**Tier gating — skip the checkpoint entirely when it is not needed:**

- If every task in the group is `mechanical` tier (per `plan-implementation`'s
  worker-tier classification) and none touches a shared interface, migration,
  auth/security path, or other risk area named in `test-strategy`, skip this
  group's checkpoint. Record on the board: "Checkpoint skipped: group is
  mechanical/low-risk; quality-reviewed only by the final whole-branch
  `review-pr` pass." This is a recorded decision, not a silent omission — the
  group is still quality-reviewed once, at the final whole-branch pass.
- If the group contains any `integration` or `judgment` tier task, or touches a
  risk area named above, run the checkpoint.
- A plan with a single PR-boundary group (the common case — most features land as
  one PR) has exactly one checkpoint, which is the same pass `review-pr` already
  runs at the end. Do not run a redundant mid-flight checkpoint for a single-PR
  plan; let the final `review-pr` pass be the one and only Codex review.
- A plan with multiple PR-boundary groups (stacked or separate PRs) runs one
  checkpoint per group, at the point that group's PR is ready — not just once at
  the very end of the whole plan.

**When a checkpoint runs:**

1. Confirm every task in the group shows spec review "passed" on the board.
2. Build one checkpoint brief from `references/quality-reviewer-brief.md`, scoped
   to the group's accumulated diff (not one task), listing every task ID it
   covers.
3. Dispatch it via the Codex plugin review policy below — one `adversarial-review`
   call over the group's diff, with the checkpoint brief as focus text.
4. Read all findings from that single pass together. Route each finding to the
   task ID it names; if several tasks in the group need fixes, dispatch each
   owning task's implementer once, in parallel if their fixes are conflict-safe.
5. After all fixes land, run exactly one re-review of the group's diff — not one
   re-review per finding. Repeat steps 4-5 only if the re-review surfaces new
   Critical/Important findings.
6. Once no Critical or Important findings remain, mark every task in the group
   "quality review: `<checkpoint id>` passed" on the board.

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

Dispatch this policy from the checkpoint step above, scoped to a PR-boundary
group's accumulated diff — never from inside `task-dispatch-loop`, and never once
per task. `task-dispatch-loop` does not invoke this policy at all. Always run one
final Codex plugin review over the whole integrated branch via `review-pr`, in
addition to any interim checkpoints for earlier PR-boundary groups.

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
- Re-implementing the dispatch/spec-review/fix loop inline instead of using
  `task-dispatch-loop`.
- Adding a code-quality or Codex dispatch back into `task-dispatch-loop` instead of
  running it once per PR-boundary group at the checkpoint.
- Running a checkpoint after every task instead of after every PR-boundary group —
  this is the exact review-volume problem checkpointing exists to avoid.
- Fixing checkpoint findings one at a time with a re-review after each, instead of
  batching all findings from one pass into one fix round and one re-review.
- Skipping a checkpoint for a group that contains an integration/judgment task or a
  named risk area, or skipping it silently instead of recording the skip decision.
- Marking a board row done because `task-dispatch-loop` returned, without reading
  its dispatch evidence and spec-review verdict.
- Starting edits before creating the task board.
- Treating sequential tasks as an excuse to skip worker delegation.
- Giving every task the strongest model instead of using the plan to lower
  execution cost, or using the strongest model for the spec reviewer or the
  Codex-dispatch subagent, which need none of that reasoning capacity.
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
- Every planned task ran through `task-dispatch-loop` (implement + spec review)
  rather than being implemented inline.
- Every board row carries the `subagent_type` and confirmation that the `Agent`
  tool call actually fired, plus the spec-review verdict from `task-dispatch-loop`.
- Code-quality review ran once per PR-boundary group, not once per task, with a
  recorded reason when a group's checkpoint was tier-gated as unnecessary.
- Each checkpoint batched its findings into one fix round and one re-review.
- Worker models matched task complexity and were escalated only with a recorded
  reason; the spec reviewer and Codex-dispatch subagent used fast/cheap models.
- Parallel tasks are conflict-safe or isolated.
- The integrated change has Codex plugin review evidence (dispatched subagent,
  companion script transport, target, verdict) from at least the final
  whole-branch pass, or an explicit accepted downgrade.
- The final branch has a spec drift report.
- The final branch has a `review-pr` whole-branch review.
- The whole change passes a final verification gate.
