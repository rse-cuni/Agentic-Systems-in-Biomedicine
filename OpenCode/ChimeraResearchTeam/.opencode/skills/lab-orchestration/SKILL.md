---
name: lab-orchestration
description: PI workflow for decomposing research requests, assigning specialist tasks, enforcing critique gates, and maintaining the append-only lab notebook.
compatibility: opencode
metadata:
  audience: pi
  workflow: research-lab
---

# Lab Orchestration

Use this skill when acting as the PI for a research lab run.

## Start a Run

- Convert the user request into a research question, working hypothesis, success criteria, constraints, and evidence requirements.
- Create task IDs that are short, stable, and descriptive, such as `t001-literature-context`.
- Assign one owner specialist and at least one required critic per task.
- Keep local outputs inside the current project folder.

## Delegate Work

- Delegate small tasks with a single clear question.
- Tell each specialist which template to use and where to write the report.
- Require task reports under `tasks/<task-id>/`.
- Require handoffs under `handoffs/<task-id>/` when another agent must continue the work.

## Enforce Review Gates

- Do not accept specialist output without the relevant critic verdict.
- If multiple domains are involved, require multiple critics.
- Treat `revise` and `reject` as blockers until the PI records a new decision.

## Maintain the Notebook

- Append only. Do not rewrite earlier entries.
- Record delegations, observations, critiques, and decisions.
- If an entry is wrong, append a correction with evidence.

