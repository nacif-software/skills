#!/usr/bin/env bash
# Example helper script (template).
#
# Skills can ship executable helpers in scripts/. The agent runs them as a step in
# the SKILL.md procedure — for deterministic work that's better done in shell than
# by the model (parsing, file generation, calling a CLI, etc.).
#
# Keep scripts:
#   - self-contained and dependency-light (prefer tools that are already present),
#   - safe (no destructive defaults; require explicit flags for anything risky),
#   - quiet on success, loud on failure (exit non-zero with a clear message).
#
# Replace this with your real script when you build a skill.

set -euo pipefail

name="${1:-world}"
echo "example-skill: hello, ${name}"
echo "This is a placeholder script. Replace it with something useful."
