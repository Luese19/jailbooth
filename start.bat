@echo off
echo  IMAGE JAIL BOOTH
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

REM Change to the project directory
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update dependencies
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM Run quick test
echo.
echo Running quick system test...
python tests\quick_test.py

REM Ask if user wants to continue
echo.
set /p choice=Start The Slammer application? (Y/N): 
if /i "%choice%"=="Y" (
    echo.
    echo Starting The Slammer...
    python src\main.py
) else (
    echo.
    echo To start manually, run: python src\main.py
)

pause
