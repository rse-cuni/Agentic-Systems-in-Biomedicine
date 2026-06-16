# Task Report

- Task ID: t004-analysis-code
- Owner agent: programmer
- Requested by: lab-pi
- Timestamp: 2026-06-15T10:10:00+02:00
- Status: ready-for-review

## Question

What code interface should support the pilot and later batch execution?

## Methods

Design a CLI-oriented script contract without implementing a real analysis in this example.

## Findings

- Provide a script with explicit `--input`, `--output-dir`, `--seed`, `--config`, and `--dry-run` arguments.
- Write a manifest containing input identifiers, parameters, environment details, and output paths.
- Include a smoke test that runs on tiny input and verifies required outputs.
- Keep HPC submission separate from analysis logic so the same script can run locally or in Slurm.

## Evidence

- Local files: none implemented in this example.
- External sources: none.
- HPC jobs or logs: none.
- Generated artifacts: none.

## Limitations

No code is implemented. This task demonstrates the expected report format and review gate.

## Recommendation

Implement the script in a real target project, then request `code-critic`.

