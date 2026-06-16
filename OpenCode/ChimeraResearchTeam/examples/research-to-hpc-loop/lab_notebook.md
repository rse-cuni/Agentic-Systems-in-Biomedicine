# Lab Notebook

This notebook is append-only. Earlier entries are kept for auditability.

## Run Metadata

- Run ID: example-research-to-hpc-loop
- Project folder: examples/research-to-hpc-loop
- PI agent: lab-pi
- Start date: 2026-06-15
- Research question: Can a small pilot analysis establish a safe and reproducible path for running a larger single-cell preprocessing comparison on Chimera?
- Success criteria: literature context, method plan, HPC plan, code plan, and reproducibility plan each receive an explicit critic verdict.
- Current status: closed example

## Task Index

| Task ID | Owner | Status | Required critic | Latest report | Latest review |
| --- | --- | --- | --- | --- | --- |
| t001-research-context | research-specialist | accepted | research-critic | tasks/t001-research-context/task_report.md | reviews/t001-research-context/research-critic.md |
| t002-methods-plan | methods-reviewer | accepted | methods-critic | tasks/t002-methods-plan/task_report.md | reviews/t002-methods-plan/methods-critic.md |
| t003-hpc-plan | hpc-operator | accepted | hpc-safety-critic | tasks/t003-hpc-plan/task_report.md | reviews/t003-hpc-plan/hpc-safety-critic.md |
| t004-analysis-code | programmer | accepted | code-critic | tasks/t004-analysis-code/task_report.md | reviews/t004-analysis-code/code-critic.md |
| t005-reproducibility | reproducibility-officer | accepted | reproducibility-critic | tasks/t005-reproducibility/task_report.md | reviews/t005-reproducibility/reproducibility-critic.md |

## PI Decision Ledger

### Decision Entry

- Timestamp: 2026-06-15T09:30:00+02:00
- Task ID: t001-research-context
- Decision: accept
- Evidence: Research report summarized why preprocessing comparisons should preserve raw inputs, record parameters, and avoid interpreting exploratory velocity-like outputs as validated biology.
- Required critic verdict: accept
- Residual risk: Example does not cite live papers; real runs must include direct citations.
- Next action: Proceed to method planning.

### Decision Entry

- Timestamp: 2026-06-15T09:45:00+02:00
- Task ID: t002-methods-plan
- Decision: accept
- Evidence: Method plan defines a pilot first, fixed metrics, and escalation criteria before larger Chimera execution.
- Required critic verdict: accept
- Residual risk: Metrics may need adaptation to the real dataset.
- Next action: Ask HPC operator for a safe run plan.

### Decision Entry

- Timestamp: 2026-06-15T10:00:00+02:00
- Task ID: t003-hpc-plan
- Decision: accept
- Evidence: HPC plan requires live MCP discovery before resource selection and starts with a small pilot job.
- Required critic verdict: accept
- Residual risk: Actual account, partition, quota, and template availability must be rediscovered in the target project.
- Next action: Hand off resource constraints to programmer.

### Decision Entry

- Timestamp: 2026-06-15T10:15:00+02:00
- Task ID: t004-analysis-code
- Decision: accept
- Evidence: Code plan defines CLI inputs, deterministic outputs, smoke test, and pilot-first behavior.
- Required critic verdict: accept
- Residual risk: No real script is implemented in this example.
- Next action: Capture reproducibility contract.

### Decision Entry

- Timestamp: 2026-06-15T10:30:00+02:00
- Task ID: t005-reproducibility
- Decision: accept
- Evidence: Reproducibility plan captures inputs, commands, environment, seeds, job IDs, and output manifest requirements.
- Required critic verdict: accept
- Residual risk: Real runs must include exact package versions and actual MCP job metadata.
- Next action: Close example run.

## Chronological Log

### Entry

- Timestamp: 2026-06-15T09:15:00+02:00
- Agent: lab-pi
- Task ID: run
- Entry type: hypothesis
- Summary: A pilot-first workflow can reduce HPC waste and improve reproducibility before scaling to larger data.
- Evidence and links: Local example reports in `tasks/`.
- Open questions: Which real dataset and Chimera account will be used in production?
- Next steps: Delegate literature, methods, HPC, code, and reproducibility tasks.

### Entry

- Timestamp: 2026-06-15T10:35:00+02:00
- Agent: lab-pi
- Task ID: run
- Entry type: decision
- Summary: Example run closed after all required critic verdicts were present.
- Evidence and links: Reports and reviews under this example folder.
- Open questions: None for the example.
- Next steps: Use this folder as a reference for real lab runs.

