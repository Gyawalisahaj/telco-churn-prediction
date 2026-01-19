@echo off
REM Quick Start Script for Nepal Telco Churn Prediction (Windows)

echo ╔════════════════════════════════════════════════════════════╗
echo ║  Nepal Telco Churn Prediction System - Quick Start         ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Check Python
echo 📋 Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% found
echo.

REM Setup virtual environment
echo 📦 Setting up virtual environment...
if not exist "tf_venv" (
    echo Creating virtual environment...
    python -m venv tf_venv
) else (
    echo Virtual environment already exists
)

REM Activate virtual environment
call tf_venv\Scripts\activate.bat
echo ✅ Virtual environment activated
echo.

REM Install requirements
echo 📥 Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)
echo ✅ Dependencies installed
echo.

REM Create logs directory
if not exist "logs" mkdir logs
echo 📁 Created logs directory
echo.

REM Display startup options
echo ╔════════════════════════════════════════════════════════════╗
echo ║  Ready to Run!                                             ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Choose how to run the application:
echo.
echo 1 - Run Streamlit UI Only:
echo    python main.py --ui
echo.
echo 2 - Run FastAPI Backend Only:
echo    python main.py --api
echo.
echo 3 - Run Both (Recommended):
echo    python main.py --both
echo.
echo 4 - Custom API Port:
echo    python main.py --api --port 9000
echo.
echo API Documentation: http://localhost:8000/docs
echo UI URL: http://localhost:8501
echo.
echo Tip: Use 'python main.py --help' for more options
echo.
pause
