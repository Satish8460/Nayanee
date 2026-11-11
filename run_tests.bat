@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Nayanee - Test Suite Runner
cls
echo =====================================================================
echo    NAYANEE - TEST SUITE AND BENCHMARK RUNNER
echo =====================================================================
echo.

set PY_CMD=
py -3.12 --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set PY_CMD=py -3.12
    goto :RUN_TESTS
)

py -3 --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set PY_CMD=py -3
    goto :RUN_TESTS
)

python --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set PY_CMD=python
    goto :RUN_TESTS
)

echo [ERROR] Python not found!
pause
exit /b 1

:RUN_TESTS
echo Running Pytest across all test suites...
%PY_CMD% -m pytest tests/ -v
if %ERRORLEVEL% neq 0 (
    echo.
    echo [FAIL] Some tests failed.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo =====================================================================
echo Running End-to-End Multilingual Live Demonstration...
echo =====================================================================
%PY_CMD% demo_e2e.py

echo.
echo =====================================================================
echo [SUCCESS] All verification tests passed cleanly!
echo =====================================================================
pause
