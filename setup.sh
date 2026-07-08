#!/bin/bash
set -e

echo "============================================"
echo "  LocalMind - First-time setup"
echo "============================================"
echo

# ── 1. Python virtual environment (backend) ────────────────────────────
if [ ! -d "venv" ]; then
    echo "[1/6] Creating Python virtual environment..."
    python3 -m venv venv
else
    echo "[1/6] Virtual environment already exists, skipping."
fi

echo "[2/6] Activating virtual environment and installing backend dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# ── 2. Ollama models ────────────────────────────────────────────────────
echo "[3/6] Checking Ollama is installed..."
if ! command -v ollama &> /dev/null; then
    echo
    echo "ERROR: Ollama was not found on PATH."
    echo "Download and install it from https://ollama.com then re-run this script."
    exit 1
fi

echo "[4/6] Pulling required AI models - this can take several minutes..."
ollama pull qwen3.5:9b
ollama pull nomic-embed-text

# ── 3. Frontend dependencies ────────────────────────────────────────────
echo "[5/6] Installing frontend dependencies (npm)..."
if ! command -v npm &> /dev/null; then
    echo
    echo "ERROR: npm was not found on PATH."
    echo "Install Node.js from https://nodejs.org then re-run this script."
    exit 1
fi

(cd frontend && npm install)

# ── 4. Data folders ──────────────────────────────────────────────────────
echo "[6/6] Preparing data folders..."
mkdir -p backend/data
mkdir -p backend/temp_uploads
if [ ! -f "backend/data/quiz_scores.json" ]; then
    echo "{}" > backend/data/quiz_scores.json
fi

echo
echo "============================================"
echo "  Setup complete!"
echo "  Run ./launch.sh to start LocalMind."
echo "============================================"
