# Design Feature Workflow

## Purpose

`design-feature` is the curated happy path for turning a loose feature idea into
clear development artifacts. It prevents agents from coding before they understand
intent, constraints, and the existing project shape.

## Flow

```text
idea
  -> discover repository context
  -> build decision map
  -> ask linked questions one at a time
  -> compare approaches
  -> write design doc
  -> self-review design
  -> ask next step
     -> stop at design
     -> plan-implementation
     -> plan-implementation then test-strategy
     -> plan-implementation then test-strategy then pr-boundary
     -> plan-implementation then test-strategy then pr-boundary then review-plan
     -> plan-implementation then test-strategy then pr-boundary then review-plan then execute-plan
```

## Discovery phase

The agent must inspect the project before grilling the user. Good discovery answers
questions like:

- What rules does this repo publish for agents or contributors?
- Where do designs, ADRs, plans, or issues normally live?
- What modules, tests, APIs, or commands already exist near the proposed change?
- What names and concepts does the project already use?

Discovery should be targeted. The agent should not read the entire repository.

## Decision map

The decision map is the live thinking artifact. It can be kept in the conversation
until the design doc is written.

```markdown
## Resolved decisions
- <decision>: <choice and reason>

## Open questions
- <question>: <why it matters>

## Assumptions
- <assumption>: <confidence or fallback>

## Out of scope
- <excluded work>
```

Every user question should close or refine a branch in this map.

## Question rules

- Ask one question at a time.
- Prefer a recommended answer with trade-offs.
- Do not ask what can be discovered from files.
- Stop asking once remaining uncertainty would not change the design.

## Design doc contract

The design doc is the stable handoff artifact. If the repo has no convention, write
it to `docs/designs/YYYY-MM-DD-<feature>.md`.

Minimum sections:

- Goal.
- Decisions.
- Behavior.
- Technical approach.
- Interfaces and data.
- Verification.
- Out of scope.

The doc should be specific enough to plan implementation but should not include
unnecessary code or speculative details.

## Next-step gate

After writing and self-reviewing the design, the agent offers exactly these choices:

1. Stop at design.
2. Create an implementation plan with `plan-implementation`.
3. Create a plan and test strategy with `test-strategy`.
4. Create a plan, test strategy, and decide PR shape with `pr-boundary`.
5. Create a plan, test strategy, PR shape, and review it with `review-plan`.
6. Create a plan, test strategy, PR shape, review it, and implement it with
   `execute-plan`.

If the user chooses implementation, the workflow chains through `plan-implementation`
and `test-strategy`, then `pr-boundary`, then `review-plan`, then `execute-plan`.

## Success criteria

- The design reflects actual repo context.
- The user has approved the important decisions.
- Open questions are either resolved or explicitly out of scope.
- The design doc can be handed to another agent without full chat history.
