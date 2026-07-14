---
name: verification-gate
description: >-
  Use when claiming work is complete, tests pass, a bug is fixed, a review finding
  is addressed, or before handing off, committing, pushing, or opening a PR.
license: MIT
metadata:
  author: nacif
  version: "0.1.0"
---

# Verification Gate

## Purpose

Make completion claims only after fresh evidence. Confidence is not evidence.

## When to use

- Use before saying work is complete, fixed, passing, reviewed, ready, or safe to merge.
- Use after applying review feedback, finishing a subagent task, or creating a PR.
- Do not use as a substitute for writing tests or doing a real review.

## Gate

Before any completion claim:

1. Name the claim.
2. Choose the command, review, or manual check that proves it.
3. Run or perform the check fresh.
4. Read the result, including exit code and failures.
5. Report the actual state with evidence.

If the check fails, say what failed and stop making the stronger claim.

## Evidence table

| Claim | Required evidence |
| --- | --- |
| Tests pass | Fresh test command with exit code 0 |
| Build works | Fresh build command with exit code 0 |
| Review finding fixed | Diff plus targeted verification for that finding |
| Bug fixed | Reproduction no longer fails and regression check exists where practical |
| Requirements met | Requirement-by-requirement checklist against the source artifact |
| Ready for PR | Drift check, review, verification, and known risks summarized |

## Red flags

- "Should pass."
- "Looks good."
- "Only docs changed, no need to check."
- "The subagent said it passed."
- "I ran this earlier."
- "I am confident."

All of these mean: run the gate before making the claim.

## Common mistakes

- Running a partial check and implying a full check passed.
- Treating formatting or linting as proof that behavior works.
- Treating passing tests as proof that the branch still matches the spec.
- Trusting generated output without reading it.
- Skipping verification because the change seems small.

## Success criteria

- The claim is named.
- The proof is fresh and specific to that claim.
- The report states the actual result, including failures or limits.
