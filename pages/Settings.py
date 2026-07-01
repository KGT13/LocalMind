"""
LocalMind — Settings Page
Minimal configuration and knowledge base management.
"""

import streamlit as st
from src.infrastructure import database
from src.config import CHAT_MODEL, EMBED_MODEL, OLLAMA_URL, CHUNK_SIZE, CHUNK_OVERLAP, TOP_K

st.set_page_config(page_title="Settings | LocalMind", page_icon=":material/settings:", layout="wide")

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
    st.page_link("app.py", label="Dashboard", icon=":material/dashboard:", disabled=("settings" == "dashboard"))
    st.page_link("pages/Upload.py", label="Upload", icon=":material/upload_file:", disabled=("settings" == "upload"))
    st.page_link("pages/Library.py", label="Library", icon=":material/database:", disabled=("settings" == "library"))
    st.page_link("pages/Ask.py", label="Ask", icon=":material/chat_bubble:", disabled=("settings" == "ask"))
    st.page_link("pages/Search.py", label="Search", icon=":material/search:", disabled=("settings" == "search"))
    st.page_link("pages/Summarize.py", label="Summarize", icon=":material/auto_stories:", disabled=("settings" == "summarize"))
    st.page_link("pages/Quiz.py", label="Quiz", icon=":material/psychology_alt:", disabled=("settings" == "quiz"))
    st.page_link("pages/Settings.py", label="Settings", icon=":material/settings:", disabled=("settings" == "settings"))

st.markdown('<p class="settings-hero"><span class="material-symbols-outlined" style="vertical-align: -6px; font-size: inherit;">settings</span> Settings</p>', unsafe_allow_html=True)
st.markdown("View system configuration and manage your knowledge base.")
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── Model Configuration ─────────────────────────────────────────────────
st.markdown('### <span class="material-symbols-outlined" style="vertical-align: -4px; font-size: 1.6rem;">smart_toy</span> Model Configuration', unsafe_allow_html=True)
st.markdown(f"""
<div class="glass-card">
    <div class="config-item">
        <span class="config-label">Chat Model</span>
        <span class="config-value">{CHAT_MODEL}</span>
    </div>
    <div class="config-item">
        <span class="config-label">Embedding Model</span>
        <span class="config-value">{EMBED_MODEL}</span>
    </div>
    <div class="config-item">
        <span class="config-label">Ollama URL</span>
        <span class="config-value">{OLLAMA_URL}</span>
    </div>
    <div class="config-item">
        <span class="config-label">Chunk Size</span>
        <span class="config-value">{CHUNK_SIZE} characters</span>
    </div>
    <div class="config-item">
        <span class="config-label">Chunk Overlap</span>
        <span class="config-value">{CHUNK_OVERLAP} characters</span>
    </div>
    <div class="config-item" style="border-bottom:none;">
        <span class="config-label">Top-K Retrieval</span>
        <span class="config-value">{TOP_K} chunks</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── Knowledge Base Status ────────────────────────────────────────────────
st.markdown('### <span class="material-symbols-outlined" style="vertical-align: -4px; font-size: 1.6rem;">bar_chart</span> Knowledge Base Status', unsafe_allow_html=True)

try:
    docs = database.list_documents()
    collection = database.get_collections()
    chunk_count = collection.count()

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Documents", len(docs))
    with c2:
        st.metric("Chunks", chunk_count)
    with c3:
        st.metric("Status", "Online" if chunk_count > 0 else "Empty")

except Exception as e:
    st.error(f"Cannot connect to knowledge base: {e}")
    docs = []

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── Danger Zone ──────────────────────────────────────────────────────────
st.markdown('### <span class="material-symbols-outlined" style="vertical-align: -4px; font-size: 1.6rem;">warning</span> Knowledge Base Management', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="glass-card" style="border-color: rgba(239,68,68,0.2);">
        <span style="color:#fca5a5; font-weight:600;"><span class="material-symbols-outlined" style="vertical-align: -4px; font-size: 1.2rem;">delete</span> Clear All Documents</span>
        <p style="color:#94a3b8; font-size:0.85rem; margin-top:8px;">
            Permanently delete all documents and chunks from the knowledge base.
            This action cannot be undone.
        </p>
    </div>
    """, unsafe_allow_html=True)

    confirm = st.checkbox("I understand this will delete all data", key="confirm_clear")
    if st.button("Clear Knowledge Base", icon=":material/delete:", use_container_width=True, disabled=not confirm):
        try:
            for doc in docs:
                database.delete_document(doc)
            st.cache_data.clear()
            st.success("Knowledge base cleared successfully.")
            st.rerun()
        except Exception as e:
            st.error(f"Failed to clear: {e}")

with col2:
    st.markdown("""
    <div class="glass-card">
        <span style="color:#a5b4fc; font-weight:600;"><span class="material-symbols-outlined" style="vertical-align: -4px; font-size: 1.2rem;">refresh</span> Refresh Status</span>
        <p style="color:#94a3b8; font-size:0.85rem; margin-top:8px;">
            Refresh the knowledge base statistics displayed above.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Refresh", icon=":material/refresh:", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── Privacy message ──────────────────────────────────────────────────────
st.markdown("""
<div class="privacy-banner">
    <div style="font-size:2rem; margin-bottom:12px;"><span class="material-symbols-outlined" style="font-size: 2.2rem;">lock</span></div>
    <div style="color:#86efac; font-size:1.1rem; font-weight:600; margin-bottom:8px;">Your Privacy is Protected</div>
    <div style="color:#94a3b8; font-size:0.9rem; line-height:1.6;">
        All documents and processing stay 100% local on your machine.<br>
        LocalMind uses Ollama for AI inference — no data is sent to external servers.<br>
        Your knowledge base is stored locally and never shared.
    </div>
</div>
""", unsafe_allow_html=True)
