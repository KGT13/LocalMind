@echo off
setlocal enabledelayedexpansion
echo ============================================
echo   LocalMind - First-time setup
echo   (installs everything needed automatically)
echo ============================================
echo.

set NEEDS_RESTART=0

REM ── 0. Check winget exists (built into Windows 10 1809+ / Windows 11) ──
where winget >nul 2>nul
if errorlevel 1 (
    echo ERROR: winget was not found on this computer.
    echo winget comes built into Windows 10 ^(May 2019 update or later^) and Windows 11.
    echo If you're on an older Windows 10, install "App Installer" from the Microsoft Store,
    echo then re-run this script.
    pause
    exit /b 1
)

REM ── 1. Python ────────────────────────────────────────────────────────
echo [Check] Python...
python --version >nul 2>nul
if errorlevel 1 (
    echo   Not found. Installing Python via winget...
    winget install --id Python.Python.3.12 -e --silent --accept-package-agreements --accept-source-agreements
    set NEEDS_RESTART=1
) else (
    echo   Found.
)

REM ── 2. Node.js ───────────────────────────────────────────────────────
echo [Check] Node.js...
node --version >nul 2>nul
if errorlevel 1 (
    echo   Not found. Installing Node.js via winget...
    winget install --id OpenJS.NodeJS.LTS -e --silent --accept-package-agreements --accept-source-agreements
    set NEEDS_RESTART=1
) else (
    echo   Found.
)

REM ── 3. Ollama ────────────────────────────────────────────────────────
echo [Check] Ollama...
where ollama >nul 2>nul
if errorlevel 1 (
    echo   Not found. Installing Ollama via winget...
    winget install --id Ollama.Ollama -e --silent --accept-package-agreements --accept-source-agreements
    set NEEDS_RESTART=1
) else (
    echo   Found.
)

REM ── If anything new was installed, stop here and ask for a fresh terminal ──
if "%NEEDS_RESTART%"=="1" (
    echo.
    echo ============================================
    echo   New software was installed.
    echo   Windows needs a FRESH terminal window to see it.
    echo.
    echo   Please:
    echo     1^) Close this window
    echo     2^) Open a new Command Prompt in this same folder
    echo     3^) Run setup.bat again
    echo ============================================
    pause
    exit /b 0
)

echo.
echo All prerequisites are installed. Continuing setup...
echo.

REM ── 4. Python virtual environment (backend) ──────────────────────────
if not exist venv (
    echo [1/5] Creating Python virtual environment...
    python -m venv venv
) else (
    echo [1/5] Virtual environment already exists, skipping.
)

echo [2/5] Installing backend dependencies...
call venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: pip install failed. Check the messages above.
    pause
    exit /b 1
)

REM ── 5. Ollama models ─────────────────────────────────────────────────
echo [3/5] Pulling required AI models - this can take several minutes...
set "CHAT_MODEL="
set "EMBED_MODEL="
pushd backend >nul
for /f "delims=" %%A in ('python -c "from src.config import CHAT_MODEL, EMBED_MODEL; print(CHAT_MODEL); print(EMBED_MODEL)"') do (
    if not defined CHAT_MODEL (
        set "CHAT_MODEL=%%A"
    ) else (
        set "EMBED_MODEL=%%A"
    )
)
popd >nul
if "%CHAT_MODEL%"=="" (
    echo ERROR: Could not read CHAT_MODEL from backend\src\config.py
    pause
    exit /b 1
)
if "%EMBED_MODEL%"=="" (
    echo ERROR: Could not read EMBED_MODEL from backend\src\config.py
    pause
    exit /b 1
)
echo Pulling Ollama chat model: %CHAT_MODEL%
ollama pull %CHAT_MODEL%
echo Pulling Ollama embed model: %EMBED_MODEL%
ollama pull %EMBED_MODEL%

REM ── 6. Frontend dependencies ─────────────────────────────────────────
echo [4/5] Installing frontend dependencies...
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

REM ── 7. Data folders ──────────────────────────────────────────────────
echo [5/5] Preparing data folders...
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
