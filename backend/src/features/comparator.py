import logging
from src.infrastructure import llm
from src.core import retrieval
from src.core.prompts import CLAIMS_EXTRACTION_PROMPT, COMPARISON_PROMPT
from src.core.schemas import ClaimsList, ContradictionsList

logger = logging.getLogger(__name__)

MAX_CLAIMS_CHUNK_SIZE = 6000

CLAIMS_SCHEMA = ClaimsList.model_json_schema()
CONTRADICTIONS_SCHEMA = ContradictionsList.model_json_schema()

def extract_claims(document_text, source_name):
    if len(document_text) < MAX_CLAIMS_CHUNK_SIZE:
        response = llm.generate_json(prompt=document_text, system_prompt=CLAIMS_EXTRACTION_PROMPT, schema=CLAIMS_SCHEMA)
        claims = response["claims"] if response else []
        logger.info(f"Extracted {len(claims)} claims from {source_name} (single chunk)")
        return claims
    else:
        chunks = []
        i = 0
        while i < len(document_text):
            chunks.append(document_text[i:i + MAX_CLAIMS_CHUNK_SIZE])
            i += (MAX_CLAIMS_CHUNK_SIZE - 200)  # 200 char overlap

        all_claims = []

        for idx, item in enumerate(chunks):
            response = llm.generate_json(prompt=item, system_prompt=CLAIMS_EXTRACTION_PROMPT, schema=CLAIMS_SCHEMA)
            claims = response["claims"] if response else []
            if claims:
                all_claims.extend(claims)
                logger.info(f"Chunk {idx+1}/{len(chunks)} of {source_name}: extracted {len(claims)} claims")
            else:
                logger.warning(f"Chunk {idx+1}/{len(chunks)} of {source_name}: no claims extracted")

        seen = set()
        unique_claims = []
        for claim in all_claims:
            claim_str = str(claim).strip().lower()
            if claim_str not in seen:
                seen.add(claim_str)
                unique_claims.append(claim)

        logger.info(f"Total unique claims from {source_name}: {len(unique_claims)} (from {len(all_claims)} raw)")
        return unique_claims

def find_contradictions(claims_a, claims_b, source_a, source_b):
    if not claims_a or not claims_b:
        logger.warning(f"Cannot find contradictions: claims_a={len(claims_a)}, claims_b={len(claims_b)}")
        return []

    contradictions = []
    total_claims = len(claims_a) + len(claims_b)

    def format_claim(c):
        if isinstance(c, dict):
            return c.get("claim", c.get("text", str(c)))
        return str(c)

    a_str = "\n".join([f"- {format_claim(c)}" for c in claims_a])

    if total_claims > 50:
        batch_size = 10
        for i in range(0, len(claims_b), batch_size):
            batch_b = claims_b[i:i + batch_size]
            b_str = "\n".join([f"- {format_claim(c)}" for c in batch_b])

            prompt = f"Document A ({source_a}):\n{a_str}\n\nDocument B ({source_b}):\n{b_str}"
            result = llm.generate_json(prompt=prompt, system_prompt=COMPARISON_PROMPT, schema=CONTRADICTIONS_SCHEMA)
            items = result["contradictions"] if result else []

            for item in items:
                item['source_a'] = source_a
                item['source_b'] = source_b
                contradictions.append(item)
    else:
        b_str = "\n".join([f"- {format_claim(c)}" for c in claims_b])
        prompt = f"Document A ({source_a}):\n{a_str}\n\nDocument B ({source_b}):\n{b_str}"
        result = llm.generate_json(prompt=prompt, system_prompt=COMPARISON_PROMPT, schema=CONTRADICTIONS_SCHEMA)
        items = result["contradictions"] if result else []

        for item in items:
            item['source_a'] = source_a
            item['source_b'] = source_b
            contradictions.append(item)

    logger.info(f"Found {len(contradictions)} contradictions between {source_a} and {source_b}")
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

    logger.info(f"Comparing {source_a} ({len(text_a)} chars) vs {source_b} ({len(text_b)} chars)")

    claims_a = extract_claims(text_a, source_a)
    claims_b = extract_claims(text_b, source_b)

    logger.info(f"Claims extracted — A: {len(claims_a)}, B: {len(claims_b)}")

    contradictions = find_contradictions(claims_a, claims_b, source_a, source_b)

    return {
        "source_a": source_a,
        "source_b": source_b,
        "total_claims_a": len(claims_a),
        "total_claims_b": len(claims_b),
        "contradictions": contradictions
    }