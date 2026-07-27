---
name: redescribe-pr
description: >-
  Rewrite the title and description of the current branch's open PR from its diff,
  blind to the current title and body. Triggers on "rewrite the PR description",
  "write the PR title and description", or "describe this PR". Never opens a PR.
license: MIT
metadata:
  author: nacif
  version: "0.1.0"
---

# Redescribe PR

Rewrite a PR's title and description from what the branch actually changed —
**blind to the current title and body**, so you describe the diff instead of echoing
a possibly-stale one.

## When to use

- The current branch already has an **open PR** whose title/description is stale,
  thin, or was never written.
- The user asks to "rewrite the PR description", "describe this PR", or similar.

Do **not** use this skill when:

- There is no open PR for the branch — this skill never creates one. Stop and say so.
- The user wants a brand-new PR opened (use your normal PR-open flow instead).
- The user wants to keep and lightly edit the existing text — that defeats the
  blind-rewrite purpose; edit it directly instead.

## Procedure

1. **Find the PR without its title or body.** Fetch only structural fields — never
   add `title`/`body`, and don't run a bare `gh pr view`:

   ```bash
   gh pr view --json number,url,baseRefName,headRefName
   ```

   No PR → stop and tell the user. Never create one.

2. **Read the diff** against the target's merge-base:

   ```bash
   git fetch origin --quiet
   git diff "origin/<baseRefName>"...HEAD
   git log "origin/<baseRefName>"..HEAD --format='%s%n%b'
   ```

3. **Write the title and description** from the diff. If the project or conversation
   carries authoring instructions (a PR template, style rules), follow them;
   otherwise just write it clearly — don't impose a format.

4. **Preview, then apply on approval:**

   ```bash
   gh pr edit <number> --title "<title>" --body-file "<file>"
   ```

Off-limits the whole way: the PR's current title, body, and web page. Fair game: the
diff, commit messages, and project docs. If you accidentally see the old text, say so.

## Success criteria

- Title and body describe **what the diff actually changes**, not what the old
  description claimed.
- The old title/body was never fetched or read (only structural fields in step 1).
- The user saw a preview and approved before `gh pr edit` ran.
- No PR was created, and no other PR fields were touched.

## Common failure modes

- **Running a bare `gh pr view`** (or adding `title`/`body` to `--json`) — this leaks
  the stale text and defeats the skill. Fetch only structural fields.
- **No open PR** — don't create one. Stop and tell the user.
- **Echoing commit-message phrasing verbatim** instead of describing the net change of
  the diff. Summarize the outcome, not the individual commits.
- **Editing without preview/approval** — always show the proposed title and body first.
- **Accidentally seeing the old text** (e.g. from a prior command in context) — disclose
  it to the user rather than silently proceeding.
