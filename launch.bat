@echo off
echo ============================================
echo   Starting LocalMind
echo ============================================
echo.

REM ── 1. Start Ollama in the background ────────────────────────────────
echo Starting Ollama server...
start "Ollama" /min ollama serve
timeout /t 3 /nobreak > nul

REM ── 2. Start the FastAPI backend ─────────────────────────────────────
echo Starting backend (FastAPI on http://localhost:8000)...
start "LocalMind Backend" cmd /k "call venv\Scripts\activate && cd backend && uvicorn main:app --reload --port 8000"
timeout /t 3 /nobreak > nul

REM ── 3. Start the React frontend ──────────────────────────────────────
echo Starting frontend (Vite on http://localhost:5173)...
start "LocalMind Frontend" cmd /k "cd frontend && npm run dev"
timeout /t 3 /nobreak > nul

echo.
echo ============================================
echo   LocalMind is starting up in two new windows:
echo     - Backend  : http://localhost:8000
echo     - Frontend : http://localhost:5173
echo.
echo   Opening the app in your browser...
echo ============================================
timeout /t 2 /nobreak > nul
start http://localhost:5173

echo.
echo Close the "LocalMind Backend" and "LocalMind Frontend"
echo windows (or press Ctrl+C in them) to stop the app.
pause
