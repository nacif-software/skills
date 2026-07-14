---
name: spec-drift-check
description: >-
  Use after implementation or before PR readiness when comparing a diff, branch, or
  completed task against a design doc, implementation plan, PR boundary, test
  strategy, issue, acceptance criteria, or promised scope.
license: MIT
metadata:
  author: nacif
  version: "0.1.0"
---

# Spec Drift Check

## Purpose

Compare implemented work against the agreed artifacts. Detect missing scope, added
scope, changed decisions, broken PR boundaries, and test-strategy drift before the
branch is called ready.

## When to use

- Use after `execute-plan` once implementation tasks have landed.
- Use before `review-pr`, PR creation, merge readiness, or completion claims.
- Use when a branch feels like it may have expanded beyond the design or plan.
- Use when tests pass but requirements may still be missing.
- Do not use instead of code review. Use `review-pr` for correctness and quality.

## Inputs

- Source artifacts: design doc, PRD, issue, accepted requirements, or task brief.
- Planning artifacts: implementation plan, `test-strategy`, `pr-boundary`,
  `review-plan`, or issue breakdown.
- Implementation evidence: diff against the correct base, changed files, commits,
  test files, verification output, and worker reports if present.

If an artifact is missing, state the gap and check against the remaining evidence.

## Procedure

1. Identify the correct base and implementation diff.
2. Read the source and planning artifacts. Prefer durable files over conversation
   memory.
3. Build a traceability table:
   - requirement or decision,
   - planned task or boundary,
   - implemented files,
   - tests or verification,
   - status.
4. Check missing scope:
   - required behavior not implemented,
   - promised test not added,
   - verification not run,
   - accepted review finding not addressed.
5. Check added scope:
   - unrelated cleanup,
   - new behavior not in the source,
   - broad refactor not required,
   - optional follow-up included,
   - files outside owned scope.
6. Check changed decisions:
   - public contracts,
   - architecture,
   - data shape,
   - PR boundary,
   - test seam,
   - rollout or rollback assumptions.
7. Classify drift by severity and decide whether it must be fixed, documented, or
   accepted by the user.
8. Route next actions to the owning workflow:
   - code or task fixes -> `execute-plan`,
   - missing or weak verification -> `test-strategy`,
   - added scope or split decisions -> `pr-boundary`,
   - accepted plan changes -> `plan-implementation`,
   - no unresolved Critical or Important drift -> `review-pr`.
9. Use `verification-gate` before claiming the branch is aligned or ready.
10. Produce a drift report with next actions.

## Severity model

- Critical: implemented work violates a core requirement, safety boundary, data
  contract, or PR boundary in a way that blocks readiness.
- Important: requirement, test, or plan drift should be fixed or explicitly accepted
  before review or merge.
- Minor: harmless drift, naming mismatch, or documentation cleanup.

## Output format

```markdown
# Spec Drift Report

## Verdict
Aligned | Drift found | Blocked

## Traceability
| Source item | Planned task or artifact | Implementation evidence | Verification | Status |
| --- | --- | --- | --- | --- |
| <requirement> | <task/boundary/test> | <files or diff> | <test/check> | aligned/missing/changed/extra |

## Findings
- [Critical] <item>: <drift>. Required action: <fix, document, or get approval>.
- [Important] <item>: <drift>. Required action: <fix, document, or get approval>.
- [Minor] <item>: <drift>. Suggested action: <action>.

## Added Scope
- <extra work>: <keep, split, revert, or ask user>

## Missing Scope
- <missing work>: <required action>

## Test Strategy Drift
- <promised test/check>: present / missing / changed, because <reason>.

## PR Boundary Drift
- <boundary>: preserved / violated / changed, because <reason>.

## Next Action
Fix with execute-plan | revise test-strategy | revise pr-boundary | update plan with approval | proceed to review-pr
```

## Common mistakes

- Treating passing tests as proof the spec was met.
- Comparing only to the latest plan and ignoring the original source requirement.
- Ignoring added scope because the code is "nice to have".
- Failing to check promised tests and verification evidence.
- Accepting changed architecture without recording the decision.
- Calling drift "minor" when it affects reviewability, rollback, or user-visible
  behavior.
- Proceeding to `review-pr` while Critical or Important drift remains unresolved.

## Success criteria

- Every important source item is mapped to implementation evidence or a gap.
- Added and missing scope are explicit.
- Test-strategy and PR-boundary drift are checked when artifacts exist.
- The branch can move to `review-pr` with fewer hidden assumptions.
- No readiness claim is made until alignment evidence has passed `verification-gate`.
