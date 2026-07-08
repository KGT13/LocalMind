#!/bin/bash

echo "============================================"
echo "  Starting LocalMind"
echo "============================================"
echo

cleanup() {
    echo
    echo "Shutting down LocalMind..."
    kill "$OLLAMA_PID" "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null
    exit 0
}
trap cleanup SIGINT SIGTERM

# ── 1. Start Ollama in the background ────────────────────────────────────
echo "Starting Ollama server..."
ollama serve > /tmp/localmind_ollama.log 2>&1 &
OLLAMA_PID=$!
sleep 3

# ── 2. Start the FastAPI backend ─────────────────────────────────────────
echo "Starting backend (FastAPI on http://localhost:8000)..."
source venv/bin/activate
(cd backend && uvicorn main:app --reload --port 8000) &
BACKEND_PID=$!
sleep 3

# ── 3. Start the React frontend ──────────────────────────────────────────
echo "Starting frontend (Vite on http://localhost:5173)..."
(cd frontend && npm run dev) &
FRONTEND_PID=$!
sleep 3

echo
echo "============================================"
echo "  LocalMind is running:"
echo "    - Backend  : http://localhost:8000"
echo "    - Frontend : http://localhost:5173"
echo "============================================"
echo
echo "Press Ctrl+C to stop all services."

# Try to open the browser (works on macOS; ignored elsewhere)
command -v open &> /dev/null && open http://localhost:5173

wait
