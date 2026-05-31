# Model settings
CHAT_MODEL    = "qwen3.5:9b"
EMBED_MODEL   = "nomic-embed-text"
OLLAMA_URL    = "http://localhost:11434"

# Chunking settings
CHUNK_SIZE    = 512
CHUNK_OVERLAP = 50

# Retrieval settings
TOP_K         = 5          # how many chunks to retrieve per query

# Storage
DB_PATH       = "./data/knowledge_base"
SCORES_PATH   = "./data/quiz_scores.json"