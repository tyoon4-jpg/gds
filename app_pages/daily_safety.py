from datetime import date, datetime, timezone

import streamlit as st

from lib import llm
from lib.knowledge import AGENTS, CATEGORY_LABELS, RECORD_CATEGORIES, RECORDS_DIR

AGENT_KEY = "site-safety"
EQUIPMENT_OPTIONS = [
    "롤러 / 다짐장비",
    "굴착기",
    "페블믹서 (현장 골재 배합장비)",
    "크레인",
    "덤프트럭",
    "수공구 / 지오셀 고정핀 작업도구",
]

st.title(":material/shield_person: 일일 안전문서")
st.caption(
    "오늘의 현장 조건을 입력하면 현장 안전(Site Safety) 담당이 안전브리핑/TBM 문서를 작성합니다 "
    "— 보호구(PPE), 일반 현장 위험, 장비 안전을 다룹니다. 플랫폼 관련 위험 항목(배제구역, 진행중인 "
    "홀드 등)은 안전(Safety) 기록을 참고해 인용할 뿐 여기서 새로 계산하지 않습니다 — 현장 현황 "
    "페이지를 확인하거나 안전 담당에게 직접 문의하세요."
)

st.session_state.setdefault("daily_safety_doc", "")

with st.form("daily_safety_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        briefing_date = st.date_input("날짜", value=date.today())
    with col2:
        site_zone = st.text_input("현장 / 구역", placeholder="예: 3구역 — 크레인 플랫폼")
    with col3:
        crew_size = st.number_input("작업 인원", min_value=0, step=1, value=0)

    col4, col5 = st.columns(2)
    with col4:
        weather = st.text_input(
            "기상 조건",
            placeholder="예: 맑음, 32°C, 약한 바람",
        )
    with col5:
        equipment = st.multiselect("오늘 투입 장비", EQUIPMENT_OPTIONS)
        other_equipment = st.text_input("기타 장비 (목록에 없는 경우)", placeholder="선택사항")

    activities = st.text_area(
        "오늘의 작업 계획",
        placeholder="예: 3구역 노상 다짐, 지오셀 패널 설치 및 고정",
    )
    known_hazards = st.text_area(
        "오늘 알려진 현장별 위험요소 (선택사항)",
        placeholder="예: 3구역에서 5m 떨어진 곳에 굴착부 있음, 어제 비로 지반이 아직 젖어있음",
    )
    platform_note = st.text_input(
        "플랫폼 관련 안내사항 (선택사항)",
        placeholder="예: 현재 배제구역, 진행중인 홀드 — 없으면 비워두세요",
    )

    submitted = st.form_submit_button("일일 안전문서 생성", icon=":material/auto_awesome:")

if submitted:
    if not activities.strip():
        st.warning("오늘의 작업 계획을 최소한 입력해야 브리핑 내용이 구체적으로 작성됩니다.")
    else:
        equipment_list = equipment + ([other_equipment] if other_equipment.strip() else [])
        prompt_lines = [
            "당신의 지침에 있는 구조를 사용해 오늘의 일일 안전문서/TBM(toolbox talk)을 작성해 "
            "주세요. 아래는 오늘의 정보입니다 — 주어진 내용만 사용하고, 제공되지 않은 항목(예: "
            "비상연락처)은 당신의 지침에 따라 현장에서 채워야 할 빈칸으로 표시하세요:",
            f"- 날짜: {briefing_date.isoformat()}",
            f"- 현장/구역: {site_zone or '[미입력]'}",
            f"- 작업 인원: {crew_size if crew_size else '[미입력]'}",
            f"- 기상 조건: {weather or '[미입력]'}",
            f"- 투입 장비: {', '.join(equipment_list) if equipment_list else '[미입력]'}",
            f"- 오늘의 작업 계획: {activities}",
        ]
        if known_hazards.strip():
            prompt_lines.append(f"- 오늘 알려진 현장별 위험요소: {known_hazards}")
        if platform_note.strip():
            prompt_lines.append(
                f"- 플랫폼 관련 안내사항 (platform-safety의 기존 판단을 인용할 것, 새로운 수치를 "
                f"직접 계산하지 말 것): {platform_note}"
            )
        prompt = "\n".join(prompt_lines)

        api_key = llm.get_api_key()
        with st.chat_message("assistant", avatar=AGENTS[AGENT_KEY]["icon"]):
            st.caption(f"**{AGENTS[AGENT_KEY]['label']}**")
            full_text = st.write_stream(
                llm.stream_agent_reply(AGENT_KEY, [{"role": "user", "content": prompt}], api_key)
            )
        st.session_state.daily_safety_doc = full_text

if st.session_state.daily_safety_doc:
    st.divider()
    st.markdown("### 생성된 문서")
    st.markdown(st.session_state.daily_safety_doc)

    with st.expander("초안 기록으로 저장", icon=":material/save:"):
        with st.form("save_daily_safety"):
            category = st.selectbox(
                "분류", RECORD_CATEGORIES,
                format_func=lambda c: CATEGORY_LABELS.get(c, c),
                index=RECORD_CATEGORIES.index("daily-safety"),
            )
            default_name = f"daily-safety-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
            filename = st.text_input("파일명 (확장자 제외)", value=default_name)
            draft_banner = (
                "> **상태: 초안(DRAFT) — 담당 기술자 검토 및 승인 대기중(PENDING)**\n"
                f"> 현장 안전(Site Safety) 일일문서 생성 도구가 작성함 "
                f"({datetime.now(timezone.utc).strftime('%Y-%m-%d')}). 승인된 기록이 아닙니다.\n\n"
            )
            content = st.text_area(
                "내용 (저장 전 수정 가능)",
                value=draft_banner + st.session_state.daily_safety_doc,
                height=300,
            )
            if st.form_submit_button("초안 저장", icon=":material/save:"):
                target_dir = RECORDS_DIR / category
                target_dir.mkdir(parents=True, exist_ok=True)
                target_path = target_dir / f"{filename}.md"
                if target_path.exists():
                    target_path = target_dir / f"{filename}-{datetime.now(timezone.utc).strftime('%H%M%S')}.md"
                target_path.write_text(content, encoding="utf-8")
                st.success(f"저장 완료: `{target_path.relative_to(RECORDS_DIR.parent)}`")
