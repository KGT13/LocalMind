import json
import os
import datetime
from src.infrastructure import llm
from src.core import retrieval
from src.config import SCORES_PATH
from src.core.prompts import QUIZ_PROMPT, QUIZ_GRADE_PROMPT

def generate_questions(source_filename, n=10, q_type="mixed"):
    try:
        text = retrieval.get_document_text(source_filename)
    except Exception:
        return []
        
    if len(text) > 10000:
        text = text[:10000]
        
    prompt = f"Target Number of Questions: {n}\nQuestion Type: {q_type}\n\nText:\n{text}"
    system_prompt_adapted = QUIZ_PROMPT.replace("exactly N", f"exactly {n}")
    
    result = llm.generate_json(prompt=prompt, system_prompt=system_prompt_adapted)
    
    if result is None:
        return []
        
    return result

def check_answer(question_obj, user_answer):
    q_type = question_obj.get("type", "")
    correct_ans = question_obj.get("correct", "")
    
    if q_type in ["mcq", "truefalse"]:
        is_correct = str(user_answer).strip().lower() == str(correct_ans).strip().lower()
        return {
            "correct": is_correct,
            "explanation": question_obj.get("explanation", "")
        }
    else:
        prompt = f"Correct Answer: {correct_ans}\nStudent's Answer: {user_answer}"
        result = llm.generate_json(prompt=prompt, system_prompt=QUIZ_GRADE_PROMPT)
        if result is None:
            # Fallback string containment check
            user_str = str(user_answer).strip().lower()
            corr_str = str(correct_ans).strip().lower()
            
            if len(user_str) < 3:
                is_correct = user_str == corr_str
            else:
                is_correct = user_str in corr_str or corr_str in user_str
                
            return {
                "correct": is_correct,
                "feedback": "Automated text matching."
            }
        return result

def save_score(source_filename, score, total):
    try:
        if os.path.exists(SCORES_PATH):
            with open(SCORES_PATH, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {}
        else:
            os.makedirs(os.path.dirname(SCORES_PATH), exist_ok=True)
            data = {}
            
        if source_filename not in data:
            data[source_filename] = []
            
        entry = {
            "score": score,
            "total": total,
            "percentage": round(score / total * 100) if total > 0 else 0,
            "date": datetime.datetime.now().strftime("%Y-%m-%d")
        }
        
        data[source_filename].append(entry)
        
        with open(SCORES_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Failed to save score: {e}")

def get_scores(source_filename=None):
    if not os.path.exists(SCORES_PATH):
        return [] if source_filename else {}
        
    try:
        with open(SCORES_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if source_filename:
            return data.get(source_filename, [])
        return data
    except Exception:
        return [] if source_filename else {}

def get_weak_areas(source_filename):
    scores = get_scores(source_filename)
    if not scores:
        return "No scores available yet."
        
    percentages = [s.get("percentage", 0) for s in scores]
    avg = sum(percentages) / len(percentages)
    
    if avg < 50:
        return f"Performance is weak. Average score is {avg:.1f}%. Needs review."
    elif avg < 80:
        return f"Performance is okay. Average score is {avg:.1f}%. Some areas might need more work."
    else:
        return f"Performance is strong. Average score is {avg:.1f}%."
