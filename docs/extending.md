# Extending the Workflow Suite

## Add a workflow when

- The task has a repeatable beginning, middle, and end.
- User choices or gates matter.
- Several smaller disciplines need to be chained.
- The output should be a durable artifact, not only a chat answer.

## Add a discipline when

- The behavior is reusable inside multiple workflows.
- It enforces a habit or judgment call.
- It can stay small and focused.
- It does not own the entire user journey.

## Required files

Every new skill needs:

- `skills/<skill-name>/SKILL.md`
- A row in `README.md`
- Documentation if it introduces a workflow, artifact contract, or extension pattern.

Workflow docs live in `docs/workflows/`. Cross-cutting docs live in `docs/`.
Decisions live in `docs/decisions/`.

## Skill authoring checklist

- Name is lowercase hyphen-case and matches the folder.
- Description starts with "Use when" and names trigger situations.
- `SKILL.md` is self-contained enough to work when installed alone.
- Long explanations move to docs or references.
- The skill tells the agent when not to use it.
- The skill has a validation or success section.
- The skill avoids project-specific rules.
- Any project-specific behavior is discovered from the target repo.

## Workflow quality bar

A workflow skill should define:

- Trigger conditions.
- Discovery phase.
- User gates.
- Artifact contracts.
- Handoff behavior.
- Verification behavior.
- Common mistakes.

## Documentation quality bar

Docs should explain:

- Why the workflow exists.
- What artifacts it produces.
- How it composes with other skills.
- How contributors should extend it later.

Implementation planning workflows should also document the expected plan contract:
file map, task graph, test seams, code-snippet policy, and verification evidence.

Test-strategy workflows should document behavior/risk matrices, seam selection,
red/green signals, manual check rules, and do-not-test decisions.

Plan-review workflows should document their verdict model, severity model,
traceability expectations, risk checklist, and PR boundary advice.

PR-boundary workflows should document landing shapes, split criteria, dependency
rules, verification expectations, and rollback considerations.

Spec-drift workflows should document traceability, added scope, missing scope,
changed decisions, test-strategy drift, and PR-boundary drift.

Avoid documenting private implementation history. Keep docs useful to future users
and contributors.

## Originality policy

Write skills in original language. Existing public workflow systems may inform the
shape of the suite, but do not copy their prose into this repo.

If future work intentionally adapts source text, include the required license and
copyright notice.

## Dogfooding checklist

Before calling a new workflow usable:

- Install it locally with `npx skills add`.
- Run it in a real project.
- Confirm it discovers project rules instead of hardcoding them.
- Confirm it produces the promised artifact.
- Confirm it avoids unnecessary context transfer.
- Record any workflow decisions that should become docs.
