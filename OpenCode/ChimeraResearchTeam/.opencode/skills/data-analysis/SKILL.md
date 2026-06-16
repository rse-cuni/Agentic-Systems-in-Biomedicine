---
name: data-analysis
description: Data analysis workflow for inspecting datasets, planning transformations, computing summaries, and reporting uncertainty without overclaiming.
compatibility: opencode
metadata:
  audience: data-analyst
  workflow: analysis
---

# Data Analysis

Use this skill for exploratory analysis, result interpretation, and data-quality assessment.

## Data Inspection

- Identify input files, formats, schema, dimensions, and provenance.
- Check missingness, duplicates, range anomalies, and unexpected categories.
- Record filters and transformations explicitly.

## Analysis

- Match the analysis to the question and method plan.
- Keep exploratory and confirmatory analyses separate.
- Produce compact tables or figures that answer the task.
- Avoid causal interpretation unless the design supports it.

## Report Expectations

- State data provenance and assumptions.
- Describe commands, scripts, or notebooks used.
- Link outputs under `artifacts/<task-id>/`.
- Identify limitations and sensitivity checks.
- Request `methods-critic` and `reproducibility-critic` when appropriate.

