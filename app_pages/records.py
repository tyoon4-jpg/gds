import streamlit as st

from lib.knowledge import RECORDS_DIR

st.title(":material/folder_open: Records")
st.caption("Draft records saved from the chat, browsable by category.")

if not RECORDS_DIR.exists():
    st.info("No `records/` directory yet — nothing has been saved.")
else:
    categories = sorted(p for p in RECORDS_DIR.iterdir() if p.is_dir())
    if not categories:
        st.info("`records/` exists but is empty.")

    search = st.text_input("Filter by filename", key="records_search")

    for category_dir in categories:
        files = sorted(category_dir.glob("*.md"))
        if search:
            files = [f for f in files if search.lower() in f.name.lower()]
        if not files:
            continue
        with st.container(border=True):
            st.subheader(category_dir.name)
            for f in files:
                content = f.read_text(encoding="utf-8")
                pending_count = content.count("PENDING")
                is_draft = "DRAFT" in content[:500]
                badges = []
                if is_draft:
                    badges.append(":orange-badge[DRAFT]")
                if pending_count:
                    badges.append(f":red-badge[{pending_count} pending]")
                label = f.stem + (" " + " ".join(badges) if badges else "")
                with st.expander(label):
                    st.markdown(content)
