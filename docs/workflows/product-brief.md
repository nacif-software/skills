# Product Brief Workflow

## Purpose

`product-brief` frames the problem before anyone designs the solution. It is the
optional, leftmost stage of the development path: it captures product/problem
context — operator, job-to-be-done, desired outcome, numbered requirements, and
relation to existing features — so `design-feature` designs toward the agreed goal
instead of producing a technically sound solution aimed at the wrong problem.

The brief is problem space only. It never says *how* — that is `design-feature`'s
job. Solution detail in the brief freezes decisions before the problem is agreed.

## Why it exists

A design doc that is strong on the "how" but thin on the "why" lets an agent build
the wrong thing coherently, with nothing upstream to catch it. The suite already
separates planning (how) from design (what) — decision 0003. `product-brief`
completes that split on the other side: framing (why / for whom / what outcome)
sits before design (what). See decision 0009.

## Flow

```text
fuzzy feature idea
  -> discover existing product context (prior briefs, designs, product surface)
  -> interview the operator on what discovery cannot answer
  -> draft the brief with numbered requirements
  -> self-review against the minimality test
  -> approve or revise
  -> write the brief artifact
  -> stop, or continue into design-feature
```

## Graduated entry points

`product-brief` is optional and gated. Start at the stage that matches what is
actually unknown:

- Net-new capability, fuzzy product context → start here.
- Known problem, unknown solution → start at `design-feature`.
- Known solution, needs sequencing → start at `plan-implementation`.

Do not write a brief for bugfixes, refactors, mechanical edits, or changes to
well-understood existing behavior.

## Discovery phase

Before interviewing, inspect what already exists: prior briefs/designs/PRDs, the
product surface the new capability will sit next to, and the product vocabulary the
project already uses. Summarize only the facts that shape the brief. The interview
then covers only what discovery could not answer.

## Interview

`product-brief` calls the `interview` discipline rather than inlining question
rules. It passes a focus (operator, outcome, requirements, feature relationships),
a stop condition (enough that design could start without guessing the problem), and
what discovery already established. The interview ends when a further answer would
not change the brief — not when every product question is exhausted.

## Minimality test

Every field must earn its place: would a different answer change the design or the
plan? If not, cut it. A half-page brief that steers the design beats a two-page
brief that documents the obvious. This is the same discipline the design doc uses —
specific enough to act on, never speculative.

## Requirements are numbered

Requirements are numbered (R1, R2, …) so design decisions and later reviews can
reference them precisely. Wiring `review-plan` and `spec-drift-check` to trace
against these IDs is a planned follow-up; today the IDs give `design-feature` a
stable anchor to cite.

## Relation to existing features

This is the hardest field to fill, because product relationships often are not in
the repo. Fill it from what the operator supplies plus what discovery found, and
mark genuinely unknown relationships as open rather than inventing them. A living
product-map artifact that accumulates these relationships across features is a
possible future extension, not part of this workflow today.

## Handoff to design

`design-feature` consumes the brief: its Goal restates the problem and desired
outcome and cites the brief, and its decisions reference the requirement IDs they
serve. `design-feature` does not re-interview the user on problem framing the brief
already settled.

## Success criteria

- The brief captures problem, operator, outcome, and requirements — not solution
  detail.
- Every field would change the design or the plan.
- Requirements are numbered, observable, and testable.
- Relation to existing features is stated or explicitly marked unknown.
- `design-feature` can start from the brief without re-litigating the problem.
