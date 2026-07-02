# PR wrap-up checklist (Phase 2 fallback)

Use when no dedicated PR-finalizing skill is available. Run everything from the
worktree created in Phase 1, and keep the same commit rule: plain `git commit`, no
hook-bypassing flags.

1. **Formatters and linters.** Run the project's own commands (discovered in the
   Inputs step from contributor docs, CI config, or package manifests). Fix what they
   flag.

2. **Self-review the full diff** against the base branch
   (`git diff origin/<baseRefName>...HEAD`):
   - Remove leftover debug logging, dead code, commented-out blocks, and TODO
     scaffolding introduced by this branch.
   - Remove AI artifacts: comments that narrate what the change does or justify it to
     a reviewer rather than stating a constraint the code can't show.
   - Check every changed file belongs to the PR's stated purpose. Scope creep →
     surface it to the user; don't silently keep or delete it.

3. **Triage reviewer feedback.** List unresolved review comments
   (`gh pr view --comments`, or `gh api repos/{owner}/{repo}/pulls/<number>/comments`
   for inline threads). Address the genuine, in-scope ones; reply to the rest with
   your reasoning. Never resolve a thread without either a fix or a reply.

4. **Run the relevant test suite** against the worktree's code (not a container
   mounting the main checkout).

5. **Update the PR title and description** to match the final state of the diff.
   Mention anything the Codex loop surfaced but deliberately did not fix.

6. **Commit and push** the branch.

7. **Watch CI**: `gh pr checks --watch`. Fix failures and repeat from step 6. Do not
   proceed while checks are red.

8. **Flip draft → ready**: `gh pr ready` — only after CI is green.

9. **Report** to the user: what changed during wrap-up, CI status, PR URL, plus the
   Codex review summary (iterations, fixes with file:line, surfaced-but-unfixed
   findings).
