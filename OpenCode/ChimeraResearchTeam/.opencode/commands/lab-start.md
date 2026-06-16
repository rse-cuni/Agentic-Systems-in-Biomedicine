---
description: Start or initialize a structured research lab run with PI delegation.
agent: lab-pi
model: einfra/agentic
---

Start a new research lab run for:

$ARGUMENTS

Act as `lab-pi`.

1. Inspect the current project folder for existing `lab_notebook.md`, `tasks/`, `reviews/`, `artifacts/`, and `handoffs/`.
2. Create missing lab-run structure if needed.
3. Initialize or append to `lab_notebook.md` using `templates/lab_notebook.md`.
4. State the research question, working hypothesis, success criteria, constraints, and first task IDs.
5. Delegate the first focused tasks to the relevant specialist subagents.
6. Record which critic is required for each task.

Do not mark any task complete. Each task must pass the relevant mandatory critic gate before PI acceptance.

