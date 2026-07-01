"""
LocalMind — Summarize Page
Generate document summaries using the LLM.
"""

import streamlit as st
from src.infrastructure import database, llm
from src.core.prompts import SUMMARY_PROMPT

st.set_page_config(page_title="Summarize | LocalMind", page_icon=":material/edit_note:", layout="wide")

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
    st.page_link("app.py", label="Dashboard", icon=":material/dashboard:", disabled=("summarize" == "dashboard"))
    st.page_link("pages/Upload.py", label="Upload", icon=":material/upload_file:", disabled=("summarize" == "upload"))
    st.page_link("pages/Library.py", label="Library", icon=":material/database:", disabled=("summarize" == "library"))
    st.page_link("pages/Ask.py", label="Ask", icon=":material/chat_bubble:", disabled=("summarize" == "ask"))
    st.page_link("pages/Search.py", label="Search", icon=":material/search:", disabled=("summarize" == "search"))
    st.page_link("pages/Summarize.py", label="Summarize", icon=":material/auto_stories:", disabled=("summarize" == "summarize"))
    st.page_link("pages/Quiz.py", label="Quiz", icon=":material/psychology_alt:", disabled=("summarize" == "quiz"))
    st.page_link("pages/Settings.py", label="Settings", icon=":material/settings:", disabled=("summarize" == "settings"))

st.markdown('<p class="summ-hero"><span class="material-symbols-outlined" style="vertical-align: -6px; font-size: inherit;">edit_note</span> Document Summarizer</p>', unsafe_allow_html=True)
st.markdown("Generate intelligent summaries from your documents using AI.")
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── Document selector ────────────────────────────────────────────────────
try:
    docs = database.list_documents()
except Exception:
    docs = []
    st.error("Could not connect to the knowledge base. Make sure Ollama is running.")

if not docs:
    st.info("No documents in the knowledge base. Upload some documents first!")
else:
    selected_doc = st.selectbox("Select a document to summarize", sorted(docs))

    # Summary type selection
    summary_tab1, summary_tab2, summary_tab3, summary_tab4 = st.tabs([
        ":material/assignment: Short Summary", ":material/menu_book: Detailed Summary", ":material/ads_click: Key Points", ":material/task_alt: Action Items"
    ])

    summary_types = {
        ":material/assignment: Short Summary": "Provide a brief, concise summary in 3-5 sentences.",
        ":material/menu_book: Detailed Summary": "Provide a comprehensive and detailed summary covering all major topics and arguments.",
        ":material/ads_click: Key Points": "Extract the key points and main takeaways as a bulleted list.",
        ":material/task_alt: Action Items": "Extract all action items, recommendations, and next steps as a clear checklist.",
    }

    for tab, (label, instruction) in zip(
        [summary_tab1, summary_tab2, summary_tab3, summary_tab4],
        summary_types.items()
    ):
        with tab:
            if st.button(f"Generate {label.split(' ', 1)[1]}", icon=":material/auto_awesome:", key=f"gen_{label}", use_container_width=True):
                with st.spinner("Gathering document chunks and generating summary..."):
                    try:
                        # Get all chunks for this document
                        doc_chunks = database.get_chunks_by_source(selected_doc)
                        all_text = "\n\n".join(doc_chunks["documents"])

                        # Truncate if too long (context window limits)
                        max_chars = 12000
                        if len(all_text) > max_chars:
                            all_text = all_text[:max_chars] + "\n\n[... content truncated for length ...]"

                        prompt = f"{SUMMARY_PROMPT}\n\n{instruction}\n\nDocument: {selected_doc}\n\nContent:\n{all_text}"

                        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                        st.markdown(f"#### {label}")
                        response = st.write_stream(llm.generate_streaming(prompt, system_prompt=SUMMARY_PROMPT))
                        st.markdown('</div>', unsafe_allow_html=True)

                        # Copy button
                        if response:
                            st.download_button(
                                "Download Summary",
                                icon=":material/download:",
                                data=response,
                                file_name=f"{selected_doc}_summary.txt",
                                mime="text/plain",
                                use_container_width=True,
                            )

                    except Exception as e:
                        st.error(f"Failed to generate summary: {e}")
