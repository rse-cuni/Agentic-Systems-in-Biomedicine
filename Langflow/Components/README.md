# Langflow Custom Components

This folder contains reusable custom components for the Langflow examples.

## e-INFRA CZ LLM

[`einfra_cz_model.py`](einfra_cz_model.py) adds an **e-INFRA CZ LLM** model-provider component for the Czech national research LLM gateway:

```text
https://llm.ai.e-infra.cz/v1
```

The gateway is OpenAI-API compatible, so the component returns a Langflow `Language Model` handle backed by `ChatOpenAI`.

Use the component output with:

- a Langflow **Language Model** component for simple chat flows
- an **Agent** component for tool-calling flows
- RAG or smart-function components that accept an LLM handle

## Add the component to Langflow

### Paste into a Custom Component

1. Open Langflow.
2. Add a **Custom Component** to the canvas.
3. Open its code editor.
4. Paste the full contents of [`einfra_cz_model.py`](einfra_cz_model.py).
5. Save the component.
6. Connect the **Language Model** output to an agent, language-model node, or RAG component.

## Authentication

Generate an API key in Open WebUI:

1. Open Open WebUI for the e-INFRA LLM gateway.
2. Go to **Settings -> Account -> API keys**.
3. Create a key.
4. Paste it into the component's **e-INFRA API Token** field.

You can also set the token as an environment variable before launching Langflow:

```bash
export E_INFRA_API_TOKEN="your-token"
```

Then leave the **e-INFRA API Token** field blank.

## Notes

- The component intentionally extends plain `Component`, not `LCModelComponent`, because `LCModelComponent` can inject fields rejected by the e-INFRA vLLM backend.
- Large MoE models can take longer than 60 seconds or occasionally return transient 502/503 errors, so `timeout` and `max_retries` are exposed in the UI.
- Thinking is opt-in and only sent for model names that look like reasoning models.
