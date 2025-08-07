@echo off
color 0B
echo Multi-AI Chat Manager v1.0.0
echo =============================
echo Starting application...
echo.

cd /d "%~dp0.."
python "src\multi_ai_chat\main.py"

if errorlevel 1 (
    echo.
    echo Error occurred. Check logs\multi_ai_chat.log for details.
    pause
)