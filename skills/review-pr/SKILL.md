---
name: review-pr
description: >-
  Use when the user asks to review a pull request, review a branch or diff, comment
  review feedback, apply PR review changes, or choose between review-only and fix mode.
license: MIT
metadata:
  author: nacif
  version: "0.3.0"
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

Code-quality findings come from the official OpenAI Codex plugin for Claude Code
([openai/codex-plugin-cc](https://github.com/openai/codex-plugin-cc)) — the same
plugin `review-and-wrap-up-pr` uses. Not a bare `codex` CLI call, not an invented
model-override flag, and not a generic Claude reviewer's own opinion.

**Prerequisite:** the plugin is installed and authenticated. Locate its runtime
once:

```bash
companion="$(ls -d "$HOME"/.claude/plugins/cache/openai-codex/codex/*/scripts/codex-companion.mjs 2>/dev/null | sort -V | tail -1)"
```

If nothing is found, report `CODEX_PLUGIN_UNAVAILABLE`. Have the user install it
(`/plugin marketplace add openai/codex-plugin-cc`, then
`/plugin install codex@openai-codex`) rather than falling back to a raw `codex`
CLI call. Setup or auth errors route to `/codex:setup`.

**Dispatch a fresh subagent** whose only job is to locate the companion script and
run it — do not run the command directly in the coordinator's own shell:

```bash
node "$companion" adversarial-review --wait --base <ref> "<PR intent, boundary, and drift context>"
# or, for uncommitted work:
node "$companion" adversarial-review --wait --scope working-tree "<review brief>"
```

Use `adversarial-review`, not plain `review` — pass the intent, PR boundary, and
spec drift context discovered in the procedure below as its focus text so the
review isn't context-free. The subagent returns the report verbatim as the
verdict; it does not summarize or edit it.

There is no model-pinning flag on this command — only the companion's separate
`task` command exposes `--model`. The plugin's configured backend model is the
review engine here; do not invent a per-call override. If the plugin is
unavailable, report `CODEX_PLUGIN_UNAVAILABLE`; use a strongest-available
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
5. Dispatch Codex plugin review using the policy above, passing the intent, PR
   boundary, and spec drift context from steps 2-3 as focus text. Treat its output
   as review evidence, not as permission to skip intent, boundary, or drift checks.
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
- Running a raw `codex` CLI call, or inventing a model-override flag, instead of
  dispatching the installed Codex plugin's companion script.
- Running the companion script directly in the coordinator's shell instead of
  dispatching a fresh subagent to run it.
- Calling `review` when `adversarial-review` was needed to carry the discovered
  intent/boundary/drift context as focus text.
- Treating Codex plugin review output as a substitute for checking the source intent.

## Success criteria

- The review uses the correct base and stated intent.
- The review accounts for spec drift and test strategy artifacts when present.
- Codex plugin review ran through a dispatched subagent with the intent/boundary/
  drift context as focus text, or the report names an accepted downgrade.
- Findings are severity-ranked and actionable.
- Mode A produces comments ready for the PR.
- Mode B applies only verified fixes and reports fresh evidence.
- Boundary or drift changes route back to `pr-boundary` or `spec-drift-check` before
  readiness claims.
