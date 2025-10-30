@echo off
echo ========================================
echo SKIN TWIN AI - Backend Pro
echo ========================================
cd /d "%~dp0"
echo Current directory: %CD%
echo.

echo [1/5] Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)
echo.

echo [2/5] Installing/Updating dependencies...
pip install -q -r requirements.txt --upgrade
if errorlevel 1 (
    echo WARNING: Some dependencies may have failed to install
)
echo.

echo [3/5] Running database migrations...
python manage.py migrate --noinput
if errorlevel 1 (
    echo ERROR: Migrations failed!
    pause
    exit /b 1
)
echo.

echo [4/5] Checking system connections...
python check_connections.py
if errorlevel 1 (
    echo WARNING: Some checks failed, but continuing...
)
echo.

echo [5/5] Starting Django server...
echo.
echo ========================================
echo ✅ SERVER STARTING
echo ========================================
echo Backend API: http://127.0.0.1:8000
echo Admin Panel: http://127.0.0.1:8000/admin
echo API Docs: http://127.0.0.1:8000/api/
echo.
echo Press Ctrl+C to stop
echo ========================================
echo.

python manage.py runserver 127.0.0.1:8000

