@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Nayanee Public Cloudflare Share Tunnel
cls
echo =====================================================================
echo    NAYANEE (ನಯनी) — PUBLIC CLOUDFLARE LIVE SHARE TUNNEL
echo =====================================================================
echo.
echo [1/2] Starting local Nayanee server in background...
start /B py -3.12 run_nayanee.py >nul 2>&1

echo [2/2] Starting Cloudflare HTTPS Quick Tunnel...
echo.
echo =====================================================================
echo Look for the "https://....trycloudflare.com" link below.
echo Copy and WhatsApp that link to anyone on mobile or desktop!
echo (Press Ctrl+C when you want to stop sharing)
echo =====================================================================
echo.
.\bin\cloudflared.exe tunnel --url http://localhost:8000
pause
