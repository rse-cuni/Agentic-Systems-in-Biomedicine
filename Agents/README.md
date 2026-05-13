# Agents

This folder contains importable Langflow agents used in this repository. Each agent package is organized so it can be opened, understood, and reused without needing to reverse-engineer the JSON first.

---

## Folder structure

| Path | Purpose |
| ---- | ------- |
| `LabValuesInterpreterAgent/` | Educational laboratory interpretation agent |
| `DeepResearchAgent/` | Multi-agent research and synthesis pipeline |
| `PersonalAssistantAgent/` | Operational assistant spanning Gmail, Docs, Sheets, Calendar, and a partial RAG branch |
| `StatisticalAssistantAgent/` | Python-first statistical analysis assistant for uploaded datasets |
| `HPCOperatorAgent/` | Chimera-focused Slurm operator with MCP-based cluster and archive tools |
| `LiteratureAgent/` | Literature review pipeline with planning, retrieval, and final synthesis stages |
| `VariantInterpretationResearchAgent/` | Variant-focused biomedical evidence workflow centered on ClinVar and PubMed |
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

## Install Langflow

You can use these agents either in Langflow Desktop or in a Python-installed Langflow instance. Desktop is the easiest path for workshops, while the Python route gives you more direct control over versions and packages.

### Option 1 - Langflow Desktop

