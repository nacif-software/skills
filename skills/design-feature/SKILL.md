---
name: design-feature
description: >-
  Use when the user wants to design a feature, turn an idea into a spec, write a
  design doc, create an implementation plan, or optionally continue into implementation.
license: MIT
metadata:
  author: nacif
  version: "0.2.0"
---

# Design Feature

## Purpose

Turn a feature idea into a clear design artifact before implementation. The workflow
may stop at the design, continue into an implementation plan, or hand off to
`plan-implementation`.

`design-feature` is solution space: *what* to build and *how*. When a
`product-brief` exists, it supplies the problem space — operator, outcome,
requirements — and this workflow designs toward it rather than re-deriving it.

## When to use

- Use for new features, product changes, architecture-affecting refactors, and
  unclear implementation requests.
- Use when the user says "design", "spec", "PRD", "plan this", "grill me", or
  "help me think through this".
- Do not use for small mechanical edits whose requirements and files are already
  explicit.

## Graduated entry points

Start at the stage that matches what is actually unknown, not always here:

- Fuzzy product context (who is this for, what outcome) → start at `product-brief`,
  which then chains here.
- **Known problem, unknown solution → start here.**
- Known solution, needs sequencing → start at `plan-implementation`.

When a `product-brief` exists, read it first (procedure step 1) and do not
re-interview the user on problem framing it already settled.

## Procedure

1. Discover local context before asking questions:
   - Read the `product-brief` for this feature if one exists — its problem,
     operator, outcome, and requirements are the frame; do not re-derive them.
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
3. Resolve the open design decisions by questioning the user. **REQUIRED SUB-SKILL:**
   use `interview`, with:
   - Focus: the solution-space decisions in the map (approach, interfaces, edge
     cases) — not problem framing a `product-brief` already settled.
   - Stop condition: enough that the design decisions are locked; stop when a
     further answer would not change the design.
   - Already known: discovery facts and, when present, the brief.
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
<one paragraph — restate the problem and desired outcome; cite the product-brief
when one exists>

## Decisions
- <decision>: <choice and reason; reference the brief requirement it serves, e.g.
  "(R2)", when a brief exists>

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

When a `product-brief` exists, the Goal cites it and decisions reference the
requirement IDs they serve, so the design stays anchored to the agreed problem.

## Common mistakes

- Asking questions before checking facts already present in the repo or brief.
- Re-interviewing the user on problem framing a `product-brief` already settled.
- Designing a solution with no clear problem — if the problem is fuzzy, start at
  `product-brief` instead of guessing.
- Treating the first idea as the design without comparing approaches.
- Writing a plan with unresolved product decisions.
- Passing the whole design conversation to implementers instead of a concise plan
  and task briefs.
- Jumping from design directly to execution for non-trivial work.
- Skipping test strategy, PR boundary, or plan review when implementation will be
  delegated, parallelized, risky, or split into PRs.

## Success criteria

- The design reflects discovered repo context and, when present, the product brief.
- Major decisions are explicit, approved, and traceable to brief requirements when a
  brief exists.
- Open questions are resolved, deferred, or marked out of scope.
- The design doc can be handed off without the full conversation.
- The next-step chain names which artifacts are required before execution.
