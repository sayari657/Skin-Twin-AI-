@echo off
REM Script batch pour arrêter Skin Twin AI automatiquement
REM Double-cliquez sur ce fichier pour arrêter le projet

echo.
echo ========================================
echo   Skin Twin AI - Arret Docker
echo ========================================
echo.

REM Aller dans le dossier du script
cd /d "%~dp0"

REM Arrêter les conteneurs
docker-compose -f docker/docker-compose.yml down

echo.
echo Conteneurs arretes!
echo.
pause






