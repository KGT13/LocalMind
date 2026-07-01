"""
LocalMind — Quiz Mode Page
Generate quizzes from documents and track scores.
"""

import json
import streamlit as st
from pathlib import Path
from src.infrastructure import database, llm
from src.core.prompts import QUIZ_PROMPT, QUIZ_GRADE_PROMPT
from src.config import SCORES_PATH

st.set_page_config(page_title="Quiz | LocalMind", page_icon=":material/ads_click:", layout="wide")

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
    st.page_link("app.py", label="Dashboard", icon=":material/dashboard:", disabled=("quiz" == "dashboard"))
    st.page_link("pages/Upload.py", label="Upload", icon=":material/upload_file:", disabled=("quiz" == "upload"))
    st.page_link("pages/Library.py", label="Library", icon=":material/database:", disabled=("quiz" == "library"))
    st.page_link("pages/Ask.py", label="Ask", icon=":material/chat_bubble:", disabled=("quiz" == "ask"))
    st.page_link("pages/Search.py", label="Search", icon=":material/search:", disabled=("quiz" == "search"))
    st.page_link("pages/Summarize.py", label="Summarize", icon=":material/auto_stories:", disabled=("quiz" == "summarize"))
    st.page_link("pages/Quiz.py", label="Quiz", icon=":material/psychology_alt:", disabled=("quiz" == "quiz"))
    st.page_link("pages/Settings.py", label="Settings", icon=":material/settings:", disabled=("quiz" == "settings"))

st.markdown('<p class="quiz-hero"><span class="material-symbols-outlined" style="vertical-align: -6px; font-size: inherit;">psychology_alt</span> Quiz Mode</p>', unsafe_allow_html=True)
st.markdown("Test your knowledge with AI-generated questions from your documents.")
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)


def load_scores():
    path = Path(SCORES_PATH)
    if path.exists():
        try:
            return json.loads(path.read_text())
        except Exception:
            return {}
    return {}


def save_scores(scores):
    Path(SCORES_PATH).write_text(json.dumps(scores, indent=2))


# ── Document & quiz settings ────────────────────────────────────────────
try:
    docs = database.list_documents()
except Exception:
    docs = []
    st.error("Could not connect to the knowledge base.")

if not docs:
    st.info("No documents in the knowledge base. Upload some documents first!")
