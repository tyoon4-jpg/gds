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
            "⚠ Anthropic API 키가 설정되어 있지 않습니다. `.streamlit/secrets.toml`에 "
            "`ANTHROPIC_API_KEY`를 설정하거나, 환경변수로 지정하거나, 사이드바에 직접 입력하세요."
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
        yield "⚠ 인증 실패 — API 키가 올바른지 확인하세요."
    except anthropic.RateLimitError:
        yield "⚠ API 사용량 제한에 걸렸습니다. 잠시 후 다시 시도하세요."
    except anthropic.APIStatusError as e:
        yield f"⚠ API 오류 ({e.status_code}): {e.message}"
    except anthropic.APIConnectionError:
        yield "⚠ Anthropic API 연결에 실패했습니다. 네트워크 연결을 확인하세요."
