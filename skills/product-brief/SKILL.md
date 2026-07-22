---
name: product-brief
description: >-
  Use before design when a net-new capability's product context is fuzzy — who the
  operator is, the job they are doing, the outcome that counts as success, how it
  relates to existing features. Produces a durable product brief that design-feature
  consumes. Triggers on "what should we build", "frame this feature", "write a
  product brief / PRD", "who is this for", or a feature request with no clear
  problem statement.
license: MIT
metadata:
  author: nacif
  version: "0.1.0"
---

# Product Brief

## Purpose

Frame the problem before anyone designs the solution. `product-brief` captures
product/problem context — operator, job-to-be-done, desired outcome, numbered
requirements, relation to existing features — so `design-feature` designs toward
the right thing instead of producing a technically coherent solution aimed at the
wrong goal.

This is problem space, not solution space. It says *why*, *for whom*, and *what
outcome* — never *how*. The "how" is `design-feature`'s job, and putting it here
freezes solution decisions before the problem is even agreed.

## When to use

`product-brief` is the leftmost, most optional entry point. The pipeline has
graduated entry points — start at the stage that matches how much is actually
unknown:

- **Net-new capability, fuzzy product context → start here.** The problem, operator,
  or success signal is not yet pinned down.
- Known problem, unknown solution → skip this; start at `design-feature`.
- Known solution, needs sequencing → skip both; start at `plan-implementation`.
- Known plan → `execute-plan`.

Do not write a brief for bugfixes, refactors, mechanical edits, or changes to
well-understood existing behavior. A brief that restates an obvious problem is
overhead nobody maintains.

## Minimality test

Every field must earn its place: **would a different answer here change the design
or the plan?** If not, cut it. A brief is not a PRD template to fill top to bottom;
it is the smallest set of product facts that steer downstream decisions. Prefer a
half-page brief that changes the design over a two-page brief that documents the
obvious.

## Procedure

1. Discover existing product context before asking anything:
   - Prior briefs, designs, PRDs, or specs in the repo's docs location.
   - The existing product surface near this change — features, flows, or modules the
     new capability will sit next to.
   - Repo instruction files (`AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`) for product
     vocabulary and naming already in use.
   - Summarize only the facts that shape the brief.
2. Interview the user on what discovery cannot answer. **REQUIRED SUB-SKILL:** use
   `interview`, with:
   - Focus: the operator and their job, the desired outcome, requirements, and
     relation to existing features.
   - Stop condition: enough that `design-feature` could start without guessing the
     problem, the operator, or what success means. Not every conceivable product
     question.
   - Already known: everything discovery established, so it is never re-asked.
3. Draft the brief in the contract below. Number the requirements (R1, R2, …) so
   design and later reviews can reference them precisely.
4. Fill "Relation to existing features" from what the user supplied plus what
   discovery found. Mark genuinely unknown relationships as open rather than
   inventing them — product relationships often are not in the repo.
5. Self-review against the minimality test: cut any field whose answer would not
   change the design or plan; confirm no solution/"how" detail leaked in; confirm
   every requirement is observable and testable, not a vague aspiration.
6. Ask the user to approve or revise the brief.
7. Write the brief to the repo's docs location. If no convention exists, use
   `docs/briefs/YYYY-MM-DD-<feature>.md`.
8. Offer the next step:
   - Stop at the brief.
   - Continue into `design-feature`, which consumes this brief.
9. Use `verification-gate` before claiming the brief is complete.

## Brief contract

```markdown
# <Feature> Product Brief

## Problem
<the job-to-be-done: what the operator is trying to accomplish and why it is hard
or unmet today — one short paragraph>

## Operator and use case
- Operator: <who they are — role, not a name>
- Situation: <when and where they hit this>
- Today: <what they do now, and the pain in it>

## Desired outcome
- <what "this worked" looks like for the operator or the business — a signal, not a
  feature list>

## Requirements
- R1: <observable, testable requirement>
- R2: <observable, testable requirement>

## Relation to existing features
- Depends on / extends: <feature, and how>
- Overlaps or conflicts with: <feature, and the tension>
- Unknown: <relationship not yet established — resolve during design>

## Constraints
- <product-level constraint: timing, must-not-disrupt flow, compliance — not
  technical constraints, which belong in design>

## Out of scope
- <explicitly excluded from this capability, and why>
```

## Handoff to design

`design-feature` consumes this brief: its Goal restates the brief's problem and
desired outcome, and its decisions should be traceable to the brief's requirements.
The brief travels as a durable artifact — `design-feature` reads it, it does not
re-interview the user on problem framing already settled here.

## Common mistakes

- Writing solution/"how" detail into the brief instead of leaving it for design.
- Filling every field regardless of whether it changes a downstream decision.
- Inventing relationships to existing features instead of marking them unknown.
- Writing aspirational requirements ("should be fast") instead of observable ones.
- Writing a brief for a bugfix or a well-understood change — overhead nobody reads.
- Re-asking, during design, problem-framing questions the brief already answered.
- Skipping discovery and interviewing the user on facts already in the docs.

## Success criteria

- The brief captures problem, operator, outcome, and requirements — not solution
  detail.
- Every field would change the design or the plan; nothing is there just to be
  complete.
- Requirements are numbered, observable, and testable.
- Relation to existing features is stated or explicitly marked unknown.
- `design-feature` can start from the brief without re-litigating the problem.
