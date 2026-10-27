@echo off
setlocal
cd /d "%~dp0"

echo ========================================
echo      NewsLens Fake News Detection
echo ========================================

where py >nul 2>nul
if errorlevel 1 (
    echo Python was not found. Install Python 3.10 or newer first.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    py -m venv .venv
    if errorlevel 1 goto :error
)

set "PYTHON=.venv\Scripts\python.exe"

echo Installing or checking dependencies...
%PYTHON% -m pip install -r requirements.txt
if errorlevel 1 goto :error

if not exist "data\Fake.csv" (
    echo Missing data\Fake.csv
    echo Download the ISOT dataset and place Fake.csv and True.csv in data\.
    pause
    exit /b 1
)

if not exist "data\True.csv" (
    echo Missing data\True.csv
    echo Download the ISOT dataset and place Fake.csv and True.csv in data\.
    pause
    exit /b 1
)

if not exist "models\newslens.joblib" (
    echo No trained model found. Training on data\...
    %PYTHON% training\train_model.py --input data
    if errorlevel 1 goto :error
) else (
    echo Existing trained model found. Skipping training.
)

echo Starting NewsLens at http://127.0.0.1:5000
%PYTHON% server.py
exit /b 0

:error
echo.
echo NewsLens could not start. Review the message above.
pause
exit /b 1
