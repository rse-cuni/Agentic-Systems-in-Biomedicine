# Chimera Research Team for OpenCode

This folder contains a copy-pasteable OpenCode agent team for biomedical and
computational research projects that may use Chimera HPC through MCP.

The pack provides:

- a primary `lab-pi` agent that plans work and delegates to specialists
- specialist subagents for literature, methods, programming, data analysis,
  Chimera/HPC operations, reproducibility, and scientific writing
- critic subagents that review work before the PI accepts it
- OpenCode commands for running the lab workflow
- project-local skills and templates for lab notes, task reports, critiques,
  and handoffs
- a small worked example in `examples/research-to-hpc-loop`

The copied version in this repository is mapped to e-INFRA models, so it works
with the provider config in [`../opencode.json`](../opencode.json).

## Prerequisites

Before using this team, set up OpenCode with the e-INFRA provider:

1. Follow [`../README.md`](../README.md) to obtain an e-INFRA API token.
2. Save the token as `E_INFRA_API_TOKEN`.
3. Copy [`../opencode.json`](../opencode.json) into either:
   - `~/.config/opencode/opencode.json`, or
   - the root of the project where you will run OpenCode.
4. If you want the HPC agents to use Chimera MCP tools, edit the SSH username
   in `opencode.json`.

The `hpc-operator` agent expects the Chimera MCP servers from `opencode.json`.
If those MCP servers are disabled or not reachable, the rest of the team can
still work, but Chimera tasks should be reported as blocked.

## Install Into a Fresh Project

From this repository root, choose a target project directory and copy the pack:

```bash
PROJECT=/path/to/research-project
mkdir -p "$PROJECT"
cp -R OpenCode/ChimeraResearchTeam/.opencode OpenCode/ChimeraResearchTeam/templates "$PROJECT"/
cp OpenCode/ChimeraResearchTeam/templates/lab_notebook.md "$PROJECT"/lab_notebook.md
mkdir -p "$PROJECT"/tasks "$PROJECT"/reviews "$PROJECT"/artifacts "$PROJECT"/handoffs
```

Then start OpenCode from the target project root:

```bash
cd /path/to/research-project
opencode
```

Inside OpenCode, check that the team loaded:

```text
/agent
```

You should see `lab-pi` as a primary agent and the specialist/critic subagents.

## Install Into an Existing OpenCode Project

If the target project already has a `.opencode` directory, inspect it before
copying so you do not overwrite local agents or commands. The useful pieces are:

- `.opencode/agents/`
- `.opencode/commands/`
- `.opencode/skills/`
- `templates/`

Copy those directories into the target project, then start OpenCode from that
project root.

## Main Commands

Run these inside OpenCode:

```text
/lab-start <research question or task>
/lab-delegate <task id and requested role>
/lab-review <task id>
/lab-close <task id or run summary>
```

For a full adaptive workflow:

```text
/lab-research Investigate whether this dataset and question can be answered with a small reproducible analysis.
```

For a small end-to-end smoke demo:

```text
/lab-full-demo Run the default tiny Iris dataset demo from start to closeout. Keep HPC cheap and optional.
```

## Workflow Contract

The team uses these project-local paths:

- `lab_notebook.md`: append-only PI decision log
- `tasks/<task-id>/`: specialist reports
- `reviews/<task-id>/`: critic reports with `accept`, `revise`, or `reject`
  verdicts
- `artifacts/<task-id>/`: generated code, figures, logs, or output files
- `handoffs/<task-id>/`: handoffs between specialists

The PI should not close or accept a task until the required critic has written
an explicit verdict in `reviews/<task-id>/`.

## Agents

Primary agent:

- `lab-pi`

Specialists:

- `research-specialist`
- `methods-reviewer`
- `programmer`
- `data-analyst`
- `hpc-operator`
- `reproducibility-officer`
- `scientific-writer`

Critics:

- `research-critic`
- `methods-critic`
- `code-critic`
- `hpc-safety-critic`
- `reproducibility-critic`

## Model Mapping

This repository version uses e-INFRA models:

- `lab-pi`: `einfra/agentic`
- critics: `einfra/thinker`
- `programmer`: `einfra/qwen3-coder`
- `hpc-operator`: `einfra/glm-5.1`
- research, data, methods, reproducibility, and writing specialists:
  `einfra/kimi-k2.6`

If your OpenCode installation uses different provider names or models, edit the
`model:` field in `.opencode/agents/*.md` and `.opencode/commands/*.md`.

## Validate the Pack

From this folder:

```bash
python3 scripts/validate_pack.py
```

The validator checks that expected agents, commands, skills, templates, and the
worked example are present and that the copied agent model mapping is consistent.

