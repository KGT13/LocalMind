import logging
from src.config import TOP_K
from src.infrastructure import database, llm
from src.core.prompts import RAG_FOLLOWUP_SYSTEM_PROMPT, RAG_SYSTEM_PROMPT, SUMMARY_PROMPT

logger = logging.getLogger(__name__)


def retrieve_chunks(question, top_k=TOP_K, filter_source=None):
    query_results = database.query(question, top_k, filter_source)
    logger.info(f"{top_k} chunks retrieved")
    return query_results

def build_context(chunks):
    retrieved_text= chunks["documents"][0]
    retrieved_metadata = chunks["metadatas"][0]
    chunk = ""
    
    for text, metadata in zip(retrieved_text, retrieved_metadata):
        chunk += f"[Source: {metadata['source']}, Page {metadata['page']}]\n{text}\n\n"
    
    return chunk    

def format_conversation_history(messages):
    
    result = []    
    for msg in messages:
        result.append(str.capitalize(msg["role"]) + ": " + msg["content"])  
    formatted_msg = "\n".join(result)  
    return formatted_msg        

def ask(question, filter_source=None, conversation_history=None):
    retrieved_chunk = retrieve_chunks(question, filter_source=filter_source)
    context = build_context(retrieved_chunk)

    if conversation_history:
        system_prompt = RAG_FOLLOWUP_SYSTEM_PROMPT
        user_prompt = f"Conversation history:\n{format_conversation_history(conversation_history)}\n\nContext:\n{context}\n\nQuestion: {question}"
    else:
        system_prompt = RAG_SYSTEM_PROMPT
        user_prompt = f"Context:\n{context}\n\nQuestion: {question}"   
    
    response = llm.generate(user_prompt, system_prompt=system_prompt)
    
    seen = set()
    unique_data = []

    for d in retrieved_chunk["metadatas"][0]:
        # Sorting ensures keys match even if added in a different order
        small_dict = {"source": d["source"], "page": d["page"]}
        track_tuple = tuple(sorted(small_dict.items()))
        if track_tuple not in seen:
            seen.add(track_tuple)
            unique_data.append(small_dict)
    
    answer = {"answer": response, "sources": unique_data} 
      
    return answer     

def ask_streaming(question, filter_source=None, conversation_history=None):
    retrieved_chunk = retrieve_chunks(question, filter_source=filter_source)
    context = build_context(retrieved_chunk)

    if conversation_history:
        system_prompt = RAG_FOLLOWUP_SYSTEM_PROMPT
        user_prompt = f"Conversation history:\n{format_conversation_history(conversation_history)}\n\nContext:\n{context}\n\nQuestion: {question}"
    else:
        system_prompt = RAG_SYSTEM_PROMPT
        user_prompt = f"Context:\n{context}\n\nQuestion: {question}"   
    
    response = llm.generate_streaming(user_prompt, system_prompt=system_prompt)
    
    seen = set()
    unique_data = []

    for d in retrieved_chunk["metadatas"][0]:
        # Sorting ensures keys match even if added in a different order
        small_dict = {"source": d["source"], "page": d["page"]}
        track_tuple = tuple(sorted(small_dict.items()))
        if track_tuple not in seen:
            seen.add(track_tuple)
            unique_data.append(small_dict)
    
    answer = {"stream": response, "sources": unique_data} 
      
    return answer

def get_document_text(filename):
   chunks = database.get_chunks_by_source(filename)
   
   pairs = list(zip(chunks["documents"], chunks["metadatas"]))
   
   sorted_pairs = sorted(pairs, key = lambda x: x[1]["chunk_index"] )
   
   exctracted_text = [value[0] for value in sorted_pairs]
   
   result = " ".join(exctracted_text)
   
   logger.info(f"document text reconstructed from {len(sorted_pairs)} chunks")
   
   return result

def summarize_topic(topic, filter_source=None):
    retrieved_chunk = retrieve_chunks(topic, filter_source=filter_source)
    context = build_context(retrieved_chunk)
    
    system_prompt = SUMMARY_PROMPT
    user_prompt = f"Context:\n{context}\n\nTopic: {topic}"
    
    response = llm.generate(user_prompt, system_prompt=system_prompt)
    
    return response