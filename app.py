"""
LocalMind — AI That Stays With You
Main Streamlit application entry point (Dashboard / Home).
"""

import streamlit as st
from src.infrastructure import database
from src.core import ingestion

# ── Page config ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LocalMind – AI That Stays With You",
    page_icon=":material/psychology:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────
def load_css():
    import os
    import streamlit as st
    css_path = os.path.join(os.path.dirname(__file__), "..", ".streamlit", "style.css")
    if not os.path.exists(css_path):
        css_path = os.path.join(os.path.dirname(__file__), ".streamlit", "style.css")
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_css()


# ── Sidebar Navigation ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 4px;"><div style="background-color: #142175; padding: 6px; border-radius: 8px; display: flex; align-items: center;"><span class="material-symbols-outlined" style="color: white; font-size: 24px;">psychology</span></div><span style="font-size: 1.5rem; font-weight: 800; color: #142175; letter-spacing: -0.5px;">LocalMind</span></div><p style="font-size: 0.85rem; color: #505f76; font-weight: 500; margin-left: 2px; margin-bottom: 24px;">AI That Stays With You</p>', unsafe_allow_html=True)
    st.page_link("app.py", label="Dashboard", icon=":material/dashboard:", disabled=("dashboard" == "dashboard"))
    st.page_link("pages/Upload.py", label="Upload", icon=":material/upload_file:", disabled=("dashboard" == "upload"))
    st.page_link("pages/Library.py", label="Library", icon=":material/database:", disabled=("dashboard" == "library"))
    st.page_link("pages/Ask.py", label="Ask", icon=":material/chat_bubble:", disabled=("dashboard" == "ask"))
    st.page_link("pages/Search.py", label="Search", icon=":material/search:", disabled=("dashboard" == "search"))
    st.page_link("pages/Summarize.py", label="Summarize", icon=":material/auto_stories:", disabled=("dashboard" == "summarize"))
    st.page_link("pages/Quiz.py", label="Quiz", icon=":material/psychology_alt:", disabled=("dashboard" == "quiz"))
    st.page_link("pages/Settings.py", label="Settings", icon=":material/settings:", disabled=("dashboard" == "settings"))

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    st.markdown('<span class="privacy-badge"><span class="material-symbols-outlined" style="vertical-align: -2px; font-size: inherit;">lock</span> 100% Local & Private</span>', unsafe_allow_html=True)
    st.markdown("")
    st.caption("Your documents never leave your machine. All processing happens locally using Ollama.")


# ── Helper: get knowledge base stats ─────────────────────────────────────
@st.cache_data(ttl=30)
def get_kb_stats():
    """Return (document_count, chunk_count)."""
    try:
        docs = database.list_documents()
        collection = database.get_collections()
        chunk_count = collection.count()
        return len(docs), chunk_count
    except Exception:
        return 0, 0


# ── Hero ─────────────────────────────────────────────────────────────────
st.markdown("")
st.markdown('<p class="hero-title">LocalMind</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-tagline">AI That Stays With You — Your private, local knowledge assistant</p>', unsafe_allow_html=True)
st.markdown("")

# ── Knowledge Base Stats ─────────────────────────────────────────────────
doc_count, chunk_count = get_kb_stats()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Documents", doc_count)
with col2:
    st.metric("Indexed Chunks", chunk_count)
with col3:
    status = "Online" if chunk_count > 0 else "Empty"
    st.metric("Knowledge Base", status)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── Feature Navigation Cards ────────────────────────────────────────────
st.markdown('### <span class="material-symbols-outlined" style="vertical-align: -4px; color: #142175;">explore</span> What would you like to do?', unsafe_allow_html=True)
st.markdown("")

col1, col2, col3 = st.columns(3)
with col1:
    st.page_link("pages/Upload.py", label="Upload Documents", icon=":material/upload_file:")
    st.page_link("pages/Search.py", label="Semantic Search", icon=":material/search:")
with col2:
    st.page_link("pages/Library.py", label="Document Library", icon=":material/database:")
    st.page_link("pages/Summarize.py", label="Summarize", icon=":material/auto_stories:")
with col3:
    st.page_link("pages/Ask.py", label="Ask LocalMind", icon=":material/chat_bubble:")
    st.page_link("pages/Quiz.py", label="Quiz Mode", icon=":material/psychology_alt:")

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── Recent Documents ────────────────────────────────────────────────────
st.markdown('### <span class="material-symbols-outlined" style="vertical-align: -4px; color: #142175;">folder_open</span> Documents in Knowledge Base', unsafe_allow_html=True)
try:
    docs = database.list_documents()
    if docs:
        for doc in docs:
            st.markdown(f"""
            <div class="glass-card" style="padding:14px 20px; display:flex; align-items:center; gap:12px;">
                <span class="material-symbols-outlined" style="font-size:1.5rem; color:#142175;">description</span>
                <span style="color:#131b2e; font-weight:600;">{doc}</span>
                <span style="margin-left:auto; color:#142175; font-size:0.8rem; font-weight: 500;">indexed</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No documents uploaded yet. Head to **Upload** to get started!")
except Exception as e:
    st.warning(f"Could not connect to the knowledge base. Make sure Ollama is running.\n\n`{e}`")
