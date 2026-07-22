---
name: ddd-planning
description: >-
  DDD-guided feature planning — walk strategic alignment, model, tactical and
  supple design before building. Use when planning a feature through Domain-Driven
  Design, defining bounded contexts, aggregates, or the ubiquitous language.
disable-model-invocation: true
license: MIT
metadata:
  author: nacif
  version: "0.1.0"
---

Plan a feature through the lens of Domain-Driven Design. Self-conducting: answer each
checklist item from the code and existing domain artifacts; **look facts up, ask only
decisions**. Stop and ask the user — one question at a time — only when a domain
decision the repo cannot answer blocks you. The checklist is an internal lens, not
output. Do not implement. Do not recommend a next step.

## Open by grounding

Before Section 1, load what already exists:

- `CONTEXT-MAP.md` (multi-context) / `CONTEXT.md`, `UBIQUITOUS_LANGUAGE.md`, `docs/adr/`.
- The code of the affected area (use codebase-memory tools).

Section 1 builds on the real map, Section 2 reuses the existing glossary, Sections 3–4
read the Entities/VOs/aggregates that already exist before proposing new ones. Without
this the walk is DDD theatre.

## Walk the four sections in order

### 1 — Strategic alignment & context
- **Bounded context** the feature lives in.
- Classify the domain: **core** (business heart), **generic** (outsourceable), or
  **supporting**.
- Context map impact: does integrating with another context need an **anticorruption
  layer** to shield your model from a legacy/external system?
- Alignment with the domain vision (skip if the repo states none).

### 2 — Knowledge crunching
- Discuss the feature in the **ubiquitous language**. New term → update model + code;
  a model term that's awkward to say → refactor it.
- Run scenarios **out loud** in model elements to expose ambiguity or needless
  complexity.
- Hunt **implicit concepts** hidden in `if/else` and make them explicit in the model.

### 3 — Tactical design
- **Entity vs Value Object**: continuous identity over time → Entity; defined only by
  its attributes and immutable → Value Object.
- **Aggregates**: which objects change together and must stay consistent? Name the
  **aggregate root** — the single external access point.
- **Domain service** (stateless) when logic is a process across many objects rather
  than belonging to one.
- Creation & access: complex construction → **Factory**; retrieval → **Repository**
  (roots only).

### 4 — Supple design
- **Intention-revealing** names — say what and why, not how.
- **Side-effect-free functions**: push logic into queries that compute and return
  without mutating state.
- **Assertions**: state pre/post-conditions and invariants explicitly.
- **Specifications** for complex validation/selection/creation rules.

## Persist as it crystallizes

- Architectural decision firms up → record an ADR via `/domain-modeling` (when available).
- Canonical term firms up → register it via `/ubiquitous-language` (when available).

Self-sufficient without them: if unavailable, note the decision/term inline instead.

## Done

End at shared understanding in chat.
