---
name: mental-model
description: >-
  Use when a developer wants to quickly understand what a PR, branch, or diff changes before
  reviewing, testing, or building on it: how the feature worked before, what changes, which
  tables, models, services, endpoints, or jobs are new, and what users will notice, in 4 to 16
  short bullets. Triggers on "mental model", "/mental-model", "help me understand this PR",
  "what does PR #1234 actually change", "catch me up on this branch", "what was this feature
  before", "give me the gist of this diff", or a bare PR link with a request to explain it.
  Not a code review and not a stakeholder brief.
license: MIT
metadata:
  author: nacif
  version: "0.1.0"
---

# Mental Model

Give a developer the smallest set of facts that lets them hold the whole change in their head:
what existed before, what this changes, what new building blocks it adds, and what a user will
notice. The output is 4 to 16 short bullets: a map, not a review. Readers consistently want it
shorter than feels natural, so err on the side of fewer, tighter bullets.

A diff shows lines, not meaning. A developer opening a PR cold needs the "before" picture first
(otherwise the "after" is noise), then the delta, then the structural additions they will have
to remember exist.

## When to use

- The user points at a PR, branch, commit range, or local diff and wants to understand it.
- Before reviewing, testing, or stacking work on someone else's change.

Do **not** use this skill when:

- The user wants bugs, risks, or code-quality findings: that is a code review.
- The user wants a release note or stakeholder-facing explanation: different audience.
- The user wants the PR title or description written.

## Inputs

A PR number or URL, a branch, a commit range, or nothing (then use the current branch against
its merge base with the default branch). If a PR URL points at one file (`#diff-...` anchor),
still model the whole PR.

## Procedure

1. **Read intent.** For a PR: `gh pr view <pr> --json title,body,baseRefName,headRefName,files,commits`.
   The description and commit messages say what the author meant; treat them as claims to
   confirm, not facts.

2. **Read the change.** `gh pr diff <pr> --name-only`, then `gh pr diff <pr>`. GitHub refuses
   diffs over 300 files; then fetch without creating branches (`git fetch origin pull/<n>/head`,
   then `git diff --stat <base>...FETCH_HEAD`), or for a merged PR diff the merge commit against
   its first parent. On a large diff, read the files that carry behavior (services, models,
   migrations, routes, pages) before tests and generated files.

3. **Reconstruct the "before".** This is the step most worth the effort, because the diff and
   the description usually omit it. For changed files that carry behavior, read the base
   version (`git show origin/<base>:<path>`) and, when needed, its callers. Answer: what did
   this feature do before, for whom, and how was it triggered? If the PR creates something
   brand new, "before" is what users had to do without it.

4. **Inventory structural additions.** Learn where each category lives in this repo from its
   agent instructions (`AGENTS.md`, `CLAUDE.md`), docs, and directory layout, then check each:
   - Schema migrations, new or changed data models, columns, backfills
   - Services, repositories, controllers, API endpoints, schemas
   - Background jobs, scheduled tasks, queue workers, agent tools
   - Data-layer models (warehouse transforms, semantic-layer definitions)
   - Frontend pages, routes, major shared components
   - Feature flags, env vars, secrets, new external services or dependencies

   Report only what exists, plus one short "no new tables/endpoints" bullet when the reader
   would expect some: that absence is part of the model.

5. **Determine the user-visible effect.** Who notices (end user, admin, internal only, nobody),
   where in the product, and whether it is behind a flag or role.

6. **Write the model** in the format below. Verify every bullet against the code; mark anything
   confirmed only by the PR description with "(per PR description)" or drop it.

## Output format

```markdown
**<PR title or short name>**: <one sentence: what this PR is, in plain words>

- **Before:** <how it worked / what existed>
- **Change:** <the core behavioral delta>
- **New:** <table / model / service / job / endpoint, and what it's for>
- **User sees:** <what a user notices, where, and who>
- **Rollout:** <flag, migration, manual step>
```

Rules:

- **Bullet count follows conceptual size, not file count.** Ask how many ideas a developer
  must hold. A flag that flips one setting is about 4 to 5 bullets even across 8 files; a
  feature with a table, a service, and a page is about 8 to 10. Reserve 12 to 16 for PRs that
  change several independent things. A 500-file reskin is still one idea plus a few
  consequences.
- **One fact per bullet, at most about 15 words.** No semicolons, no parentheticals, no lists
  of more than three. If a bullet needs a clause to be true, the clause is detail; drop it.
- **The cut test.** For each bullet ask: would the reader's picture of the system be *wrong*
  without it? If it would only be *less detailed*, cut it. Mechanics (how a value is threaded
  through, which helper was renamed), exact numbers, copy tweaks, docs or tooling side-additions,
  test changes, and dependency bumps almost never pass.
- **At most one identifier per bullet**, in backticks, and only when the reader will need to
  find it. Skip file paths.
- **Concepts over code.** "Retries now happen in the background job, not the request" beats
  "moved `retry()` to `jobs.py`".
- **Order:** Before, Change, New, User sees, Rollout. Labels are prefixes on a flat list;
  reuse or drop them as needed.
- **No closing "Watch", "Gotchas", or "Risks" section.** Bugs, gaps, and cost concerns belong in
  a review. A single **Rollout** bullet may name what the developer must do to run the code
  (restart workers, create a flag, merge order).

## Example

Input: "mental model for #1234" (hypothetical PR)

**Workspace subscriptions**: self-serve workspaces now have to pay after a trial.

- **Before:** Self-serve workspaces were free forever, with no billing state.
- **Change:** New workspaces get a 14-day trial, then features lock until they pick a plan.
- **New:** `workspace_subscriptions` table mirrors each workspace's Stripe subscription status.
- **New:** A Stripe webhook endpoint keeps that table in sync.
- **User sees:** A Billing page in Settings and a paywall banner after the trial.
- **Rollout:** Flag `self_serve_subscriptions` gates the paywall; Stripe secrets needed per env.

(Illustrative only. Always derive the content from the actual change.)

## Success criteria

- 4 to 16 bullets, scaled to the number of ideas, each about 15 words or fewer.
- At least one **Before** bullet that the diff alone would not have told the reader.
- States explicitly whether anything structural is new, and what users notice (or that nothing
  changes for them).
- Every bullet is backed by code; description-only claims are marked or dropped.
- No review findings, no file tours.

## Common failure modes

- **Bullets that grow clauses.** Thirty-word bullets defeat the point. Split or cut.
- **Inflating the count to match the diff size.** Big diffs are often one idea.
- **A review section sneaking in.** "Watch" or "Gotchas" lines that flag bugs or cost issues
  turn the map into a review. Leave them out.
- **Skipping the before.** Restating the PR description gives the after without the before;
  read the base version of the files.
- **Narrating mechanics.** Context vars, helper renames, and import moves rarely change the
  reader's model.
