import logging
from src.infrastructure import llm
from src.core import retrieval
from src.core.prompts import CLAIMS_EXTRACTION_PROMPT, COMPARISON_PROMPT

logger = logging.getLogger(__name__)

MAX_CLAIMS_CHUNK_SIZE = 6000

def extract_claims(document_text, source_name):
    if len(document_text) < MAX_CLAIMS_CHUNK_SIZE:
        response = llm.generate_json(prompt=document_text, system_prompt=CLAIMS_EXTRACTION_PROMPT)
        if response is None:
            logger.warning(f"Could not generate claim; source: {source_name}")
            return []
        else:
            return response
    else:
        chunks = []
        i = 0
        while i < len(document_text):
            chunks.append(document_text[i:i + MAX_CLAIMS_CHUNK_SIZE])
            i += (MAX_CLAIMS_CHUNK_SIZE - 200) # 200 char overlap
            
        all_claims = []
        
        for item in chunks:
            response = llm.generate_json(prompt=item, system_prompt=CLAIMS_EXTRACTION_PROMPT)
            if response is None:
                logger.warning(f"Could not generate claim; source: {source_name}")
            else:
                if isinstance(response, list):
                    all_claims.extend(response)
        return all_claims

def find_contradictions(claims_a, claims_b, source_a, source_b):
    contradictions = []
    total_claims = len(claims_a) + len(claims_b)
    
    a_str = "\n".join([f"- {c}" for c in claims_a])
    
    if total_claims > 50:
        batch_size = 10
        for i in range(0, len(claims_b), batch_size):
            batch_b = claims_b[i:i + batch_size]
            b_str = "\n".join([f"- {c}" for c in batch_b])
            
            prompt = f"Document A ({source_a}):\n{a_str}\n\nDocument B ({source_b}):\n{b_str}"
            result = llm.generate_json(prompt=prompt, system_prompt=COMPARISON_PROMPT)
            
            if result and isinstance(result, list):
                for item in result:
                    item['source_a'] = source_a
                    item['source_b'] = source_b
                    contradictions.append(item)
    else:
        b_str = "\n".join([f"- {c}" for c in claims_b])
        prompt = f"Document A ({source_a}):\n{a_str}\n\nDocument B ({source_b}):\n{b_str}"
        result = llm.generate_json(prompt=prompt, system_prompt=COMPARISON_PROMPT)
        
        if result and isinstance(result, list):
            for item in result:
                item['source_a'] = source_a
                item['source_b'] = source_b
                contradictions.append(item)
                
    return contradictions

def compare_documents(source_a, source_b, text_a=None, text_b=None):
    if text_a is None:
        try:
            text_a = retrieval.get_document_text(source_a)
        except Exception as e:
            logger.error(f"Error reading {source_a}: {e}")
            text_a = ""
            
    if text_b is None:
        try:
            text_b = retrieval.get_document_text(source_b)
        except Exception as e:
            logger.error(f"Error reading {source_b}: {e}")
            text_b = ""
            
    if not text_a:
        return {"error": f"Could not read document {source_a}"}
    if not text_b:
        return {"error": f"Could not read document {source_b}"}
        
    claims_a = extract_claims(text_a, source_a)
    claims_b = extract_claims(text_b, source_b)
    
    contradictions = find_contradictions(claims_a, claims_b, source_a, source_b)
    
    return {
        "source_a": source_a,
        "source_b": source_b,
        "total_claims_a": len(claims_a),
        "total_claims_b": len(claims_b),
        "contradictions": contradictions
    }