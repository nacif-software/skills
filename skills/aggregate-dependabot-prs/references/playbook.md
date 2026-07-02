# Playbook: aggregating Dependabot PRs

Detailed commands for each step of the procedure in `SKILL.md`. `<repo>` is the
repository directory name; `<g>` is the 1-indexed group number of `<N>` total.

## Conventions

| Item | Convention |
|------|------------|
| Worktree path | `../<repo>-dep-agg-<g>` |
| Branch name | `chore/dependabot-aggregate-<YYYYMMDD>-<g>` |
| PR title | `chore(deps): bundle Dependabot updates (group <g>/<N>)` |
| Original PR close comment | `Superseded by #<agg_pr> (aggregate Dependabot bundle).` |
| Group size | 5 |
| CI poll interval | ~5 minutes |

## Step 1: Discover

```bash
gh pr list --author "app/dependabot" --state open --limit 100 \
  --json number,title,headRefName,labels
```

For each PR, parse the title (`bump <pkg> from <old> to <new> in /<dir>`) to extract
package, old version, new version, and the directory. Map the directory (and/or the
PR's ecosystem labels) to a manifest path and ecosystem using what you learned from
`.github/dependabot.yml` and the repo's manifests. Skip and warn for any PR whose
title doesn't parse.

If the repo maintains a known-blocked list (dependencies whose updates repeatedly
fail CI — often kept in a doc, an agent memory, or Dependabot `ignore` config),
exclude those PRs from grouping and note them in the final report.

## Step 3: Build each group

Build groups sequentially in one session; their CI runs proceed in parallel.

**3.1. Worktree off the latest default branch** (substitute the repo's default
branch for `main` throughout):

```bash
git fetch origin main
WORKTREE="../<repo>-dep-agg-${g}"
BRANCH="chore/dependabot-aggregate-$(date +%Y%m%d)-${g}"
git worktree add "$WORKTREE" -b "$BRANCH" origin/main
```

If `$WORKTREE` already exists: abort the run and ask the user to clean up. Never
auto-delete.

**3.2. Cherry-pick each Dependabot commit.** Most Dependabot PRs only modify the
lockfile; some also touch the manifest. Cherry-pick handles both uniformly.

```bash
( cd "$WORKTREE" && git fetch origin pull/<pr1>/head pull/<pr2>/head ... )

# -X theirs absorbs header conflicts (e.g. a lockfile generator-version line that
# every Dependabot PR rewrites to the same value):
for sha in <sha1> <sha2> ...; do
  ( cd "$WORKTREE" && git cherry-pick -X theirs "$sha" )
done
```

If a cherry-pick conflicts beyond what `-X theirs` resolves: abort that group,
leave the worktree for inspection, and report it. Do not resolve dependency
conflicts unattended.

**3.3. Regenerate the lockfile.** Cherry-picking lockfile slices from independent
PRs (each computed against its own base) can leave the lockfile inconsistent with
the cumulative manifest — lockfiles that embed a manifest content-hash make CI
fast-fail on install. Always regenerate with the ecosystem's native tool before
pushing:

| Ecosystem | Regenerate with | Notes |
|-----------|-----------------|-------|
| Poetry | `poetry lock` | `poetry.lock` embeds a `pyproject.toml` content-hash, so this is mandatory. `--no-update` was removed in Poetry 2.x — use the bare command. |
| npm | `npm install --package-lock-only` | |
| pnpm | `pnpm install --lockfile-only` | |
| yarn v1 | usually consistent as cherry-picked (no content-hash); if CI complains, `yarn install` and stage `yarn.lock` | |
| Bundler | `bundle lock` | |
| Go modules | `go mod tidy` | |
| Cargo | `cargo update --workspace` (or verify the picked `Cargo.lock` builds) | |

Run the tool under the runtime version the project pins (check manifests and CI
config). If the host doesn't match, use a container, e.g.:

```bash
docker run --rm -v "$WORKTREE/<manifest-dir>":/work -w /work \
  <language-image:pinned-version> bash -c "<install tool> && <regenerate command>"
```

If regeneration fails: abort that group, leave the worktree, do not push.

**3.4. Commit and push.** Stage only the manifest/lockfile paths that this group
actually touches:

```bash
( cd "$WORKTREE" && \
  git add <manifest and lockfile paths> && \
  git commit -m "chore(deps): bundle Dependabot updates (group ${g}/${N})" && \
  git push -u origin "$BRANCH" )
```

**3.5. Open the aggregate PR.** Body template:

```markdown
Bundles {count} Dependabot updates into a single CI run.

| Package | Bump | Source PR | Ecosystem |
|---------|------|-----------|-----------|
| <pkg>   | <old> → <new> | #<orig> | <ecosystem> |

Closes #<orig1>, #<orig2>, ...

> If another aggregate group merges before this one, the lockfile may conflict.
> Resolve by regenerating it (see the table above) on top of the merged default
> branch — do not hand-merge.
```

**3.6. Persist group state** to `$WORKTREE/.git/aggregate-dependabot-state.json`:

```json
{
  "group": 1,
  "agg_pr": 1234,
  "branch": "chore/dependabot-aggregate-20260701-1",
  "originals": [1201, 1198, 1190, 1185, 1177],
  "deps": [
    {"pr": 1201, "package": "<pkg>", "old": "1.2.3", "new": "1.3.0",
     "ecosystem": "<ecosystem>", "manifest": "<path>"}
  ],
  "status": "ci_pending"
}
```

## Step 4: Wait for CI

```bash
for AGG in <agg_pr_1> <agg_pr_2> ...; do
  gh pr checks "$AGG" --json statusCheckRollup
done
```

Interpretation per PR:

- any check `IN_PROGRESS` / `QUEUED` / `PENDING` → still waiting
- all required checks `SUCCESS` → green
- any required check `FAILURE` / `TIMED_OUT` / `CANCELLED` → red

While any group is `ci_pending`, schedule a wake-up (or ask the user to re-invoke)
in ~5 minutes rather than busy-looping. On every tick, re-read each group's state
file and skip groups whose status is no longer `ci_pending`. If an aggregate PR was
merged or closed externally in the meantime, tear that group down (remove worktree,
drop from state).

## Step 5: Resolve each group

**Green:**

```bash
gh pr close <orig_pr> --delete-branch \
  --comment "Superseded by #<agg_pr> (aggregate Dependabot bundle)."   # each original

git worktree remove "../<repo>-dep-agg-<g>"
```

Set state `status` to `green_cleaned`. The aggregate PR stays open for human merge.

**Red:** print the aggregate PR URL, the failing check name and URL (from
`statusCheckRollup`), and the group's dependencies so a human can bisect. Set state
to `red_failed`. Leave the aggregate PR, the originals, and the worktree intact.

## Step 6: Consolidate green groups

Once every group is `green_cleaned` or `red_failed`, bundle only the **green**
groups into one final PR (red groups stay isolated for investigation):

```bash
git fetch origin main
WT="../<repo>-dep-agg-final"
git worktree add "$WT" -b "chore/dependabot-aggregate-<YYYYMMDD>-final" origin/main

( cd "$WT" && \
  git fetch origin <every PR ref from green groups> && \
  for sha in <every Dependabot commit sha from green groups>; do
    git cherry-pick -X theirs "$sha"
  done )

# Regenerate the lockfile across the union — each per-group lock is stale here:
# (same per-ecosystem table as step 3.3)

( cd "$WT" && git add <lockfile paths> && \
  git commit -m "chore(deps): regenerate lockfile for consolidated bundle" && \
  git push -u origin "chore/dependabot-aggregate-<YYYYMMDD>-final" )
```

Open the consolidated PR: title `chore(deps): consolidated Dependabot bundle
(<N> deps)`; body with the full bump table, a `Closes #<every-original>` footer,
and `Supersedes #<group-pr-1>, #<group-pr-2>, ...`.

Poll its CI as in step 4. Then:

**Green:** close each green group's aggregate PR (`--delete-branch`, comment
`Superseded by #<final> (consolidated bundle).`), remove their worktrees, and leave
the consolidated PR open for human merge. Keep the consolidated worktree until the
human merges, so you can rebase if the default branch moves.

**Red:** leave the consolidated PR open and the green group PRs intact — they
passed individually and remain a valid fallback. Print the failing check and the
union of deps.

## Edge cases

| Case | Handling |
|------|----------|
| No open Dependabot PRs | Print "Nothing to aggregate.", exit. |
| Worktree path already exists | Abort, ask user to remove. Do not auto-delete. |
| Unrecognized ecosystem or unparseable title | Skip the PR with a warning, continue. |
| Cherry-pick conflicts beyond `-X theirs` | Abort that group, leave worktree for inspection. |
| Lockfile regeneration fails | Abort that group, leave worktree, do not push. |
| Aggregate PR merged/closed externally on resume | Tear down (remove worktree, drop from state). |
| Dependabot opens a new PR mid-run | Out of scope this run; the next invocation picks it up. |
| Dep on the known-blocked list | Exclude from grouping; leave its PR open and note it in the report. |
