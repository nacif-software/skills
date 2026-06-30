# Review Plan Workflow

## Purpose

`review-plan` is the quality gate between implementation planning and execution.
It reviews the plan artifact while changes are still cheap: before code, subagent
dispatch, issue creation, or PR shape hardens.

## Flow

```text
implementation plan
  -> identify source artifact and intended next step
  -> inspect only needed repo context
  -> check requirement coverage
  -> check executability
  -> read or check test strategy
  -> check task and subagent safety
  -> check relevant risk areas
  -> read or recommend PR boundary
  -> report verdict and findings
  -> revise plan, revise test strategy, revise PR boundary, or execute
```

## Review dimensions

### Requirement coverage

Every source requirement should map to a task. Out-of-scope items should remain
excluded. Assumptions should be explicit enough that a worker does not invent them
during implementation.

### Executability

A plan is executable when it names files, task order, dependencies, shared
contracts, verification commands, and expected signals. Vague work such as "handle
errors", "wire up UI", or "add tests" should become concrete before execution.

### Test Strategy

The review should read the `test-strategy` artifact when present. If it is missing,
the review checks whether the plan proves behavior at useful boundaries. Good tests
verify risk without coupling to brittle internals. When automation is not practical,
the plan should name the manual check and the reason it is acceptable. Do-not-test
decisions should have reasons.

### Task and subagent safety

Parallel work is safe only when write scopes are disjoint or shared contracts are
already specified. If two tasks would negotiate an interface while coding, they are
sequential or need a contract task first.

### Risk areas

Review only relevant risks, but do not skip obvious ones:

- Security and auth.
- Privacy and data integrity.
- Migrations and compatibility.
- Performance.
- Observability.
- Rollout and rollback.
- Documentation and operator impact.

## PR boundary model

The plan review should read the `pr-boundary` artifact when present. If it is
missing, the review should recommend how the work should land:

- **One PR:** the change has one intent, one review surface, shared verification,
  and should deploy atomically.
- **Stacked PRs:** one change enables the next and can be reviewed in order.
- **Separate PRs:** changes are independently valuable or risky.
- **Follow-up:** work is useful but not required for the source goal.

Split unrelated cleanup, broad refactors, risky migrations, and optional polish
unless they are required for the feature to work safely.

## Verdicts

- **Blocked:** Critical findings exist; execution would be unsafe or likely wrong.
- **Needs revisions:** Important findings exist; fix the plan before execution.
- **Ready:** no Critical or Important findings remain.

Minor findings should be recorded, but they do not block execution.

## Success criteria

- Findings are severity-ranked and actionable.
- Test strategy advice names useful seams and avoids brittle test bloat.
- PR boundary advice says what belongs together and what should split.
- The review can be attached to the plan as durable context.
- `execute-plan` can proceed without inheriting hidden assumptions.
- `execute-plan` starts only after no Critical or Important findings remain and
  required test strategy and PR boundary artifacts are ready.
