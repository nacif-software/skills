# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Nacif Skills is a collection of agent skills — each skill is a folder under `skills/` with a `SKILL.md` (frontmatter + prose) plus optional `references/`, `scripts/`, and `assets/`. Skills are distributed straight from GitHub via `npx skills` and as a Claude Code plugin marketplace (`.claude-plugin/marketplace.json`).

The primary deliverable is the content of each `SKILL.md` and its supporting docs. Check `README.md` and `CONTRIBUTING.md` for the current install/distribution story, and `docs/` for the suite model.

## Where the authoritative guidance lives

- `CONTRIBUTING.md` — how to scaffold, write, name, and test a skill; the required `SKILL.md` sections.
- `docs/architecture.md` — the suite model: skill types, the default workflow graph, and how skills relate.
- `docs/subagents.md` — delegation and context rules.
- `docs/workflows/<workflow>.md` — per-workflow behavior and artifact contracts.
- `docs/decisions/` — numbered ADRs; read the relevant one before changing suite-level behavior.
- `skills/example-skill/` — the annotated template to copy when starting a new skill.

## Validating a skill

Skills are prose contracts rather than compiled code, so validation is behavioral:

```bash
claude plugin validate .                 # validate the marketplace manifest
npx skills add ./skills/<skill-name>     # install one skill into a test project and dogfood it
```

To confirm a skill works, install it and give an agent a task that should trigger it — verify it activates and produces the promised artifact. Match whatever build/lint/test tooling exists at the time by inspecting the repo (package manifests, CI config, `docs/`) rather than assuming.

## The two skill types

Every skill is either:

- **Workflow skill** — owns an end-to-end user journey with user-facing gates and durable artifacts (e.g. `design-feature`, `plan-implementation`, `execute-plan`, `review-pr`). It decides the next phase and asks the user to choose.
- **Discipline skill** — enforces one reusable habit used *inside* workflows; stays small and never owns the full journey (e.g. `context-briefing`, `task-dispatch-loop`, `verification-gate`).

Workflow skills chain to other skills **by name** in their prose. When you change one skill's contract, check the references to it in the others (grep the skill name across `skills/*/SKILL.md`) and the graph in `docs/architecture.md`. Treat that graph as the source of truth for the current default path and its hard gates (e.g. code-quality review cadence is set by `docs/decisions/0008-*`).

## Conventions to preserve when authoring or editing skills

- **`description` is the routing rule.** The agent reads *only* the description to decide whether to activate a skill, so it must state what the skill does AND the concrete triggering situations/phrases. Vague descriptions never fire. `name` must be lowercase-hyphens and match the folder name.
- **Keep `SKILL.md` lean** — it loads into the agent's context. Push long checklists, tables, and examples into `references/` and link to them.
- **Skills are project-agnostic.** Do not hardcode conventions from any one codebase. Skills should *discover* local project rules by inspecting the target repo's agent instructions (`AGENTS.md`/`CLAUDE.md`/`.cursor/rules`), docs, tooling (package scripts, test config, linters, CI), and nearby examples. When sources conflict, the most local explicit instruction wins and the skill should say which it followed.
- **Portable language.** Use "subagent" as the generic role and "tool"/"CLI" over platform-specific names in skill bodies. Platform-specific examples belong in `docs/workflows/`, not baked into skill instructions.
- **Artifact-based handoffs, not conversation.** The unit of handoff is a durable artifact (design doc, plan, test matrix, PR boundary, review report, verification evidence). Give a subagent the smallest brief that preserves intent, constraints, and verification — not the full conversation.
- **Self-contained.** A skill must work when installed alone; the top-level docs explain the system, but each `SKILL.md` still needs the core behavior inlined.

## When adding or changing a skill

Follow `CONTRIBUTING.md`. In brief: copy `skills/example-skill/` and rename (folder name = `name:` field); write `SKILL.md` with the sections listed there; update the relevant `docs/` (workflow doc, and `docs/architecture.md`/`docs/subagents.md` if the suite model or delegation rules change) and add a numbered ADR under `docs/decisions/` for important choices; and add a row to the skills table in `README.md`, which is maintained by hand.
