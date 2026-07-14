# Implementer Brief Template

Fill in every field before dispatch. This is the entire `prompt` value for the
`Agent` call, not a summary of it.

## Task
<one sentence>

## Role and capability
- Role: implementer
- Capability: mechanical / integration / judgment
- Model: <selected model or platform default>
- Escalate when: <conditions that require more context, a stronger model, or replanning>

## Context to read
- `<path>`: <why it matters>
- Plan task: <task ID or section>
- Test strategy rows: <only rows relevant to this task>
- PR boundary: <same PR / separate PR / excluded work>
- Plan review findings: <only findings relevant to this task>

## Scope
- Owns: <files/modules>
- Do not touch: <files/modules>

## Requirements
- <acceptance criteria>
- Do not expand scope beyond <task or PR boundary>

## Constraints
- <repo rules, safety rules, compatibility constraints>

## Verification
- Run: `<command>`
- Expected: <specific signal>

## Report back
- Status: DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT, or BLOCKED
- Changed files
- Verification evidence
- Drift concerns: missing scope, added scope, changed decisions, or none
- Concerns or follow-ups

## If this dispatch is a fix pass
- Finding to fix: <exact finding text from the reviewer>
- Fix only this finding. Do not use this pass to make unrelated changes.
