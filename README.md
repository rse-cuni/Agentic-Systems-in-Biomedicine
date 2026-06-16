# Agentic Systems in Biomedicine


This repository accompanies the **Agentic Systems in Biomedicine** learning programme. It collects workshop materials, Langflow exports, custom components, and example agent workflows used to discuss how large-language-model-based agents can support biomedical research, analysis, and research infrastructure.

The main emphasis is practical: what agentic systems are, how they differ from ordinary chatbots, how they use tools and workflows, and where they are useful or risky in professional biomedical settings.

## Course overview

- **Program type:** Learning programme
- **Target group:** Pedagogical staff, PhD students, DPP employees, and related research or technical staff
- **Format:** Hands-on workshop with Langflow and OpenCode examples

Agentic systems based on large language models can plan analysis steps, call external tools, work with files and structured data, and interact with computational resources. In biomedical research, that makes them interesting not only for literature work and interpretation tasks, but also for operational workflows that span scripts, APIs, and HPC environments.

This workshop introduces agentic systems in the context of biomedical research and data analysis. It focuses on practical applications, limitations, and the principles of safe and meaningful deployment. It also briefly introduces the **Model Context Protocol (MCP)** as a standardized way to connect a language model to external services and tools, including university HPC infrastructure.

## What the workshop covers

- What agentic systems are and how they differ from ordinary chatbots
- Working with tools, scripts, and workflows instead of plain chat
- Biomedical use cases for literature review, interpretation, and analysis support
- Practical introduction to MCP-enabled tool connection
- Agent access to computational infrastructure such as an HPC cluster
- Limitations, failure modes, and safe deployment considerations

## What is in this repository

The repository is organized around reusable teaching materials and concrete flow examples.

| Path | Purpose |
| ---- | ------- |
| [`Langflow/`](Langflow/) | Langflow setup notes, including the JupyterHub launcher and local install options |
| [`Langflow/Agents/`](Langflow/Agents/) | Importable Langflow agent workflows used in the course |
| [`Langflow/Components/`](Langflow/Components/) | Reusable Langflow custom components, including the e-INFRA CZ LLM provider |
| [`OpenCode/`](OpenCode/) | OpenCode config, e-INFRA setup notes, and the Chimera research-team agent pack |
| [`OpenCode/ChimeraResearchTeam/`](OpenCode/ChimeraResearchTeam/) | Copy-pasteable OpenCode agents, subagents, commands, skills, and templates for a research lab team |
| [`Presentations/`](Presentations/) | Slide decks and exported presentation assets |
| [`Langflow/README.md`](Langflow/README.md) | How to access Langflow through JupyterHub and install it locally if needed |
| [`Langflow/Agents/README.md`](Langflow/Agents/README.md) | Overview of the agent packages and import notes |
| [`OpenCode/README.md`](OpenCode/README.md) | Where to obtain the e-INFRA API token, where to save it, and where to copy the OpenCode config |
| [`Presentations/README.md`](Presentations/README.md) | Overview of the teaching decks |

## Included example agents

These flows are designed as teaching prototypes rather than polished products. They are useful for demonstrating different patterns of tool use, workflow decomposition, and agent behavior.

- [`LabValuesInterpreterAgent`](Langflow/Agents/LabValuesInterpreterAgent/README.md): educational interpretation of laboratory values
- [`LiteratureAgent`](Langflow/Agents/LiteratureAgent/README.md): literature planning, search, and synthesis
- [`DeepResearchAgent`](Langflow/Agents/DeepResearchAgent/README.md): staged multi-agent research workflow
- [`StatisticalAssistantAgent`](Langflow/Agents/StatisticalAssistantAgent/README.md): Python-backed analysis of uploaded datasets
- [`PersonalAssistantAgent`](Langflow/Agents/PersonalAssistantAgent/README.md): operational assistant spanning productivity tools and a partial RAG branch
- [`HPCOperatorAgent`](Langflow/Agents/HPCOperatorAgent/README.md): Chimera-focused Slurm and archive operations through MCP tools
- [`VariantInterpretationResearchAgent`](Langflow/Agents/VariantInterpretationResearchAgent/README.md): ClinVar-first variant evidence workflow for biomedical research questions

## How to use the materials

1. Open one of the slide decks in [`Presentations/`](Presentations/) if you want the teaching narrative first.
2. Follow [`Langflow/README.md`](Langflow/README.md) to open Langflow through JupyterHub or install it locally if needed.
3. Browse [`Langflow/Agents/README.md`](Langflow/Agents/README.md) to choose a demonstration flow.
4. Drag and drop a `.json` export from [`Langflow/Agents/`](Langflow/Agents/) into Langflow to import it.
5. For the terminal-based coding-agent session, follow [`OpenCode/README.md`](OpenCode/README.md).
6. Read the specific agent README for setup details such as API keys, custom components, or MCP servers.
7. Run the flow in Langflow Playground and adapt it for your own teaching or experimentation.

## Why Langflow

This repository uses Langflow because it is a strong fit for teaching agentic systems visually. It makes the execution graph explicit, keeps tool wiring inspectable, and lowers the barrier to experimenting with prompts, tool calls, and multi-step workflows.

- [Langflow website](https://www.langflow.org/)
- [Langflow documentation](https://docs.langflow.org/)

## Related links

- [RSE CUNI group](https://rse.cuni.cz/RSE-1.html)
- [Langflow](https://www.langflow.org/)

## Practical note

These examples are meant for research, teaching, and workflow prototyping. They should not be treated as autonomous clinical systems, and several of them intentionally expose points where human review, constrained tool access, and clear reporting of uncertainty matter.
