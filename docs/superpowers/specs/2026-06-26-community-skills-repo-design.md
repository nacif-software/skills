# Community Skills Repo — Design

**Date:** 2026-06-26
**Repo:** `nacif-software/skills` (https://github.com/nacif-software/skills)

## Goal

Set up an empty repo so anyone can install our agent skills with:

```bash
npx skills add nacif-software/skills
```

Ship a full installable scaffold plus one labeled template skill, so our team and
the community can add new skills consistently.

## How `npx skills` works (context)

- The [`vercel-labs/skills`](https://github.com/vercel-labs/skills) CLI is a package
  manager for agent skills, run via `npx` (no install). Commands: `add`, `remove`,
  `update`, `find`, `list`, `use`, `init`.
- **GitHub is the registry.** `npx skills add nacif-software/skills` maps directly to
  the GitHub repo. [skills.sh](https://skills.sh) is a discovery index on top of GitHub.
- **Discovery = directory walk.** The CLI scans `skills/` (one level deep, plus catalog
  layouts), agent dirs, or a root `SKILL.md`. It also honors `.claude-plugin/marketplace.json`.
- **Install target** = user's agent dir: `.claude/skills/` (project) or `~/.claude/skills/`
  (global, `-g`), via symlink or copy. Auto-detects 70+ agents.
- **A skill** = a folder whose `SKILL.md` has YAML frontmatter with `name`
  (lowercase-hyphens, must equal the folder name) and `description` (the routing rule
  that tells the agent when to activate it). Optional: `license`, `metadata`, plus
  `references/` and `scripts/` supporting folders.

## Repository layout

```
nacif-software/skills/              ← repo root
├── README.md                       ← what it is, install, skill index, About Nacif, contributing
├── LICENSE                         ← MIT (2026, nacif-software)
├── CONTRIBUTING.md                 ← how to author + add a new skill
├── .claude-plugin/
│   └── marketplace.json            ← Claude Code marketplace manifest (extra discoverability)
└── skills/                         ← the directory the CLI walks (one level deep)
    └── example-skill/
        ├── SKILL.md                ← template: frontmatter + every body section, commented
        ├── references/
        │   └── reference-template.md
        └── scripts/
            └── example.sh
```

## Decisions

- **Seed:** scaffold + one example skill (no real skills migrated yet).
- **Example skill:** a clearly labeled `example-skill` template — placeholder content
  demonstrating every part of the format (required + optional frontmatter, `references/`,
  `scripts/`). Not meant to run as-is.
- **Manifest:** include `.claude-plugin/marketplace.json` so the repo is also a Claude Code
  plugin marketplace. Additive — does not affect `npx skills add`.
- **License:** MIT.

## Component details

### `skills/example-skill/SKILL.md`
- Frontmatter: `name: example-skill` (matches folder), `description` written as a routing
  rule with explicit trigger phrases, plus optional `license` and `metadata` to show they
  exist. Inline comments explain each field.
- Body sections: purpose, when to use (triggers), inputs, step-by-step procedure, validation
  criteria, common failure modes — pointing detail into `references/`.
- Keep lean; the body teaches the format more than it does any real task.

### `.claude-plugin/marketplace.json`
- Marketplace manifest making the repo double as a Claude Code plugin marketplace.
- Schema verified against the live Claude Code docs. Decisions:
  - Marketplace `name: nacif-software` (the org namespace; `agent-skills` /
    `anthropic-agent-skills` etc. are reserved and cannot be used).
  - One plugin `nacif-skills` with `source: "./"` and `skills: ["./skills/"]` so it
    auto-bundles every skill in `skills/`. Install: `/plugin install nacif-skills@nacif-software`.
  - `strict: false` so the marketplace entry is the authority and no separate
    `plugin.json` is required.
  - `version` omitted on purpose → every git commit is treated as a new version, so
    users auto-update as we add skills.

### `README.md`
- What the repo is + the agentic-engineering framing.
- Install: `npx skills add nacif-software/skills` (all), `--skill <name>` (one), `-g` (global).
- Skill index table (currently just `example-skill`).
- How to use a skill once installed.
- **About Nacif** section (verbatim, supplied by the user).
- Contributing pointer + license.

### `CONTRIBUTING.md`
- One folder per skill under `skills/`; folder name == `name:` == lowercase-hyphens.
- `description` is the routing rule — must say what it does AND when to use it (triggers).
- Keep `SKILL.md` lean; push detail into `references/`. Scripts go in `scripts/`.
- Local test loop: `npx skills add ./skills/<name>` or point at the repo.

### About Nacif (README content, verbatim)

> ## About Nacif
>
> Nacif is a boutique software consultancy. We integrate with your business to form the
> engineering team your product needs, from first commit to long-term growth.
>
> We build with AI as a real force multiplier, not a buzzword. As AI makes the typing cheap,
> judgement, architecture, and ownership are what move products forward. This repo is part of
> how we work: the skills our engineers actually use in production codebases, shared with the
> community.
>
> [nacif.software](https://nacif.software)

## Out of scope (YAGNI)

- Migrating real personal skills (separate follow-up per skill).
- CI/CD, linting, automated skill validation workflows.
- A `skills.sh.json` registry file (CLI discovers via directory walk; not required).
```
