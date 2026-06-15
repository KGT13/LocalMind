import logging  # python logger
import chromadb
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction
from src.config import EMBED_MODEL, OLLAMA_URL, DB_PATH, TOP_K


# module level logger
logger = logging.getLogger(__name__)

def get_collections():
    client = chromadb.PersistentClient(path = DB_PATH) #create a persistent client for the db
    
    ollama_ef = OllamaEmbeddingFunction(url=OLLAMA_URL, model_name=EMBED_MODEL) #create embedding function
    
    collection = client.get_or_create_collection(name="documents", embedding_function=ollama_ef) 
    
    return collection

def add_chunks(chunks, metadata, ids):
    collection = get_collections()
    collection.add(documents=chunks, metadatas=metadata, ids=ids)
    logger.info(f"Amount of chunks added to collection: {len(chunks)}")

def query(question_text, top_k=TOP_K, filter_source=None):
    collection = get_collections()
    
    # check if there's a metadata filter
    if filter_source:                               
        where_filter = {"source": filter_source}
    else:
        where_filter = None    
    
    results = collection.query(query_texts=[question_text], n_results=top_k, where=where_filter)
    logger.info(f"Query returned {len(results['documents'][0])} results.")
    return results

def get_chunks_by_source(filename):
    collection = get_collections()
    results = collection.get(where={"source":filename})
    logger.info(f"Amount of chunks exctracted from source: {len(results)}")
    return results

def document_exists(filename):
    document_chunks = get_chunks_by_source(filename)
    return bool(document_chunks.get("ids"))

def delete_document(filename):
    collections = get_collections()
    
    document_chunks = get_chunks_by_source(filename)
    ids_list = document_chunks.get("ids")
    
    if ids_list:
        collections.delete(ids= ids_list)
        logger.info(f"{len(ids_list)} chunks deleted")
    else:
        logger.warning("Tried to delete a nonexistent file")
 
def list_documents():
    collections = get_collections()
    response = collections.get(limit=10000, include=["metadatas"])  
    unique_sources =list({meta["source"] for meta in response["metadatas"] if meta and "source" in meta})
    logger.info(f"Amount of unique elements in collection: {len(unique_sources)}") 
             
    return unique_sources