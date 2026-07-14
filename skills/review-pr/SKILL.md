---
name: review-pr
description: >-
  Use when the user asks to review a pull request, review a branch or diff, comment
  review feedback, apply PR review changes, or choose between review-only and fix mode.
license: MIT
metadata:
  author: nacif
  version: "0.2.0"
---

# Review PR

## Purpose

Review a branch or pull request against its intent, then either prepare review
comments or apply accepted review changes with verification.

## When to use

- Use for PR review, branch review, diff review, pre-merge review, or review feedback.
- Use when the user wants either comments for a PR or help applying review changes.
- Do not use for designing new work from scratch. Use `design-feature` first.

## Review engine policy

Prefer native Codex review for code-quality findings. In Claude Code, the preferred
interactive command is `/codex:review --base <ref> --wait`. Some installations mark
the command user-only; ask the user to invoke it rather than claiming the workflow ran
it. Use the slash command only after confirming the active Codex configuration selects
`gpt-5.6-sol`; otherwise use the explicitly pinned CLI command below.

For autonomous review, run:

```bash
codex review -c 'model="gpt-5.6-sol"' --base <ref>
codex review -c 'model="gpt-5.6-sol"' --uncommitted
```

`gpt-5.6-sol` is the only GPT model allowed for this review path. If native Codex
review is unavailable, report `CODEX_REVIEW_UNAVAILABLE`; use a strongest-available
Anthropic reviewer only after the user accepts that downgrade.

## Procedure

1. Identify the review target:
   - PR URL/number if provided.
   - Otherwise base branch and current branch.
   - If unclear, inspect git remotes and branch state before asking.
2. Discover intent:
   - Read PR description, linked issue/spec, commits, or local design docs.
   - Read test strategy and spec drift report when present.
   - Read a PR boundary artifact when one exists.
   - For planned feature work with durable artifacts but no drift report, run or
     request `spec-drift-check` before readiness review.
   - If no intent exists, infer from diff and state the assumption.
3. Discover repo rules and verification commands before reviewing.
4. Inspect the diff against the correct base.
5. Run or ingest native Codex review using the policy above. Treat its output as review
   evidence, not as permission to skip intent, boundary, or drift checks.
6. Review in this order:
   - Correctness and user-visible behavior.
   - Spec or intent alignment.
   - PR boundary alignment: unrelated work, missing split, unsafe stack, or follow-up
     accidentally included.
   - Spec drift alignment: missing scope, added scope, changed decisions, or accepted
     drift.
   - Missing tests or weak verification.
   - Maintainability and local idioms.
   - Security, privacy, data integrity, migrations, and compatibility where relevant.
7. Report findings by severity:
   - Critical: likely breakage, data loss, security issue, or failed core requirement.
   - Important: should fix before merge.
   - Minor: optional cleanup.
8. Ask the user to choose a mode:
   - A: Comment review to PR.
   - B: Apply review changes.

## Mode A: comment review to PR

Prepare concise comments that can be posted to the PR. Include file and line when
available, severity, problem, and suggested fix. Do not apply code changes.

If a GitHub/GitLab CLI is configured and the user asked to post comments, use the
project's normal review command. Otherwise return comments as Markdown.

## Mode B: apply review changes

1. Re-check each finding before changing code.
2. Fix Critical and Important findings unless the user narrows scope.
3. Preserve user changes and unrelated work.
4. Run targeted verification after each fix cluster.
5. Run the full appropriate verification before completion.
6. Run `spec-drift-check` again if fixes changed scope, behavior, test strategy, PR
   boundary, or accepted plan decisions.
7. Summarize applied fixes, rejected findings with reasons, and remaining risks.
8. Use `verification-gate` before saying the branch is ready.

## Review output format

```markdown
## Findings
- [Critical] `<file:line>`: <problem>. Suggested fix: <fix>.
- [Important] `<file:line>`: <problem>. Suggested fix: <fix>.
- [Minor] `<file:line>`: <problem>. Suggested fix: <fix>.

## Questions or assumptions
- <only if needed>

## Mode
Choose A to comment on the PR, or B to apply accepted changes.
```

## Common mistakes

- Reviewing only style while missing intent or correctness.
- Applying review feedback without verifying the finding is real.
- Posting vague comments that do not name the fix.
- Claiming the PR is ready without fresh verification.
- Ignoring a PR boundary artifact and reviewing only the raw diff.
- Ignoring a spec drift report or test strategy artifact.
- Applying review fixes that change scope without re-running `spec-drift-check`.
- Silently using a different GPT model when native Codex review requires
  `gpt-5.6-sol`.
- Treating native review output as a substitute for checking the source intent.

## Success criteria

- The review uses the correct base and stated intent.
- The review accounts for spec drift and test strategy artifacts when present.
- Native Codex review used `gpt-5.6-sol`, or the report names an accepted downgrade.
- Findings are severity-ranked and actionable.
- Mode A produces comments ready for the PR.
- Mode B applies only verified fixes and reports fresh evidence.
- Boundary or drift changes route back to `pr-boundary` or `spec-drift-check` before
  readiness claims.
