import logging
from datetime import date
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.config import CHUNK_SIZE, CHUNK_OVERLAP
from src.infrastructure import file_reader, database

logger = logging.getLogger(__name__)

def chunk_text(text, source_filename, page_number, start_index=0):
    
    chunk_dict = []
    today = str(date.today())
    
    # Initialize the text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", "!", "?", " ", ""]
    )

    # Split your document
    texts = text_splitter.split_text(text)
    for items in texts:
        
        chunk_dict.append({
            "text": items,
            "source": source_filename,
            "page": page_number,
            "chunk_index": start_index,
            "date_added": today
        })
        start_index += 1
    
    logger.info(f"{len(texts)} chunks created")    
    return chunk_dict

def ingest_file(file_path):
    name = file_reader.get_filename(file_path)
    chunk_list = []
    
    if database.document_exists(name):
        logger.warning("File already exists")
        return {"filename": name, "pages": 0, "chunks_stored": 0, "message": "File already exists"}
    else:
        file = file_reader.read_file(file_path)
        start_index = 0
        
        for page, text in file:
            
            page_chunks = chunk_text(text, name, page, start_index)
            chunk_list += page_chunks
            start_index += len(page_chunks)
        
        chunks = [value["text"] for value in chunk_list] 
        
        metadata = [{k: v for k, v in value.items() if k != "text"} for value in chunk_list]
               
        ids = [value["source"] + "_chunk_"+ str(value["chunk_index"]) for value in chunk_list]         
        
        try:
            database.add_chunks(chunks, metadata, ids)
            return {"filename": name, "pages": len(file), "chunks_stored": len(chunks)}
        except Exception as e:
            database.delete_document(name)
            logger.warning(f"File could not be added to database: {e}")
            return {"filename": name, "pages": 0, "chunks_stored": 0, "message": "File not added"}
        
def ingest_text(text, source_label):
    chunk_list = []
    
    if database.document_exists(source_label):
        logger.warning("File already exists")
        return {"filename": source_label,"pages": 0, "chunks_stored": 0, "message": "File already exists"}
    else:
        
        chunk_list = chunk_text(text, source_label, page_number=1)
        
        chunks = [value["text"] for value in chunk_list] 
        
        metadata = [{k: v for k, v in value.items() if k != "text"} for value in chunk_list]
               
        ids = [value["source"] + "_chunk_"+ str(value["chunk_index"]) for value in chunk_list]         
        
        try:
            database.add_chunks(chunks, metadata, ids)
            return {"filename": source_label, "pages": 1, "chunks_stored": len(chunks)}
        except Exception as e:
            database.delete_document(source_label)
            logger.warning(f"File could not be added to database: {e}")
            return {"filename": source_label, "pages": 0, "chunks_stored": 0, "message": "File not added"}
            
def delete_document(filename):
    database.delete_document(filename)
    logger.info(f"{filename} deleted succesfully") 
    return {"filename": filename, "message": "File deleted"}           
                