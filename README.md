<p align="center">
  <a href="https://nacif.software">
    <img src="assets/nacif-logo.png" alt="Nacif" height="44">
  </a>
</p>

<h1 align="center">Nacif Skills</h1>

Agent skills you can drop into Claude Code, Cursor, Codex, and 70+ other coding
agents. These are the prompts, workflows, and tooling we use in production
codebases at [Nacif](#about-nacif), shared openly with the community.

A **skill** is a folder with a `SKILL.md` file. Its frontmatter `description` tells
your agent *when* to use it, and the body tells it *how*. Once installed, the agent
loads the right skill automatically when a task matches.

## Install

Skills are distributed straight from this GitHub repo — no account, no registry.

### With `npx skills` (any agent)

```bash
# Install every skill in this repo (auto-detects your installed agents)
npx skills add nacif-software/skills

# Install one skill
npx skills add nacif-software/skills --skill example-skill

# Install globally (into ~/… instead of the current project)
npx skills add -g nacif-software/skills

# Browse what's here without installing
npx skills add nacif-software/skills --list
```

[`npx skills`](https://github.com/vercel-labs/skills) installs each skill into your
agent's skills directory (e.g. `.claude/skills/` for a project, `~/.claude/skills/`
globally) and works across 70+ agents.

### As a Claude Code plugin marketplace

This repo is also a Claude Code plugin marketplace, so you can install the whole
collection as one plugin:

```text
/plugin marketplace add nacif-software/skills
/plugin install nacif-skills@nacif-software
```

## Skills

| Skill | What it does |
| --- | --- |
| [`aggregate-dependabot-prs`](skills/aggregate-dependabot-prs/) | Bundles a backlog of open Dependabot PRs into a few CI-validated aggregate PRs, closing originals only for bundles that pass — never auto-merges. |
| [`example-skill`](skills/example-skill/) | Template only — copy it as the starting point for a new skill. Not a working skill. |
| [`post-deploy-changelog`](skills/post-deploy-changelog/) | Turns a production-deploy PR into concise, product-facing release notes and posts them to your team's changelog channel in its existing style. |
| [`pr-wrap-up`](skills/pr-wrap-up/) | Finalizes a finished PR for human review: linters, AI-comment cleanup, self-review, feedback triage, CI watch, draft → ready. |
| [`review-and-wrap-up-pr`](skills/review-and-wrap-up-pr/) | Hardens a PR with an adversarial Codex review loop (fixing only real P1/P2 issues) before running the wrap-up flow. |
| [`review-dependabot-prs`](skills/review-dependabot-prs/) | Reviews every open Dependabot PR in parallel, checks changelogs for breaking changes, and gives a per-PR merge-safety verdict. |
| [`scope-check`](skills/scope-check/) | Checks a feature or plan against the original ask — flags scope creep and needless complexity against the minimum-viable version. |
| [`whatsapp-analyzer`](skills/whatsapp-analyzer/) | Extracts, transcribes, and OCRs WhatsApp chat exports (text, voice, images, PDFs) into one structured, timeline-based report. |

_More coming — this repo is just getting started._

## Using a skill

After installing, just describe your task naturally. The agent matches it against
each skill's `description` and applies the relevant one. You don't invoke skills by
name (though in Claude Code you can: `/example-skill`).

## Contributing

Want to add a skill? See [CONTRIBUTING.md](CONTRIBUTING.md). The short version: copy
`skills/example-skill/`, rename the folder, rewrite `SKILL.md`, and open a PR.

## About Nacif

Nacif is a boutique software consultancy. We integrate with your business to form the
engineering team your product needs, from first commit to long-term growth.

We build with AI as a real force multiplier, not a buzzword. As AI makes the typing
cheap, judgement, architecture, and ownership are what move products forward. This
repo is part of how we work: the skills our engineers actually use in production
codebases, shared with the community.

[nacif.software](https://nacif.software)

## License

[MIT](LICENSE) © 2026 Nacif
