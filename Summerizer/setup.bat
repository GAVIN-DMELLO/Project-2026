@echo off
echo ==========================================
echo Academic Summarizer - Quick Start
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo √ Python detected

REM Navigate to backend directory
cd backend

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo √ Virtual environment created
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo To start the application:
echo.
echo 1. (Optional) Set your Claude API key:
echo    set ANTHROPIC_API_KEY=your-api-key-here
echo.
echo 2. Start the backend server:
echo    python app.py
echo.
echo 3. Open frontend\index.html in your browser
echo.
echo ==========================================
pause
