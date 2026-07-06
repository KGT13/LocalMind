import os
import sys
import asyncio
from typing import List, Optional
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse

# Ensure src can be imported from backend directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.infrastructure import database, file_reader, llm
from src.core import ingestion, retrieval
from src.features.quiz import generate_questions, check_answer, save_score, get_weak_areas
from src.features.comparator import compare_documents

app = FastAPI(title="LocalMind API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    question: str
    filter_source: Optional[str] = None
    conversation_history: Optional[List[dict]] = None

class SummarizeRequest(BaseModel):
    document: str
    instruction: str

class CompareRequest(BaseModel):
    doc_a: str
    doc_b: str

class QuizGenerateRequest(BaseModel):
    document: str
    num_questions: int
    q_type: str

class QuizGradeRequest(BaseModel):
    question_obj: dict
    user_answer: str

@app.get("/api/kb/stats")
async def get_stats():
    docs = database.list_documents()
    collection = database.get_collections()
    chunk_count = collection.count()
    return {
        "documents": len(docs),
        "chunks": chunk_count,
        "status": "Online" if chunk_count > 0 else "Empty"
    }

@app.get("/api/documents")
async def get_documents():
    docs = database.list_documents()
    counts = database.get_all_chunk_counts()
    result = []
    for doc in sorted(docs):
        result.append({
            "name": doc,
            "chunks": counts.get(doc, 0)
        })
    return {"documents": result}

@app.delete("/api/documents/{filename}")
async def delete_document(filename: str):
    ingestion.delete_document(filename)
    return {"status": "success", "message": f"{filename} deleted"}

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    # Save the file temporarily
    from src.config import TEMP_DIR
    from pathlib import Path
    folder = Path(TEMP_DIR)
    folder.mkdir(parents=True, exist_ok=True)
    
    file_path = folder / file.filename
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
        
    try:
        result = ingestion.ingest_file(str(file_path))
        return result
    finally:
        file_reader.cleanup_upload(str(file_path))

@app.post("/api/upload/text")
async def upload_text(title: str = Form(...), content: str = Form(...)):
    filename = title.strip().replace(" ", "_")
    if not filename.lower().endswith(".txt"):
        filename += ".txt"
        
    from src.config import TEMP_DIR
    from pathlib import Path
    folder = Path(TEMP_DIR)
    folder.mkdir(parents=True, exist_ok=True)
    file_path = folder / filename
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    try:
        result = ingestion.ingest_file(str(file_path))
        return result
    finally:
        file_reader.cleanup_upload(str(file_path))

@app.post("/api/ask")
async def ask_question(request: AskRequest):
    async def event_generator():
        retrieved_chunk = retrieval.retrieve_chunks(request.question, filter_source=request.filter_source)
        context = retrieval.build_context(retrieved_chunk)

        if request.conversation_history:
            from src.core.prompts import RAG_FOLLOWUP_SYSTEM_PROMPT
            system_prompt = RAG_FOLLOWUP_SYSTEM_PROMPT
            user_prompt = f"Conversation history:\n{retrieval.format_conversation_history(request.conversation_history)}\n\nContext:\n{context}\n\nQuestion: {request.question}"
        else:
            from src.core.prompts import RAG_SYSTEM_PROMPT
            system_prompt = RAG_SYSTEM_PROMPT
            user_prompt = f"Context:\n{context}\n\nQuestion: {request.question}"   

        # Yield sources first as JSON metadata
        seen = set()
        unique_sources = []
        for d in retrieved_chunk["metadatas"][0]:
            key = (d["source"], d["page"])
            if key not in seen:
                seen.add(key)
                unique_sources.append({"source": d["source"], "page": d["page"]})
        
        import json
        yield {"event": "sources", "data": json.dumps(unique_sources)}
        
        # Stream the response
        response_stream = llm.generate_streaming(user_prompt, system_prompt=system_prompt)
        for chunk in response_stream:
            if chunk:
                yield {"event": "message", "data": json.dumps({"text": chunk})}
            await asyncio.sleep(0.01)
            
        yield {"event": "done", "data": "done"}

    return EventSourceResponse(event_generator())

@app.post("/api/search")
async def search(question: str = Form(...), top_k: int = Form(5), filter_source: Optional[str] = Form(None)):
    if filter_source == "All Documents":
        filter_source = None
    results = database.query(question, top_k=top_k, filter_source=filter_source)
    
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0] if "distances" in results else [None] * len(documents)
    
    response_data = []
    for doc_text, meta, dist in zip(documents, metadatas, distances):
        relevance = max(0, min(100, int((1 - dist / 2) * 100))) if dist is not None else 50
        response_data.append({
            "text": doc_text,
            "source": meta.get("source", "Unknown"),
            "page": meta.get("page", "?"),
            "relevance": relevance
        })
    return {"results": response_data}

@app.post("/api/summarize")
async def summarize(request: SummarizeRequest):
    async def event_generator():
        all_text = retrieval.get_document_text(request.document)
        
        max_chars = 12000
        if len(all_text) > max_chars:
            all_text = all_text[:max_chars] + "\n\n[... content truncated for length ...]"
            
        from src.core.prompts import SUMMARY_PROMPT
        prompt = f"{SUMMARY_PROMPT}\n\n{request.instruction}\n\nDocument: {request.document}\n\nContent:\n{all_text}"
        
        response_stream = llm.generate_streaming(prompt, system_prompt=SUMMARY_PROMPT)
        import json
        for chunk in response_stream:
            if chunk:
                yield {"event": "message", "data": json.dumps({"text": chunk})}
            await asyncio.sleep(0.01)
        yield {"event": "done", "data": "done"}

    return EventSourceResponse(event_generator())

@app.post("/api/compare")
async def compare_docs(request: CompareRequest):
    result = compare_documents(request.doc_a, request.doc_b)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@app.post("/api/quiz/generate")
async def quiz_generate(request: QuizGenerateRequest):
    quiz_data = generate_questions(request.document, n=request.num_questions, q_type=request.q_type)
    if isinstance(quiz_data, dict) and "questions" in quiz_data:
        quiz_data = quiz_data["questions"]
    return {"questions": quiz_data}

@app.post("/api/quiz/grade")
async def quiz_grade(request: QuizGradeRequest):
    result = check_answer(request.question_obj, request.user_answer)
    return result

@app.post("/api/quiz/save_score")
async def quiz_save_score(document: str = Form(...), correct_count: int = Form(...), total: int = Form(...)):
    save_score(document, correct_count, total)
    return {"status": "success"}

@app.get("/api/quiz/weak_areas")
async def get_quiz_weak_areas(document: str):
    return {"analysis": get_weak_areas(document)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
