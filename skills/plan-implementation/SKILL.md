---
name: plan-implementation
description: >-
  Use when a design doc, PRD, issue, or approved requirements need to become a
  concrete implementation plan before coding or delegating work.
license: MIT
metadata:
  author: nacif
  version: "0.3.0"
---

# Plan Implementation

## Purpose

Turn an approved design or requirement artifact into a decision-complete build plan.
The plan should be precise enough for `execute-plan` or another agent to implement
without inventing architecture, file ownership, test strategy, task order, or PR
scope.

When model selection is available, author and review the plan with the strongest
available reasoning model. In Claude Code, prefer the strongest available Anthropic
model for this judgment-heavy work.

## When to use

- Use after `design-feature` when the user chooses to plan or implement.
- Use before dispatching subagents, creating issues, or starting non-trivial coding.
- Use when a design exists but exact files, tests, dependencies, and task order are
  not written down.
- Do not use for tiny mechanical edits with explicit files and tests.

## Procedure

1. Read the source artifact and extract goal, decisions, out-of-scope items, and
   acceptance criteria. If the source is a design that cites a `product-brief`, read
   the brief too so requirement references stay meaningful.
   - If a requirement or decision is genuinely ambiguous and no artifact settles it,
     use `interview` (focus: the specific ambiguity; stop when the plan can proceed)
     rather than guessing and encoding the guess as a task.
2. Discover repo rules and nearby implementation patterns before planning.
3. Pick test seams before task seams. Use `test-strategy` when behavior, risk, or
   verification is non-trivial.
4. Map files and responsibilities:
   - Create, modify, or delete paths.
   - What each file owns.
   - Which files must not be touched.
5. Split work into vertical tasks that each leave the project closer to working
   software. Avoid all-backend, all-frontend, all-tests task splits.
6. Mark task dependencies, parallel safety, and worker profile:
   - Parallel-safe only when write scopes are disjoint or isolated and shared
     interfaces are already specified.
   - Sequential when tasks share files, contracts, migrations, or unresolved decisions.
   - Mechanical: narrow, decision-complete work suitable for a fast model.
   - Integration: cross-file work suitable for a balanced model such as Claude Sonnet.
   - Judgment: architecture or ambiguous work that must stay with the strongest model
     or return to planning before dispatch.
7. Recommend PR shape or call `pr-boundary` when the landing shape is non-trivial:
   - One PR, stacked PRs, separate PRs, prep plus feature, migration sequence, or
     follow-up work.
   - What belongs together and what should be split.
   - Why the boundary is safe for review, deploy, and rollback.
8. Write task steps with enough detail to execute:
   - Exact files.
   - Test or verification command.
   - Expected failing signal for new tests.
   - Expected passing signal after implementation.
   - Code snippets for public interfaces, schemas, test skeletons, state machines,
     commands, or tricky logic.
9. Include implementation code only where it prevents ambiguity. Do not paste large
   obvious bodies just to look precise.
10. Self-review the plan before handoff.
11. For non-trivial, delegated, parallelized, risky, or multi-PR work, enforce the
    default pre-execution route: `test-strategy`, `pr-boundary`, `review-plan`,
    then `execute-plan`.
12. Do not run `execute-plan` until required test strategy and PR boundary artifacts
    are present or explicitly unnecessary, and no Critical or Important `review-plan`
    findings remain.
13. Offer next step: stop at plan, create or review `test-strategy`, decide
    `pr-boundary`, review with `review-plan`, split into issues, or run
    `execute-plan` after the gates are clear.

## Plan contract

```markdown
# <Feature> Implementation Plan

## Goal
<one paragraph>

## Source
- Design/PRD/issue: `<path-or-url>`

## Architecture
- <implementation approach>
- Test seam: <where behavior is verified>
- Test strategy: <path or inline summary if `test-strategy` was used>

## File Map
- Create: `<path>` - <responsibility>
- Modify: `<path>` - <responsibility>
- Do not touch: `<path>` - <reason>

## Task Graph
- Task 1: <name> - blocked by: none - parallel: no/yes, <reason> - worker: mechanical/integration/judgment
- Task 2: <name> - blocked by: Task 1 - parallel: no/yes, <reason> - worker: mechanical/integration/judgment

## PR Shape
- Recommended: one PR / stacked PRs / separate PRs / prep plus feature / migration sequence / follow-up.
- Same PR: <changes that belong together and why>
- Separate or follow-up: <changes to split and why>
- Boundary artifact: <path or inline summary if `pr-boundary` was used>

## Tasks
### Task 1: <name>

**Files**
- <paths>

**Acceptance criteria**
- <observable result>

**Worker profile**
- Tier: mechanical / integration / judgment
- Reason: <why this tier can execute without inventing decisions>
- Escalate when: <missing context, architecture choice, unexpected coupling>

**Steps**
- [ ] Write or update the focused test.
  - Run: `<command>`
  - Expected: <specific failure>
  - Contract snippet:
    ```<language>
    <test, interface, schema, or state shape>
    ```
- [ ] Implement the smallest change that satisfies the test.
- [ ] Run targeted verification.
  - Run: `<command>`
  - Expected: <specific success>
- [ ] Update docs or fixtures if required.

## Final Verification
- `<command>` should <expected result>

## Execution Gate
- Test strategy: artifact path / not needed because <reason>
- PR boundary: artifact path / one PR is safe because <reason>
- Plan review: Ready / not needed because <reason>
```

## Self-review checklist

- Every source requirement maps to at least one task.
- No placeholders remain.
- File paths are exact.
- Task dependencies are explicit.
- Parallel-safe claims explain why the tasks will not collide.
- Every task has a worker profile and escalation condition.
- Mechanical and integration workers do not need to invent architecture.
- PR shape names what stays together and what splits, or references a `pr-boundary`
  artifact.
- Tests verify behavior through useful interfaces.
- Test strategy names useful seams, expected red/green signals, and do-not-test
  choices.
- Code snippets lock contracts, not speculative implementation detail.
- `review-plan` can evaluate the plan without reading the full conversation.
- `execute-plan` can run from this plan without reading the full conversation.
- The execution gate states whether `test-strategy`, `pr-boundary`, and
  `review-plan` are complete or explicitly unnecessary.

## Common mistakes

- Writing a design summary instead of a build plan.
- Hiding decisions in vague steps such as "add validation" or "handle errors".
- Planning horizontal layers instead of vertical slices.
- Marking tasks parallel-safe before shared contracts are stable.
- Assigning a fast worker to a task that still contains design decisions.
- Spending the strongest model on mechanical edits after the plan removed ambiguity.
- Hiding refactors, migrations, cleanup, or optional polish inside the feature PR.
- Treating PR shape as a final packaging detail instead of an implementation input.
- Omitting the expected red failure for new tests.
- Saying "add tests" instead of producing a risk-based `test-strategy`.
- Treating `review-plan` as optional for delegated, parallel, risky, or multi-PR
  implementation.

## Success criteria

- The plan is decision-complete.
- A worker can implement each task from the plan plus local repo context.
- Reviewers can check spec compliance task by task.
- `review-plan` can evaluate coverage, tests, risk, parallel safety, and PR shape.
- Execution can proceed with minimal subagent briefs, not full chat history.
