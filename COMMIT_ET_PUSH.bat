@echo off
REM Script pour commit et push des corrections du workflow ML Monitoring
echo ========================================
echo Commit et Push - Corrections ML Monitoring
echo ========================================
echo.

REM Vérifier que nous sommes dans un repo git
git status >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Ce n'est pas un repository git!
    pause
    exit /b 1
)

echo [1/4] Verification des fichiers modifies...
git status --short
echo.

echo [2/4] Ajout des fichiers de correction ML Monitoring...
git add mlops/scripts/run_monitoring.py
git add .github/workflows/ml_monitoring.yml
git add mlops/scripts/setup_mlops.py
git add DEBUG_MONITORING.md
git add PROCHAINES_ETAPES.md
echo Fichiers ajoutes avec succes!
echo.

echo [3/4] Creation du commit...
git commit -m "fix: Corriger le workflow ML Monitoring avec script executable et etapes de debogage

- Ajout du script run_monitoring.py pour execution dans GitHub Actions
- Amelioration du workflow avec etapes de debogage
- Gestion d'erreurs amelioree dans setup_mlops.py
- Ajout de guides de debogage (DEBUG_MONITORING.md, PROCHAINES_ETAPES.md)"
echo.

if errorlevel 1 (
    echo ATTENTION: Le commit a echoue. Verifiez les erreurs ci-dessus.
    pause
    exit /b 1
)

echo [4/4] Push vers GitHub...
echo.
echo Voulez-vous push vers GitHub maintenant? (O/N)
set /p push_confirm=

if /i "%push_confirm%"=="O" (
    echo.
    echo Push en cours...
    git push origin main 2>nul
    if errorlevel 1 (
        git push origin master 2>nul
        if errorlevel 1 (
            echo ERREUR: Impossible de push. Verifiez votre branche.
            echo Branches disponibles:
            git branch -a
            pause
            exit /b 1
        )
    )
    echo.
    echo ========================================
    echo Push reussi!
    echo ========================================
    echo.
    echo Prochaines etapes:
    echo 1. Allez sur GitHub dans l'onglet Actions
    echo 2. Relancez le workflow ML Monitoring
    echo 3. Consultez les logs pour verifier que tout fonctionne
    echo.
) else (
    echo.
    echo Push annule. Vous pouvez le faire manuellement avec:
    echo   git push origin main
    echo ou
    echo   git push origin master
    echo.
)

pause

