# 0009: Frame Product Context Before Design

**Date:** 2026-07-16

## Decision

Add an optional, gated workflow — `product-brief` — upstream of `design-feature`,
and extract the shared questioning rules into a reusable `interview` discipline.

`product-brief` captures problem space: operator, job-to-be-done, desired outcome,
numbered requirements, relation to existing features, and product-level
constraints. `design-feature` consumes it and stays in solution space.

`interview` holds the question rules (one at a time, never ask what a file answers,
stop when the answer would not change the outcome) that previously lived only inside
`design-feature`. `product-brief`, `design-feature`, and `plan-implementation` all
call it, each passing its own focus and stop condition.

## Rationale

Design docs were strong on *how* and thin on *why*: they did not systematically
capture who the operator is, what outcome counts as success, or how a feature relates
to the existing product surface. An agent could produce a coherent design aimed at
the wrong goal, with nothing upstream to catch it.

The suite already separated planning (how) from design (what) in decision 0003. This
completes the split on the other side — framing (why / for whom / what outcome)
before design (what): problem → solution → sequencing.

The question rules were duplicated implicitly across stages and would drift as each
stage was edited. Extracting them into one discipline keeps them consistent and lets
each stage pass only its own focus and stop condition, the same way
`task-dispatch-loop` was extracted from `execute-plan` in decision 0008.

## Consequences

- `product-brief` is a new workflow skill, gated behind graduated entry points: used
  for net-new capability with fuzzy product context, skipped for bugfixes and
  well-understood changes. It is never mandatory overhead.
- `interview` is a new discipline skill. `design-feature`'s inlined question rules
  now delegate to it; `plan-implementation` calls it when a requirement is ambiguous
  and no artifact settles it.
- Briefs number their requirements (R1, R2, …) to give design and later reviews a
  stable anchor.
- Wiring `review-plan` and `spec-drift-check` to trace against requirement IDs is a
  deliberate follow-up, not part of this change — traceability still roots at the
  design doc for now.
- A persistent product-map artifact that accumulates feature relationships across
  briefs is noted as a possible future extension, not built here.
- The minimality test — would a different answer change the design or plan? — keeps
  the brief from becoming a heavyweight PRD nobody maintains.
