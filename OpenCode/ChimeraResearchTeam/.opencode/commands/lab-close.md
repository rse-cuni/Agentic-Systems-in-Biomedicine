---
description: Close a lab task or run only after required critic verdicts are present.
agent: lab-pi
model: einfra/agentic
---

Close or summarize this lab task or run:

$ARGUMENTS

Act as `lab-pi`.

1. Inspect `tasks/<task-id>/`, `reviews/<task-id>/`, `artifacts/<task-id>/`, `handoffs/<task-id>/`, and `lab_notebook.md`.
2. Verify that each required critic has written an explicit `accept`, `revise`, or `reject` verdict.
3. If required reviews are missing, do not close the task. Delegate `/lab-review` first.
4. If verdicts are `accept`, append a PI decision entry with evidence, residual risks, and next steps.
5. If any verdict is `revise` or `reject`, append a PI decision entry explaining the required revision or rejection.
6. Produce a concise final summary for the user.

Never mark work complete without the required critic verdicts.

