import logging
from src.infrastructure import llm
from src.core import retrieval, ingestion
from src.core.prompts import VALIDATION_PROMPT

logger = logging.getLogger(__name__)

def check_fact(statement):
    passage = retrieval.retrieve_chunks(statement)
    
    context = retrieval.build_context(passage)
    
    prompt = f"statement: {statement}\ncontext: {context}"
    
    response = llm.generate_json(prompt=prompt, system_prompt= VALIDATION_PROMPT)
    
    
    
    
    if response is None:
        return {"verdict": "not_found", "confidence": "low", "explanation": "Could not verify — AI response was unreadable.", "suggestion": "", "sources": []}    
       
    else:
        sources = []
        for element in passage["metadatas"][0]:
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
                        