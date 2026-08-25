import streamlit as st

from lib.knowledge import AGENTS
from lib.llm import get_api_key

st.set_page_config(
    page_title="Aggregate Working Platform — 현장 지원 도구",
    page_icon=":material/engineering:",
    layout="wide",
)

st.session_state.setdefault("chat_histories", {})
st.session_state.setdefault("selected_agent", "auto")
st.session_state.setdefault("api_key_override", "")

with st.sidebar:
    st.markdown("### Aggregate Working Platform")
    st.caption("페블테크 / 하이셀 — 현장 기술자 지원 도구 (프로토타입)")

    agent_options = ["auto"] + list(AGENTS.keys())
    agent_labels = {"auto": "자동 라우팅"} | {k: v["label"] for k, v in AGENTS.items()}
    st.session_state.selected_agent = st.selectbox(
        "전문 분야",
        agent_options,
        format_func=lambda k: agent_labels[k],
        key="agent_select",
        index=agent_options.index(st.session_state.selected_agent),
    )
    if st.session_state.selected_agent == "auto":
        st.caption("질문 내용에 맞는 전문 분야로 자동 연결됩니다 (위험 상황은 안전을 최우선으로 처리).")
    else:
        st.caption(AGENTS[st.session_state.selected_agent]["blurb"])

    with st.expander("API 키", icon=":material/key:"):
        active_key = get_api_key()
        if active_key:
            st.caption("API 키가 설정되어 있습니다 (secrets 또는 환경변수 사용 중).")
        st.text_input(
            "API 키 직접 입력 (선택)",
            type="password",
            key="api_key_override",
            help="secrets 또는 환경변수에 ANTHROPIC_API_KEY가 설정되어 있지 않을 때만 입력하세요.",
        )

    with st.expander("이 프로토타입 정보", icon=":material/info:"):
        st.markdown(
            "이 저장소의 `.claude/agents/` 프로그램을 독립형 대시보드 형태로 만든 버전입니다. "
            "답변은 PRD와 지식 베이스 파일을 근거로 작성되지만, 이 화면은 "
            "**실시간 파일 접근 기능이 없습니다** — 특정 `GDS_spec/` 문서나 기존 "
            "`records/` 초안이 필요한 경우, 이 저장소에서 Claude Code를 직접 사용하세요."
        )
        st.caption("모델: claude-sonnet-5")

pages = [
    st.Page("app_pages/chat.py", title="질문하기", icon=":material/chat:"),
    st.Page("app_pages/design_calculator.py", title="설계 계산기", icon=":material/calculate:"),
    st.Page("app_pages/daily_safety.py", title="일일 안전문서", icon=":material/shield_person:"),
    st.Page("app_pages/status.py", title="현장 현황", icon=":material/monitoring:"),
    st.Page("app_pages/records.py", title="기록", icon=":material/folder_open:"),
]
nav = st.navigation(pages, position="top")
nav.run()
