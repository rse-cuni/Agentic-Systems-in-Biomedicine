---
name: hpc-lab-operations
description: Lab-specific HPC operating protocol for using Chimera MCP skills safely within research tasks and producing auditable job handoffs.
compatibility: opencode
metadata:
  audience: hpc-operator
  workflow: chimera-hpc
---

# HPC Lab Operations

Use this skill for lab-facing Chimera work. It complements the installed Chimera skills:

- Use `chimera-slurm-mcp` for live Slurm MCP workflows.
- Use `chimera-filecompress-mcp` for safe archive planning and execution.
- Use `chimera-cluster` for manual, explanatory, or non-MCP Chimera guidance.

## Discovery First

- Before non-trivial HPC advice, discover live state through MCP when available.
- Do not invent accounts, partitions, QOS values, job IDs, queue state, paths, or quotas.
- If discovery fails, record exactly what failed and what remains unknown.

## Pilot First

- Prefer a tiny pilot job before any larger run.
- Capture job ID, stdout, stderr, accounting, efficiency, output manifest, and failure diagnosis.
- For arrays, summarize the array first, then inspect failed task elements.

## Safety Rules

- Do not run heavy compute on login or head nodes.
- Do not move, overwrite, delete, or archive large data without explicit PI context.
- Keep local reports inside the current project folder.
- Use handoffs when programmer, data analyst, or reproducibility officer must continue from HPC results.

## Report Expectations

- Name each MCP tool used and summarize the relevant result.
- Include resource rationale and risk assessment.
- End with what `hpc-safety-critic` must verify.

