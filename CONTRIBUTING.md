# Contributing a skill

Thanks for adding to the collection. A skill is just a folder with a `SKILL.md`.
Nacif Skills favors documented workflows that can be reused across real projects.

## 1. Scaffold the folder

Copy the template and rename it:

```bash
cp -r skills/example-skill skills/my-new-skill
```

Each skill lives in its own directory directly under `skills/`. The CLI walks
`skills/` one level deep, so keep the layout flat:

```
skills/
└── my-new-skill/
    ├── SKILL.md            # required
    ├── references/         # optional: detailed docs the agent reads on demand
    ├── scripts/            # optional: executable helpers the agent runs
    └── assets/             # optional: templates/configs/fixtures
```

## 2. Write `SKILL.md`

The frontmatter has two required fields:

```yaml
---
name: my-new-skill          # lowercase-hyphens; match the folder name
description: >-             # the ROUTING RULE — see below
  Use when ... . Triggers on ... .
---
```

- **`name`** must be lowercase letters, numbers, and hyphens, and should match the
  folder name. It's the identifier the skill installs under.
- **`description`** is the most important thing you write. The agent reads only the
  description to decide whether to activate the skill, so it must say **what the
  skill does AND the concrete situations/phrases that trigger it.** Vague
  descriptions never fire.

  - ✅ `Use when the user wants to draft release notes from merged PRs. Triggers on "changelog", "release notes", or "what changed since the last release".`
  - ❌ `Helps with changelogs.`

Optional frontmatter we like to include: `license`, and `metadata` (`author`,
`version`). See `skills/example-skill/SKILL.md` for the full annotated template.

Keep `SKILL.md` lean — it's loaded into the agent's context. Push long checklists,
tables, and examples into `references/` and link to them.

For real skills, include:

- Purpose.
- When to use and when not to use.
- Inputs or discovery rules.
- Procedure.
- Validation or success criteria.
- Common failure modes.

The skill must be self-contained enough to work when installed alone. Top-level docs
can explain the system, but the installed `SKILL.md` still needs the core behavior.

## 3. Naming and collisions

`npx skills add` installs skills **flat** into the user's skills directory, so the
folder name is global on their machine. Pick a specific name, and if a skill is
likely to clash with common ones, consider prefixing it (e.g. `nacif-<skill>`) —
remember to make the folder name and the `name:` field match.

(When installed via the Claude Code plugin marketplace, skills are automatically
namespaced under the plugin, so collisions aren't a concern there.)

## 4. Test it locally

Install the skill from your local checkout into a test project:

```bash
npx skills add ./skills/my-new-skill
```

Or validate the marketplace manifest with Claude Code:

```bash
claude plugin validate .
```

Then start your agent and give it a task that should trigger the skill — confirm it
activates and does the right thing.

For workflow skills, dogfood in a real repo before calling the skill usable:

- Confirm it discovers local project rules instead of hardcoding them.
- Confirm it produces the promised artifact.
- Confirm it asks only questions that cannot be answered by repo inspection.
- Confirm upstream and downstream skill links are explicit in `SKILL.md`.
- Confirm it avoids passing full conversation history to subagents.
- Confirm verification evidence is required before completion claims.

## 5. Document the workflow

If the skill introduces a workflow, add or update docs:

- `docs/workflows/<workflow>.md` for workflow behavior.
- `docs/architecture.md` if it changes the suite model.
- `docs/subagents.md` if it changes delegation or context rules.
- `docs/decisions/<number>-<topic>.md` for important product or architecture choices.

Good docs explain the artifact contract, user gates, composition with other skills,
and how contributors should extend the pattern later.

## 6. Update the index and open a PR

Add a row for your skill to the table in [README.md](README.md), then open a pull
request. Keep skills focused, safe, and documented.

## Workflow vs discipline

Create a **workflow** when the skill owns an end-to-end user journey with gates and
artifacts. Examples: `design-feature`, `plan-implementation`, `test-strategy`,
`pr-boundary`, `review-plan`, `execute-plan`, `spec-drift-check`, `review-pr`.

Create a **discipline** when the skill enforces a reusable habit inside several
workflows. Examples: `context-briefing`, `verification-gate`.

Workflow skills may chain to discipline skills by name. Discipline skills should
stay small and avoid owning the full user journey.

## Originality and attribution

Write new skills in original language. You may learn from public workflow systems,
but do not copy their prose into this repo.

If future work intentionally adapts source text, include the required license and
copyright notice.
