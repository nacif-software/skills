---
name: review-and-wrap-up-pr
description: >-
  Use when a PR branch is done and the user wants it hardened by an external Codex
  review loop (via the official OpenAI Codex plugin for Claude Code) before being
  finalized for human review. Triggers on "review and wrap up the PR", "codex review
  then ship", "harden and finish the PR", "run a codex review loop on this branch".
license: MIT
metadata:
  author: nacif
  version: "0.2.0"
---

# Review and Wrap-Up PR

## Purpose

Harden a finished PR branch with an adversarial second-model review before any human
sees it: Codex — driven through the official OpenAI Codex plugin for Claude Code
([openai/codex-plugin-cc](https://github.com/openai/codex-plugin-cc)) — reviews the
diff, you fix only the genuine must-fix / should-fix findings, re-review until
convergence, then finalize the PR (lint, self-review, CI, draft → ready). The core
discipline throughout: **fix only what is a genuine issue AND adds zero unnecessary
complexity; surface everything else to the user.**

## When to use

- Use when: implementation on a PR branch is complete and the user wants it reviewed
  and hardened before it goes to human review.
- Do not use when: the user wants a review only, with no fixes applied (run just the
  review step and report), or there is no PR and the user has not asked to review
  uncommitted changes. **Never create a PR from this skill.**

## Inputs

- `gh` CLI authenticated for the repo's host.
- The official OpenAI Codex plugin installed and authenticated. Locate its runtime
  once (used by every review in the loop):

  ```bash
  companion="$(ls -d "$HOME"/.claude/plugins/cache/openai-codex/codex/*/scripts/codex-companion.mjs 2>/dev/null | sort -V | tail -1)"
  ```

  If nothing is found, stop and have the user install it
  (`/plugin marketplace add openai/codex-plugin-cc`, then
  `/plugin install codex@openai-codex`). If reviews fail with a setup or auth error,
  direct the user to `/codex:setup` — don't improvise alternate auth flows or fall
  back to raw `codex` CLI calls.
- The PR for the current branch: `gh pr view --json number,isDraft,url,title,headRefName,baseRefName`.
  If there is no PR, tell the user; you may still review uncommitted changes if they ask.
- Project specifics — **discover, never assume**: the base branch (`baseRefName`
  above), the lint/format/test commands (check `CLAUDE.md`/`AGENTS.md`/`CONTRIBUTING.md`,
  CI config, package manifests), whether tooling must run inside a container or VM, and
  whether the repo squash-merges PRs (repo merge settings, or ask the user).

## Procedure

Two phases, in order. Track them as todos: one for the review loop, one for the wrap-up.

### Phase 1 — Codex review loop

**1. Check out the branch in a dedicated worktree.** This skill edits the branch
(fixes, sync with base, tests), so isolate it from the user's checkout:

```bash
git fetch origin
git worktree add .worktrees/<pr-name> <headRefName>
cd .worktrees/<pr-name>
```

Skip this only if the user is already on the PR branch and explicitly wants the work
done in place. Two worktree gotchas to resolve **before** the loop starts:

- A fresh worktree lacks gitignored local files (env files, `node_modules`, build
  caches). Copy or symlink what the project's tooling needs from the main checkout,
  and follow any worktree conventions in the project's contributor docs.
- If the project runs tooling through a long-lived container (`docker compose exec …`),
  that container usually mounts the *main* checkout — it will not see the worktree's
  edits. Find a mode that runs against the worktree's own files (a test compose file,
  a one-off `docker compose run` from the worktree directory, or host tooling); the
  project's CI config usually shows one.

**Committing (every commit in this flow):** use a plain `git commit`. Do **not** pass
`--no-verify` or other hook-bypassing flags — let the project's hooks run. If a hook
genuinely errors, surface that to the user; don't bypass it.

**2. Sync with the base branch** so Codex reviews the real merged state and CI won't
go red later from unrelated drift:

```bash
git fetch origin
git merge origin/<baseRefName>
```

Resolve conflicts and commit the merge before continuing. Uncommitted changes blocking
the merge → surface to the user rather than stashing or forcing. (Merge, not rebase —
the branch is likely already pushed.)

**3. Run a Codex review** through the plugin runtime (the same path `/codex:review`
uses), from the worktree directory — it reviews the CWD's git state:

```bash
node "$companion" review --wait --base "origin/<baseRefName>"
```

- A `--base` review diffs **committed state only** — commit everything first, or Codex
  reviews stale code.
- Reviews take a few minutes; progress logs go to stderr, the report to stdout. Give
  the Bash call a generous timeout, or run it in the background and collect the output
  when it finishes.
- The report is `# Codex Review` with findings as `- [P0|P1|P2|P3] title — file:line`
  plus an explanation each. A clean pass is a short summary with no findings list.
- On a setup or auth error, stop and direct the user to `/codex:setup`.

**4. Plan the fixes.** No P0/P1/P2 findings → skip to Phase 2. Otherwise draft a fix
plan for this round — via a planning subagent if your harness has one, else yourself —
from only the P0–P2 findings plus the relevant file references, under this constraint:

> Produce a step-by-step plan to fix ONLY these specific findings. Do not propose, add,
> or change anything not directly required to resolve them — no refactors, no renames,
> no new abstractions, no "while we're here" improvements. Each step must trace back to
> a specific finding. Keep the change as small as possible.

**5. Implement the fixes**, applying the triage rules:

- **P3** → never fixed. Collect them to report at the end.
- **Pre-existing / out-of-diff** → only fix findings in code **this PR changes**. A
  P0–P2 in untouched code is scope creep — surface it with a one-line reason.
- **False positives** (your judgment) → don't fix; record in the collected list.
- **Complexity guard:** if a genuine fix would reshape the PR (new file, new
  abstraction, new dependency, broader refactor), do **not** silently expand the PR —
  surface it to the user instead.

After fixing, run the project's formatters/linters and the relevant tests — against the
worktree's code (see step 1's container gotcha) — so the next review sees clean code.

