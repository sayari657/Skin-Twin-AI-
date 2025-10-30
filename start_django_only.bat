@echo off
echo ========================================
echo    DEMARRAGE SERVEUR DJANGO
echo ========================================

cd /d "C:\Users\Mohamed\Desktop\skin twin ai\skin-twin-ai\backend"
echo Repertoire actuel: %CD%
echo.
echo Demarrage du serveur Django...
python manage.py runserver

echo.
echo Appuyez sur une touche pour fermer...
pause > nul






