# 0002: Use Artifacts And Minimal Briefs To Control Context

**Date:** 2026-06-30

## Decision

Make context-bloat control a core contract of the suite.

Agents should prefer durable artifacts and minimal task briefs over passing full
conversation history to every worker.

## Rationale

Large context packets make agents slower, less focused, and more likely to follow
stale or irrelevant details. A small brief with the correct source artifacts gives
workers enough information while preserving the coordinator's ability to manage the
whole task.

## Consequences

- `context-briefing` is a first-class discipline skill.
- `plan-implementation` creates the precise artifact that keeps execution briefs small.
- `test-strategy` records evidence expectations without reloading the planning
  conversation.
- `pr-boundary` records what belongs together and what intentionally splits.
- `review-plan` records plan-review findings as durable context before work is
  delegated.
- `spec-drift-check` records final alignment before review or readiness claims.
- `execute-plan` must classify tasks before parallelizing.
- Workflow docs must name the artifacts they produce and consume.
- Review reports and verification evidence are part of the handoff, not optional
  summaries.
