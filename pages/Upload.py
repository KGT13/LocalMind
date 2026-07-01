"""
LocalMind — Upload Documents Page
Handles file uploads with progress indicators, ingesting documents into the knowledge base.
"""

import streamlit as st
import os
from src.infrastructure import file_reader
from src.core import ingestion

st.set_page_config(page_title="Upload | LocalMind", page_icon=":material/upload:", layout="wide")

# ── Header ───────────────────────────────────────────────────────────────
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
    st.page_link("app.py", label="Dashboard", icon=":material/dashboard:", disabled=("upload" == "dashboard"))
    st.page_link("pages/Upload.py", label="Upload", icon=":material/upload_file:", disabled=("upload" == "upload"))
    st.page_link("pages/Library.py", label="Library", icon=":material/database:", disabled=("upload" == "library"))
    st.page_link("pages/Ask.py", label="Ask", icon=":material/chat_bubble:", disabled=("upload" == "ask"))
    st.page_link("pages/Search.py", label="Search", icon=":material/search:", disabled=("upload" == "search"))
    st.page_link("pages/Summarize.py", label="Summarize", icon=":material/auto_stories:", disabled=("upload" == "summarize"))
    st.page_link("pages/Quiz.py", label="Quiz", icon=":material/psychology_alt:", disabled=("upload" == "quiz"))
    st.page_link("pages/Settings.py", label="Settings", icon=":material/settings:", disabled=("upload" == "settings"))

st.markdown('<p class="upload-hero"><span class="material-symbols-outlined" style="vertical-align: -6px; font-size: inherit;">upload_file</span> Add Documents</p>', unsafe_allow_html=True)
st.markdown("Add documents to your local knowledge base by uploading files or writing text directly.")
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Upload Files", "Write Text"])

with tab1:
    # ── Upload area ──────────────────────────────────────────────────────────
    uploaded_files = st.file_uploader(
        "Drag and drop files here, or click to browse",
        type=["pdf", "docx", "txt", "md"],
        accept_multiple_files=True,
        key="doc_uploader"
    )

    if uploaded_files:
        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        st.markdown('### <span class="material-symbols-outlined" style="vertical-align: -4px; color: #142175;">list_alt</span> Processing Queue', unsafe_allow_html=True)

        for uploaded_file in uploaded_files:
            with st.container():
                st.markdown(f"""
                <div class="glass-card" style="padding:16px 20px;">
                    <span style="font-size:1.1rem; color:#131b2e; font-weight:600;"><span class="material-symbols-outlined" style="vertical-align: -4px; color: #142175;">description</span> {uploaded_file.name}</span>
                    <span style="float:right; color:#505f76; font-size:0.85rem; font-weight:500;">{uploaded_file.size / 1024:.1f} KB</span>
                </div>
                """, unsafe_allow_html=True)

        if st.button("Ingest All Documents", use_container_width=True, key="ingest_btn", icon=":material/rocket_launch:"):
            for uploaded_file in uploaded_files:
                with st.status(f"Processing **{uploaded_file.name}**...", expanded=True) as status:
                    st.write("Saving file locally...")
                    file_path = file_reader.save_upload(uploaded_file)

                    st.write("Extracting text...")
                    st.write("Chunking document...")
                    st.write("Creating embeddings & storing...")

                    try:
                        result = ingestion.ingest_file(str(file_path))

                        if result.get("message") == "File already exist":
                            status.update(label=f":material/warning: {uploaded_file.name} — already in knowledge base", state="complete")
                            st.warning("This file has already been ingested.")
                        elif result.get("message") == "File not added":
                            status.update(label=f":material/error: {uploaded_file.name} — failed", state="error")
                            st.error("Could not add file to knowledge base.")
                        else:
                            status.update(label=f":material/check_circle: {uploaded_file.name} — {result['chunks_stored']} chunks stored", state="complete")
                            st.markdown(f"""
                            <div class="success-card">
                                <strong>{result['filename']}</strong> processed successfully<br>
                                Pages: {result['pages']} &nbsp;|&nbsp; Chunks: {result['chunks_stored']}
                            </div>
                            """, unsafe_allow_html=True)
                    except Exception as e:
                        status.update(label=f":material/error: {uploaded_file.name} — error", state="error")
                        st.error(f"Error: {e}")
                    finally:
                        file_reader.cleanup_upload(file_path)

            st.cache_data.clear()

with tab2:
    doc_title = st.text_input("Document Title", placeholder="e.g., meeting_notes", key="text_title")
    doc_content = st.text_area("Content", height=300, placeholder="Type or paste your text here...", key="text_content")
    
    if st.button("Save & Ingest Text", use_container_width=True, key="ingest_text_btn", icon=":material/save:"):
        if doc_title.strip() and doc_content.strip():
            filename = doc_title.strip().replace(" ", "_")
            if not filename.lower().endswith(".txt"):
                filename += ".txt"
            
            from src.config import TEMP_DIR
            from pathlib import Path
            folder = Path(TEMP_DIR)
            folder.mkdir(parents=True, exist_ok=True)
            file_path = folder / filename
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(doc_content)
                
            with st.status(f"Processing **{filename}**...", expanded=True) as status:
                st.write("Extracting text...")
                st.write("Chunking document...")
                st.write("Creating embeddings & storing...")
                
                try:
                    result = ingestion.ingest_file(str(file_path))

                    if result.get("message") == "File already exist":
                        status.update(label=f":material/warning: {filename} — already in knowledge base", state="complete")
                        st.warning("This file has already been ingested.")
                    elif result.get("message") == "File not added":
                        status.update(label=f":material/error: {filename} — failed", state="error")
                        st.error("Could not add file to knowledge base.")
                    else:
                        status.update(label=f":material/check_circle: {filename} — {result['chunks_stored']} chunks stored", state="complete")
                        st.markdown(f"""
                        <div class="success-card">
                            <strong>{result['filename']}</strong> processed successfully<br>
                            Pages: {result['pages']} &nbsp;|&nbsp; Chunks: {result['chunks_stored']}
                        </div>
                        """, unsafe_allow_html=True)
                except Exception as e:
                    status.update(label=f":material/error: {filename} — error", state="error")
                    st.error(f"Error: {e}")
                finally:
                    file_reader.cleanup_upload(file_path)
            st.cache_data.clear()
        else:
            st.warning("Please provide both a title and content to save.")
