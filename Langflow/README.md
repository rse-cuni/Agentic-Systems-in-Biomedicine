# Langflow

This folder contains the Langflow exports and documentation used in the Agentic Systems in Biomedicine workshop.

For the workshop, the recommended way to run Langflow is through the managed JupyterHub instance. Local installation is possible on Windows, Linux, and macOS, but it can be hard to debug because Langflow has many Python and system-level dependencies.

## Recommended: JupyterHub

Use the JupyterHub-hosted Langflow whenever possible:

<https://hpc.troja.mff.cuni.cz:8000/hub/spawn>

You need access through CAS. If you cannot log in, ask for CAS or JupyterHub access before trying to install Langflow locally.

After logging in:

1. Open the JupyterHub spawn page.
2. Find the **Notebook** section.
3. Click the **LangFlow** launcher tile. In the provided screenshot, it is in the first row of notebook launchers, between **gnuplot** and **NEST Desktop**.
4. Wait for Langflow to start.
5. Drag and drop one of the JSON flows from [`Agents/`](Agents/) into Langflow to import it.

## Local Installation Warning

Local Langflow installation is useful for personal experimentation, but it is not the preferred workshop path. It may fail because of Python version mismatches, missing build tools, package dependency conflicts, unavailable system libraries, or differences between shells and virtual environments.

If you only need to follow the workshop, use the JupyterHub Langflow launcher instead.

## Install on Windows

The easiest Windows route is Langflow Desktop.

1. Download Langflow Desktop from <https://www.langflow.org/>.
2. Run the `.msi` installer.
3. If the installer or package setup asks for Microsoft C++ Build Tools, install them and rerun Langflow.
4. Open Langflow Desktop.
5. Drag and drop a flow JSON file from [`Agents/`](Agents/) into Langflow to import it.

For a Python-based installation, use PowerShell:

```powershell
uv venv langflow-venv
.\langflow-venv\Scripts\activate
uv pip install langflow
uv run langflow run
```

Then open:

```text
http://127.0.0.1:7860
```

## Install on Linux

On Linux, Docker is often the least painful local option if Docker is already available:

```bash
docker run -p 7860:7860 langflowai/langflow:latest
```

Then open:

```text
http://127.0.0.1:7860
```

For a Python-based installation:

```bash
uv venv langflow-venv
source langflow-venv/bin/activate
uv pip install langflow
uv run langflow run
```

Then open:

```text
http://127.0.0.1:7860
```

## Install on macOS

The easiest macOS route is Langflow Desktop.

1. Download Langflow Desktop from <https://www.langflow.org/>.
2. Install the app from the downloaded disk image.
3. Open Langflow Desktop.
4. Drag and drop a flow JSON file from [`Agents/`](Agents/) into Langflow to import it.

For a Python-based installation:

```bash
uv venv langflow-venv
source langflow-venv/bin/activate
uv pip install langflow
uv run langflow run
```

Then open:

```text
http://127.0.0.1:7860
```

## Import the Workshop Flows

The flow exports are in [`Agents/`](Agents/). Start with [`Agents/README.md`](Agents/README.md) for the list of available agents and setup notes.

General import process:

1. Open Langflow.
2. Drag and drop the relevant `.json` file from [`Agents/`](Agents/) into the Langflow workspace.
3. If your Langflow version shows an import action, you can use it, but there may be no visible **Import flow** button.
4. Configure required API keys and credentials.
5. Run a small test in the Langflow Playground before using the full workflow.

## Add the e-INFRA CZ LLM Component

This repository includes an e-INFRA CZ model-provider component at [`Components/einfra_cz_model.py`](Components/einfra_cz_model.py). It connects Langflow to the OpenAI-compatible e-INFRA LLM gateway:

```text
https://llm.ai.e-infra.cz/v1
```

The fastest way to add it:

1. Open Langflow.
2. Add a **Custom Component** to the canvas.
3. Open the component code editor.
4. Paste the full contents of [`Components/einfra_cz_model.py`](Components/einfra_cz_model.py).
5. Save the component.
6. Connect its **Language Model** output to an Agent, Language Model, RAG, or smart-function component.

You can also load it from disk by copying it into Langflow's custom components directory and restarting Langflow:

```bash
mkdir -p "$HOME/.langflow/components"
cp Langflow/Components/einfra_cz_model.py "$HOME/.langflow/components/"
```

If you start Langflow from this repository, another option is to point `LANGFLOW_COMPONENTS_PATH` at the included folder:

```bash
export LANGFLOW_COMPONENTS_PATH="$PWD/Langflow/Components"
uv run langflow run
```

Create an e-INFRA API key in Open WebUI under **Settings -> Account -> API keys**. Paste it into the component's **e-INFRA API Token** field, or set it before starting Langflow:

```bash
export E_INFRA_API_TOKEN="your-token"
```

See [`Components/README.md`](Components/README.md) for the full component guide.

## Useful Links

- [Langflow installation documentation](https://docs.langflow.org/get-started-installation)
- [Langflow website](https://www.langflow.org/)
- [Workshop agent flows](Agents/)
