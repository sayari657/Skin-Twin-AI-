@echo off
echo ========================================
echo    DEMARRAGE DES SERVEURS SKIN TWIN AI
echo ========================================

echo.
echo [1/3] Demarrage du serveur Django...
cd /d "C:\Users\Mohamed\Desktop\skin twin ai\skin-twin-ai\backend"
start "Django Server" cmd /k "python manage.py runserver"

echo.
echo [2/3] Attente de 3 secondes...
timeout /t 3 /nobreak > nul

echo.
echo [3/3] Demarrage du serveur React...
cd /d "C:\Users\Mohamed\Desktop\skin twin ai\skin-twin-ai\frontend"
start "React Server" cmd /k "npm start"

echo.
echo ========================================
echo    SERVEURS DEMARRES !
echo ========================================
echo.
echo Backend Django: http://127.0.0.1:8000
echo Frontend React: http://localhost:3000
echo.
echo Appuyez sur une touche pour fermer...
pause > nul




