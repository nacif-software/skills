# 0008: Dispatch Codex Review Through The Claude Code Plugin Agent

**Date:** 2026-07-14

## Decision

In Claude Code, code-quality review owned by `codex-review` must dispatch the OpenAI
Codex plugin agent `codex:codex-rescue` automatically with fresh context, a read-only
review brief, and `gpt-5.6-sol`.

Raw Bash `codex review`, asking the user to invoke `/codex:review`, a generic Claude
reviewer, and the plugin Stop hook do not satisfy this whole-branch review gate.

## Rationale

The interactive `/codex:review` command is user-only, so a skill cannot invoke it
autonomously. The previous fallback to Bash preserved the Codex model but bypassed
the Claude Code plugin and did not receive the suite's complete review contract.

The plugin's `codex:codex-rescue` agent is model-invocable and forwards a bounded
prompt through the shared Codex plugin runtime. A fresh, read-only review task can
therefore receive source intent, durable artifacts, review priorities, and output
requirements without user intervention.

The optional plugin Stop hook is not the whole-branch gate. It reviews edits from the
immediately previous Claude turn and may run at unrelated stop points.

## Consequences

- `review-pr` requires `codex-review` for code-quality findings.
- `execute-plan` requires a final integrated `codex-review` before readiness.
- Claude Code review blocks with `CODEX_PLUGIN_REVIEW_UNAVAILABLE` when the plugin
  agent or `gpt-5.6-sol` is unavailable.
- Review evidence records actual transport, agent, model, target, fresh-context state,
  and verdict.
- Review fixes stay with implementation workers; the Codex reviewer remains read-only.
