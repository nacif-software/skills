---
name: interview
description: >-
  Use when a workflow needs to reduce real uncertainty in an artifact by
  questioning the user — framing a product brief, closing design decisions, or
  resolving ambiguous plan requirements. Triggers when product-brief,
  design-feature, or plan-implementation reaches a point where a file cannot answer
  the question, or on "grill me", "interview me", "ask me questions about this".
license: MIT
metadata:
  author: nacif
  version: "0.1.0"
---

# Interview

## Purpose

Reduce uncertainty in an artifact through disciplined questioning. This is the
shared questioning engine the framing and planning workflows call, so the same
rules — ask one thing at a time, never ask what a file already answers, stop when
the answer would not change the outcome — do not get re-written (and quietly
weakened) inside every workflow.

This skill does not own any artifact. It gathers answers; the calling workflow
folds them into its brief, decision map, or plan.

## When to use

- Use when a calling workflow (`product-brief`, `design-feature`,
  `plan-implementation`, or similar) hits uncertainty that a file, artifact, or
  prior decision cannot resolve.
- Use when the user explicitly asks to be grilled or interviewed about a feature,
  problem, or plan.
- Do not use to re-ask anything discoverable from the repo, an existing artifact,
  or an answer already given. Discover first, ask only what remains.
- Do not use to interrogate past the point of usefulness — see the stop condition.

## Caller contract

The calling workflow supplies three things before the interview starts:

- **Focus:** the dimension of uncertainty to resolve (e.g. "the operator and their
  job" for a brief, "the storage approach" for a design, "task ordering and
  contracts" for a plan). Questions outside the focus are out of scope for this
  session.
- **Stop condition:** what "enough" means for this stage. The interview ends the
  moment further answers would not change the artifact the caller is building — not
  when every conceivable question is exhausted.
- **Already known:** the facts discovery and prior artifacts have established, so
  the interview never re-asks them.

## Question rules

- Ask exactly one question at a time. Wait for the answer before the next.
- Every question must close or refine a real branch that changes a downstream
  decision. If the answer would not change the artifact, do not ask it.
- Prefer a recommended answer with its trade-offs over an open prompt. Give the
  user something to react to, not a blank field.
- Never ask what a file, artifact, or earlier answer already establishes. Say what
  you found and confirm only if it is load-bearing and genuinely uncertain.
- Surface assumptions explicitly. If you are proceeding on an unconfirmed
  assumption, name it and let the user correct it rather than burying it.
- Track answers as you go so a later question never contradicts an earlier one.

## Stop condition

Stop asking when any is true:

- Remaining uncertainty would not change the artifact the caller is building.
- The remaining unknowns are cheaper to resolve later (during design, planning, or
  implementation) than to speculate on now — hand them back as open questions with
  that note.
- The user signals they want to move on. Record what is still open rather than
  forcing more answers.

Do not pad the session to look thorough. A short interview that resolved the
load-bearing unknowns is a success, not a shortcut.

## Output

Return the resolved answers in the shape the caller expects:

```markdown
## Resolved
- <question>: <answer, and the decision it settles>

## Assumptions
- <assumption>: <why, and how to falsify it later>

## Still open
- <question>: <why it can wait, and the stage that should settle it>
```

The caller folds `Resolved` into its artifact, keeps `Assumptions` visible, and
carries `Still open` forward as explicit open questions.

## Common mistakes

- Asking several questions in one turn so the user has to untangle them.
- Asking anything the repo, an artifact, or a prior answer already settles.
- Open prompts with no recommendation, making the user do all the framing.
- Continuing past the stop condition to seem diligent.
- Asking outside the caller's focus and drifting into unrelated design or planning.
- Letting an unconfirmed assumption stay implicit instead of naming it.
- Losing track of earlier answers and asking contradictory follow-ups.

## Success criteria

- Every question changed a downstream decision.
- Nothing discoverable was asked.
- The session stopped at the caller's stop condition, not at exhaustion.
- The caller received `Resolved`, `Assumptions`, and `Still open` cleanly separated.
