@echo off
setlocal enabledelayedexpansion
echo ============================================
echo   LocalMind - First-time setup
echo ============================================
echo.

REM ── 1. Python virtual environment (backend) ──────────────────────────
if not exist venv (
    echo [1/6] Creating Python virtual environment...
    python -m venv venv
) else (
    echo [1/6] Virtual environment already exists, skipping.
)

echo [2/6] Activating virtual environment and installing backend dependencies...
call venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: pip install failed. Check the messages above.
    pause
    exit /b 1
)

REM ── 2. Ollama models ─────────────────────────────────────────────────
echo [3/6] Checking Ollama is installed...
where ollama >nul 2>nul
if errorlevel 1 (
    echo.
    echo ERROR: Ollama was not found on PATH.
    echo Download and install it from https://ollama.com then re-run this script.
    pause
    exit /b 1
)

echo [4/6] Pulling required AI models - this can take several minutes...
ollama pull qwen3.5:9b
ollama pull nomic-embed-text

REM ── 3. Frontend dependencies ─────────────────────────────────────────
echo [5/6] Installing frontend dependencies (npm)...
where npm >nul 2>nul
if errorlevel 1 (
    echo.
    echo ERROR: npm was not found on PATH.
    echo Install Node.js from https://nodejs.org then re-run this script.
    pause
    exit /b 1
)

pushd frontend
call npm install
if errorlevel 1 (
    echo.
    echo ERROR: npm install failed. Check the messages above.
    popd
    pause
    exit /b 1
)
popd

REM ── 4. Data folders ──────────────────────────────────────────────────
echo [6/6] Preparing data folders...
if not exist backend\data mkdir backend\data
if not exist backend\temp_uploads mkdir backend\temp_uploads
if not exist backend\data\quiz_scores.json (
    echo {} > backend\data\quiz_scores.json
)

echo.
echo ============================================
echo   Setup complete!
echo   Run launch.bat to start LocalMind.
echo ============================================
pause
