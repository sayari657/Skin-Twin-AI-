@echo off
echo ========================================
echo    DEMARRAGE SERVEUR DJANGO
echo ========================================

echo Repertoire actuel: %CD%
echo.

echo Changement vers le repertoire backend...
cd /d "C:\Users\Mohamed\Desktop\skin twin ai\skin-twin-ai\backend"

echo Nouveau repertoire: %CD%
echo.

echo Verification des fichiers...
if exist "manage.py" (
    echo ✅ manage.py trouve
) else (
    echo ❌ manage.py non trouve
    echo Fichiers dans le repertoire:
    dir
    pause
    exit
)

echo.
echo Demarrage du serveur Django...
echo URL: http://127.0.0.1:8000
echo.
python manage.py runserver 127.0.0.1:8000

echo.
echo Serveur arrete. Appuyez sur une touche pour fermer...
pause > nul




