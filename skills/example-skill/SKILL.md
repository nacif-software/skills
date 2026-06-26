---
# `name` and `description` are the only REQUIRED fields.
# `name` must be lowercase letters, numbers, and hyphens, and should match this
# folder's name (example-skill). It is the identifier the skill installs under.
name: example-skill
# `description` is the most important line you will write. It is the ROUTING RULE:
# the agent reads it to decide *whether to activate this skill*. State what the
# skill does AND the exact situations/phrases that should trigger it. Be specific —
# vague descriptions never fire.
description: >-
  TEMPLATE — not a working skill. Copy this folder as the starting point for a real
  skill, then rewrite everything. A good description names what the skill does and
  the concrete triggers, e.g. "Use when the user asks to draft a release changelog
  from merged PRs. Triggers on mentions of changelog, release notes, or 'what
  changed since the last release'."
# Everything below is OPTIONAL but recommended.
license: MIT
metadata:
  author: nacif
  version: "0.1.0"
---

# Example Skill (template)

> Delete this notice in real skills. This file exists to show the format and the
> sections we like our skills to have. It is intentionally not useful on its own.

## Purpose

One or two sentences: what does this skill let the agent do that it wouldn't do as
well without it? Keep `SKILL.md` lean — it is loaded into the agent's context, so
spend words on instructions, not prose. Push long material into `references/`.

## When to use

Restate the trigger conditions from the `description`, expanded. List the situations
this skill applies to and, just as importantly, when it does **not** apply so the
agent doesn't fire it inappropriately.

- Use when: <situation A>, <situation B>.
- Do not use when: <situation that looks similar but isn't>.

## Inputs

What the skill needs before it can run (files, a URL, an API token, a selection,
arguments). If something is required, say how the agent should obtain it.

## Procedure

Numbered, imperative steps. This is the heart of the skill.

1. Do the first thing.
2. Do the next thing. Reference a helper script when shell work is involved, e.g.
   run `scripts/example.sh <arg>`.
3. Consult `references/reference-template.md` for the detailed rules/checklist
   rather than inlining them here.

## Validation

How the agent confirms it actually succeeded — the command to run, the output to
check, the file that should now exist. Evidence before claiming done.

## Common failure modes

- <Mistake the agent tends to make> → <how to avoid it>.
- <Edge case> → <how to handle it>.

## Supporting files

- `references/` — detailed docs, checklists, templates the agent reads on demand.
- `scripts/` — executable helpers the agent runs.
- `assets/` — (optional) templates, configs, or fixtures the skill copies or fills in.
