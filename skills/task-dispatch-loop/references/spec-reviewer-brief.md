# Spec Reviewer Brief Template

Read-only. Do not edit files, apply patches, or commit changes.

## Task under review
- Task ID: <id>
- Source artifact: `<design/plan/PR path>`
- Acceptance criteria: <copied from the task text, not paraphrased>

## Scope to inspect
- Diff, commit, or worktree: <exact target>
- Files this task owns: <paths>
- Files this task must not touch: <paths, if any>

## Check
1. Every acceptance criterion is met by the actual code, not by the implementer's
   summary of it.
2. No scope was added beyond the task or the PR boundary.
3. No scope was silently dropped or narrowed from the source artifact.
4. Sibling task boundaries and do-not-touch files were respected.

## Output

```markdown
## Verdict
Spec compliant | Gaps found | Extra scope found

## Findings
- Missing: <requirement>. Evidence: <file:line or absence>.
- Extra: <unrequested change>. Evidence: <file:line>.
- Changed decision: <what changed from the source artifact>. Evidence: <file:line>.
```

State `Spec compliant, no findings` when nothing is wrong. Do not comment on code
quality, style, or naming here — that belongs to the quality reviewer.
