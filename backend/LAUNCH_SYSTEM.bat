@echo off
title FTM-2077 // SYSTEM LAUNCHER
color 0a
cls

echo.
echo =======================================================
echo           FTM-2077 // OMEGA  SYSTEM BOOTING
echo =======================================================
echo.

:: Move script directory
cd /d "%~dp0"

:: 1. Python check
echo [*] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found! Install Python 3.10+ and retry.
    pause
    exit
)

:: 2. Install dependencies
echo [*] Installing Dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit
)
echo [OK] Dependencies loaded.

:: 3. Initialize Folder Structure
echo [*] Initializing System Folders...
python setup_final.py
echo [OK] File System Ready.

:: 4. Launch Frontend UI
echo [*] Launching Visual Interface...
start "" http://localhost:5500/frontend/index.html

:: 5. Start Backend Server (Correct Way)
echo.
echo ---------------------------------------------------------
echo   BACKEND SERVER LIVE:  http://localhost:8000
echo   PRESS CTRL+C TO STOP SERVER
echo ---------------------------------------------------------
echo.

:: Fix Path for VSCode live-server
:: If live-server installed → use it
where live-server >nul 2>&1
if %errorlevel% == 0 (
    echo [*] Starting Local Frontend Server (live-server)...
    start "" live-server --port=5500 --no-browser
) else (
    echo [WARN] live-server not installed. Install using:
    echo        npm install -g live-server
    echo.
)

:: Start API
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

pause
