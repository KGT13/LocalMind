import os
import logging

# Logging info
LOG_LEVEL = logging.INFO 

# Model settings
CHAT_MODEL    = "qwen3.5:9b"
EMBED_MODEL   = "nomic-embed-text"
OLLAMA_URL    = "http://localhost:11434"

# Chunking settings
# 2000 char ~ 500 tokens
CHUNK_SIZE    = 2000
CHUNK_OVERLAP = 200

# Retrieval settings
TOP_K         = 5          # how many chunks to retrieve per query

# JSON generation
JSON_MAX_RETRIES = 3       # retry count when LLM returns malformed JSON

# Storage
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))   # .../backend/src
DB_PATH       = os.path.join(BASE_DIR, "..", "data", "knowledge_base")
SCORES_PATH   = os.path.join(BASE_DIR, "..", "data", "quiz_scores.json")
TEMP_DIR      = os.path.join(BASE_DIR, "..", "temp_uploads")