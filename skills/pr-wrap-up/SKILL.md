---
name: pr-wrap-up
description: >-
  Use when implementation on a PR branch is done and the PR needs to be finalized
  for human review, without an external second-model review loop. Triggers on
  "wrap up the PR", "finish the PR", "get this ready for review", or a request to
  clean up and ship a draft PR.
license: MIT
metadata:
  author: nacif
  version: "0.1.0"
---

# PR Wrap-Up

## Purpose

Final pass over a finished PR: linters green, AI comment noise removed, self-review
done, reviewer feedback triaged, CI green, draft flipped to ready. The core
discipline: **fix only what is obvious AND adds zero complexity; surface everything
else to the user.**

## When to use

- Use when: implementation on the current branch is complete and a PR already
  exists that needs finalizing for human review.
- Do not use when: no PR exists for the branch (this skill never creates one —
  stop and tell the user), or the implementation itself is still in flux.

## Inputs

- **An authenticated GitHub CLI.** `gh` resolves the repo from the working
  directory's git remote — nothing is hardcoded.
- **The project's lint/format/test commands.** Discover them from the repo, in
  this order: agent instructions file (CLAUDE.md / AGENTS.md), CI workflow files
  (e.g. `.github/workflows/`), package manifests (package.json scripts, Makefile,
  pyproject.toml). If you cannot determine how CI runs lint/tests, ask the user —
  do not guess.
- **The project's commit conventions.** Infer them from recent `git log` messages.

## Procedure

Work through these stages in order. Track one todo per stage.

### 1. Identify the PR

```bash
gh pr view --json number,isDraft,url,title,headRefName
```

No PR for the current branch → stop and tell the user. Never create one.

### 2. Linters

Run the project's lint/format commands (see Inputs) the way CI runs them. Fix any
failures — formatting fixes are always safe to apply.

### 3. Remove AI comment noise

Review only the comments **this PR added** (`git diff <base>...HEAD`), and judge
each one:

| Comment type | Action |
|---|---|
| Narrates WHAT the code does (`# loop through users`) | Delete |
| Summary/changelog (`# Added as part of refactor`, `# New helper`) | Delete |
| Section banners restating the function name | Delete |
| Explains WHY / non-obvious constraint (locks, ordering, API quirks, workarounds) | Keep |
| TODO with a real owner/condition | Keep |
| Docstrings required by project conventions | Keep |

Test: would a competent reader learn something from this comment that the code
doesn't already say? No → delete.

### 4. Final self-review

Read the full diff with fresh eyes. Look for: leftover debug code, dead code,
accidental scope creep, unhandled error paths, secrets, files that shouldn't be in
the PR. Fix what's clear-cut; surface anything structural.

### 5. Triage PR reviews and comments

```bash
gh pr view --json reviews,comments
gh api repos/{owner}/{repo}/pulls/<number>/comments   # inline review comments
```

For each unresolved piece of feedback, classify it with these guard clauses, in
order:

1. Scope or product question? → **Surface to user** with a recommendation.
2. Not an obvious fix (typo, off-by-one, wrong name, missing null check) — or in
   doubt? → **Surface to user** with a recommendation.
3. Fix adds ANY complexity (new file, new abstraction, new dependency, broader
   refactor)? → **Surface to user** with a recommendation.
4. Otherwise → **Fix it now.**

**"Adds complexity" is disqualifying even when the suggestion is good.** A
reviewer proposing "extract this into a shared module" may be right — but a new
file/abstraction/dependency changes the shape of the PR, so it goes to the user,
not into the diff. "The reviewer suggested it" is not authorization to expand the
PR.

When in doubt between fix and surface: **surface.** Present each surfaced item
with your recommendation (do it in this PR / follow-up PR / decline) so the user
makes a one-word decision.

### 6. Commit, push, monitor CI

Run the project's test suite locally first if feasible. Commit fixes following the
project's commit conventions, push, then:

```bash
gh pr checks <number> --watch
```

Run this in the background and report check results as they land. A failing check
→ diagnose and fix, push, re-watch. Don't mark ready while anything is red or
pending.

### 7. Mark ready

Only when all checks are green and no surfaced items are blocking:

```bash
gh pr ready <number>
```

If the PR wasn't a draft, skip this.

## Validation

- `gh pr checks <number>` shows every check completed green — not pending, not
  skipped-by-failure.
- The PR is no longer a draft (if it started as one).
- Finish with a short summary: lint status, comments removed, fixes applied, items
  surfaced (each with your recommendation), CI status.

## Common failure modes

- "The reviewer suggested it, so it's pre-approved" → suggestions that reshape the
  PR still go to the user.
- "It's a clear improvement" → improvement ≠ obvious AND complexity-free; both are
  required.
- "I'll just quickly extract this helper" → new abstractions are never "quick";
  surface it.
- Deleting WHY comments along with WHAT comments → concurrency, ordering, and
  workaround comments stay.
- Editing comments in files the PR didn't touch → only clean comments in this PR's
  diff.
- Answering scope questions on the reviewer's thread yourself → scope/product
  questions always go to the user.
- Marking ready while checks are pending → green means completed-green, not
  "running".
- Batching surfaced items vaguely ("a few comments need attention") → list each
  item with a concrete recommendation.
