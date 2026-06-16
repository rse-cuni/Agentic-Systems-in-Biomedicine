---
description: Run a full adaptive research workflow from question to reviewed closeout.
agent: lab-pi
model: einfra/agentic
---

Run a complete adaptive lab research workflow for:

$ARGUMENTS

Act as `lab-pi`. Load `$lab-orchestration` and `$critique-gate`.

## Intent

Create and execute a full start-to-end research workflow. Let the specialist team identify subproblems, propose fixes, revise work after critique, and adapt the task graph as evidence appears.

This command is not tied to a specific demo dataset. It should work for literature-only, code, data-analysis, local-compute, or Chimera-assisted research tasks.

## Non-Negotiable Rules

- Keep all local outputs inside the current project folder.
- Use `lab_notebook.md`, `tasks/`, `reviews/`, `artifacts/`, and `handoffs/`.
- Do not accept any task without explicit critic verdicts.
- Do not hide failures, unavailable tools, missing evidence, failed downloads, failed tests, or failed HPC discovery.
- Do not invent data, papers, paths, job IDs, metrics, or command outputs.
- For Chimera work, delegate to `hpc-operator` and require `hpc-safety-critic`.
- If the run cannot be completed safely, close it as `blocked` with exact reasons and next actions.

## Adaptive Workflow

1. Define the run
   - Extract the research question, hypothesis, success criteria, constraints, and expected artifacts.
   - If key information is missing, make a reasonable bounded assumption and record it in `lab_notebook.md`.
   - Create task IDs and initial task folders.

2. Build the initial task graph
   - Use `research-specialist` when literature, dataset background, tool docs, or context are needed.
   - Use `methods-reviewer` when experimental design, metrics, controls, or analysis choices are needed.
   - Use `programmer` when code, scripts, tests, or automation are needed.
   - Use `data-analyst` when data inspection, summaries, plots, or result interpretation are needed.
   - Use `hpc-operator` when Chimera discovery, Slurm jobs, logs, arrays, quotas, or archive operations are needed.
   - Use `reproducibility-officer` before final closeout.
   - Use `scientific-writer` only after the underlying evidence has been accepted.

3. Execute with critique gates
   - After each specialist report, invoke the required critic:
     - `research-critic` for literature or context.
     - `methods-critic` for design, metrics, or interpretation.
     - `code-critic` for code and tests.
     - `hpc-safety-critic` for Chimera or resource work.
     - `reproducibility-critic` for rerun evidence and provenance.
   - If verdict is `accept`, append a PI accept decision and continue.
   - If verdict is `revise`, send the exact required fixes back to the relevant specialist, then request a follow-up critique.
   - If verdict is `reject`, stop that path unless the PI can define a narrower replacement task.

4. Let the team resolve problems
   - Specialists may create handoffs when another role is better suited.
   - Critics may request targeted revisions.
   - The PI may add new tasks when evidence reveals a missing subproblem.
   - Keep revision loops bounded. After two failed revision rounds on the same issue, stop and record the blocker.

5. Close the run
   - Require `reproducibility-officer` and `reproducibility-critic`.
   - Ask `scientific-writer` for a short final summary based only on accepted evidence.
   - Append a final PI closeout decision:
     - `accept` if success criteria are met.
     - `partial` if useful accepted outputs exist but some goals remain unresolved.
     - `blocked` if a required step could not be completed safely or honestly.

## Expected Final Response

At the end, report:

- Final run status: accept | partial | blocked
- Accepted tasks
- Revised or rejected tasks
- Key artifacts
- Critical evidence
- Residual risks
- Next recommended action

