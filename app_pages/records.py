import streamlit as st

from lib.knowledge import CATEGORY_LABELS, RECORDS_DIR

st.title(":material/folder_open: 기록")
st.caption("채팅에서 저장된 초안 기록을 분류별로 확인할 수 있습니다.")

if not RECORDS_DIR.exists():
    st.info("아직 `records/` 폴더가 없습니다 — 저장된 내용이 없습니다.")
else:
    categories = sorted(p for p in RECORDS_DIR.iterdir() if p.is_dir())
    if not categories:
        st.info("`records/` 폴더는 있지만 비어 있습니다.")

    search = st.text_input("파일명으로 검색", key="records_search")

    for category_dir in categories:
        files = sorted(category_dir.glob("*.md"))
        if search:
            files = [f for f in files if search.lower() in f.name.lower()]
        if not files:
            continue
        with st.container(border=True):
            st.subheader(CATEGORY_LABELS.get(category_dir.name, category_dir.name))
            for f in files:
                content = f.read_text(encoding="utf-8")
                pending_count = content.count("PENDING")
                is_draft = "DRAFT" in content[:500]
                badges = []
                if is_draft:
                    badges.append(":orange-badge[초안]")
                if pending_count:
                    badges.append(f":red-badge[대기 {pending_count}건]")
                label = f.stem + (" " + " ".join(badges) if badges else "")
                with st.expander(label):
                    st.markdown(content)
