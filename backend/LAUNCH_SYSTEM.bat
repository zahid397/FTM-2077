@echo off
title FTM-2077 // SYSTEM LAUNCHER
color 0a
cls

:: ---------------------------------------------------
:: FTM-2077 BOOT SEQUENCE
:: ---------------------------------------------------

echo.
echo  =======================================================
echo   FTM-2077 // NEURAL LINK ESTABLISHED
echo  =======================================================
echo.

:: 1. Script er nijer folder e dhukbe (Path fix)
cd /d "%~dp0"

:: 2. Dependencies Install/Check korbe
echo  [*] SCANNING PYTHON MODULES...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo  [!] CRITICAL ERROR: Python Libraries missing.
    echo  [!] Make sure Python is installed and added to PATH.
    pause
    exit
)
echo  [OK] MODULES INTEGRATED.
echo.

:: 3. Folder Structure Setup korbe
echo  [*] INITIALIZING FILE SYSTEMS...
python setup_final.py
echo  [OK] SYSTEM READY.
echo.

:: 4. Frontend (HTML) ta Browser e open korbe
echo  [*] BOOTING VISUAL INTERFACE...
start "" "frontend/index.html"

:: 5. Backend Server Start korbe
echo  [*] CONNECTING TO MAINFRAME (Server)...
echo  -------------------------------------------------------
echo  [LOG] Server running at: http://localhost:8000
echo  [LOG] Press CTRL+C to Shutdown.
echo  -------------------------------------------------------
echo.

:: Uvicorn start via Python
python backend/main.py

pause
