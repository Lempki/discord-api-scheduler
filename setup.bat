@echo off
setlocal
echo === discord-api-scheduler setup ===
echo.

:: Require Python 3.12+
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Install Python 3.12+ from https://python.org
    pause
    exit /b 1
)

:: Create virtual environment if it doesn't already exist
if not exist ".venv\" (
    echo Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment.
        pause
        exit /b 1
    )
) else (
    echo Virtual environment already exists, skipping creation.
)

:: Upgrade pip
echo Upgrading pip...
.venv\Scripts\python -m pip install --upgrade pip --quiet
if errorlevel 1 (
    echo ERROR: Failed to upgrade pip.
    pause
    exit /b 1
)

:: Install package with dev extras (editable)
echo Installing package and dev dependencies...
.venv\Scripts\python -m pip install -e ".[dev]"
if errorlevel 1 (
    echo ERROR: Failed to install dependencies.
    pause
    exit /b 1
)

:: Copy .env.template to .env if .env doesn't exist yet
if not exist ".env" (
    copy ".env.template" ".env" >nul
    echo Created .env from .env.template
    echo   ^> Edit .env and set DISCORD_API_SECRET before running the API.
) else (
    echo .env already exists, skipping.
)

echo.
echo Setup complete!
echo   Activate venv : .venv\Scripts\activate
echo   Run the API   : .venv\Scripts\python -m uvicorn scheduler_api.main:app --reload
echo   Run tests     : .venv\Scripts\python -m pytest
echo.
pause
endlocal
