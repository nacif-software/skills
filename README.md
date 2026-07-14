<p align="center">
  <a href="https://nacif.software">
    <img src="assets/nacif-logo.png" alt="Nacif" height="44">
  </a>
</p>

<h1 align="center">Nacif Skills</h1>

Agent workflows you can drop into Claude Code, Codex, Cursor, and 70+ other
coding agents. These are the prompts, workflows, and tooling we use in production
codebases at [Nacif](#about-nacif), shared openly with the community.

A **skill** is a folder with a `SKILL.md` file. Its frontmatter `description` tells
your agent *when* to use it, and the body tells it *how*. Once installed, the agent
loads the right skill automatically when a task matches.

This repo is organized around a recommended development path:

```text
design-feature -> plan-implementation -> test-strategy -> pr-boundary -> review-plan -> execute-plan -> spec-drift-check -> review-pr -> verification-gate
```

For non-trivial implementation, `execute-plan` starts only after the plan, test
strategy, PR boundary, and plan review are ready or explicitly marked unnecessary.
After execution, the branch moves through spec drift, PR review, and verification
before any readiness claim.

The flagship workflows are project-agnostic. They discover local repository rules
instead of hardcoding conventions from any one codebase.

## Install

Skills are distributed straight from this GitHub repo — no account, no registry.

### With `npx skills` (any agent)

```bash
# Install every skill in this repo (auto-detects your installed agents)
npx skills add nacif-software/skills

# Install one skill
npx skills add nacif-software/skills --skill design-feature

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

### Automatic Codex review in Claude Code

The `codex-review` gate requires OpenAI's Codex plugin for Claude Code. Install it
once alongside this marketplace:

```text
/plugin marketplace add openai/codex-plugin-cc
/plugin install codex@openai-codex
/reload-plugins
/codex:setup
```

After setup, `codex:codex-rescue` must appear in `/agents`. Workflow reviews dispatch
that plugin agent automatically; users do not run `/codex:review` during the flow.

## Skills

| Skill | What it does |
| --- | --- |
| [`aggregate-dependabot-prs`](skills/aggregate-dependabot-prs/) | Bundles a backlog of open Dependabot PRs into a few CI-validated aggregate PRs, closing originals only for bundles that pass — never auto-merges. |
| [`design-feature`](skills/design-feature/) | Curated feature design workflow: discover context, ask linked questions, write a design doc, and optionally continue to planning or implementation. |
| [`plan-implementation`](skills/plan-implementation/) | Converts an approved design or PRD into a decision-complete implementation plan with files, tasks, test seams, snippets, and verification. |
| [`test-strategy`](skills/test-strategy/) | Creates a risk-based test matrix with seams, commands, red/green signals, manual checks, and do-not-test decisions. |
| [`pr-boundary`](skills/pr-boundary/) | Decides whether work should land as one PR, stacked PRs, separate PRs, prep work, migration sequence, or follow-up. |
| [`review-plan`](skills/review-plan/) | Reviews implementation plans before execution for requirement coverage, test strategy, task safety, risk, and PR boundaries. |
| [`execute-plan`](skills/execute-plan/) | Implementation workflow for approved plans, including task splitting, subagent briefs, review gates, and verification. |
| [`spec-drift-check`](skills/spec-drift-check/) | Compares implemented work against design, plan, test strategy, PR boundary, and accepted scope before PR readiness. |
| [`review-pr`](skills/review-pr/) | PR/branch review workflow with comment-only mode and apply-changes mode. |
| [`codex-review`](skills/codex-review/) | Dispatches an automatic, fresh, read-only Codex quality review through the Claude Code OpenAI Codex plugin agent. |
| [`context-briefing`](skills/context-briefing/) | Discipline for passing minimal, useful context to subagents and handoffs. |
| [`verification-gate`](skills/verification-gate/) | Discipline for requiring fresh evidence before completion, fixed, ready, or passing claims. |
| [`example-skill`](skills/example-skill/) | Template only — copy it as the starting point for a new skill. Not a working skill. |
| [`post-deploy-changelog`](skills/post-deploy-changelog/) | Turns a production-deploy PR into concise, product-facing release notes and posts them to your team's changelog channel in its existing style. |
| [`pr-wrap-up`](skills/pr-wrap-up/) | Finalizes a finished PR for human review: linters, AI-comment cleanup, self-review, feedback triage, CI watch, draft → ready. |
| [`review-and-wrap-up-pr`](skills/review-and-wrap-up-pr/) | Hardens a PR with an adversarial Codex review loop via the official [OpenAI Codex plugin](https://github.com/openai/codex-plugin-cc) (fixing only real must-fix issues) before running the wrap-up flow. |
| [`review-dependabot-prs`](skills/review-dependabot-prs/) | Reviews every open Dependabot PR in parallel, checks changelogs for breaking changes, and gives a per-PR merge-safety verdict. |
| [`scope-check`](skills/scope-check/) | Checks a feature or plan against the original ask — flags scope creep and needless complexity against the minimum-viable version. |
| [`whatsapp-analyzer`](skills/whatsapp-analyzer/) | Extracts, transcribes, and OCRs WhatsApp chat exports (text, voice, images, PDFs) into one structured, timeline-based report. |

More workflows are expected to grow out of real use.

## Using a skill

After installing, just describe your task naturally. The agent matches it against
each skill's `description` and applies the relevant one. You don't invoke skills by
name (though in Claude Code you can use slash commands such as `/design-feature`).

Example prompts:

```text
Help me design this feature before we build it.
Create a test strategy for this implementation plan.
Decide what should stay in this PR and what should split out.
Review this implementation plan before we hand it to agents.
Check whether this branch drifted from the agreed plan before we open a PR.
Review the current branch against main and tell me whether to comment on the PR or apply fixes.
Take this reviewed plan and implement it with subagents where the tasks are independent.
```

## Documentation

- [Architecture](docs/architecture.md): how workflows, discipline skills, artifacts,
  and context control fit together.
- [Design feature workflow](docs/workflows/design-feature.md): the full happy path
  for feature design.
- [Plan implementation workflow](docs/workflows/plan-implementation.md): the plan
  contract between design and execution.
- [Test strategy workflow](docs/workflows/test-strategy.md): risk-based test matrix
  planning for behavior, seams, and verification.
- [PR boundary workflow](docs/workflows/pr-boundary.md): how planned or existing
  work should be split for review, deploy, and rollback.
- [Review plan workflow](docs/workflows/review-plan.md): the quality gate for
  implementation plans before execution.
- [Review PR workflow](docs/workflows/review-pr.md): review modes and finding format.
- [Execute plan workflow](docs/workflows/execute-plan.md): implementation task
  splitting, review gates, and verification.
- [Spec drift check workflow](docs/workflows/spec-drift-check.md): trace final work
  back to agreed artifacts before PR review.
- [Subagents](docs/subagents.md): task briefs, parallelization, and review loops.
- [Extending](docs/extending.md): how to add a workflow or discipline.

## Contributing

Want to add a skill? See [CONTRIBUTING.md](CONTRIBUTING.md). The short version: copy
`skills/example-skill/`, rename the folder, rewrite `SKILL.md`, document any new
workflow contract, test it in a real project, and open a PR.

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
