---
name: review-dependabot-prs
description: >-
  Use when the user wants to review open Dependabot PRs in a repository, check
  dependency changelogs for breaking changes, and get a merge-safety verdict for
  each. Triggers on mentions of Dependabot, dependency update PRs, "review the
  dependency PRs", "are these bumps safe to merge", or batch-reviewing open
  dependency PRs.
license: MIT
metadata:
  author: nacif
  version: "0.1.0"
---

# Review Dependabot PRs

## Purpose

Review every open Dependabot PR in a repository in parallel — one agent per PR —
checking the dependency's changelog between the old and new version, assessing
breaking-change risk, and reporting a per-PR merge verdict plus a summary table.

## When to use

- Use when: the user asks to review, triage, or assess open Dependabot (or other
  bot-authored) dependency PRs, or asks which dependency bumps are safe to merge.
- Do not use when: the user wants to review a single human-authored PR (use a
  normal PR review flow), or wants to *merge/consolidate* dependency PRs without
  review (that is a different task).

## Inputs

Discover these from the environment rather than asking, when possible:

- **Repository**: derive from the current directory's `git remote -v` or
  `gh repo view --json nameWithOwner`. If not in a repo checkout, ask the user.
- **PR author filter**: default to `app/dependabot`. If the project uses a
  different bot (e.g. Renovate), adjust the `--author` filter accordingly.
- **Known-blocked list** (optional): some projects keep a list of dependency
  bumps that are known to fail (incompatible peer deps, pending migrations).
  Check the repo's contributor docs (`CONTRIBUTING.md`, `CLAUDE.md`, or similar
  notes) for one, or ask the user if repeated CI failures suggest a pattern.
  Verdicts for bumps on that list are **DO NOT MERGE** regardless of changelog.

## Procedure

1. **Fetch open Dependabot PRs:**
   ```bash
   gh pr list --author "app/dependabot" --state open --json number,title --limit 50
   ```

2. **Spawn one background agent per PR**, using the prompt template below. Each
   agent must:
   - Read the full PR body: `gh pr view <number> --json body,title` (Dependabot
     embeds release notes and changelog excerpts there)
   - Search the web for the dependency's changelog/release notes covering the
     old-to-new version range
   - Check for breaking changes, deprecations, or behavioral changes
   - Check whether the dependency is direct or transitive: look for it in the
     project's manifest files (`package.json`, `pyproject.toml`, `go.mod`, etc.)
     and search the codebase for imports/usages
   - Check CI status: `gh pr checks <number>`
   - Report: bump type (patch/minor/major), key changes, breaking changes or
     risks, CI status, and a verdict (see criteria below)

3. **Compile a summary table** as agents complete, updating it incrementally:

   ```
   | PR | Package | Bump | Verdict | Notes |
   |----|---------|------|---------|-------|
   ```

4. **Final summary** once all agents finish: group by verdict, highlight any PR
   that needs human attention, and note any recurring failures worth adding to
   the project's known-blocked list.

### Agent prompt template

```
Review Dependabot PR #<NUMBER> for repo <OWNER/REPO>. It bumps **<PACKAGE>** from <OLD> to <NEW> in /<DIRECTORY>.

Your task:
1. Run `gh pr view <NUMBER> --json body,title` to get the full PR body with changelogs
2. Search the web for <PACKAGE> changelog/release notes for versions <OLD> to <NEW>
3. Check for breaking changes, deprecations, or behavioral changes
4. Check whether <PACKAGE> is a direct or transitive dependency (manifest files, imports)
5. Check the PR's CI status: `gh pr checks <NUMBER>`

Report back concisely:
- Version bump type (patch/minor/major)
- Key changes in the update
- Any breaking changes or risks
- CI status (passing/failing)
- Your recommendation: SAFE TO MERGE, NEEDS REVIEW, or DO NOT MERGE
```

### Verdict criteria

- **SAFE TO MERGE**: patch/minor bump, no breaking changes, CI green, clean changelog
- **NEEDS REVIEW**: CI failing, minor bump with notable deprecations, or changelog
  mentions behavioral changes that touch code the project uses
- **DO NOT MERGE**: major bump with breaking changes affecting the project, known
  incompatibility, or the bump is on the project's known-blocked list

## Validation

The task is done when every open Dependabot PR appears in the summary table with
a verdict and a one-line justification, and the final message groups PRs by
verdict. Spot-check that verdicts cite evidence (changelog entry or CI result),
not just the bump type.

## Common failure modes

- **Trusting the bump type alone** → a "patch" release can still break things;
  always read the changelog and CI results before calling something safe.
- **Missing transitive-only dependencies** → a package absent from the codebase's
  imports may still matter if a direct dependency pins it; check the manifest
  before downgrading risk.
- **Stale CI status** → checks may still be running; re-run `gh pr checks` before
  finalizing a NEEDS REVIEW verdict based on pending checks.
- **Repeatedly re-reviewing known-bad bumps** → if the same package fails every
  cycle, recommend recording it in a known-blocked list (and a Dependabot
  `ignore` rule) instead of re-deriving the verdict each time.
