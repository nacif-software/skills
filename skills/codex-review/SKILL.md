---
name: codex-review
description: >-
  Use when implemented code needs an independent Codex quality review, especially
  during plan execution, PR review, or a pre-merge gate in Claude Code.
license: MIT
metadata:
  author: nacif
  version: "0.1.0"
---

# Codex Review

## Purpose

Run a fresh, read-only code-quality review through the host's Codex integration. In
Claude Code, the review must be dispatched automatically through the OpenAI Codex
plugin agent so the reviewer receives the workflow's exact review brief.

## Hard contract

- Review only. The Codex reviewer must not edit files or apply fixes.
- Use fresh reviewer context for every review and re-review.
- In Claude Code, dispatch the `codex:codex-rescue` plugin subagent with the Agent
  tool. Do not ask the user to run a slash command.
- The Agent prompt's first line must be exactly
  `--fresh --wait --model gpt-5.6-sol`.
- In Claude Code, never satisfy this skill with Bash `codex review`, `/codex:review`,
  a generic Claude subagent, or the plugin Stop hook.
- If the plugin subagent or required model is unavailable, report
  `CODEX_PLUGIN_REVIEW_UNAVAILABLE` and leave the review gate blocked. Do not silently
  downgrade.

Claude Code prerequisite: OpenAI's Codex plugin is installed and
`codex:codex-rescue` is visible to the Agent tool. This is installation-time setup,
not a per-review user action.

## Host routing

### Claude Code

Invoke the plugin agent directly:

```text
Agent({
  subagent_type: "codex:codex-rescue",
  prompt: "--fresh --wait --model gpt-5.6-sol\n<review brief>"
})
```

The prompt must explicitly say the task is read-only review work. Do not call
`Skill(codex:rescue)`; that re-enters the command wrapper instead of dispatching the
plugin agent. Do not launch `codex review` with Bash as a substitute.

### Codex

When already running inside Codex, use the host's native independent review
capability with fresh context. Do not create a nested Claude Code dependency.

### Other hosts

Use a first-class Codex integration only when the host exposes one and the model can
be pinned. Otherwise report `CODEX_PLUGIN_REVIEW_UNAVAILABLE` and keep the gate
blocked.

## Procedure

1. Identify the exact target: base and head refs, uncommitted work, commit, or isolated
   task diff.
2. Build a minimal review brief using `context-briefing`. Include source intent,
   relevant durable artifacts, local rules, verification evidence, and review scope.
3. In Claude Code, dispatch `codex:codex-rescue` automatically with
   `--fresh --wait --model gpt-5.6-sol` and the review brief below.
4. Read the returned findings. Re-check file paths, lines, and claims against the
   actual diff before accepting them.
5. Route accepted findings to the owning implementer. The reviewer remains read-only.
6. After fixes, dispatch a new fresh plugin review over the changed scope.
7. Record transport, agent, model, target, and verdict as review evidence.

## Review brief

```markdown
Review only. Do not edit files, apply patches, or commit changes.

## Target
- Repository: <working directory>
- Scope: <base...head / uncommitted / commit / task diff>
- Base: <ref when applicable>

## Intent and artifacts
- Source intent: <issue, design, PR description, or concise goal>
- Read: <only relevant design, plan, test strategy, PR boundary, and drift report paths>
- Local rules: <relevant instruction files>

## Review priorities
1. Correctness and user-visible behavior.
2. Source intent and requirement alignment.
3. Regression, failure, boundary, concurrency, and data-integrity risks.
4. Test quality and missing verification.
5. Maintainability and local conventions.
6. PR-boundary or spec drift visible in the target.

## Output
- Findings first, ordered Critical, Important, then Minor.
- For each finding: severity, file and line, concrete failure, and expected fix.
- State `No findings` when no actionable issue exists.
- End with assumptions and residual test gaps only when material.
```

## Evidence contract

```markdown
## Codex review evidence
- Transport: Claude Code OpenAI Codex plugin / Codex native
- Agent: `codex:codex-rescue` / native reviewer
- Model: `gpt-5.6-sol`
- Target: <scope and base>
- Fresh context: yes
- Verdict: findings / no findings / unavailable
```

In Claude Code, `Transport` may say plugin only when the main thread actually made an
Agent tool call with `subagent_type: "codex:codex-rescue"`. Command text or reviewer
self-report is not proof of transport.

## Common mistakes

- Running `codex review` through Bash because it is easier to automate.
- Asking the user to invoke `/codex:review` during an autonomous workflow.
- Using the Stop hook as whole-branch review; it reviews only the previous turn.
- Reusing a prior Codex thread and carrying stale assumptions into re-review.
- Letting the review agent apply its own fixes.
- Sending the full conversation instead of a bounded review brief.
- Accepting a finding without checking it against the actual code.
- Claiming plugin review without an actual plugin Agent dispatch.

## Success criteria

- Claude Code dispatched the OpenAI Codex plugin agent automatically.
- The reviewer ran read-only with fresh context on `gpt-5.6-sol`.
- The reviewer received source intent, exact scope, and the workflow review contract.
- Findings were independently checked before fixes were assigned.
- A re-review used a new fresh plugin dispatch.
- Review evidence names the actual transport, model, target, and verdict.
