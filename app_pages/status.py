from datetime import datetime, timezone

import streamlit as st

from lib.knowledge import RECORDS_DIR

st.title(":material/monitoring: Site status")
st.caption(
    "Live view of records/ — refreshes automatically. Leave this open on a shared screen for "
    "construction/safety/QA-QC to see current holds and recent activity without asking."
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
        st.metric("Total records", total, border=True)
        st.metric("Open holds", open_holds, border=True, delta_color="inverse")
        st.metric("Open PENDING items", total_pending, border=True, delta_color="inverse")
        st.metric(
            "Last updated",
            datetime.now(timezone.utc).strftime("%H:%M:%S UTC"),
            border=True,
        )

    if by_category:
        with st.container(horizontal=True):
            for cat, count in by_category.items():
                st.metric(cat, count, border=True)

    st.markdown("### Recent activity")
    if not rows:
        st.info("No records yet — nothing has been saved to `records/`.")
        return

    for r in rows[:20]:
        with st.container(border=True):
            cols = st.container(horizontal=True, horizontal_alignment="distribute")
            with cols:
                label = f"**{r['name']}**  ·  {r['category']}"
                st.markdown(label)
                badges = []
                if r["hold_open"]:
                    badges.append(":red-badge[HOLD OPEN]")
                if r["is_draft"]:
                    badges.append(":orange-badge[DRAFT]")
                if r["pending_count"]:
                    badges.append(f":gray-badge[{r['pending_count']} pending]")
                st.markdown(" ".join(badges) if badges else ":green-badge[no open items]")
            mtime = datetime.fromtimestamp(r["mtime"], tz=timezone.utc)
            st.caption(f"Last modified: {mtime.strftime('%Y-%m-%d %H:%M UTC')}")


live_status_board()
