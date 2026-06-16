---
description: Run the full Iris research lab demo from start to PI closeout.
agent: lab-pi
model: einfra/agentic
---

Run the full end-to-end lab demo.

User request or overrides:

$ARGUMENTS

Act as `lab-pi`. Load `$lab-orchestration` and `$critique-gate`.

## Default Demo

Unless the user gives a different tiny dataset or question, use this default:

- Research question: Can the classic Iris dataset support a simple, reproducible demonstration that petal measurements separate Iris species better than sepal measurements?
- Dataset: `https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv`
- Constraints: tiny public CSV only, no large downloads, no GPU, no long jobs, one plot, one simple metric or classifier, optional safe Chimera execution only after discovery.

## Required End-to-End Sequence

Create or update the local lab structure:

- `lab_notebook.md`
- `tasks/`
- `reviews/`
- `artifacts/`
- `handoffs/`

Then run the pipeline in order. Do not skip critique gates.

1. `t001-literature-context`
   - Delegate to `research-specialist`.
   - Ask for a brief context review of the Iris dataset and why it is used for classification demos.
   - Require `research-critic`.
   - If verdict is not explicit `accept`, stop and record required revisions.

2. `t002-methods-plan`
   - Delegate to `methods-reviewer`.
   - Ask for a minimal method: summary statistics, one simple visualization, and one simple classifier or PCA-style separation check.
   - Require `methods-critic`.
   - If verdict is not explicit `accept`, stop and record required revisions.

3. `t003-analysis-script`
   - Delegate to `programmer`.
   - Ask for a small Python script that downloads or loads the Iris CSV, computes petal-vs-sepal summaries, creates one plot, and writes outputs under `artifacts/t003-analysis-script/`.
   - Run locally first if safe and cheap.
   - Require `code-critic`.
   - If verdict is not explicit `accept`, stop and record required revisions.

4. `t004-data-interpretation`
   - Delegate to `data-analyst`.
   - Ask for interpretation of the generated summaries and plot.
   - Require `methods-critic` if the interpretation makes method claims.
   - If verdict is not explicit `accept`, stop and record required revisions.

5. `t005-hpc-tiny-job`
   - Delegate to `hpc-operator`.
   - Ask for Chimera MCP discovery first.
   - Submit a tiny safe job only if a clearly safe short template or project-script path is available and the required inputs are in the allowed MCP/project scope.
   - If no safe tiny submission path is available, stop after discovery and report why. This can still be accepted as the HPC result if `hpc-safety-critic` agrees.
   - Require `hpc-safety-critic`.
   - If verdict is not explicit `accept`, stop and record required revisions.

6. `t006-reproducibility`
   - Delegate to `reproducibility-officer`.
   - Ask for exact commands, input URL, output paths, environment assumptions, seeds, local execution result, and any Chimera MCP/job metadata.
   - Require `reproducibility-critic`.
   - If verdict is not explicit `accept`, stop and record required revisions.

7. `t007-final-writing`
   - Delegate to `scientific-writer`.
   - Ask for a short final scientific summary based only on accepted reports and critic verdicts.
   - PI reviews the final writing against accepted evidence.

## Closeout

Append all delegations, critique verdicts, and PI decisions to `lab_notebook.md`.

Close the run only when every required critic verdict is present and accepted. If any stage stops early, write a clear blocked closeout with the exact missing evidence or required revision.

