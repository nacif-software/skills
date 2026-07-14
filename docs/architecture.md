# Workflow Suite Architecture

## Goal

Nacif Skills is a public collection of agent workflows for real development work.
The suite starts with a curated happy path, then grows into smaller skills that can
be used independently.

V1 has two flagship workflows:

- `design-feature`: turn a feature idea into a design doc, optional plan, and
  optional implementation handoff.
- `review-pr`: review a pull request or branch, then either prepare review comments
  or apply accepted changes.

The implementation path adds supporting workflows:

- `plan-implementation`: convert an approved design into exact tasks, files, tests,
  and verification.
- `test-strategy`: create a risk-based test matrix that names seams, commands,
  red/green signals, manual checks, and do-not-test decisions.
- `pr-boundary`: decide how work should land across one PR, stacked PRs, separate
  PRs, migration sequences, and follow-ups.
- `review-plan`: review the implementation artifact for coverage, risk, task
  safety, and PR boundaries before execution.
- `execute-plan`: run an approved implementation plan with bounded context and review
  gates.
- `spec-drift-check`: compare the implemented branch against agreed artifacts before
  PR review or readiness claims.

## Skill types

### Workflow skills

Workflow skills own an end-to-end process and user-facing gates. They decide which
phase comes next and when to ask the user for a choice.

Examples:

- `design-feature`
- `plan-implementation`
- `test-strategy`
- `pr-boundary`
- `review-plan`
- `execute-plan`
- `spec-drift-check`
- `review-pr`

### Discipline skills

Discipline skills enforce a reusable habit inside a workflow. They should stay
small and focused.

Examples:

- `context-briefing`
- `verification-gate`

## Default graph

```text
design-feature
  -> plan-implementation
     -> test-strategy
     -> pr-boundary
     -> review-plan
        -> execute-plan
           -> context-briefing
              -> parallel-safe subagents
           -> spec-drift-check
              -> review-pr
                 -> verification-gate
```

Hard gates:

- `execute-plan` does not start for non-trivial work until test strategy, PR boundary,
  and plan review are ready or explicitly unnecessary.
- Parallel subagents are dispatched only from `execute-plan`, only with
  `context-briefing`, and only for independent tasks.
- `review-pr` follows `spec-drift-check` in the happy path.
- `verification-gate` precedes every completion, ready, fixed, commit, push, or PR
  claim.

Model routing:

- In Claude Code, prefer Anthropic models for planning, coordination, implementation,
  requirement checks, and verification.
- Use the strongest available Anthropic model for plan authoring and plan review.
- Use Claude Sonnet or a faster capable Anthropic model for decision-complete worker
  tasks; escalate only when task complexity requires it.
- Use native Codex review with `gpt-5.6-sol` for code-quality review. Do not silently
  substitute another GPT model.

## Chaining model

Workflow skills may chain to other skills by name:

```text
design-feature
  -> context-briefing, when preparing handoff or subagent briefs
  -> plan-implementation, when the user chooses to plan or implement
  -> verification-gate, before completion claims

plan-implementation
  -> context-briefing, when shaping task briefs
  -> test-strategy, when verification shape is non-trivial
  -> pr-boundary, when PR shape is not trivial
  -> review-plan, before non-trivial execution

test-strategy
  -> plan-implementation, when task steps need test updates
  -> review-plan, when the test matrix is ready to review

pr-boundary
  -> plan-implementation, when the plan needs task or sequencing changes
  -> review-plan, when the boundary artifact is ready to review

review-plan
  -> plan-implementation, when the plan needs revision
  -> test-strategy, when tests are missing or weak
  -> pr-boundary, when PR shape is missing or unsafe
  -> execute-plan, when no Critical or Important findings remain

execute-plan
  -> context-briefing, for each subagent task brief
  -> spec-drift-check, after implementation and before branch readiness
  -> review-pr, for whole-branch review after blocking drift is cleared
  -> verification-gate, after tasks and before branch completion

spec-drift-check
  -> execute-plan, when drift needs code or task fixes
  -> test-strategy, when verification drift needs a matrix update
  -> pr-boundary, when added scope or split decisions need a boundary update
  -> review-pr, when no Critical or Important drift remains

review-pr
  -> verification-gate, before saying findings are fixed or ready
  -> context-briefing, when delegating review or fix tasks
```

Skill bodies must remain useful when installed alone. Top-level docs provide deeper
explanation for contributors and dogfooding, but each `SKILL.md` must include the
minimum process needed to run.

## Repository profile discovery

The suite is project-agnostic. It should discover project rules instead of hardcoding
rules from any one codebase.

Before designing, reviewing, or implementing, agents should inspect likely sources:

- Agent instructions: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.cursor/rules`.
- Project docs: `README.md`, `CONTRIBUTING.md`, `docs/`, ADRs, specs.
- Tooling: package scripts, test config, linters, build files, CI config.
- Local examples: nearby tests, existing components, services, routes, modules.

If multiple sources conflict, the most local and explicit instruction wins. The
agent should state the conflict and the rule it will follow.

## Context-bloat control

The default unit of handoff is an artifact, not a conversation.

Durable artifacts:

- Design docs.
- Decision maps.
- Implementation plans.
- Test strategy matrices.
- PR boundary artifacts.
- Plan reviews.
- Spec drift reports.
- Task briefs.
- Review reports.
- Verification evidence.

Do not give every subagent the full conversation. Give each worker the smallest
brief that preserves intent, constraints, and verification.

## Review gates

Implementation work is not accepted only because a worker says it is done. The
coordinator must inspect the result and run a gate:

1. Test strategy: what evidence should prove the behavior and risk?
2. PR boundary: should this land as one PR, stacked PRs, separate PRs, or follow-up?
3. Plan review: is the plan complete, executable, safe to split, and correctly scoped
   for PRs?
4. Spec drift: does the implemented branch still match the agreed artifacts?
5. Spec review: does the change satisfy the source artifact without extra scope?
6. Quality review: is it maintainable, idiomatic, and safe?
7. Verification: what fresh evidence proves the accepted claim?

Critical and Important findings must be addressed or explicitly rejected with a
reason before completion.

## Platform support

V1 targets Codex and Claude Code. The language intentionally stays portable:

- Use "subagent" as the generic role.
- Use "tool" or "CLI" instead of platform-specific names when possible.
- Name concrete commands only when they are user-visible install or validation steps.

Platform-specific examples can live in workflow docs, but skill instructions should
still make sense to any capable coding agent.
