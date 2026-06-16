# Task Report

- Task ID: t003-hpc-plan
- Owner agent: hpc-operator
- Requested by: lab-pi
- Timestamp: 2026-06-15T09:55:00+02:00
- Status: ready-for-review

## Question

How should the pilot be run safely on Chimera?

## Methods

The operator should use Chimera MCP discovery tools in the real project before submitting any job. This example does not record real cluster state.

## Findings

- Start with live discovery: cluster state, user associations, quotas, visible templates, and existing jobs.
- Submit only a small pilot first.
- Capture job ID, stdout, stderr, accounting, efficiency, and output manifest before considering scale-up.
- Avoid hard-coded accounts, partitions, QOS values, or fixed Chimera paths.

## Evidence

- Local files: `handoffs/t003-hpc-plan/hpc-to-programmer.md`.
- External sources: none.
- HPC jobs or logs: none in this example.
- Generated artifacts: `artifacts/t003-hpc-plan/README.md`.

## Limitations

This example intentionally avoids real Chimera values. A real run must call the configured MCP tools and record returned state.

## Recommendation

Hand the pilot resource and logging requirements to `programmer`. Required critic: `hpc-safety-critic`.

