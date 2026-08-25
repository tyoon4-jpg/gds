from datetime import datetime, timezone

import streamlit as st

from lib import llm, routing
from lib.knowledge import AGENTS, CATEGORY_LABELS, RECORD_CATEGORIES, RECORDS_DIR

st.title(":material/chat: 프로그램에 질문하기")

bucket = st.session_state.selected_agent
st.session_state.chat_histories.setdefault(bucket, [])
exchanges = st.session_state.chat_histories[bucket]

SUGGESTIONS = {
    "auto": [
        "노상 준비 중에 연약한 부분을 발견했습니다 — 어떻게 해야 하나요?",
        "하이셀 플랫폼은 평판재하시험을 얼마나 자주 해야 하나요?",
        "연약 점토 지반에서 50톤 크레인을 위해 필요한 두께는 얼마인가요?",
    ],
    "platform-design": [
        "Cu=25kPa 점토 지반에서 50톤 무한궤도 크레인에 필요한 두께는 얼마인가요?",
        "하이셀이 필요한가요, 아니면 골재만으로 충분한가요?",
    ],
    "platform-construction": [
        "다짐을 위한 최대 층두께는 얼마인가요?",
        "하이셀 지오셀 패널은 어떻게 설치하나요?",
    ],
    "platform-safety": [
        "크레인에서 3m 떨어진 비탈머리 근처에 인장균열이 있습니다 — 지금 어떻게 해야 하나요?",
        "굴착부에서 필요한 이격거리는 얼마인가요?",
    ],
    "site-safety": [
        "오늘 안전브리핑을 작성해주세요 — 노상 다짐과 지오셀 설치, 맑음 32°C.",
        "페블믹서 가동 중 배제구역은 어디까지인가요?",
        "지오셀 패널 설치·고정 작업에 필요한 보호구(PPE)는 무엇인가요?",
    ],
    "platform-qaqc": [
        "크레인 통행을 허용하기 전에 필요한 시험은 무엇인가요?",
        "준공 인수인계 패키지에는 무엇이 포함되나요?",
    ],
}


def build_agent_history(agent_key: str, up_to: int | None = None) -> list[dict]:
    """Reconstruct this specialist's own message history — only the exchanges it was
    actually consulted on, so its context matches what a real dispatch would see."""
    msgs = []
    for exchange in exchanges[:up_to]:
        if agent_key in exchange["responses"]:
            msgs.append({"role": "user", "content": exchange["user_text"]})
            msgs.append({"role": "assistant", "content": exchange["responses"][agent_key]})
    return msgs


def save_draft_form(exchange_idx: int, agent_key: str, response_text: str) -> None:
    agent_label = AGENTS[agent_key]["label"]
    with st.expander("초안 기록으로 저장", icon=":material/save:"):
        with st.form(key=f"save_form_{bucket}_{exchange_idx}_{agent_key}"):
            category = st.selectbox(
                "분류", RECORD_CATEGORIES,
                format_func=lambda c: CATEGORY_LABELS.get(c, c),
                key=f"cat_{bucket}_{exchange_idx}_{agent_key}",
            )
            default_name = f"{agent_key}-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
            filename = st.text_input("파일명 (확장자 제외)", value=default_name, key=f"fn_{bucket}_{exchange_idx}_{agent_key}")
            draft_banner = (
                f"> **상태: 초안(DRAFT) — 담당 기술자 검토 및 승인 대기중(PENDING)**\n"
                f"> {agent_label} 채팅 어시스턴트가 생성함 "
                f"({datetime.now(timezone.utc).strftime('%Y-%m-%d')}). 승인된 기록이 아닙니다.\n\n"
            )
            content = st.text_area(
                "내용 (저장 전 수정 가능)",
                value=draft_banner + response_text,
                height=240,
                key=f"content_{bucket}_{exchange_idx}_{agent_key}",
            )
            if st.form_submit_button("초안 저장", icon=":material/save:"):
                target_dir = RECORDS_DIR / category
                target_dir.mkdir(parents=True, exist_ok=True)
                target_path = target_dir / f"{filename}.md"
                if target_path.exists():
                    target_path = target_dir / f"{filename}-{datetime.now(timezone.utc).strftime('%H%M%S')}.md"
                target_path.write_text(content, encoding="utf-8")
                st.success(f"저장 완료: `{target_path.relative_to(RECORDS_DIR.parent)}`")


# --- Render prior exchanges ---
if not exchanges:
    st.pills("이렇게 물어보세요:", SUGGESTIONS.get(bucket, SUGGESTIONS["auto"]), key="suggestion_pill")
    if st.session_state.get("suggestion_pill"):
        st.session_state["_pending_prompt"] = st.session_state["suggestion_pill"]

for i, exchange in enumerate(exchanges):
    with st.chat_message("user"):
        st.write(exchange["user_text"])
    for agent_key, text in exchange["responses"].items():
        avatar = AGENTS[agent_key]["icon"]
        with st.chat_message("assistant", avatar=avatar):
            st.caption(f"**{AGENTS[agent_key]['label']}**")
            st.write(text)
            save_draft_form(i, agent_key, text)

# --- Handle new input ---
prompt = st.chat_input("질문을 입력하세요", submit_mode="disable")
if not prompt and st.session_state.get("_pending_prompt"):
    prompt = st.session_state.pop("_pending_prompt")

if prompt:
    if bucket == "auto":
        agents_to_ask = routing.route(prompt)
    else:
        agents_to_ask = [bucket]

    with st.chat_message("user"):
        st.write(prompt)

    if bucket == "auto" and routing.is_hazard(prompt):
        st.warning(
            "위험 상황일 가능성이 있어 안전(Safety) 담당에게 먼저 연결합니다.",
            icon=":material/warning:",
        )

    api_key = llm.get_api_key()
    new_exchange = {"user_text": prompt, "responses": {}}
    exchanges.append(new_exchange)

    for agent_key in agents_to_ask:
        avatar = AGENTS[agent_key]["icon"]
        with st.chat_message("assistant", avatar=avatar):
            st.caption(f"**{AGENTS[agent_key]['label']}**")
            history = build_agent_history(agent_key, up_to=len(exchanges) - 1)
            history.append({"role": "user", "content": prompt})
            full_text = st.write_stream(llm.stream_agent_reply(agent_key, history, api_key))
            new_exchange["responses"][agent_key] = full_text
            save_draft_form(len(exchanges) - 1, agent_key, full_text)

    st.rerun()
