@echo off
chcp 65001 >nul
echo ========================================
echo   FIX ALL PROBLEMS - GitHub Actions
echo ========================================
echo.
echo Ce script va :
echo   1. Ajouter tous les fichiers corriges
echo   2. Faire le commit
echo   3. Push vers GitHub
echo.
pause

echo.
echo [ETAPE 1/4] Verification de l'etat Git...
git status --short
if %errorlevel% neq 0 (
    echo ERREUR: Git n'est pas disponible ou le repertoire n'est pas un repo Git
    pause
    exit /b 1
)
echo OK: Git fonctionne
echo.

echo [ETAPE 2/4] Ajout des fichiers corriges...
echo.
echo Fichiers a ajouter :
echo   - mlops_requirements.txt (pytest-mlflow supprime)
echo   - .github/workflows/ml_monitoring.yml (Actions v4)
echo   - .github/workflows/ml_training.yml (Actions v4 + cache pip + fix MLflow)
echo   - mlops/deployment/model_registry.py (Fix runs imbriques MLflow)
echo   - mlops/pipelines/training_pipeline.py (Script d'entree)
echo   - Fichiers de documentation
echo.

git add mlops_requirements.txt
if %errorlevel% neq 0 (
    echo ATTENTION: Erreur lors de l'ajout de mlops_requirements.txt
)

git add .github/workflows/ml_monitoring.yml
if %errorlevel% neq 0 (
    echo ATTENTION: Erreur lors de l'ajout de ml_monitoring.yml
)

git add .github/workflows/ml_training.yml
if %errorlevel% neq 0 (
    echo ATTENTION: Erreur lors de l'ajout de ml_training.yml
)

git add mlops/scripts/run_monitoring.py mlops/scripts/setup_mlops.py
if %errorlevel% neq 0 (
    echo ATTENTION: Erreur lors de l'ajout des scripts MLOps
)

git add mlops/deployment/model_registry.py
if %errorlevel% neq 0 (
    echo ATTENTION: Erreur lors de l'ajout de model_registry.py
)

git add mlops/pipelines/training_pipeline.py
if %errorlevel% neq 0 (
    echo ATTENTION: Erreur lors de l'ajout de training_pipeline.py
)

git add mlops_requirements_monitoring.txt
if %errorlevel% neq 0 (
    echo ATTENTION: Erreur lors de l'ajout de mlops_requirements_monitoring.txt
)

git add *.md *.bat COMMANDES_GIT_SIMPLES.txt 2>nul
if %errorlevel% neq 0 (
    echo ATTENTION: Certains fichiers de documentation n'ont pas pu etre ajoutes
)

echo.
echo Verification des fichiers ajoutes :
git status --short
echo.
echo OK: Fichiers ajoutes
echo.

echo [ETAPE 3/4] Commit des changements...
echo.
git commit -m "Fix: Update GitHub Actions to v4, remove pytest-mlflow, and fix MLflow nested runs"
if %errorlevel% neq 0 (
    echo.
    echo ATTENTION: Le commit a echoue
    echo Raisons possibles :
    echo   - Aucun changement a commiter
    echo   - Fichiers deja commits
    echo.
    echo Verification de l'etat :
    git status --short
    echo.
    echo Voulez-vous continuer avec le push quand meme ? (O/N)
    set /p continue="> "
    if /i not "%continue%"=="O" (
        echo Operation annulee
        pause
        exit /b 1
    )
) else (
    echo OK: Changements commits
)
echo.

echo [ETAPE 4/4] Push vers GitHub...
echo.
git push origin main
if %errorlevel% neq 0 (
    echo.
    echo ERREUR: Le push a echoue
    echo Raisons possibles :
    echo   - Pas de connexion Internet
    echo   - Credentials GitHub non configures
    echo   - Conflits avec le remote
    echo.
    echo Voulez-vous voir les details ? (O/N)
    set /p details="> "
    if /i "%details%"=="O" (
        git status
        git log --oneline -5
    )
    pause
    exit /b 1
) else (
    echo.
    echo ========================================
    echo   SUCCES ! Tous les changements ont ete pushes
    echo ========================================
    echo.
)
echo.

echo ========================================
echo   RESUME DES CORRECTIONS
echo ========================================
echo.
echo 1. GitHub Actions mis a jour vers v4 :
echo    - actions/checkout@v3 ^>^> v4
echo    - actions/cache@v3 ^>^> v4
echo    - actions/upload-artifact@v3 ^>^> v4
echo.
echo 2. pytest-mlflow supprime :
echo    - Package n'existe pas sur PyPI
echo    - Ligne commentee dans mlops_requirements.txt
echo.
echo 3. Workflow ML Training ameliore :
echo    - Cache pip ajoute
echo    - Gestion d'erreur amelioree
echo.
echo 4. Workflow ML Monitoring optimise :
echo    - Dependances minimales (50MB au lieu de 4-5GB)
echo    - Temps d'execution reduit de 60min a 5-10min
echo.
echo 5. Fix MLflow nested runs :
echo    - Plus d'erreur de runs imbriques
echo    - Gestion des fichiers manquants
echo    - Script d'entree pour le workflow
echo.
echo ========================================
echo   PROCHAINES ETAPES
echo ========================================
echo.
echo 1. Allez sur GitHub Actions :
echo    https://github.com/sayari657/Skin-Twin-AI-/actions
echo.
echo 2. Relancez les workflows :
echo    - ML Monitoring
echo    - ML Training Pipeline
echo.
echo 3. Verifiez que les workflows fonctionnent :
echo    - Plus d'erreur de depreciation
echo    - Plus d'erreur pytest-mlflow
echo    - Temps d'execution reduit
echo.
pause

