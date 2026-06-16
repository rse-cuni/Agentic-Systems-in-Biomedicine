---
name: reproducibility-audit
description: Reproducibility workflow for provenance, environment capture, command history, seeds, manifests, and rerun evidence.
compatibility: opencode
metadata:
  audience: reproducibility-officer
  workflow: reproducibility
---

# Reproducibility Audit

Use this skill for provenance, rerun plans, and reproducibility critique.

## Capture Required State

- Inputs with paths, identifiers, versions, and checksums when possible.
- Outputs with paths, expected names, and validation criteria.
- Exact commands, configs, environment, dependencies, and software versions.
- Random seeds and nondeterminism sources.
- HPC job IDs, logs, accounting, and efficiency where relevant.

## Rerun Contract

- A new agent should be able to rerun the work from the report and artifacts.
- State expected runtime and resource needs.
- Record failed or skipped steps rather than omitting them.
- Link critic verdicts and PI decisions.

## Critique Focus

When reviewing, reject claims that cannot be audited, rerun, or traced back to inputs and commands.

