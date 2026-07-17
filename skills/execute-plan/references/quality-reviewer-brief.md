# Quality Reviewer Brief Template

This content is the checkpoint review's instructions, passed as the developer/
review instructions for the native Codex review command (`execute-plan`'s Codex
plugin review policy). Read-only — do not edit files, apply patches, or commit
changes. Every task in scope already passed spec review — do not re-litigate
requirements here; check quality across the whole checkpoint's accumulated diff,
not one task at a time.

## Scope to inspect
- Diff, commit, or worktree: <exact target — the PR-boundary group's accumulated
  diff, not a single task>
- Tasks covered by this checkpoint: <task IDs and one-line summaries>
- Source intent: <one line, for context only>
- Local rules: <relevant repo conventions, e.g. AGENTS.md / CLAUDE.md excerpts>

## Check, in order
1. Correctness and user-visible behavior.
2. Regression, failure, boundary, and concurrency risk.
3. Test quality and missing verification.
4. Maintainability and local idioms.
5. Security, privacy, and data-integrity concerns where relevant.
6. Consistency across tasks in this checkpoint — a pattern that's wrong in one
   task and repeated in a sibling task should be reported once, with all
   occurrences listed.

## Output

```markdown
## Verdict
Approved | Findings

## Findings
- [Critical] `<file:line>` (Task <ID>): <problem>. Suggested fix: <fix>.
- [Important] `<file:line>` (Task <ID>): <problem>. Suggested fix: <fix>.
- [Minor] `<file:line>` (Task <ID>): <problem>. Suggested fix: <fix>.
```

State `Approved, no findings` when nothing is wrong. Critical and Important
findings block acceptance; Minor findings may be recorded without blocking.
