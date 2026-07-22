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

The framing path adds an optional upstream workflow:

- `product-brief`: frame the problem before design — operator, job-to-be-done,
  desired outcome, numbered requirements, and relation to existing features. Feeds
  `design-feature`. Optional and gated: used for net-new capability with fuzzy
  product context, skipped for bugfixes and well-understood changes.

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

- `product-brief`
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

- `interview`
- `context-briefing`
- `task-dispatch-loop`
- `verification-gate`

## Default graph

```text
product-brief            (optional; net-new capability with fuzzy context)
  -> design-feature
     -> plan-implementation
        -> test-strategy
        -> pr-boundary
        -> review-plan
           -> execute-plan
              -> context-briefing
                 -> task-dispatch-loop, one instance per task (implement + spec review)
              -> checkpoint Codex review, once per PR-boundary group
              -> spec-drift-check
                 -> review-pr
                    -> verification-gate
```

Graduated entry points: start at the stage that matches what is unknown, not always
at the left. Fuzzy product context → `product-brief`; known problem, unknown
solution → `design-feature`; known solution → `plan-implementation`; known plan →
`execute-plan`. `interview` is the shared questioning discipline the framing and
planning stages call; it is not a stage of its own.

Hard gates:

- `execute-plan` does not start for non-trivial work until test strategy, PR boundary,
  and plan review are ready or explicitly unnecessary.
- Parallel subagents are dispatched only from `execute-plan`, only through
  `task-dispatch-loop` with a `context-briefing` brief, and only for independent
  tasks.
- Every `task-dispatch-loop` instance dispatches its implementer through a literal,
  named subagent call; a drafted brief that never fired is not delegation.
- `task-dispatch-loop` runs implementation and spec review only. Code-quality
  (Codex plugin) review runs once per PR-boundary group at `execute-plan`'s
  checkpoint step, never once per task — see decision 0008.
- `review-pr` follows `spec-drift-check` in the happy path.
- `verification-gate` precedes every completion, ready, fixed, commit, push, or PR
  claim.

Model routing:

- In Claude Code, prefer Anthropic models for planning, coordination, implementation,
  requirement checks, and verification.
- Use the strongest available Anthropic model for plan authoring and plan review.
- Use Claude Sonnet or a faster capable Anthropic model for decision-complete worker
  tasks, including the per-task spec reviewer; escalate only when task complexity
  requires it.
- Use native Codex review through the official OpenAI Codex plugin for code-quality
  review — a dispatched subagent whose only job is to run the plugin's companion
  script. Do not substitute a raw `codex` CLI call, an invented model-override
  flag, or a generic reviewer's own opinion. That dispatch subagent itself needs no
  reasoning capability — use the fastest/cheapest available model for it.

## Chaining model

Workflow skills may chain to other skills by name:

```text
product-brief
  -> interview, to gather problem-space context the repo cannot answer
  -> design-feature, when the brief is approved and design should start
  -> verification-gate, before claiming the brief is complete

design-feature
  -> interview, to resolve open design decisions
  -> context-briefing, when preparing handoff or subagent briefs
  -> plan-implementation, when the user chooses to plan or implement
  -> verification-gate, before completion claims

plan-implementation
  -> interview, when a requirement is ambiguous and no artifact settles it
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
  -> task-dispatch-loop, to run each task's implement/review/fix loop
  -> spec-drift-check, after implementation and before branch readiness
  -> review-pr, for whole-branch review after blocking drift is cleared
  -> verification-gate, after tasks and before branch completion

task-dispatch-loop
  -> context-briefing, to build the implementer brief
  -> execute-plan, when it escalates a blocker it cannot resolve itself

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

- Product briefs.
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
   Runs per task, immediately.
6. Quality review: is it maintainable, idiomatic, and safe? Runs once per
   PR-boundary group (not once per task) plus once over the whole branch —
   batched findings, tier-gated, to keep review volume proportional to risk
   rather than to task count.
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
