---
name: ddd-review
description: >-
  Review code in the light of Domain-Driven Design. Invoke on a diff (default) or
  a file/directory. Use when checking that an implementation faithfully reflects the
  domain model — ubiquitous language, layer isolation, aggregates, supple design.
disable-model-invocation: true
license: MIT
metadata:
  author: nacif
  version: "0.1.0"
---

# DDD Review

Review code against Domain-Driven Design principles, checking that the implementation
faithfully reflects the domain model and keeps the system's integrity.

## Target detection

Pick the scope from the argument:

- **No argument** → review the **diff since the base**: `git diff $(git merge-base HEAD <default-branch>)...HEAD`.
  Find the default branch generically (e.g. `git symbolic-ref refs/remotes/origin/HEAD`,
  falling back to `main`/`master`). A diff usually spans multiple files and layers at once —
  reviewing what each change put in each layer is where DDD is most tested, so this is a
  first-class target, not a shallow fallback. **Handle a whole multi-file, multi-layer diff**
  without choking: read the changed files for context, don't review lines in isolation.
- **A file path** → scope to that file/class and its immediate neighbours.
- **A directory** → scope to that module/context; sweep the folder.

## Ubiquitous Language source

Before Section 1, look for a domain glossary in the project: `UBIQUITOUS_LANGUAGE.md`,
`CONTEXT.md`, or similar. If found, use it as the source of truth for domain terms.
If none exists, infer the domain language from the code itself and **state explicitly that
you are inferring** — flag internal inconsistencies (synonyms, technical terms leaking in)
rather than validating against an external source.

## Process

Read the target, then walk the **five sections below in order, at equal weight**. Layer
separation matters, but it does not outrank the other sections. Go through every checklist
item internally; only surface what deviates.

## Output (inline, hybrid)

Report inline in the chat:

1. **Panorama** — one status line per section (✅ ok / ⚠️ pontos de atenção / ❌ violações),
   so the reader sees coverage at a glance.
2. **Findings** — detailed items only where there is something to act on. Each finding:
   - **Severity**: **❌ Violação** (breaks a central invariant/principle — e.g. business
     logic in the application layer, a mutable Value Object) · **⚠️ Cheiro** (a deviation that
     raises the risk/cost of change — e.g. an aggregate with no clear root) · **💡 Sugestão**
     (expressiveness/naming improvement).
   - `file:line`
   - The DDD principle at stake
   - Why it matters
   - A short suggestion

Do not print a line for every checklist item — the checklist is the internal lens, not the output.

---

# Checklist

## 1. Ubiquitous Language

The code should be a communication channel that uses the same terms spoken by domain experts and developers.

- **Terminology:** Do class, method, variable, and module names reflect the domain language?
- **Expressiveness:** Can you read the code and understand the business rule without external technical explanation?
- **Sync:** If the agreed language changed with the experts, was that reflected in the code (e.g. renaming methods and classes)?

## 2. Layered Architecture (Domain Isolation)

The heart of the software should be isolated from technical complexity so the model can evolve.

- **Isolation:** Is the domain layer free of dependencies on infrastructure (database, network frameworks), UI, or application logic?
- **Application-layer responsibility:** Does this layer only coordinate tasks and delegate work to domain objects? It must hold no business rules.
- **Framework intrusion:** Is framework use in the domain layer minimal, not "cementing" the model's expressiveness?

## 3. Building Blocks

Every object in the system should have a clear conceptual role defined by the model.

### Entities

- **Identity:** Does the object have a unique identity that persists through state and time changes?
- **Focus:** Is the class defined around its continuity and lifecycle, not just its attributes?

### Value Objects

- **Immutability:** Is the object treated as immutable? (Any change should yield a new instance.)
- **Wholeness:** Does the object represent a complete concept (Whole Value) rather than a loose bag of attributes?
- **No identity:** Is the object defined only by its attributes? (Two objects with the same values are interchangeable.)

### Aggregates

- **Aggregate root:** Is there a single entity defined as the root controlling access and guaranteeing integrity?
- **Encapsulation:** Do external objects hold references only to the aggregate root, never persistently to internal members?
- **Invariants:** Are all internal consistency rules of the aggregate satisfied at the end of every transaction?

### Repositories

- **Global access:** Are repositories provided only for aggregate roots that genuinely need direct access?
- **Abstraction:** Does the repository offer the illusion of an in-memory collection, hiding technical search/persistence details (SQL, infrastructure criteria)?

### Factories

- **Creation complexity:** Is the creation of complex aggregates encapsulated in a factory, ensuring the object comes out valid and consistent?

### Domain Services

- **Nature of the operation:** Does the operation represent a domain concept that doesn't naturally fit an Entity or Value Object?
- **Stateless:** Is the service stateless, so any client can use it without regard to instance history?

## 4. Supple Design

The design should make the code a pleasure to work with and easy to change.

- **Intention-revealing interfaces:** Do class and method names describe the *goal* and *effect* (the "what") rather than the means of execution (the "how")?
- **Side-effect-free functions:** Is complex logic and calculation concentrated in methods that return results without altering system state (especially in Value Objects)?
- **Assertions:** Are the side effects of commands (state-changing methods) clear and, where possible, guarded by pre/post-conditions or automated unit tests?
- **Conceptual contours:** Is the code decomposed into cohesive units that follow the domain's axes of change and stability?
- **Standalone classes:** Is coupling between classes minimized to reduce the cognitive load needed to understand a module?

## 5. Strategy and Modules

- **Bounded Contexts:** Does the code respect the boundaries of its original context, using translation layers (Anticorruption Layers) when it must interact with external models?
- **Module cohesion:** Do modules (packages) contain related concepts that tell a domain story, rather than being grouped by technical pattern (e.g. all repositories in one package and all entities in another)?
