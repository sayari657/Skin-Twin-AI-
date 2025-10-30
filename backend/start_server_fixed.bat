@echo off
echo ========================================
echo Starting Django Backend Server
echo ========================================
cd /d "%~dp0"
echo Current directory: %CD%
echo.
echo Checking Python...
python --version
echo.
echo Installing dependencies...
pip install -q django djangorestframework django-cors-headers requests
echo.
echo Running migrations...
python manage.py migrate --noinput
echo.
echo Starting server...
echo Server will run on http://127.0.0.1:8000
echo Press Ctrl+C to stop
echo ========================================
python manage.py runserver 127.0.0.1:8000