else:
    col_doc, col_type, col_num = st.columns([3, 2, 1])
    with col_doc:
        selected_doc = st.selectbox("Select Document", sorted(docs))
    with col_type:
        quiz_type = st.selectbox("Question Type", ["Multiple Choice", "True/False", "Short Answer", "Mixed"])
    with col_num:
        num_questions = st.number_input("# Questions", min_value=1, max_value=10, value=3)

    # Map UI labels to prompt types
    type_map = {
        "Multiple Choice": "mcq",
        "True/False": "truefalse",
        "Short Answer": "open",
        "Mixed": "mixed (a combination of mcq, truefalse, and open)",
    }

    if st.button("Generate Quiz", icon=":material/casino:", use_container_width=True, key="gen_quiz"):
        with st.spinner("Generating quiz questions from your document..."):
            try:
                # Get document text
                doc_chunks = database.get_chunks_by_source(selected_doc)
                all_text = "\n\n".join(doc_chunks["documents"])

                # Truncate if needed
                max_chars = 8000
                if len(all_text) > max_chars:
                    all_text = all_text[:max_chars]

                prompt = QUIZ_PROMPT.replace("N", str(num_questions))
                prompt += f"\n\nQuestion type: {type_map[quiz_type]}\n\nText:\n{all_text}"

                quiz_data = llm.generate_json(prompt, system_prompt=QUIZ_PROMPT.replace("N", str(num_questions)))

                if quiz_data is None:
                    st.error("Failed to generate valid quiz questions. Please try again.")
                else:
                    # Handle both list and dict with "questions" key
                    if isinstance(quiz_data, dict) and "questions" in quiz_data:
                        quiz_data = quiz_data["questions"]

                    st.session_state["quiz_questions"] = quiz_data
                    st.session_state["quiz_doc"] = selected_doc
                    st.session_state["quiz_answers"] = {}
                    st.session_state["quiz_graded"] = False

            except Exception as e:
                st.error(f"Failed to generate quiz: {e}")

    # ── Display quiz ─────────────────────────────────────────────────────
    if "quiz_questions" in st.session_state and st.session_state.get("quiz_doc") == selected_doc:
        questions = st.session_state["quiz_questions"]

        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        st.markdown(f'### <span class="material-symbols-outlined" style="vertical-align: -4px; font-size: 1.6rem;">edit_note</span> Quiz — {selected_doc}', unsafe_allow_html=True)

        for i, q in enumerate(questions):
            st.markdown(f"""
            <div class="question-card">
                <span style="color:#a5b4fc; font-weight:600;">Question {i+1}</span>
                <span style="color:#64748b; font-size:0.8rem; margin-left:8px;">({q.get('type', 'unknown').upper()})</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"**{q['question']}**")

            q_type = q.get("type", "open")
            options = q.get("options", [])

            if q_type == "mcq" and options:
                answer = st.radio(
                    "Your answer:",
                    options,
                    key=f"q_{i}",
                    label_visibility="collapsed",
                )
                st.session_state["quiz_answers"][i] = answer

            elif q_type == "truefalse":
                answer = st.radio(
                    "Your answer:",
                    ["True", "False"],
                    key=f"q_{i}",
                    label_visibility="collapsed",
                )
                st.session_state["quiz_answers"][i] = answer

            else:  # open / short answer
                answer = st.text_input(
                    "Your answer:",
                    key=f"q_{i}",
                    label_visibility="collapsed",
                    placeholder="Type your answer here..."
                )
                st.session_state["quiz_answers"][i] = answer

            st.markdown("")

        # ── Submit & grade ───────────────────────────────────────────────
        if st.button("Submit Answers", icon=":material/check_circle:", use_container_width=True, key="submit_quiz"):
            correct_count = 0
            total = len(questions)

            for i, q in enumerate(questions):
                user_answer = st.session_state["quiz_answers"].get(i, "")
                correct_answer = str(q.get("correct", ""))

                # For MCQ/TF, direct comparison; for open, use LLM grading
                if q.get("type") in ("mcq", "truefalse"):
                    is_correct = str(user_answer).strip().lower() == correct_answer.strip().lower()
                    feedback = q.get("explanation", "")
                else:
                    # Use LLM to grade open-ended
                    grade_prompt = f"Correct answer: {correct_answer}\nStudent answer: {user_answer}"
                    grade_result = llm.generate_json(grade_prompt, system_prompt=QUIZ_GRADE_PROMPT)
                    if grade_result:
                        is_correct = grade_result.get("correct", False)
                        feedback = grade_result.get("feedback", "")
                    else:
                        is_correct = str(user_answer).strip().lower() == correct_answer.strip().lower()
                        feedback = q.get("explanation", "")

                if is_correct:
                    correct_count += 1
                    st.success(f"**Q{i+1}: Correct!** {feedback}", icon=":material/check_circle:")
                else:
                    st.error(f"**Q{i+1}: Incorrect.** The answer was: *{correct_answer}*. {feedback}", icon=":material/cancel:")

            # Show score
            pct = int((correct_count / total) * 100) if total > 0 else 0
            score_class = "score-good" if pct >= 70 else ("score-mid" if pct >= 40 else "score-low")

            st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Correct", f"{correct_count}/{total}")
            with c2:
                st.metric("Score", f"{pct}%")
            with c3:
                if pct >= 70:
                    badge_html = '<span class="material-symbols-outlined" style="vertical-align:-4px;">celebration</span> Great job!'
                elif pct >= 40:
                    badge_html = '<span class="material-symbols-outlined" style="vertical-align:-4px;">menu_book</span> Keep studying!'
                else:
                    badge_html = '<span class="material-symbols-outlined" style="vertical-align:-4px;">fitness_center</span> Try again!'

                st.markdown(f'<div class="score-badge {score_class}">{badge_html}</div>', unsafe_allow_html=True)

            # Save score
            scores = load_scores()
            if selected_doc not in scores:
                scores[selected_doc] = []
            scores[selected_doc].append({"score": pct, "correct": correct_count, "total": total})
            save_scores(scores)
