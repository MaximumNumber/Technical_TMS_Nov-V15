@echo off
chcp 65001 >nul 2>&1
title TMS - Development Server

echo.
echo ============================================================
echo   TMS - Starting Development Server
echo   URL: http://localhost:5000
echo   Press Ctrl+C to stop
echo ============================================================
echo.

if not exist "venv\Scripts\activate.bat" (
    echo   ERROR: Virtual environment not found.
    echo   Please run setup.bat first.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
python manage.py runserver 0.0.0.0:5000
