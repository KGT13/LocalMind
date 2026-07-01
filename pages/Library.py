"""
LocalMind — Document Library Page
Lists all indexed documents with management actions.
"""

import streamlit as st
from src.infrastructure import database
from src.core import ingestion

st.set_page_config(page_title="Library | LocalMind", page_icon=":material/library_books:", layout="wide")

def load_css():
    import os
    import streamlit as st
    css_path = os.path.join(os.path.dirname(__file__), "..", ".streamlit", "style.css")
    if not os.path.exists(css_path):
        css_path = os.path.join(os.path.dirname(__file__), ".streamlit", "style.css")
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_css()

with st.sidebar:
    st.markdown('<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 4px;"><div style="background-color: #142175; padding: 6px; border-radius: 8px; display: flex; align-items: center;"><span class="material-symbols-outlined" style="color: white; font-size: 24px;">psychology</span></div><span style="font-size: 1.5rem; font-weight: 800; color: #142175; letter-spacing: -0.5px;">LocalMind</span></div><p style="font-size: 0.85rem; color: #505f76; font-weight: 500; margin-left: 2px; margin-bottom: 24px;">AI That Stays With You</p>', unsafe_allow_html=True)
    st.page_link("app.py", label="Dashboard", icon=":material/dashboard:", disabled=("library" == "dashboard"))
    st.page_link("pages/Upload.py", label="Upload", icon=":material/upload_file:", disabled=("library" == "upload"))
    st.page_link("pages/Library.py", label="Library", icon=":material/database:", disabled=("library" == "library"))
    st.page_link("pages/Ask.py", label="Ask", icon=":material/chat_bubble:", disabled=("library" == "ask"))
    st.page_link("pages/Search.py", label="Search", icon=":material/search:", disabled=("library" == "search"))
    st.page_link("pages/Summarize.py", label="Summarize", icon=":material/auto_stories:", disabled=("library" == "summarize"))
    st.page_link("pages/Quiz.py", label="Quiz", icon=":material/psychology_alt:", disabled=("library" == "quiz"))
    st.page_link("pages/Settings.py", label="Settings", icon=":material/settings:", disabled=("library" == "settings"))

st.markdown('<p class="lib-hero"><span class="material-symbols-outlined" style="vertical-align: -6px; font-size: inherit;">database</span> Document Library</p>', unsafe_allow_html=True)
st.markdown("Browse and manage all documents stored in your local knowledge base.")
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── Stats row ────────────────────────────────────────────────────────────
try:
    docs = database.list_documents()
    collection = database.get_collections()
    total_chunks = collection.count()

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Total Documents", len(docs))
    with c2:
        st.metric("Total Chunks", total_chunks)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    if not docs:
        st.info("Your knowledge base is empty. Go to **Upload** to add documents!")
    else:
        for doc_name in sorted(docs):
            # Get chunk count for this document
            doc_chunks = database.get_chunks_by_source(doc_name)
            chunk_count = len(doc_chunks.get("ids", []))

            with st.container():
                col_info, col_chunks, col_action = st.columns([4, 2, 2])

                with col_info:
                    ext = doc_name.rsplit(".", 1)[-1].upper() if "." in doc_name else "FILE"
                    st.markdown(f"""
                    <div class="doc-card">
                        <span style="font-size:1.1rem; color:#e0e7ff; font-weight:600;"><span class="material-symbols-outlined" style="vertical-align: -4px; font-size: 1.2rem;">description</span> {doc_name}</span><br>
                        <span style="color:#94a3b8; font-size:0.8rem;">Type: {ext} &nbsp;•&nbsp; {chunk_count} chunks indexed</span>
                    </div>
                    """, unsafe_allow_html=True)

                with col_chunks:
                    st.markdown("")
                    st.markdown(f"**{chunk_count}** chunks")

                with col_action:
                    st.markdown("")
                    if st.button("Delete", icon=":material/delete:", key=f"del_{doc_name}", use_container_width=True):
                        ingestion.delete_document(doc_name)
                        st.cache_data.clear()
                        st.rerun()

except Exception as e:
    st.error(f"Could not connect to the knowledge base. Make sure Ollama is running.\n\n`{e}`")
