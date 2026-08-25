from datetime import datetime, timezone

import streamlit as st

from lib.knowledge import CATEGORY_LABELS, RECORDS_DIR

st.title(":material/monitoring: 현장 현황")
st.caption(
    "records/ 폴더의 실시간 현황 — 자동으로 갱신됩니다. 공용 화면에 띄워두면 시공/안전/품질 "
    "담당자가 별도 요청 없이 현재 홀드(작업중지) 및 최근 활동을 확인할 수 있습니다."
)


def _scan_records() -> list[dict]:
    rows = []
    if not RECORDS_DIR.exists():
        return rows
    for category_dir in sorted(p for p in RECORDS_DIR.iterdir() if p.is_dir()):
        for f in sorted(category_dir.glob("*.md")):
            content = f.read_text(encoding="utf-8")
            rows.append({
                "category": category_dir.name,
                "name": f.stem,
                "path": f,
                "is_draft": "DRAFT" in content[:500],
                "pending_count": content.count("PENDING"),
                "hold_open": "OPEN, NOT LIFTED" in content or "HOLD — OPEN" in content,
                "mtime": f.stat().st_mtime,
            })
    rows.sort(key=lambda r: r["mtime"], reverse=True)
    return rows


@st.fragment(run_every="15s")
def live_status_board():
    rows = _scan_records()

    total = len(rows)
    open_holds = sum(1 for r in rows if r["hold_open"])
    total_pending = sum(r["pending_count"] for r in rows)
    by_category = {}
    for r in rows:
        by_category.setdefault(r["category"], 0)
        by_category[r["category"]] += 1

    with st.container(horizontal=True):
        st.metric("전체 기록", total, border=True)
        st.metric("미해제 홀드(작업중지)", open_holds, border=True, delta_color="inverse")
        st.metric("미처리 대기 항목", total_pending, border=True, delta_color="inverse")
        st.metric(
            "마지막 갱신",
            datetime.now(timezone.utc).strftime("%H:%M:%S UTC"),
            border=True,
        )

    if by_category:
        with st.container(horizontal=True):
            for cat, count in by_category.items():
                st.metric(CATEGORY_LABELS.get(cat, cat), count, border=True)

    st.markdown("### 최근 활동")
    if not rows:
        st.info("아직 기록이 없습니다 — `records/`에 저장된 내용이 없습니다.")
        return

    for r in rows[:20]:
        with st.container(border=True):
            cols = st.container(horizontal=True, horizontal_alignment="distribute")
            with cols:
                label = f"**{r['name']}**  ·  {CATEGORY_LABELS.get(r['category'], r['category'])}"
                st.markdown(label)
                badges = []
                if r["hold_open"]:
                    badges.append(":red-badge[홀드 진행중]")
                if r["is_draft"]:
                    badges.append(":orange-badge[초안]")
                if r["pending_count"]:
                    badges.append(f":gray-badge[대기 {r['pending_count']}건]")
                st.markdown(" ".join(badges) if badges else ":green-badge[미해결 항목 없음]")
            mtime = datetime.fromtimestamp(r["mtime"], tz=timezone.utc)
            st.caption(f"최종 수정: {mtime.strftime('%Y-%m-%d %H:%M UTC')}")


live_status_board()
