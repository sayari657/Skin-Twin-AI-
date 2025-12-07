@echo off
echo ========================================
echo Fix: Update GitHub Actions to v4
echo ========================================
echo.

echo [1/3] Adding workflow files...
git add .github/workflows/ml_monitoring.yml .github/workflows/ml_training.yml
if %errorlevel% neq 0 (
    echo ERROR: Failed to add files
    pause
    exit /b 1
)
echo OK: Files added
echo.

echo [2/3] Committing changes...
git commit -m "Fix: Update GitHub Actions to v4 (fix deprecation error)"
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
echo 2. Relaunch the workflows
echo 3. They should now work without deprecation errors
echo.
pause

