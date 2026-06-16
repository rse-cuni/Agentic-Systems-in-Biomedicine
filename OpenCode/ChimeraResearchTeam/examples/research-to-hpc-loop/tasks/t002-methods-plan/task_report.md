# Task Report

- Task ID: t002-methods-plan
- Owner agent: methods-reviewer
- Requested by: lab-pi
- Timestamp: 2026-06-15T09:40:00+02:00
- Status: ready-for-review

## Question

What pilot method should be used before a larger Chimera run?

## Methods

Define a pilot that runs on a small subset or toy dataset first, records deterministic parameters, and compares outputs with fixed metrics before any full-scale submission.

## Findings

- Use a two-stage design: local or small-HPC smoke test, then larger batch execution only if the pilot passes.
- Predefine outputs: run manifest, metrics table, logs, and summary figure.
- Predefine failure thresholds: missing output, nonzero exit status, excessive runtime, or unexplained data loss blocks scale-up.

## Evidence

- Local files: `lab_notebook.md`.
- External sources: none in this example.
- HPC jobs or logs: none.
- Generated artifacts: none.

## Limitations

The plan does not choose real metrics because no target dataset or package has been provided.

## Recommendation

Ask `hpc-operator` to produce a live-discovery-based Chimera plan. Required critic: `methods-critic`.

