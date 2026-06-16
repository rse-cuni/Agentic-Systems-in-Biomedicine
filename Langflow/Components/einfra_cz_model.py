"""
e-INFRA CZ LLM - Model Provider for Langflow
============================================
A pure model-provider component for the Czech national research LLM gateway
(https://llm.ai.e-infra.cz/v1), which is OpenAI-API compatible.

Wire its "Language Model" output into:
  - Language Model component   (simple chat flows)
  - Agent component            (agentic / tool-calling flows)
  - any RAG / Smart-function component that takes an LLM handle

Install:
  - Paste into a Custom Component's code editor in the Langflow canvas, OR
  - Copy to ~/.langflow/components/ (or LANGFLOW_COMPONENTS_PATH) and restart.

Auth:
  - Generate an API key in Open WebUI (Settings -> Account -> API keys).
  - Either paste it into the "e-INFRA API Token" field, or set the
    E_INFRA_API_TOKEN environment variable and Langflow will auto-read it.

Notes on the design choices:
  - Extends the plain `Component`, NOT `LCModelComponent`. The latter injects a
    `reasoning_effort="minimal"` field that the e-INFRA vLLM backend rejects.
  - `timeout` / `max_retries` are exposed because large MoE models
    (kimi, deepseek-v4-pro) can take >60 s and occasionally 502 on a cold start.
  - Thinking is opt-in via `extra_body` and only for *-thinking models.
"""

import os
from typing import Any

import httpx
from langchain_openai import ChatOpenAI
from langflow.custom import Component
from langflow.field_typing import LanguageModel
from langflow.field_typing.range_spec import RangeSpec
from langflow.inputs.inputs import (
    BoolInput,
    DropdownInput,
    FloatInput,
    IntInput,
    SecretStrInput,
    SliderInput,
    StrInput,
)
from langflow.template import Output

EINFRA_BASE_URL = "https://llm.ai.e-infra.cz/v1"

# Model lineup per docs.cerit.io (effective 2026-03-30). Availability shifts;
# query GET /v1/models for the live list, or use the "Custom Model" override.
EINFRA_CHAT_MODELS = [
    # Guaranteed long-term availability
    "gpt-oss-120b",
    "deepseek-v4-pro-thinking",
    "qwen3.5-122b",
    # Experimental
    "glm-5",
    "kimi-k2.6",
    "qwen3.5",
    "mistral-medium-3.5",
    # Deprecated, kept for reproducibility and may vanish
    "deepseek-v3.2-thinking",
    "deepseek-v3.2",
    "gemma3-it",
    "mistral-small-4",
]

# Models that accept a thinking/reasoning budget through extra_body.
THINKING_HINTS = ("thinking", "thinker", "reason")

DEFAULT_TIMEOUT = 120


class EInfraCZModelComponent(Component):
    """Model provider for the e-INFRA CZ OpenAI-compatible LLM gateway."""

    display_name = "e-INFRA CZ LLM"
    description = (
        "Provides a Language Model handle for the Czech e-INFRA research LLM "
        "gateway (llm.ai.e-infra.cz). Requires a MetaCentrum / Open WebUI API key."
    )
    icon = "cpu"
    name = "EInfraCZModel"

    inputs = [
        DropdownInput(
            name="model_name",
            display_name="Model",
            options=EINFRA_CHAT_MODELS,
            value="gpt-oss-120b",
            info="Pick a model from the gateway. Tool-calling-capable choices "
            "for Agent flows: qwen3.5, qwen3.5-122b, kimi-k2.6, glm-5, "
            "deepseek-v4-pro-thinking, mistral-medium-3.5.",
            advanced=False,
        ),
        StrInput(
            name="custom_model",
            display_name="Custom Model (override)",
            info="If set, overrides the dropdown. Use the exact, case-sensitive "
            "name from GET /v1/models, for example 'llama3.3:latest'.",
            advanced=True,
        ),
        SecretStrInput(
            name="api_key",
            display_name="e-INFRA API Token",
            info="Open WebUI API key. Auto-reads the E_INFRA_API_TOKEN env-var "
            "if left blank.",
            required=False,
        ),
        StrInput(
            name="base_url",
            display_name="Base URL",
            value=EINFRA_BASE_URL,
            info="OpenAI-compatible endpoint. Change only if e-INFRA moves it.",
            advanced=True,
        ),
        SliderInput(
            name="temperature",
            display_name="Temperature",
            value=0.7,
            range_spec=RangeSpec(min=0, max=2, step=0.01),
            advanced=False,
        ),
        IntInput(
            name="max_tokens",
            display_name="Max Output Tokens",
            info="0 / blank = let the model decide.",
            advanced=True,
        ),
        BoolInput(
            name="enable_thinking",
            display_name="Enable Thinking",
            value=False,
            info="Only for *-thinking / reasoning models. Sends "
            "extra_body.chat_template_kwargs.enable_thinking.",
            advanced=True,
        ),
        IntInput(
            name="thinking_budget",
            display_name="Thinking Budget (tokens)",
            value=2048,
            info="Max tokens the model may spend reasoning. Ignored unless "
            "Enable Thinking is on and the model supports it.",
            advanced=True,
        ),
        IntInput(
            name="timeout",
            display_name="Request Timeout (s)",
            value=DEFAULT_TIMEOUT,
            info="Total read timeout. Bump to 180-300 for big MoE models.",
            advanced=True,
        ),
        IntInput(
            name="max_retries",
            display_name="Max Retries",
            value=2,
            info="Auto-retries on transient 502/503/timeouts.",
            advanced=True,
        ),
        FloatInput(
            name="top_p",
            display_name="Top P",
            value=1.0,
            advanced=True,
        ),
        BoolInput(
            name="streaming",
            display_name="Stream",
            value=True,
            advanced=True,
        ),
    ]

    outputs = [
        Output(
            display_name="Language Model",
            name="model_output",
            method="build_model",
        ),
    ]

    def build_model(self) -> LanguageModel:
        model_id = (self.custom_model or "").strip() or self.model_name

        # Send thinking fields only when explicitly enabled for a reasoning model.
        extra_body: dict[str, Any] = {}
        if self.enable_thinking and any(h in model_id.lower() for h in THINKING_HINTS):
            extra_body["chat_template_kwargs"] = {"enable_thinking": True}
            if self.thinking_budget and self.thinking_budget > 0:
                extra_body["thinking_budget"] = int(self.thinking_budget)

        timeout_val = float(self.timeout or DEFAULT_TIMEOUT)
        http_timeout = httpx.Timeout(timeout_val, connect=10.0)

        api_key = self.api_key or os.getenv("E_INFRA_API_TOKEN") or None

        kwargs: dict[str, Any] = {
            "model": model_id,
            "base_url": (self.base_url or EINFRA_BASE_URL).rstrip("/"),
            "api_key": api_key,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "streaming": self.streaming,
            "timeout": http_timeout,
            "max_retries": int(self.max_retries or 0),
        }

        if self.max_tokens:
            kwargs["max_tokens"] = int(self.max_tokens)
        if extra_body:
            kwargs["extra_body"] = extra_body

        return ChatOpenAI(**kwargs)
