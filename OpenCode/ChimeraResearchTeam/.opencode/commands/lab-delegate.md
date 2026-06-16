---
description: Delegate a focused lab task from the PI to the right specialist subagent.
agent: lab-pi
model: einfra/agentic
---

Delegate or refine a lab task:

$ARGUMENTS

Act as `lab-pi`.

1. Identify the task ID, owner specialist, expected output folder, and required critic.
2. If the task ID is missing, create a concise task ID.
3. Ask the specialist subagent to write a structured report using `templates/task_report.md`.
4. Require outputs to stay inside the current project folder under `tasks/<task-id>/`, `artifacts/<task-id>/`, or `handoffs/<task-id>/`.
5. Append a delegation entry to `lab_notebook.md`.

Do not accept the specialist output until `/lab-review` has produced the required critic verdict.

