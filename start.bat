@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Nayanee - No-Device Vision Intelligence (ZEISS Theme 2 & 1)
cls
echo =====================================================================
echo    NAYANEE - NO-DEVICE VISION INTELLIGENCE & ACCESSIBLE CLINICAL UX
echo    ZEISS Hackathon - Theme 2 (Primary) & Theme 1 (AFI Complementary)
echo =====================================================================
echo.
echo [1/3] Detecting Python environment...

set PY_CMD=
py -3.12 --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set PY_CMD=py -3.12
    goto :FOUND
)

py -3 --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set PY_CMD=py -3
    goto :FOUND
)

python --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set PY_CMD=python
    goto :FOUND
)

echo [ERROR] Python was not found on your system!
echo Please install Python 3.12 or ensure Python is added to your PATH.
echo.
pause
exit /b 1

:FOUND
echo [OK] Using Python interpreter: %PY_CMD%
echo.
echo [2/3] Preparing Nayanee server at http://localhost:8000 ...
echo [INFO] Supported Native Languages: Kannada, Hindi, Tamil, Telugu, Malayalam, English
echo [INFO] Zero-GPU, frugal smartphone and web architecture ready.
echo.
echo [3/3] Opening browser at http://localhost:8000 ...
start "" "http://localhost:8000"

echo =====================================================================
echo   SERVER RUNNING. Press Ctrl+C in this window to stop the server.
echo =====================================================================
echo.
%PY_CMD% run_nayanee.py
if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] Server exited with code %ERRORLEVEL%.
    pause
)
