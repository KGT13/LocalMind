import fitz
from docx import Document
from pathlib import Path
from src.config import TEMP_DIR
import logging

logger = logging.getLogger(__name__)

# read pdf
def read_pdf(file_path):
    doc = fitz.open(file_path)
    text =[]
    try:
        for page_number, page in enumerate(doc, start=1):
            text.append((page_number, page.get_text()))
    finally:
        doc.close()
    logger.info("pdf succesfully read")
    return text    

# read txt 
def read_txt(file_path):
    with open(file_path, "r", encoding="utf-8", errors="replace") as file:
        content = [(1,file.read())]
    logger.info("txt succesfully read")    
    return content    

# read markdown
def read_md(file_path):
    with open(file_path, "r", encoding="utf-8", errors="replace") as file:
        content = [(1,file.read())]
    logger.info("md succesfully read")    
    return content

# read word document 
def read_docx(file_path):
    doc = Document(file_path)
    full_text = []
    
    for para in doc.paragraphs:
        full_text.append(para.text)
    
    content = [(1,"\n".join(full_text))]  
    logger.info("docx succesfully read")  
    return content

# select correct function basen on file extension
def read_file(file_path):
    
    uploaded_file = Path(file_path)
    
    # get the file extension and convert to lowercase to ensure matching works properly
    ext = uploaded_file.suffix.lower()
    
    if  ext == ".pdf":
        return read_pdf(file_path)
    
    elif ext == ".txt":
        return read_txt(file_path)
    
    elif ext == ".md":
        return read_md(file_path)
    
    elif ext == ".docx":
        return read_docx(file_path)   
    
    else:
        raise ValueError(f"Unsupported file extension: {ext}") 

def get_filename(file_path):   
    #separate the name of the file from the whole path
    filename = Path(file_path).name
    
    return filename
        
def save_upload(uploaded_file):
    
    # Define the folder path
    folder = Path(TEMP_DIR)

    # Create the folder safely
    folder.mkdir(parents=True, exist_ok=True)        

    file_path = folder / uploaded_file.name
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getvalue())
    
    logger.info(f"file saved to {folder}")
    return file_path    

def cleanup_upload(file_path):
    Path(file_path).unlink(missing_ok=True)
    logger.info("file succesfully deleted") 