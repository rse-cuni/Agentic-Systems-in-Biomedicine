# Repository Instructions

This repository contains an OpenCode agent pack, not an application runtime. Keep changes focused on markdown agent definitions, command prompts, templates, examples, and validation scripts.

## Structure

- `.opencode/agents/`: OpenCode markdown agent definitions.
- `.opencode/commands/`: OpenCode custom command definitions.
- `.opencode/skills/`: Project-local OpenCode skills used by specialist agents.
- `templates/`: copyable lab notebook and report templates.
- `examples/research-to-hpc-loop/`: reference output for the intended workflow.
- `scripts/validate_pack.py`: static validation for the pack.

## Editing Rules

- Keep pack content in English.
- Preserve the current project folder as the working boundary in agent prompts.
- Do not add a fixed Chimera root path. HPC access should go through the configured Chimera MCP tools.
- Do not use deprecated `tools` frontmatter in agent files; use `permission`.
- Prefer narrow `permission.skill` maps over broad `skill: allow` when a specialist should only load specific skills.
- Keep `lab_notebook.md` semantics append-only.
- Critics must return explicit `accept`, `revise`, or `reject` verdicts.

## Validation

After changing agent files, command files, templates, or examples, run:

```sh
python3 scripts/validate_pack.py
```
