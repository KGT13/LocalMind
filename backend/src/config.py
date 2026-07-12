import os
import logging
import sys
import json

# Logging info
LOG_LEVEL = logging.INFO 

if sys.platform == "win32":
    app_data = os.getenv("APPDATA") or os.path.expanduser("~")
    DATA_DIR = os.path.join(app_data, "LocalMind", "backend_data")
else:
    DATA_DIR = os.path.join(os.path.expanduser("~"), ".localmind", "backend_data")

DB_PATH       = os.path.join(DATA_DIR, "knowledge_base")
SCORES_PATH   = os.path.join(DATA_DIR, "quiz_scores.json")
TEMP_DIR      = os.path.join(DATA_DIR, "temp_uploads")
SETTINGS_PATH = os.path.join(DATA_DIR, "settings.json")

os.makedirs(DB_PATH, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# Default Model settings
DEFAULT_CHAT_MODEL    = "qwen3.5:4b"
EMBED_MODEL   = "nomic-embed-text"
OLLAMA_URL    = "http://localhost:11434"
AVAILABLE_CHAT_MODELS = ["qwen3.5:4b", "qwen3.5:9b"]

def get_chat_model():
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, "r") as f:
                settings = json.load(f)
                return settings.get("chat_model", DEFAULT_CHAT_MODEL)
        except Exception:
            pass
    return DEFAULT_CHAT_MODEL

def set_chat_model(model_name):
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, "r") as f:
                settings = json.load(f)
        except Exception:
            pass
    settings["chat_model"] = model_name
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f)

# Chunking settings
CHUNK_SIZE    = 2000
CHUNK_OVERLAP = 200

# Retrieval settings
TOP_K         = 5

# JSON generation
JSON_MAX_RETRIES = 3