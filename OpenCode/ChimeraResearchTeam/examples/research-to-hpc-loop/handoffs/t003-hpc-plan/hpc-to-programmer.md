# Handoff

- Task ID: t003-hpc-plan
- From agent: hpc-operator
- To agent: programmer
- Timestamp: 2026-06-15T10:02:00+02:00
- Status: closed

## Context

The pilot should be runnable with a small input before any larger Chimera submission. The real run must discover accounts, partitions, quotas, and templates through Chimera MCP before submission.

## Inputs

- Files: `tasks/t003-hpc-plan/task_report.md`
- Reports: `tasks/t002-methods-plan/task_report.md`
- Reviews: `reviews/t003-hpc-plan/hpc-safety-critic.md`
- HPC jobs or paths: none in this example
- External references: none

## Requested Action

Design the analysis script so it can run locally for smoke tests and under Slurm for the pilot.

## Constraints

Do not hard-code Chimera account, partition, QOS, or data root values. Make output paths explicit and manifest-driven.

## Completion Criteria

Write the code plan or implementation report under `tasks/t004-analysis-code/` and request `code-critic`.

