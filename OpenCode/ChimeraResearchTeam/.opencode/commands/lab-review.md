---
description: Run the mandatory role-specific critique gate for a lab task.
agent: lab-pi
model: einfra/agentic
---

Run the required critique gate for:

$ARGUMENTS

Act as `lab-pi`.

1. Identify the task report in `tasks/<task-id>/`.
2. Determine which critic or critics are required:
   - `research-critic` for literature and context claims.
   - `code-critic` for code, scripts, tests, or implementation claims.
   - `methods-critic` for design, statistics, metrics, or analysis assumptions.
   - `hpc-safety-critic` for Chimera, Slurm, quota, resource, archive, or data movement work.
   - `reproducibility-critic` for rerun, provenance, environment, or audit claims.
3. Ask each critic to write a review using `templates/critique_report.md` under `reviews/<task-id>/`.
4. Append a critique entry to `lab_notebook.md` summarizing the verdict.

If any required verdict is `revise` or `reject`, send the work back to the appropriate specialist instead of accepting it.

