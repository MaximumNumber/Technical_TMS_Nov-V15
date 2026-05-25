@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul 2>&1
title TMS - Sudan University Timetable Management System - Windows Setup

echo.
echo ============================================================
echo   TMS - Timetable Management System
echo   Sudan University of Science and Technology
echo   Windows Setup Script
echo ============================================================
echo.

:: ── Check Python ────────────────────────────────────────────────────────────
echo [1/7] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo   ERROR: Python is not installed or not in PATH.
    echo   Please download Python 3.11+ from https://www.python.org/downloads/
    echo   Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)
for /f "tokens=2" %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo   Found Python %PYVER%

:: ── Check pip ────────────────────────────────────────────────────────────────
echo [2/7] Checking pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo   ERROR: pip is not available.
    echo   Run: python -m ensurepip --upgrade
    pause
    exit /b 1
)
echo   pip found.

:: ── Create virtual environment ───────────────────────────────────────────────
echo [3/7] Creating virtual environment...
if exist "venv\" (
    echo   Virtual environment already exists, skipping.
) else (
    python -m venv venv
    echo   Virtual environment created.
)

:: ── Activate venv ────────────────────────────────────────────────────────────
echo [4/7] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo   ERROR: Failed to activate virtual environment.
    pause
    exit /b 1
)
echo   Virtual environment activated.

:: ── Install dependencies ─────────────────────────────────────────────────────
echo [5/7] Installing Python dependencies...
python -m pip install --upgrade pip --quiet
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo   ERROR: Failed to install some dependencies.
    echo   Check requirements.txt and your internet connection.
    pause
    exit /b 1
)
echo   All dependencies installed.

:: ── Check PostgreSQL ─────────────────────────────────────────────────────────
echo [6/7] Checking database connection...
echo   NOTE: PostgreSQL must be running with correct credentials.
echo   Configure your DB settings in the .env file (see .env.example).
echo   Attempting migration...
python manage.py migrate --noinput
if errorlevel 1 (
    echo.
    echo   ERROR: Database migration failed.
    echo   Make sure PostgreSQL is running and .env is configured correctly.
    echo   See README.md for database setup instructions.
    pause
    exit /b 1
)
echo   Database ready.

:: ── Collect static files ─────────────────────────────────────────────────────
echo [7/7] Collecting static files...
python manage.py collectstatic --noinput --quiet
if errorlevel 1 (
    echo   WARNING: Static files collection had issues.
)
echo   Static files collected.

:: ── Seed admin ───────────────────────────────────────────────────────────────
echo.
echo Seeding admin user (admin / admin123)...
python manage.py seed_admin --username admin --password admin123 2>nul || echo   Admin already exists.

:: ── Optional: seed demo data ─────────────────────────────────────────────────
echo.
set /p SEED_DATA="Do you want to load demo/seed data? (y/n): "
if /i "%SEED_DATA%"=="y" (
    echo   Loading seed data...
    python manage.py seed_data
    if errorlevel 1 (
        echo   WARNING: Seed data had some issues, continuing anyway.
    ) else (
        echo   Seed data loaded successfully.
    )
)

:: ── Done ─────────────────────────────────────────────────────────────────────
echo.
echo ============================================================
echo   Setup complete!
echo.
echo   To start the development server, run:
echo     run_dev.bat
echo   or manually:
echo     venv\Scripts\activate
echo     python manage.py runserver 0.0.0.0:5000
echo.
echo   Default login:  admin / admin123
echo   URL:            http://localhost:5000
echo ============================================================
echo.
pause
