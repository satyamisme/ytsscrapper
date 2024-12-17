@echo off
setlocal

REM Check if Python is installed
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if venv is available (Python 3.3+ includes venv)
python -m venv --help >nul 2>&1
if %errorlevel% neq 0 (
    echo venv is not available. Please install Python 3.3 or higher.
    pause
    exit /b 1
)

REM Create virtual environment
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment (Windows)
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing requirements from requirements.txt...
pip install -r requirements.txt

REM Run the Python script
echo Running the Python script...
python f1.py

REM Deactivate virtual environment (Optional)
echo Deactivating virtual environment...
deactivate

endlocal
pause