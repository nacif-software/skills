# Review PR Workflow

## Purpose

`review-pr` gives agents a repeatable review path for pull requests, branches, and
diffs. It supports two modes:

- Mode A: prepare or post PR review comments.
- Mode B: apply accepted review changes and verify them.

For code-quality review, use `codex-review` with `gpt-5.6-sol`. In Claude Code, that
skill automatically dispatches the OpenAI Codex plugin agent with a fresh, read-only
brief containing this workflow's target, intent, artifacts, priorities, and output
contract. Direct CLI review, the user-only `/codex:review` command, and the plugin
Stop hook do not satisfy the whole-branch gate.

## Flow

```text
review request
  -> identify target and base
  -> discover intent
  -> read or request spec-drift-check for planned feature work
  -> discover repo rules and verification commands
  -> inspect diff
  -> codex-review plugin agent
  -> validate Codex findings against intent and artifacts
  -> report findings by severity
  -> ask mode
     -> A: comment review to PR
     -> B: apply review changes
```

## Target discovery

The agent should prefer explicit user input. If the user gives no PR URL or number,
inspect git state:

- Current branch.
- Upstream branch.
- Likely base branch.
- Open PR if the platform CLI can identify it.

If the base remains ambiguous, ask before reviewing.

## Intent discovery

Review against the work's stated purpose, not only the diff. Sources include:

- PR description.
- Linked issue.
- Design doc or implementation plan.
- Test strategy.
- PR boundary artifact.
- Spec drift report.
- Commit messages.
- Nearby tests and changed files.

If no source exists, infer intent from the diff and state the assumption.

## Severity model

- Critical: likely breakage, data loss, security issue, or failed core requirement.
- Important: should fix before merge.
- Minor: optional cleanup, naming, clarity, or future maintainability.

Findings should be actionable. Each finding names the problem and the expected fix.

## Boundary alignment

When a PR boundary artifact exists, review whether the current diff matches it.
Findings should call out unrelated cleanup, missing split work, unsafe stack order,
or follow-up work that accidentally entered the PR.

## Drift and test alignment

When a spec drift report exists, review whether Critical and Important drift was
fixed or explicitly accepted. When a test strategy exists, review whether promised
tests and checks landed or whether changes to the strategy are explained.

## Mode A: comment review

Mode A does not edit files. The agent produces review comments ready for a PR.

Each comment should include:

- Severity.
- File and line when available.
- Problem.
- Suggested fix.

If the user explicitly asks to post comments and the repo has a configured CLI, the
agent may post them. Otherwise it returns Markdown.

## Mode B: apply changes

Mode B edits files. The agent must:

1. Re-validate each finding before editing.
2. Fix Critical and Important findings unless the user narrows scope.
3. Avoid unrelated refactors.
4. Preserve unrelated user changes.
5. Run targeted verification after fix clusters.
6. Re-run `spec-drift-check` if fixes alter scope, behavior, test strategy, PR
   boundary, or accepted plan decisions.
7. Run the broad appropriate verification before completion.

Rejected findings must be listed with technical reasons.

## Success criteria

- Review uses the correct base and intent.
- Review accounts for drift and test strategy artifacts when present.
- Findings are ordered by severity.
- Comments are concrete enough to act on.
- Applied fixes are verified with fresh evidence.
- Applied fixes that change scope are checked for drift before readiness claims.
