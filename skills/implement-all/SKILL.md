---
name: implement-all
description: >-
  Implements tickets or items one at a time using /implement serially with
  subagents. Use when the user provides a batch/list of things to implement.
license: MIT
metadata:
  author: nacif
  version: "0.1.0"
---

# Implement All

## Overview
Runs `/implement` in series, one item at a time, each producing its own
commit. Stops at the first failure instead of continuing silently.

## When to use
- User provides/references a list of items to build (loose list, a batch
  of `docs/issues/*.md`, a PRD checklist)
- Each item should become its own commit
- NOT for items that need to run in parallel or that should collapse
  into a single commit

## Workflow

### 1. Parse and confirm
- Extract the items into a numbered list (dedupe; if an item looks
  already done, flag it instead of silently including it)
- If items reference files or an external resource, resolve them and
  read the full content — don't just pass along the title
- Show the numbered list and get explicit confirmation before starting

### 2. Execute, IN SERIES (never parallel — `/implement` commits to the
current branch; concurrent commits collide)

For each item, in order:
- Build a self-contained prompt for the subagent, starting with
  `/implement`. It has no memory of this conversation or the other
  items — include: the item's text, acceptance criteria, source
  file/link, and any cross-item context it needs (e.g. a decision made
  on a prior item that affects this one)
- Spawn ONE subagent, wait for it to finish
- Verify a commit was actually created (`git log`) — a subagent
  reporting success without a commit still counts as a failure
- On failure (subagent error OR no commit): STOP. Do not move to the
  next item.

### 3. Consolidated report
- Completed items + each commit's SHA
- Skipped/failed items + why

### 4. Next steps
Suggest a follow-up action (e.g. open a PR, run tests)

## Red flags — stop and ask
- Thinking about parallelizing items "to save time"
- Thinking about continuing past a failure because "the rest are
  independent"
- An item too vague to give the subagent full context
