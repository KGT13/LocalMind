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
DB_PATH       = "./data/knowledge_base"
SCORES_PATH   = "./data/quiz_scores.json"
TEMP_DIR      = "./temp_uploads"