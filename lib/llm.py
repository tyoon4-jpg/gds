"""Anthropic API wrapper for the dashboard's chat agents."""

from __future__ import annotations

import os
from collections.abc import Iterator

import anthropic
import streamlit as st

from lib.knowledge import build_system_prompt

MODEL = "claude-sonnet-5"
MAX_TOKENS = 8000


def get_api_key() -> str | None:
    """Resolve the API key: sidebar override > st.secrets > environment variable."""
    override = st.session_state.get("api_key_override")
    if override:
        return override
    try:
        secret = st.secrets.get("ANTHROPIC_API_KEY")
        if secret:
            return secret
    except Exception:
        pass
    return os.environ.get("ANTHROPIC_API_KEY")


@st.cache_resource(show_spinner=False)
def _get_client(api_key: str) -> anthropic.Anthropic:
    return anthropic.Anthropic(api_key=api_key)


def stream_agent_reply(agent_key: str, messages: list[dict], api_key: str) -> Iterator[str]:
    """Yield response text chunks for one specialist answering the given message history.
    Yields a single formatted error string (instead of raising) on failure, so the chat UI
    stays usable — callers should treat a yielded string starting with '⚠' as an error."""
    if not api_key:
        yield (
            "⚠ No Anthropic API key configured. Set `ANTHROPIC_API_KEY` in "
            "`.streamlit/secrets.toml`, as an environment variable, or in the sidebar field."
        )
        return

    client = _get_client(api_key)
    system_prompt = build_system_prompt(agent_key)

    try:
        with client.messages.stream(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=[
                {
                    "type": "text",
                    "text": system_prompt,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=messages,
        ) as stream:
            yield from stream.text_stream
    except anthropic.AuthenticationError:
        yield "⚠ Authentication failed — check that the API key is valid."
    except anthropic.RateLimitError:
        yield "⚠ Rate limited by the API. Wait a moment and try again."
    except anthropic.APIStatusError as e:
        yield f"⚠ API error ({e.status_code}): {e.message}"
    except anthropic.APIConnectionError:
        yield "⚠ Network error reaching the Anthropic API. Check your connection."
