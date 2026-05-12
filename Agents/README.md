# Agents

This folder contains importable Langflow agents used in this repository. Each agent package is organized so it can be opened, understood, and reused without needing to reverse-engineer the JSON first.

---

## Folder structure

| Path | Purpose |
| ---- | ------- |
| `LabValuesInterpreter/` | Educational laboratory interpretation agent |
| `DeepResearchAgent/` | Multi-agent research and synthesis pipeline |
| `PersonalAssistant/` | Operational assistant spanning Gmail, Docs, Sheets, Calendar, and a partial RAG branch |
| `*/README.md` | Human-readable guide for the flow |
| `*/images/` | Screenshots used in the documentation |
| `*.json` | Langflow export ready to import |

---

## Why we use a custom OpenAI component

Langflow is a very useful open-source workflow builder, especially for prototyping and teaching. In practice, though, its built-in model selectors can lag behind the newest high-end OpenAI models and naming changes.

That matters in this repo because the agents are meant to work with stronger and newer model families, not only the default model options that happen to ship with a given Langflow release.

To make the flows more stable, every agent JSON in this folder uses an `OpenAI Custom Model` component pattern. The idea is simple:

1. Keep OpenAI authentication inside the flow.
2. Let the user pick from common model names.
3. Keep an escape hatch for any current or future model string.
4. Avoid being blocked by Langflow UI lag when frontier models change faster than the builder UI.

---

## Standard custom component

Use this component when Langflow does not expose the model you need in the default OpenAI node.

```python
from langflow.custom import Component
from langflow.io import Output, SecretStrInput, StrInput, DropdownInput, FloatInput
from langflow.field_typing import LanguageModel
from langchain_openai import ChatOpenAI


class CustomOpenAIModel(Component):
    display_name = "OpenAI Custom Model"
    description = "OpenAI with selectable model or custom string"

    OPENAI_MODELS = [
        # GPT-5.5 family (flagship, 2026)
        "gpt-5.5",
        # GPT-5.4 family (current production tier)
        "gpt-5.4",
        "gpt-5.4-thinking",
        "gpt-5.4-pro",
        "gpt-5.4-mini",
        "gpt-5.4-nano",
        # GPT-5 family (previous gen, still solid)
        "gpt-5",
        "gpt-5-mini",
        "gpt-5-nano",
        # GPT-4.1 family (cheap workhorses)
        "gpt-4.1",
        "gpt-4.1-mini",
        "gpt-4.1-nano",
        # GPT-4o family (legacy multimodal)
        "gpt-4o",
        "gpt-4o-mini",
        # Reasoning models
        "o3",
        "o3-mini",
        "o4-mini",
        # Escape hatch
        "custom",
    ]

    inputs = [
        SecretStrInput(
            name="api_key",
            display_name="API Key",
            required=True,
        ),
        DropdownInput(
            name="model_name",
            display_name="Model",
            options=OPENAI_MODELS,
            value="gpt-5.4-mini",
            info="Pick a model. Choose 'custom' to type any model string in the field below.",
        ),
        StrInput(
            name="custom_model_name",
            display_name="Custom Model String",
            value="",
            info="Only used if 'custom' is selected above. Type any valid OpenAI model string (e.g. gpt-5.4-nano-2026-03-17).",
            advanced=True,
        ),
        FloatInput(
            name="temperature",
            display_name="Temperature",
            value=0.3,
            info="0 = deterministic, 1 = creative. Use 0.2 for tool use, 0.7+ for writing.",
        ),
    ]

    outputs = [
        Output(
            name="model",
            display_name="Language Model",
            method="build_model",
        )
    ]

    def build_model(self) -> LanguageModel:
        model = self.model_name
        if model == "custom":
            if not self.custom_model_name.strip():
                raise ValueError(
                    "You selected 'custom' but didn't enter a model string. "
                    "Either pick a model from the dropdown or fill in the Custom Model String field."
                )
            model = self.custom_model_name.strip()

        return ChatOpenAI(
            model=model,
            api_key=self.api_key,
            temperature=self.temperature,
        )
```

---

## How to use the component in Langflow

1. Import one of the JSON files from this folder.
2. Open the `OpenAI Custom Model` node inside the flow.
3. Paste your OpenAI API key.
4. Choose a model from the dropdown, or select `custom` and type the exact model string.
5. Connect the `Language Model` output to the relevant agent or language model node if you are building a new flow.

If a flow imports without the custom node rendering correctly, recreate the component with the code above and reconnect its output.

---

## Agent packages in this folder

- [`LabValuesInterpreter`](LabValuesInterpreter/README.md): structured educational interpretation of laboratory results
- [`DeepResearchAgent`](DeepResearchAgent/README.md): staged research workflow for source gathering, synthesis, review, and final writing
- [`PersonalAssistant`](PersonalAssistant/README.md): multi-agent operational assistant for email, documents, calendar work, and knowledge retrieval

---

## Practical note

These flows are designed as working research prototypes. Langflow provides the orchestration layer, while the custom OpenAI component keeps model choice flexible enough for newer or stronger LLMs that may not yet be exposed cleanly in the stock UI.
