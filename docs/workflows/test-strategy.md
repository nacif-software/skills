# Test Strategy Workflow

## Purpose

`test-strategy` turns requirements, plans, bugs, or PRs into a durable test matrix.
It exists to avoid vague verification such as "add tests" and to keep test work
focused on the risks that matter.

## Flow

```text
source intent and change shape
  -> discover local test conventions
  -> identify behaviors and risks
  -> choose test seams
  -> build matrix
  -> name red and green signals
  -> name do-not-test cases
  -> produce test strategy artifact
  -> feed relevant rows to plan tasks, review-plan, execute-plan, or review-pr
```

## Test Seams

- **Unit:** pure logic, edge cases, transformations, validation, reducers.
- **Integration:** persistence, API handlers, services, queues, jobs, workflows.
- **Contract:** public APIs, schemas, events, generated clients, compatibility.
- **End-to-end:** user-critical paths where lower-level tests miss wiring risk.
- **Manual:** checks that are too expensive, brittle, visual, or environment-specific
  to automate safely.

Prefer the highest useful seam that proves behavior without coupling tests to
implementation details.

## Risk Matrix

Good strategies consider only relevant risks, but they should not skip obvious ones:

- Happy path.
- Boundary and invalid input.
- Permissions and tenancy.
- Regression case.
- Failure behavior.
- Data integrity.
- Migrations and compatibility.
- Performance or concurrency.
- Rollout and rollback.
- Documentation or operator impact.

## Red And Green Signals

For new automated tests, the matrix should say what failure proves the test is
useful before implementation and what success proves after implementation. This is
especially important when the strategy will feed a TDD implementation plan.

## Do Not Test

The artifact should explicitly name tests that are not worth adding now:

- Already covered by a stronger seam.
- Would assert private implementation.
- Would be brittle or slow compared with the risk.
- Belongs to unrelated legacy behavior.
- Should be follow-up work.

## Success Criteria

- The matrix maps behavior and risk to exact tests or checks.
- Each proposed test has a useful seam.
- Manual checks are justified.
- Do-not-test decisions prevent test bloat.
- Future agents can use the artifact without replaying the discussion.
- Subagent briefs can carry only the rows relevant to each task.
