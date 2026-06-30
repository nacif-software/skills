---
name: design-feature
description: >-
  Use when the user wants to design a feature, turn an idea into a spec, write a
  design doc, create an implementation plan, or optionally continue into implementation.
license: MIT
metadata:
  author: nacif
  version: "0.1.0"
---

# Design Feature

## Purpose

Turn a feature idea into a clear design artifact before implementation. The workflow
may stop at the design, continue into an implementation plan, or hand off to
`plan-implementation`.

## When to use

- Use for new features, product changes, architecture-affecting refactors, and
  unclear implementation requests.
- Use when the user says "design", "spec", "PRD", "plan this", "grill me", or
  "help me think through this".
- Do not use for small mechanical edits whose requirements and files are already
  explicit.

## Procedure

1. Discover local context before asking questions:
   - Read repo instruction files such as `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`,
     and relevant docs.
   - Inspect nearby code, tests, routes, package scripts, or schemas that define the
     current shape.
   - Summarize only the facts that affect the design.
2. Start a decision map:
   - Resolved decisions.
   - Open questions.
   - Assumptions.
   - Out-of-scope items.
3. Ask one linked question at a time. Each question must resolve a real branch in
   the decision map. Prefer a recommendation with trade-offs.
4. When enough is known, present 2-3 viable approaches and recommend one.
5. Draft the design in sections:
   - Problem and goal.
   - User-visible behavior.
   - Technical approach.
   - Interfaces, data flow, or contracts.
   - Edge cases and failure modes.
   - Test and verification strategy.
   - Out of scope.
6. Ask the user to approve or revise the design.
7. Write the design doc in the repo's preferred docs location. If no convention
   exists, use `docs/designs/YYYY-MM-DD-<feature>.md`.
8. Self-review the design for placeholders, contradictions, unresolved decisions,
   unclear acceptance criteria, and accidental scope creep.
9. Offer the next step:
   - Stop at design.
   - Create an implementation plan with `plan-implementation`.
   - Create a plan and test strategy with `test-strategy`.
   - Create a plan, test strategy, and PR shape with `pr-boundary`.
   - Create a plan, test strategy, PR shape, and review it with `review-plan`.
   - Create a plan, test strategy, PR shape, review it, and continue into
     `execute-plan`.
10. If the user chooses implementation for non-trivial work, chain through
    `plan-implementation`, `test-strategy`, `pr-boundary`, `review-plan`, and then
    `execute-plan`. Do not jump from design directly to execution.
11. Use `verification-gate` before claiming the design artifact or any chained
    artifact is complete.

## Design doc minimum

```markdown
# <Feature> Design

## Goal
<one paragraph>

## Decisions
- <decision>: <choice and reason>

## Behavior
- <observable behavior>

## Technical Approach
- <implementation shape without unnecessary code>

## Interfaces and Data
- <APIs, commands, schemas, events, or state touched>

## Verification
- <tests and manual checks>

## Out of Scope
- <explicit exclusions>
```

## Common mistakes

- Asking questions before checking facts already present in the repo.
- Asking several unrelated questions at once.
- Treating the first idea as the design without comparing approaches.
- Writing a plan with unresolved product decisions.
- Passing the whole design conversation to implementers instead of a concise plan
  and task briefs.
- Jumping from design directly to execution for non-trivial work.
- Skipping test strategy, PR boundary, or plan review when implementation will be
  delegated, parallelized, risky, or split into PRs.

## Success criteria

- The design reflects discovered repo context.
- Major decisions are explicit and approved.
- Open questions are resolved, deferred, or marked out of scope.
- The design doc can be handed off without the full conversation.
- The next-step chain names which artifacts are required before execution.
