import logging
from src.infrastructure import llm
from src.core.schemas import ValidationResult
from src.core import retrieval, ingestion
from src.core.prompts import VALIDATION_PROMPT

logger = logging.getLogger(__name__)

RELEVANCE_THRESHOLD = 75  # same cutoff used in /api/search — keeps behavior consistent app-wide

def check_fact(statement):
    passage = retrieval.retrieve_chunks(statement)

    documents = passage["documents"][0]
    metadatas = passage["metadatas"][0]
    distances = passage["distances"][0] if "distances" in passage else [None] * len(documents)

    # Filter out chunks that aren't actually relevant to the statement.
    # Without this, retrieve_chunks() always returns its top-k nearest matches
    # even when nothing in the knowledge base is actually related — handing
    # the LLM irrelevant context and letting it rationalize a false "contradiction".
    filtered_docs = []
    filtered_metas = []
    for doc, meta, dist in zip(documents, metadatas, distances):
        relevance = max(0, min(100, int((1 - dist / 2) * 100))) if dist is not None else 50
        if relevance >= RELEVANCE_THRESHOLD:
            filtered_docs.append(doc)
            filtered_metas.append(meta)

    # Nothing relevant found — return not_found deterministically, without
    # ever calling the LLM. This is the actual fix for the "var 1 is A" case.
    if not filtered_docs:
        return {
            "verdict": "not_found",
            "confidence": "high",
            "explanation": "No sufficiently relevant passages were found in your knowledge base to check this statement against.",
            "suggestion": "",
            "sources": []
        }

    filtered_passage = {"documents": [filtered_docs], "metadatas": [filtered_metas]}
    context = retrieval.build_context(filtered_passage)

    prompt = f"statement: {statement}\ncontext: {context}"

    response = llm.generate_json(prompt=prompt, system_prompt=VALIDATION_PROMPT, schema=ValidationResult.model_json_schema())

    if response is None:
        return {"verdict": "not_found", "confidence": "low", "explanation": "Could not verify — AI response was unreadable.", "suggestion": "", "sources": []}

    else:
        sources = []
        for element in filtered_metas:
            entry = {"source": element["source"], "page": element["page"]}
            if entry not in sources:
                sources.append(entry)

        response["sources"] = sources
        return response

def should_flag(result):
    if result["verdict"] == "contradicted" and result["confidence"] == "high":
        return True
    else:
        return False

def store_note(text, source_label, bypass_validation=False):
    if bypass_validation == True:
        ingestion.ingest_text(text, source_label)
        return {"stored": True, "result": None}
    else:
        result = check_fact(text)
        if should_flag(result=result) == True:
            return {"stored": False, "flag": result}
        else:
            ingestion.ingest_text(text, source_label)
            return {"stored": True, "result": result}