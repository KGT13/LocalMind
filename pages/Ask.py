"""
LocalMind — AI Q&A Page
Chat-style interface with streaming responses and source citations.
"""

import streamlit as st
from src.infrastructure import database, llm
from src.core import ingestion
from src.core.prompts import RAG_SYSTEM_PROMPT, RAG_FOLLOWUP_SYSTEM_PROMPT
from src.config import TOP_K

st.set_page_config(page_title="Ask | LocalMind", page_icon=":material/chat:", layout="wide")

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
    st.page_link("app.py", label="Dashboard", icon=":material/dashboard:", disabled=("ask" == "dashboard"))
    st.page_link("pages/Upload.py", label="Upload", icon=":material/upload_file:", disabled=("ask" == "upload"))
    st.page_link("pages/Library.py", label="Library", icon=":material/database:", disabled=("ask" == "library"))
    st.page_link("pages/Ask.py", label="Ask", icon=":material/chat_bubble:", disabled=("ask" == "ask"))
    st.page_link("pages/Search.py", label="Search", icon=":material/search:", disabled=("ask" == "search"))
    st.page_link("pages/Summarize.py", label="Summarize", icon=":material/auto_stories:", disabled=("ask" == "summarize"))
    st.page_link("pages/Quiz.py", label="Quiz", icon=":material/psychology_alt:", disabled=("ask" == "quiz"))
    st.page_link("pages/Settings.py", label="Settings", icon=":material/settings:", disabled=("ask" == "settings"))

    st.markdown("---")
    st.markdown("#### :material/filter_list: Filter by Document")
    try:
        doc_list = database.list_documents()
        options = ["All Documents"] + sorted(doc_list)
        selected_filter = st.selectbox("Search scope", options, label_visibility="collapsed")
    except Exception:
        selected_filter = "All Documents"
        doc_list = []

    if st.button("Clear Chat", icon=":material/delete:", use_container_width=True):
        st.session_state.pop("chat_messages", None)
        st.rerun()

st.markdown('<p class="ask-hero"><span class="material-symbols-outlined" style="vertical-align: -6px; font-size: inherit;">chat_bubble</span> Ask LocalMind</p>', unsafe_allow_html=True)
st.markdown("Ask questions about your documents. Answers include source citations.")
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── Chat state ───────────────────────────────────────────────────────────
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# Display existing messages
for msg in st.session_state.chat_messages:
    with st.chat_message(msg["role"], avatar=":material/person:" if msg["role"] == "user" else ":material/psychology:"):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("Sources", icon=":material/attachment:", expanded=False):
                for src in msg["sources"]:
                    st.markdown(f"""
                    <div class="source-card">
                        <span class="source-label"><span class="material-symbols-outlined" style="vertical-align: -2px; font-size: inherit;">description</span> {src['source']}</span>
                        <span class="source-page">&nbsp;•&nbsp; Page {src['page']}</span>
                    </div>
                    """, unsafe_allow_html=True)

# ── Chat input ───────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask a question about your documents..."):
    # Show user message
    st.session_state.chat_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=":material/person:"):
        st.markdown(prompt)

    # Determine filter
    filter_source = None if selected_filter == "All Documents" else selected_filter

    # Build conversation history for follow-ups (last 6 exchanges max)
    history = st.session_state.chat_messages[:-1][-12:]  # keep last 12 messages (6 pairs)

    with st.chat_message("assistant", avatar=":material/psychology:"):
        try:
            # Retrieve chunks
            query_results = database.query(prompt, top_k=TOP_K, filter_source=filter_source)

            # Build context
            retrieved_text = query_results["documents"][0]
            retrieved_metadata = query_results["metadatas"][0]
            context = ""
            for text, meta in zip(retrieved_text, retrieved_metadata):
                context += f"[Source: {meta['source']}, Page {meta['page']}]\n{text}\n\n"

            # Build prompt with or without history
            conv_history = [m for m in history if m["role"] in ("user", "assistant") and "sources" not in m]
            if conv_history:
                formatted = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in conv_history])
                system_prompt = RAG_FOLLOWUP_SYSTEM_PROMPT
                user_prompt = f"Conversation history:\n{formatted}\n\nContext:\n{context}\n\nQuestion: {prompt}"
            else:
                system_prompt = RAG_SYSTEM_PROMPT
                user_prompt = f"Context:\n{context}\n\nQuestion: {prompt}"

            # Stream response
            full_response = st.write_stream(llm.generate_streaming(user_prompt, system_prompt=system_prompt))

            # Deduplicate sources
            seen = set()
            unique_sources = []
            for d in retrieved_metadata:
                key = (d["source"], d["page"])
                if key not in seen:
                    seen.add(key)
                    unique_sources.append({"source": d["source"], "page": d["page"]})

            # Show sources
            if unique_sources:
                with st.expander("Sources", icon=":material/attachment:", expanded=True):
                    for src in unique_sources:
                        st.markdown(f"""
                        <div class="source-card">
                            <span class="source-label"><span class="material-symbols-outlined" style="vertical-align: -2px; font-size: inherit;">description</span> {src['source']}</span>
                            <span class="source-page">&nbsp;•&nbsp; Page {src['page']}</span>
                        </div>
                        """, unsafe_allow_html=True)

            # Save to history
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": full_response,
                "sources": unique_sources,
            })

        except Exception as e:
            st.error(f"Something went wrong. Is Ollama running with the correct model?\n\n`{e}`")
