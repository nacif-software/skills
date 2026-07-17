# 0008: Run Codex Review Once Per PR-Boundary Group, Not Once Per Task

**Date:** 2026-07-16

## Decision

Code-quality review (native Codex review through the OpenAI Codex plugin) runs at
most once per PR-boundary group — the same unit `pr-boundary` already produces —
plus once over the whole integrated branch. It does not run inside
`task-dispatch-loop`, and it does not run once per task.

Within a checkpoint, findings from one review pass are batched: every task in the
group gets its fixes routed and applied before a single re-review, not one
re-review per finding. Checkpoints for groups made entirely of `mechanical`-tier,
low-risk tasks (per `plan-implementation`'s worker-tier classification and
`test-strategy`'s named risk areas) are skipped, with the skip recorded on the task
board — the group is still quality-reviewed once, at the final whole-branch pass.

## Rationale

`task-dispatch-loop` originally ran a Codex quality review after every task, with a
fix-and-re-review cycle per individual finding. For an 18-task plan that is
roughly 40-80 Codex calls, each taking real wall-clock minutes — the difference
between a same-day feature and one that spans days, with no proportional increase
in the safety the extra calls buy. Most of that volume comes from reviewing the
same kind of narrow, low-risk change repeatedly rather than from catching more
real issues.

Spec review is unaffected by this decision: it stays per task, cheap, and
immediate, because it is the review that keeps drift from compounding while it is
still cheap to fix. Code-quality review is the expensive, high-latency check, so
it is the one that needs a coarser cadence.

## Consequences

- `task-dispatch-loop` dispatches an implementer and a spec reviewer only. It never
  dispatches Codex or any code-quality reviewer.
- `execute-plan` owns a new checkpoint step: run once per PR-boundary group when
  that group's tasks are all spec-approved, batch all findings from one pass into
  one fix round and one re-review, and tier-gate the checkpoint away for
  mechanical-only, low-risk groups.
- A single-PR plan — the common case — has exactly one checkpoint, which is the
  same pass `review-pr` already runs at the end; no separate mid-flight checkpoint
  is needed.
- The task board carries a PR-boundary group column and a quality-review status
  distinct from spec-review status, so "deferred to checkpoint" is a visible,
  intentional state rather than a silent gap.
- The final whole-branch `review-pr` pass is unchanged and remains the backstop:
  every task's code is quality-reviewed at least once, even when its group's
  checkpoint was skipped.
- Neither the per-task spec reviewer nor the subagent that dispatches Codex needs
  the strongest available model — the spec reviewer checks compliance against a
  brief, and the Codex-dispatch subagent only runs a command and relays its
  output. Both should use fast/cheap models.
