@echo off
echo ========================================
echo Fix: ML Training Workflow - pytest-mlflow
echo ========================================
echo.

echo [1/3] Adding fixed files...
git add mlops_requirements.txt .github/workflows/ml_training.yml FIX_TRAINING_WORKFLOW.md
if %errorlevel% neq 0 (
    echo ERROR: Failed to add files
    pause
    exit /b 1
)
echo OK: Files added
echo.

echo [2/3] Committing changes...
git commit -m "Fix: Remove non-existent pytest-mlflow dependency and improve ML Training workflow"
if %errorlevel% neq 0 (
    echo ERROR: Failed to commit
    pause
    exit /b 1
)
echo OK: Changes committed
echo.

echo [3/3] Pushing to GitHub...
git push origin main
if %errorlevel% neq 0 (
    echo ERROR: Failed to push
    pause
    exit /b 1
)
echo OK: Changes pushed to GitHub
echo.

echo ========================================
echo SUCCESS! All done.
echo ========================================
echo.
echo Next steps:
echo 1. Go to GitHub Actions
echo 2. Relaunch "ML Training Pipeline"
echo 3. The workflow should now work without pytest-mlflow error
echo.
pause

