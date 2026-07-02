---
name: post-deploy-changelog
description: >-
  Use when the user wants to write a changelog or release notes for a production
  deploy and (optionally) post them to a team chat channel. Triggers on mentions of
  changelog, release notes, deploy notes, prod deploy announcement, "post the
  changelog", "changelog for PR <n>", or "what's shipping in this deploy".
license: MIT
metadata:
  author: nacif
  version: "0.1.0"
---

# Post Deploy Changelog

## Purpose

Find the production-deploy PR (open or recently merged), turn the changes it ships
into concise product-facing release notes, and post them to the team's changelog
channel in that channel's established style.

## When to use

- Use when: a production deploy is about to ship or just shipped and someone wants
  release notes for it; the user points at a specific deploy PR and asks for a
  changelog; the user asks "what's in this deploy?".
- Do not use when: the user wants a `CHANGELOG.md` file maintained in the repo, or
  full commit-by-commit history — this skill produces curated, human-facing deploy
  announcements.

## Inputs

Discover each of these once; don't guess.

- **Target repo.** Use the current directory's repo: `gh repo view --json
  nameWithOwner` (or parse `git remote get-url origin`). If the user names a repo,
  use that.
- **Deploy convention.** Teams ship differently. Check, in order: a deploy PR
  between long-lived branches (e.g. an open or recently merged PR whose base is a
  production/release branch and head is the default branch — `gh pr list --base
  <prod-branch> --state all`), release tags (`gh release list` / `git tag`), or a
  deploy label/title convention. If none is evident, ask the user how deploys are
  cut in this repo.
- **Destination channel.** Ask the user, or read it from project docs (README,
  CLAUDE.md, CONTRIBUTING) if they record one. Remember it for the session.
- **House style.** Read the last several changelog posts in the destination channel
  and match them: title line, bullet characters, length, tone, whether people get
  cc'd. Do not impose your own format on a channel that already has one.

## Procedure

1. **Find the deploy PR.** If the user gave a PR number, use it. Otherwise apply the
   repo's deploy convention. Prefer an **open** deploy PR (about to ship); if none,
   take the most recently merged one (just shipped).

2. **Enumerate what it ships.** The cleanest unit is one bullet per merged feature
   PR. Scope strictly to the un-deployed range so nothing is re-announced:
   ```bash
   git fetch origin --quiet
   git log --oneline origin/<prod-branch>..origin/<default-branch> | grep -E '\(#[0-9]+\)'
   ```
   For an already-merged deploy PR, use `gh pr view <n> --json commits,title,body,url`
   instead. Read each feature PR's body for intent (bodies are often auto-generated
   summaries), but trust the merged-PR list for what actually ships.

3. **Curate into product-facing notes.** This is the judgment that matters:
   - Lead with what users/teammates notice. Order: new integrations & features →
     UX improvements → notable fixes → internal cleanup (at most one line, often
     omitted entirely).
   - Group related commits into one bullet; never transcribe every commit.
   - Omit unless notable: dev-infra and tooling, CI, pure refactors, test-only
     changes, dependency bumps, backend perf with no user-visible effect.
   - Append "(under feature flag)" or the channel's equivalent to anything gated
     and not yet on for everyone.
   - If a bullet improves something announced in a previous post, frame it as a
     refinement, not a brand-new feature — skim recent channel posts if unsure.
   - cc/mention people only if the channel's precedent does, and only when a line
     is directly in their lane. Never ping by default.

4. **Draft in the house format** derived from the channel's recent posts. If the
   channel has no prior changelog posts, default to a short title line plus plain
   bullets.

5. **Confirm, then post.** Show the user the draft. Posting to a shared channel
   needs explicit user go-ahead — if they already said "post it", post directly;
   otherwise wait for a clear yes. Post with whatever Slack/chat tool is connected
   and return the message link. If no chat tool is available, hand the user the
   final paste-ready text instead and say so — that is a successful outcome, not a
   failure.

## Validation

- The bullet list maps 1:1 onto the un-deployed range — nothing announced that
  isn't in it, nothing user-facing in it left out.
- The draft visually matches the channel's recent posts (title, bullets, length).
- If posted: fetch or link the message to confirm it landed in the right channel.

## Common failure modes

- Listing every commit instead of grouping into a handful of product-facing bullets.
- Announcing internal/infra/test/refactor commits that mean nothing to readers.
- Forgetting the feature-flag annotation on gated features — sets wrong expectations.
- Re-announcing a feature that shipped in a prior deploy — the
  `<prod-branch>..<default-branch>` range guards against this; respect it.
- Posting before the user has approved the draft.
- Using your own markdown formatting instead of the channel's established style.
- Assuming a deploy convention (e.g. main→production PRs) that this repo doesn't
  use — verify it or ask.
