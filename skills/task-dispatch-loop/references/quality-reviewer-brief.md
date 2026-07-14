# Quality Reviewer Brief Template

Read-only. Do not edit files, apply patches, or commit changes. Spec compliance
already passed for this revision — do not re-litigate requirements here.

## Scope to inspect
- Diff, commit, or worktree: <exact target>
- Source intent: <one line, for context only>
- Local rules: <relevant repo conventions, e.g. AGENTS.md / CLAUDE.md excerpts>

## Check, in order
1. Correctness and user-visible behavior.
2. Regression, failure, boundary, and concurrency risk.
3. Test quality and missing verification.
4. Maintainability and local idioms.
5. Security, privacy, and data-integrity concerns where relevant.

## Output

```markdown
## Verdict
Approved | Findings

## Findings
- [Critical] `<file:line>`: <problem>. Suggested fix: <fix>.
- [Important] `<file:line>`: <problem>. Suggested fix: <fix>.
- [Minor] `<file:line>`: <problem>. Suggested fix: <fix>.
```

State `Approved, no findings` when nothing is wrong. Critical and Important
findings block acceptance; Minor findings may be recorded without blocking.