1. Download and install Langflow Desktop from the [Langflow website](https://www.langflow.org/).
2. Open the app once so it can create its internal files and virtual environment.
3. Import one of the flow JSON files from this folder.
4. Configure the credentials required by that agent.

Langflow Desktop creates its own Python environment. That means packages used by Langflow tools, especially the **Python Interpreter**, must be installed into the Desktop environment instead of only into your normal system Python.

On macOS, the Desktop Python interpreter is usually:

```bash
"$HOME/.langflow/.langflow-venv/bin/python"
```

To install one package directly into that environment:

```bash
"$HOME/.langflow/.langflow-venv/bin/python" -m pip install PACKAGE_NAME
```

On Windows, the Desktop Python interpreter is usually:

```powershell
& "$env:APPDATA\com.Langflow\.langflow-venv\Scripts\python.exe"
```

To install one package directly into that environment:

```powershell
& "$env:APPDATA\com.Langflow\.langflow-venv\Scripts\python.exe" -m pip install PACKAGE_NAME
```

The safer Desktop method is to add packages to Langflow Desktop's `requirements.txt` file and then restart the app. Langflow Desktop will install those packages into its own virtual environment.

On macOS, the file is:

```bash
$HOME/.langflow/data/requirements.txt
```

On Windows, the file is:

```powershell
$env:APPDATA\com.Langflow\data\requirements.txt
```

### Option 2 - Python package with uv

Use this route if you want a browser-based local Langflow server and full control over the Python environment.

```bash
uv venv langflow-venv
source langflow-venv/bin/activate
uv pip install langflow
uv run langflow run
```

Then open Langflow in your browser at:

```text
http://127.0.0.1:7860
```

On Windows PowerShell:

```powershell
uv venv langflow-venv
.\langflow-venv\Scripts\Activate.ps1
uv pip install langflow
uv run langflow run
```

Then open:

```text
http://127.0.0.1:7860
```

---

## Installing Python libraries for agents

The `StatisticalAssistantAgent` and any flow using the **Python Interpreter** need their analysis libraries installed in the same Python environment that Langflow is using.

Useful starter libraries for statistics and data analysis are:

```text
pandas
numpy
scipy
statsmodels
scikit-learn
matplotlib
seaborn
plotly
openpyxl
```

### Langflow Desktop on macOS

Add the starter libraries to Desktop's requirements file:

```bash
mkdir -p "$HOME/.langflow/data"
cat >> "$HOME/.langflow/data/requirements.txt" <<'EOF'
pandas
numpy
scipy
statsmodels
scikit-learn
matplotlib
seaborn
plotly
openpyxl
EOF
```

Restart Langflow Desktop after editing `requirements.txt`.

If you only need one package quickly, you can install it directly:

```bash
"$HOME/.langflow/.langflow-venv/bin/python" -m pip install PACKAGE_NAME
```

### Langflow Desktop on Windows

Add the starter libraries to Desktop's requirements file:

```powershell
New-Item -ItemType Directory -Force "$env:APPDATA\com.Langflow\data" | Out-Null
@"
pandas
numpy
scipy
statsmodels
scikit-learn
matplotlib
seaborn
plotly
openpyxl
"@ | Add-Content "$env:APPDATA\com.Langflow\data\requirements.txt"
```

Restart Langflow Desktop after editing `requirements.txt`.

If you only need one package quickly, you can install it directly:

```powershell
& "$env:APPDATA\com.Langflow\.langflow-venv\Scripts\python.exe" -m pip install PACKAGE_NAME
```

### Python-installed Langflow

If you installed Langflow with `uv`, activate the same environment first and install the packages there:

```bash
source langflow-venv/bin/activate
uv pip install pandas numpy scipy statsmodels scikit-learn matplotlib seaborn plotly openpyxl
```

On Windows PowerShell:

```powershell
.\langflow-venv\Scripts\Activate.ps1
uv pip install pandas numpy scipy statsmodels scikit-learn matplotlib seaborn plotly openpyxl
```

---

## How to import flows into Langflow

Use the same general process for all agent packages in this folder.

### Option 1 - Langflow in the browser

1. Open your Langflow workspace in the browser, for example `http://localhost:7860`.
2. Click **New Flow**.
3. Choose **Import from file**.
4. Select the relevant `.json` file from this folder.
5. Open the imported flow and configure the required credentials or tools.
6. Launch **Playground** and test a simple request first.

### Option 2 - Langflow desktop app

1. Open the Langflow desktop app.
2. Go to your workspace or flows view.
3. Create a new flow or use the import action from the main toolbar or menu.
4. Choose **Import from file**.
5. Select the relevant `.json` file from this folder.
6. Open the imported flow and configure the required credentials or tools.
7. Launch **Playground** inside the app and test a simple request first.

### Flow files

| Agent | Flow file |
| ----- | --------- |
| `LabValuesInterpreterAgent` | `Agents/LabValuesInterpreterAgent/LabValuesInterpreterAgent.json` |
| `DeepResearchAgent` | `Agents/DeepResearchAgent/DeepResearchAgent.json` |
| `PersonalAssistantAgent` | `Agents/PersonalAssistantAgent/PersonalAssistantAgent.json` |
| `StatisticalAssistantAgent` | `Agents/StatisticalAssistantAgent/StatisticalAssistantAgent.json` |
| `HPCOperatorAgent` | `Agents/HPCOperatorAgent/HPCOperatorAgent.json` |
| `LiteratureAgent` | `Agents/LiteratureAgent/LiteratureAgent.json` |
| `VariantInterpretationResearchAgent` | `Agents/VariantInterpretationResearchAgent/VariantInterpretationResearchAgent.json` |

### Setup notes by agent

| Agent | What to configure after import |
| ----- | ------------------------------ |
| `LabValuesInterpreterAgent` | Add your OpenAI API key in the custom model node |
| `DeepResearchAgent` | Add one OpenAI API key and choose the shared model for all research agents |
| `PersonalAssistantAgent` | Add OpenAI API keys, complete Composio auth for Gmail, Docs, Sheets, and Calendar, and configure Astra DB if you want the RAG branch |
| `StatisticalAssistantAgent` | Add your OpenAI API key and confirm the Python Interpreter and Read File tools are available |
| `HPCOperatorAgent` | Add your OpenAI API key and confirm the `chimera-slurm` and `chimera-filecompress` MCP servers are available |
| `LiteratureAgent` | Add your OpenAI API key and confirm the `arXiv`, Web Search, and URL components can run in your Langflow environment |
| `VariantInterpretationResearchAgent` | Add your OpenAI API key, point `LANGFLOW_COMPONENTS_PATH` at `Agents/VariantInterpretationResearchAgent/custom_components`, and fill in the NCBI email plus optional NCBI API key on the ClinVar and PubMed components |

### Personal Assistant Gmail hotfix

The `PersonalAssistantAgent` uses the Composio Gmail component. If Gmail fails with a Composio `type` or schema error, avoid upgrading straight to `composio==0.13.0` in Langflow Desktop. That version can pull newer LangChain dependencies that may not be safe for the Desktop Langflow version used in this workshop.

Patch the older Composio file directly instead.

On macOS, the file is:

```bash
$HOME/.langflow/.langflow-venv/lib/python3.12/site-packages/composio/core/models/_files.py
```

Create a backup:

```bash
cp -n "$HOME/.langflow/.langflow-venv/lib/python3.12/site-packages/composio/core/models/_files.py" \
   "$HOME/.langflow/.langflow-venv/lib/python3.12/site-packages/composio/core/models/_files.py.bak"
```

Apply the hotfix:

```bash
"$HOME/.langflow/.langflow-venv/bin/python" - <<'PY'
from pathlib import Path

p = Path.home() / ".langflow/.langflow-venv/lib/python3.12/site-packages/composio/core/models/_files.py"
s = p.read_text()

old = 'if isinstance(request[_param], dict) and params[_param]["type"] == "object":'
new = 'if isinstance(request[_param], dict) and isinstance(params.get(_param), dict) and params[_param].get("type") == "object":'

if old not in s:
    print("Pattern not found. The file may already be patched or the code is different.")
else:
    p.write_text(s.replace(old, new))
    print("Patch applied.")
PY
```

On Windows, the file is usually:

```powershell
$env:APPDATA\com.Langflow\.langflow-venv\Lib\site-packages\composio\core\models\_files.py
```

Create a backup:

```powershell
$source = "$env:APPDATA\com.Langflow\.langflow-venv\Lib\site-packages\composio\core\models\_files.py"
$backup = "$source.bak"
if (-not (Test-Path $backup)) {
  Copy-Item $source $backup
}
```

Apply the hotfix:

```powershell
& "$env:APPDATA\com.Langflow\.langflow-venv\Scripts\python.exe" -c @'
from pathlib import Path
import os

p = Path(os.environ["APPDATA"]) / "com.Langflow/.langflow-venv/Lib/site-packages/composio/core/models/_files.py"
s = p.read_text()

old = 'if isinstance(request[_param], dict) and params[_param]["type"] == "object":'
new = 'if isinstance(request[_param], dict) and isinstance(params.get(_param), dict) and params[_param].get("type") == "object":'

if old not in s:
    print("Pattern not found. The file may already be patched or the code is different.")
else:
    p.write_text(s.replace(old, new))
    print("Patch applied.")
'@
```

The hotfix changes the unsafe lookup:

```python
if isinstance(request[_param], dict) and params[_param]["type"] == "object":
```

to a guarded lookup:

```python
if isinstance(request[_param], dict) and isinstance(params.get(_param), dict) and params[_param].get("type") == "object":
```

This prevents Composio from crashing when a Gmail tool parameter named `type` or a malformed schema entry reaches the file handling logic.

### Suggested first test

- Start with a simple request after import so you can confirm the flow loads, credentials work, and the main tool path is connected before trying a more complex task.

---

## Agent packages in this folder

- [`LabValuesInterpreterAgent`](LabValuesInterpreterAgent/README.md): structured educational interpretation of laboratory results
- [`DeepResearchAgent`](DeepResearchAgent/README.md): staged research workflow for source gathering, synthesis, review, and final writing
- [`PersonalAssistantAgent`](PersonalAssistantAgent/README.md): multi-agent operational assistant for email, documents, calendar work, and knowledge retrieval
- [`StatisticalAssistantAgent`](StatisticalAssistantAgent/README.md): reproducible statistical analysis flow with file reading and Python execution
- [`HPCOperatorAgent`](HPCOperatorAgent/README.md): Slurm operations assistant for Chimera with MCP-based job, file, and archive tooling
- [`LiteratureAgent`](LiteratureAgent/README.md): staged literature search and synthesis flow using `arXiv`, web search, and URL retrieval
- [`VariantInterpretationResearchAgent`](VariantInterpretationResearchAgent/README.md): ClinVar-first variant evidence workflow for biomedical research questions

---

## Practical note

These flows are designed as working research prototypes. Langflow provides the orchestration layer, while the custom OpenAI component keeps model choice flexible enough for newer or stronger LLMs that may not yet be exposed cleanly in the stock UI.
