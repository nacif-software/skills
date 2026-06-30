---
name: execute-plan
description: >-
  Use when an approved or reviewed implementation plan, issue breakdown, or task
  list is ready to be implemented by one or more agents.
license: MIT
metadata:
  author: nacif
  version: "0.1.0"
---

# Execute Plan

## Purpose

Implement an approved or reviewed plan through bounded tasks, minimal context
briefs, review gates, and fresh verification. Prefer parallel subagents only when
the tasks are independent.

## When to use

- Use after an implementation plan, task list, or issue breakdown is approved.
- Prefer a `review-plan` pass first for non-trivial, parallelized, risky, or
  multi-PR work.
- Use when work can be split into task briefs for agents or humans.
- Do not use when requirements or implementation shape are still being discovered.
  Use `design-feature` or `plan-implementation` first.
- Do not use while Critical or Important `review-plan` findings remain unresolved.

## Procedure

1. Read the implementation plan, test strategy, PR boundary artifact, plan review if
   present, and list the deliverables.
   - For non-trivial, delegated, parallelized, risky, or multi-PR work, stop if the
     test strategy, PR boundary, or plan review is missing and not explicitly marked
     unnecessary.
2. Discover local repo rules before editing. Look for files such as `AGENTS.md`,
   `CLAUDE.md`, `CONTRIBUTING.md`, package scripts, test config, and existing docs.
3. Split work into tasks with ownership, acceptance criteria, and verification.
   Preserve the selected PR boundary; do not merge separate PR scopes just because
   they are convenient to implement together.
4. Classify tasks:
   - Parallel-safe: disjoint files, stable interfaces, isolated worktrees, or generated
     outputs that merge cleanly.
   - Sequential: shared files, schema/API contracts, migrations, or unclear ownership.
5. For each task, create a minimal brief using `context-briefing`. Include only the
   relevant source artifact, plan task, test-strategy rows, PR boundary membership,
   plan-review findings, local rules, and verification commands.
6. Dispatch parallel-safe tasks together when the platform supports subagents. Do not
   dispatch tasks in parallel when they share files, unstable contracts, unresolved
   review findings, or conflicting PR boundaries.
7. Require each worker to report status, changed files, evidence, and concerns.
8. Review each task before accepting it:
   - Spec review: matches the source artifact and adds nothing unnecessary.
   - Quality review: simple, maintainable, locally idiomatic, and tested.
9. Fix or reassign any Critical or Important review finding before marking the task done.
10. Run `spec-drift-check` after all tasks land and before branch readiness review.
11. Run `review-pr` as the whole-branch review after unresolved Critical or Important
    drift is fixed or explicitly accepted.
12. Use `verification-gate` before any completion, commit, push, or PR claim.

## Parallelization rules

Parallelize only when both are true:

- Workers have disjoint write scopes or isolated worktrees.
- The task brief contains enough contract detail that workers do not need to invent
  shared interfaces independently.

Prefer sequential execution when tasks touch the same files, change shared public
interfaces, require migrations, or depend on a decision not yet written down.

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
- Report-back format.

## Common mistakes

- Dispatching agents in parallel because tasks look small, not because they are independent.
- Passing the entire conversation instead of a brief.
- Omitting the test-strategy rows, PR boundary, or plan-review findings from task
  briefs.
- Accepting a worker report without inspecting diff and evidence.
- Starting quality review before spec review.
- Claiming completion before a whole-branch verification gate.
- Executing directly from a broad design when a concrete implementation plan is needed.
- Executing a plan with unresolved Critical or Important plan-review findings.
- Ignoring the PR boundary artifact and producing one oversized mixed branch.
- Ignoring the test strategy and adding only convenient tests.
- Skipping spec drift check because tests pass.

## Success criteria

- Each task has clear ownership, acceptance criteria, and verification.
- Parallel tasks are conflict-safe or isolated.
- Every accepted task has review evidence and verification evidence.
- The final branch has a spec drift report.
- The final branch has a `review-pr` whole-branch review.
- The whole change passes a final verification gate.
