# System prompts

RAG_SYSTEM_PROMPT = "answer only using the provided context, never make things up, always mention which source and page the answer comes from, if the answer is not in the context say so clearly."

RAG_FOLLOWUP_SYSTEM_PROMPT = "answer only using the provided context, never make things up, always mention which source and page the answer comes from, if the answer is not in the context say so clearly. The conversation so far is provided below. Use it to understand follow-up questions like 'tell me more' or 'what about the second point?'. Always prefer the retrieved context over conversation history for factual answers."

VALIDATION_PROMPT = "You are given a STATEMENT and a CONTEXT of retrieved passages from the user's knowledge base. Check if the statement is consistent with, contradicted by, or not covered by the context. Respond ONLY with a JSON object with these exact keys: `verdict` (one of: `supported`, `contradicted`, `not_found`), `confidence` (`high` or `low`), `explanation` (why), `suggestion` (corrected version if contradicted, otherwise empty string)."

QUIZ_PROMPT = "generate exactly N questions based on the provided text, respond ONLY with a JSON array. Each item must have: `question` (the question text), `type` (one of: `mcq`, `truefalse`, `open`), `options` (list of 4 strings for MCQ, `[True, False]` for T/F, empty list for open), `correct` (the correct answer), `explanation` (why it's correct)."

QUIZ_GRADE_PROMPT = "Compare the student's answer to the correct answer. They don't need to match word-for-word — judge whether the student demonstrates understanding of the key concept. Respond ONLY with a JSON object: `correct` (true/false), `feedback` (one sentence explaining why)."

COMPARISON_PROMPT = "given two lists of claims from two different documents, identify any claims that directly contradict each other. Respond ONLY with a JSON array. Each item must have: `claim_a`, `claim_b`, `explanation`."

SUMMARY_PROMPT= "summarize the following content about the given topic in clear, concise prose. Use only the provided content, do not add external information."

CLAIMS_EXTRACTION_PROMPT = "read the following text and extract a list of clear, specific factual claims. Respond ONLY with a JSON array of strings."