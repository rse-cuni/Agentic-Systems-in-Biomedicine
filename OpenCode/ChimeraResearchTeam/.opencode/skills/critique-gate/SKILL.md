---
name: critique-gate
description: Mandatory review-gate workflow for critic agents using accept, revise, or reject verdicts grounded in evidence.
compatibility: opencode
metadata:
  audience: critics
  workflow: review
---

# Critique Gate

Use this skill whenever reviewing specialist output.

## Verdicts

- `accept`: adequate for PI decision with stated residual risks.
- `revise`: useful but blocked by specific fixable issues.
- `reject`: unsupported, unsafe, incorrect, or not aligned with the task.

## Review Shape

- Lead with blocking issues.
- Ground each issue in evidence, file paths, source links, command output, MCP state, or explicit reasoning.
- Separate blocking and non-blocking issues.
- State exact required revisions.
- Do not rewrite the specialist report for them.

## Evidence Standard

- Claims need traceable support.
- Missing evidence is a finding.
- Failed checks must be visible.
- Review scope must say what was not reviewed.