**6. Commit and re-review.** Commit the round's fixes first (a `--base` review only
sees commits, so uncommitted fixes are invisible to Codex), then re-run step 3.
Intermediate commits are fine; if the repo doesn't squash-merge, tidy history at the
very end, never mid-loop. Repeat review → plan → fix → commit → re-review.

**Exit condition:** stop when no *actionable, in-scope* P0/P1/P2 findings remain. A
finding you consciously decided not to fix (pre-existing, or a complexity-reshaping fix
you surfaced) counts as resolved for loop purposes. Convergence means "everything
fixable in scope has been fixed," not literally "Codex returns zero findings."
Guardrails:

- Cap at ~4–5 iterations. If new in-scope P0–P2 findings keep appearing or oscillating,
  stop and surface the situation instead of looping forever.
- If Codex re-raises a finding you intentionally skipped, don't flip-flop — keep your
  decision and note the disagreement for the user.

Keep a running tally across iterations: what was fixed, and the collected P3 and
deliberately-skipped findings.

### Phase 2 — Wrap-up

If a dedicated PR-finalizing skill (e.g. `pr-wrap-up`) is available in your
environment, invoke it; otherwise follow `references/wrap-up-checklist.md`. Either way,
stay in the worktree and keep running lint/tests against the worktree's code. Remove
the worktree (`git worktree remove .worktrees/<pr-name>`) only after the PR is pushed
and marked ready, and nothing is left uncommitted.

Append the **Codex review summary** to the final report:

- Iterations run and what was fixed (with file:line).
- All remaining P3 findings (file:line) for the user's follow-up.
- Any P0–P2 surfaced instead of fixed, with your recommendation.

## Validation

- The last Codex review reports no actionable, in-scope P0/P1/P2 findings.
- The project's own lint and test commands pass, run against the worktree's code.
- CI is green and the PR is marked ready for review.
- The final report includes the iteration tally and every surfaced-but-unfixed finding.

## Common failure modes

- "I'll fix the P3 nits too" → no; only P0–P2 get fixed, the rest are surfaced.
- "While fixing this finding I'll tidy the nearby code" → the diff stays scoped to the
  listed findings only.
- "It's a P1, so a new module/dependency is justified" → a real P1 still doesn't
  authorize silently reshaping the PR; surface it.
- "The loop keeps finding new things, I'll keep going" → cap iterations and surface.
- Re-reviewing with uncommitted fixes → a `--base` review only sees commits; commit
  first or Codex re-reviews the pre-fix code.
- "The review errored, I'll retry the same command a few times" → read the error; if
  it's setup/auth, send the user to `/codex:setup` and stop.
- "The plugin isn't installed, I'll use the codex CLI directly" → no; have the user
  install the plugin instead.
- "I'll mark ready before re-review converges" → wrap-up only starts after no P0–P2
  remain.
- Running tests through a container that mounts the main checkout → they silently test
  the wrong code; verify your test command sees the worktree's edits.

## Supporting files

- `references/wrap-up-checklist.md` — the fallback PR-finalizing checklist for Phase 2.
