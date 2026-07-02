---
name: scope-check
description: >-
  Reviews a feature implementation or plan against the original ask — flags scope
  beyond the minimum version, complexity beyond the simplest implementation, and at
  most three strictly-capped low-hanging-fruit wins, reporting findings without
  applying changes. Use when a feature implementation or plan exists (working tree,
  branch diff, or design doc) and it should be checked before commit/PR — after
  finishing a feature, when a diff feels bigger than the ask, when unsure whether
  extra fields/endpoints/abstractions belong, or when the user asks "is this the
  minimal version?" or invokes /scope-check.
license: MIT
metadata:
  author: nacif
  version: "0.1.0"
---

# Scope Check

## Purpose

Review a feature against two questions: is this the **minimum version** of what was asked, and is it the **simplest implementation** of that version? The yardstick is the ask — not best practice, not extensibility, not what a mature product would have. Report findings; do not apply changes.

## Procedure

1. **Reconstruct the ask.** State it in 1–3 sentences, quoting the request (conversation, ticket, chat thread) where possible. Also list explicit user decisions made along the way — **anything the user explicitly requested or approved is in scope by definition**, even if it looks speculative (e.g., a registry with one entry the user asked for). If you cannot state the ask, stop and ask the user for it.
2. **Collect the actual change.** Diff the branch against the repo's default branch — discover it (`main`, `master`, `develop`) rather than assuming `main`, e.g. `git diff "$(git remote show origin | sed -n 's/.*HEAD branch: //p')"...HEAD` — plus uncommitted work. Or the plan, if reviewing pre-code. Review what exists, not what you remember writing.
3. **Minimum-version check.** Trace every element — column, endpoint, config flag, param, UI state, event, error type — back to the ask. Untraceable elements are findings. Frequent offenders: audit/`*_updated_by` fields, analytics events, enable/disable flags, second endpoints (write when only read was asked), format/option params, handling inputs that cannot occur, "while I'm here" refactors.
4. **Simplest-implementation check** (surviving scope only). Signals: abstraction with one implementation, new pattern where the codebase has an established one, caching/async/queue where a direct call works, new dependency for a stdlib-sized job, indirection layers a reader must traverse.
5. **Low-hanging fruit** — optional wins, strictly capped: each must ride on code already in the diff, take ≲10 lines / ~15 minutes, and add **no** new tables, columns, endpoints, dependencies, or config. Maximum 3. "None" is a good answer; never pad this section.

## Required output shape

```markdown
## Scope Check: <feature>

**The ask:** <1–3 sentences, quoted where possible>
**In scope by explicit decision:** <list, or "None">

**Verdict:** <✅ Minimum version | ⚠️ N items beyond the ask> · <✅ Simplest implementation | ⚠️ M complexity findings>

### Beyond the ask
| Item | Where | Why it exceeds the ask | Suggested change |
(or "None.")

### Simpler alternatives
| Item | Where | Current | Simpler |
(or "None.")

### Low-hanging fruit (max 3)
- <item — why it's nearly free> (or "None.")
```

Every section appears, even when empty. Suggested changes are concrete (what to delete, which existing path to reuse). Then stop — the user decides what to cut.

## Calibration

Flagging everything is as useless as flagging nothing.

| Not a finding | Why |
|---|---|
| Auth/tenancy guards, 404s on reachable paths | Correctness the codebase requires, not creep |
| Tests, migrations for kept fields | Cost of the kept scope |
| Boilerplate an established pattern requires | Matching patterns is the simple option |
| Anything the user explicitly approved | The ask includes their decisions |

| Rationalization | Reality |
|---|---|
| "Audit fields / analytics are good practice" | Not asked for = a finding. Mention as a one-line option at most |
| "It's already written and tested" | Sunk cost. Cutting is cheapest now |
| "The abstraction makes it extensible" | Extensibility nobody asked for is complexity |
| "This fruit is only a day's work" | Then it is not low-hanging. Cap is ~15 minutes |
