@echo off
color 0B
echo Multi-AI Chat Manager v1.0.0
echo =============================

cd /d "%~dp0.."

echo Checking for configuration file...
if exist "config.yml" (
    echo Configuration found: config.yml
) else if exist "src\multi_ai_chat\config\config.yml" (
    echo Configuration found: src\multi_ai_chat\config\config.yml
) else (
    echo.
    echo ERROR: No config.yml found!
    echo Please create configuration first:
    echo   python scripts\setup_config.py
    echo.
    pause
    exit /b 1
)

echo Starting application...
echo.

python "src\multi_ai_chat\main.py"

if errorlevel 1 (
    echo.
    echo Error occurred. Check logs\multi_ai_chat.log for details.
    echo If config issues, run: python scripts\setup_config.py
    pause
)