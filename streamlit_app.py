import streamlit as st

from lib.knowledge import AGENTS
from lib.llm import get_api_key

st.set_page_config(
    page_title="Aggregate Working Platform — Site Assistant",
    page_icon=":material/engineering:",
    layout="wide",
)

st.session_state.setdefault("chat_histories", {})
st.session_state.setdefault("selected_agent", "auto")
st.session_state.setdefault("api_key_override", "")

with st.sidebar:
    st.markdown("### Aggregate Working Platform")
    st.caption("페블테크 / 하이셀 — site engineer assistant (prototype)")

    agent_options = ["auto"] + list(AGENTS.keys())
    agent_labels = {"auto": "Auto-route"} | {k: v["label"] for k, v in AGENTS.items()}
    st.session_state.selected_agent = st.selectbox(
        "Specialist",
        agent_options,
        format_func=lambda k: agent_labels[k],
        key="agent_select",
        index=agent_options.index(st.session_state.selected_agent),
    )
    if st.session_state.selected_agent == "auto":
        st.caption("Routes to the right specialist automatically (safety first on hazards).")
    else:
        st.caption(AGENTS[st.session_state.selected_agent]["blurb"])

    with st.expander("API key", icon=":material/key:"):
        active_key = get_api_key()
        if active_key:
            st.caption("A key is active (from secrets or environment).")
        st.text_input(
            "Override API key",
            type="password",
            key="api_key_override",
            help="Only needed if no ANTHROPIC_API_KEY is set via secrets or environment.",
        )

    with st.expander("About this prototype", icon=":material/info:"):
        st.markdown(
            "Standalone dashboard version of the repo's `.claude/agents/` program. "
            "Answers are grounded in the PRD and knowledge base files, but this interface "
            "has **no live file access** — for anything needing a specific `GDS_spec/` "
            "document or an existing `records/` draft, use Claude Code against this repo "
            "directly."
        )
        st.caption("Model: claude-sonnet-5")

pages = [
    st.Page("app_pages/chat.py", title="Ask", icon=":material/chat:"),
    st.Page("app_pages/design_calculator.py", title="Design calculator", icon=":material/calculate:"),
    st.Page("app_pages/status.py", title="Site status", icon=":material/monitoring:"),
    st.Page("app_pages/records.py", title="Records", icon=":material/folder_open:"),
]
nav = st.navigation(pages, position="top")
nav.run()
