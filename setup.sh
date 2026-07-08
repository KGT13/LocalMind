#!/bin/bash
set -e

echo "============================================"
echo "  LocalMind - First-time setup"
echo "  (installs everything needed automatically)"
echo "============================================"
echo

OS_TYPE="$(uname -s)"

# ── 0. Homebrew (macOS package manager) ──────────────────────────────────
if [ "$OS_TYPE" = "Darwin" ]; then
    if ! command -v brew &> /dev/null; then
        echo "[Check] Homebrew not found. Installing Homebrew..."
        echo "You may be asked for your Mac password - this is normal."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        eval "$(/opt/homebrew/bin/brew shellenv 2>/dev/null || /usr/local/bin/brew shellenv)"
    else
        echo "[Check] Homebrew found."
    fi
fi

# ── 1. Python ─────────────────────────────────────────────────────────────
echo "[Check] Python3..."
if ! command -v python3 &> /dev/null; then
    echo "  Not found. Installing..."
    if [ "$OS_TYPE" = "Darwin" ]; then
        brew install python
    else
        sudo apt-get update && sudo apt-get install -y python3 python3-venv python3-pip
    fi
else
    echo "  Found."
fi

# ── 2. Node.js ────────────────────────────────────────────────────────────
echo "[Check] Node.js..."
if ! command -v node &> /dev/null; then
    echo "  Not found. Installing..."
    if [ "$OS_TYPE" = "Darwin" ]; then
        brew install node
    else
        curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
        sudo apt-get install -y nodejs
    fi
else
    echo "  Found."
fi

# ── 3. Ollama ─────────────────────────────────────────────────────────────
echo "[Check] Ollama..."
if ! command -v ollama &> /dev/null; then
    echo "  Not found. Installing..."
    if [ "$OS_TYPE" = "Darwin" ]; then
        brew install ollama
    else
        curl -fsSL https://ollama.com/install.sh | sh
    fi
else
    echo "  Found."
fi

echo
echo "All prerequisites are installed. Continuing setup..."
echo

# ── 4. Python virtual environment (backend) ──────────────────────────────
if [ ! -d "venv" ]; then
    echo "[1/5] Creating Python virtual environment..."
    python3 -m venv venv
else
    echo "[1/5] Virtual environment already exists, skipping."
fi

echo "[2/5] Installing backend dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# ── 5. Ollama models ──────────────────────────────────────────────────────
echo "[3/5] Pulling required AI models - this can take several minutes..."
# Make sure the Ollama background service is running before pulling models
if [ "$OS_TYPE" = "Darwin" ]; then
    brew services start ollama 2>/dev/null || ollama serve > /tmp/localmind_ollama.log 2>&1 &
else
    (ollama serve > /tmp/localmind_ollama.log 2>&1 &) 
fi
sleep 3
ollama pull qwen3.5:9b
ollama pull nomic-embed-text

# ── 6. Frontend dependencies ──────────────────────────────────────────────
echo "[4/5] Installing frontend dependencies..."
(cd frontend && npm install)

# ── 7. Data folders ───────────────────────────────────────────────────────
echo "[5/5] Preparing data folders..."
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
