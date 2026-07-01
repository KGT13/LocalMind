"""
LocalMind — Semantic Search Page
Search the knowledge base by meaning, not just keywords.
"""

import streamlit as st
from src.infrastructure import database
from src.config import TOP_K

st.set_page_config(page_title="Search | LocalMind", page_icon=":material/search:", layout="wide")

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
    st.page_link("app.py", label="Dashboard", icon=":material/dashboard:", disabled=("search" == "dashboard"))
    st.page_link("pages/Upload.py", label="Upload", icon=":material/upload_file:", disabled=("search" == "upload"))
    st.page_link("pages/Library.py", label="Library", icon=":material/database:", disabled=("search" == "library"))
    st.page_link("pages/Ask.py", label="Ask", icon=":material/chat_bubble:", disabled=("search" == "ask"))
    st.page_link("pages/Search.py", label="Search", icon=":material/search:", disabled=("search" == "search"))
    st.page_link("pages/Summarize.py", label="Summarize", icon=":material/auto_stories:", disabled=("search" == "summarize"))
    st.page_link("pages/Quiz.py", label="Quiz", icon=":material/psychology_alt:", disabled=("search" == "quiz"))
    st.page_link("pages/Settings.py", label="Settings", icon=":material/settings:", disabled=("search" == "settings"))

    st.markdown("---")
    st.markdown("#### :material/settings: Search Settings")
    num_results = st.slider("Number of results", 1, 20, TOP_K)

    try:
        doc_list = database.list_documents()
        options = ["All Documents"] + sorted(doc_list)
        filter_doc = st.selectbox("Filter by document", options)
    except Exception:
        filter_doc = "All Documents"

st.markdown('<p class="search-hero"><span class="material-symbols-outlined" style="vertical-align: -6px; font-size: inherit;">search</span> Semantic Search</p>', unsafe_allow_html=True)
st.markdown("Search your knowledge base by **meaning**, not just keywords. The system understands context and intent.")
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── Search bar ───────────────────────────────────────────────────────────
query = st.text_input("What are you looking for?", placeholder="e.g., What are the ethical considerations of AI?", label_visibility="collapsed")

if query:
    filter_source = None if filter_doc == "All Documents" else filter_doc

    with st.spinner("Searching your knowledge base..."):
        try:
            results = database.query(query, top_k=num_results, filter_source=filter_source)

            documents = results["documents"][0]
            metadatas = results["metadatas"][0]
            distances = results["distances"][0] if "distances" in results else [None] * len(documents)

            st.markdown(f"### :material/bar_chart: Found {len(documents)} results")
            st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

            for i, (doc_text, meta, dist) in enumerate(zip(documents, metadatas, distances)):
                # ChromaDB returns distances (lower = more similar). Convert to relevance score.
                if dist is not None:
                    relevance = max(0, min(100, int((1 - dist / 2) * 100)))
                else:
                    relevance = 50

                col_main, col_score = st.columns([5, 1])

                with col_main:
                    st.markdown(f"""
                    <div class="result-card">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                            <span style="color:#a5b4fc; font-weight:600; font-size:0.9rem;"><span class="material-symbols-outlined" style="vertical-align: -2px; font-size: 1.1rem;">description</span> {meta.get('source', 'Unknown')} &nbsp;•&nbsp; Page {meta.get('page', '?')}</span>
                            <span style="color:#22c55e; font-weight:600; font-size:0.85rem;">{relevance}% match</span>
                        </div>
                        <div class="relevance-bg"><div class="relevance-bar" style="width:{relevance}%;"></div></div>
                        <p style="color:#cbd5e1; font-size:0.9rem; margin-top:12px; line-height:1.6;">{doc_text[:500]}{'...' if len(doc_text) > 500 else ''}</p>
                    </div>
                    """, unsafe_allow_html=True)

                with col_score:
                    st.markdown("")
                    st.markdown(f"**#{i+1}**")
                    if st.button("Use in Q&A", icon=":material/chat:", key=f"use_qa_{i}", use_container_width=True):
                        st.session_state["prefill_question"] = query
                        st.switch_page("pages/Ask.py")

        except Exception as e:
            st.error(f"Search failed. Make sure Ollama is running.\n\n`{e}`")
else:
    st.markdown("""
    <div style="text-align:center; padding:60px 20px; color:#64748b;">
        <div style="font-size:4rem; margin-bottom:16px;"><span class="material-symbols-outlined" style="font-size: 4rem;">search</span></div>
        <div style="font-size:1.1rem; font-weight:500;">Enter a query above to search your knowledge base</div>
        <div style="font-size:0.85rem; margin-top:8px;">Try searching by concept — the system understands meaning, not just exact words</div>
    </div>
    """, unsafe_allow_html=True)
