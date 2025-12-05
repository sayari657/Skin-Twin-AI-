@echo off
chcp 65001 >nul
REM Script batch pour demarrer Skin Twin AI automatiquement
REM Double-cliquez sur ce fichier pour demarrer le projet

echo.
echo ========================================
echo   Skin Twin AI - Demarrage Docker
echo ========================================
echo.

REM Aller dans le dossier du script
cd /d "%~dp0"

REM Lancer le script PowerShell (avec version fixe si disponible)
if exist ".\DEMARRER_COMPLET_FIX.ps1" (
    powershell.exe -ExecutionPolicy Bypass -NoProfile -File ".\DEMARRER_COMPLET_FIX.ps1"
) else (
    powershell.exe -ExecutionPolicy Bypass -NoProfile -File ".\DEMARRER_COMPLET.ps1"
)

REM Verifier le code de retour
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERREUR] Erreur lors du demarrage!
    echo.
    pause
)

