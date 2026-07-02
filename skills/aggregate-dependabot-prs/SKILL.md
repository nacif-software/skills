---
name: aggregate-dependabot-prs
description: >-
  Use when a repo has a backlog of open Dependabot PRs and the user wants them
  consolidated into a few CI-validated aggregate PRs — not reviewed individually
  and not auto-merged. Triggers on "aggregate dependabot", "bundle dependency
  PRs", "consolidate dependabot PRs", or "clean up the dependabot backlog".
license: MIT
metadata:
  author: nacif
  version: "0.1.0"
---

# Aggregate Dependabot PRs

## Purpose

Turn N open Dependabot PRs into a handful of aggregate PRs that each get one CI run, instead of N runs and N rebases. Bundles that pass CI supersede their originals; bundles that fail stay open with a report so a human can bisect. Nothing is ever merged automatically — the final merge is a human decision.

## When to use

- Use when: a repo has several open Dependabot PRs and the user wants them consolidated into CI-validated bundles.
- Do not use when: the user wants individual dependency PRs reviewed for breaking changes (a review task), or wants updates auto-merged.

## Inputs

- `gh` CLI authenticated against the repo, with permission to push branches and open/close/comment on PRs.
- A local clone (all work happens in throwaway git worktrees, never in the user's checkout).
- Repo knowledge, discovered up front — do not assume:
  - **CI gate:** read the CI config (`.github/workflows/*.yml` or equivalent) to learn what validates a PR and which checks are required.
  - **Ecosystems:** read `.github/dependabot.yml` and the manifests/lockfiles present (`package.json` + lockfile, `pyproject.toml` + `poetry.lock`, `go.mod`, `Cargo.toml`, `Gemfile`, ...) to map each PR to an ecosystem and manifest path.
  - **Runtime/tool versions:** note version constraints from manifests or CI config — lockfile regeneration must run under matching versions (use a container if the host doesn't match).

## Procedure

Command sequences, templates, and the state-file schema live in `references/playbook.md`. The shape:

1. **Discover** — `gh pr list --author "app/dependabot" --state open` and parse each title (`bump <pkg> from <old> to <new> ...`) into package, versions, and ecosystem. Skip unparseable PRs with a warning. If the repo keeps a known-blocked list (updates that have repeatedly failed CI before), exclude those so one known-bad bump doesn't poison a bundle. Nothing left → report "Nothing to aggregate." and stop.
2. **Group** — sort by PR number, chunk into groups of at most 5. Small groups keep the blast radius small when CI fails.
3. **Build each group** — fresh worktree off the latest default branch; fetch each PR's ref and cherry-pick its commit (`-X theirs` absorbs the header lines every Dependabot PR rewrites identically); **regenerate the lockfile** with the ecosystem's native tool instead of trusting the merged slices; commit, push, and open an aggregate PR whose body tables every bump and carries `Closes #<original>` footers. Persist a state file per group so the run is resumable.
4. **Wait on CI** — poll `gh pr checks` for each aggregate PR on a few-minute interval using a scheduled wake-up or timer, never a busy loop. Re-read the state files on each tick to pick up where the last one left off.
5. **Resolve each group** — green: close each original with a "Superseded by #<agg>" comment and remove the worktree. Red: report the failing check and the group's dependencies so a human can bisect; leave the aggregate PR, the originals, and the worktree untouched.
6. **Consolidate** — cherry-pick the union of all green groups onto a fresh default-branch worktree, regenerate the lockfile again (per-group locks are stale against the union), open one final PR, and validate via CI. Green: close the group PRs, leave the final PR open for human merge. Red: keep the green group PRs intact as the fallback.
7. **Report** — final summary: each group and its status, the consolidated PR and its status, totals closed.

## Validation

- Every aggregate PR shows all required checks green (`gh pr checks <pr>`) **before** any original is closed.
- Each aggregate diff contains only manifest and lockfile changes — no application code.
- The final summary accounts for every discovered PR: bundled and closed, bundled but red, or skipped (with the reason).

## Common failure modes

- **Hand-merging lockfiles** → never. Combine manifest changes, then regenerate with the native tool; lockfiles that embed a manifest content-hash fail CI fast otherwise.
- **Closing originals before CI is green** → cleanup is gated strictly on green CI, per group.
- **Auto-deleting a worktree path that already exists** → abort and ask the user; it could hold in-progress work.
- **Working in the user's checkout** → always operate in dedicated worktrees.
- **Cherry-pick conflicts beyond what `-X theirs` resolves** → abort that group and leave the worktree for inspection; never resolve dependency conflicts unattended.
- **Regenerating a lockfile under the wrong runtime/tool version** → pin a container to the versions the manifests or CI require.
- **One mega-PR instead of groups** → a single bad bump blocks everything; cap groups at 5.
- **Polling in a tight loop** → use scheduled wake-ups on a ~5-minute interval.

## Supporting files

- `references/playbook.md` — full command sequences, per-ecosystem lockfile regeneration, PR body template, state-file schema, and the edge-case table.
