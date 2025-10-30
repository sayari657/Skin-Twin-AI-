@echo off
echo ========================================
echo    DEMARRAGE SERVEUR REACT
echo ========================================

echo Repertoire actuel: %CD%
echo.

echo Changement vers le repertoire frontend...
cd /d "C:\Users\Mohamed\Desktop\skin twin ai\skin-twin-ai\frontend"

echo Nouveau repertoire: %CD%
echo.

echo Verification des fichiers...
if exist "package.json" (
    echo ✅ package.json trouve
) else (
    echo ❌ package.json non trouve
    echo Fichiers dans le repertoire:
    dir
    pause
    exit
)

echo.
echo Demarrage du serveur React...
echo URL: http://localhost:3000
echo.
npm start

echo.
echo Serveur arrete. Appuyez sur une touche pour fermer...
pause > nul




