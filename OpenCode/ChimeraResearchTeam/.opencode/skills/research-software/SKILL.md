---
name: research-software
description: Research programming workflow for small, testable analysis code, command-line interfaces, validation, and maintainable implementation reports.
compatibility: opencode
metadata:
  audience: programmer
  workflow: research-code
---

# Research Software

Use this skill when designing, implementing, or reviewing research software.

## Implementation Rules

- Keep changes scoped to the task.
- Prefer explicit command-line interfaces for analysis scripts.
- Separate analysis logic from HPC submission logic.
- Make inputs, outputs, config, seed, and dry-run behavior explicit.
- Avoid hidden global state and undocumented path assumptions.

## Verification

- Add a smoke test for tiny input when possible.
- Run the narrowest useful test command and record output.
- Record failed commands, partial results, and skipped checks.
- Prefer deterministic behavior or document nondeterminism.

## Report Expectations

- List changed files or proposed files.
- Include commands run and their outcomes.
- State expected inputs, outputs, runtime, and dependencies.
- Identify the required critic: usually `code-critic`, often `reproducibility-critic`.

## Review Focus

When reviewing, prioritize bugs, incorrect assumptions, missing tests, fragile paths, silent data loss, and irreproducible behavior.

