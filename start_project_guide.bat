@echo off
echo ========================================
echo   GUIDE DE DEMARRAGE - SKIN TWIN AI
echo ========================================
echo.

echo [1/5] Verification des prerequis...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installe ou pas dans le PATH
    echo Telechargez Python depuis: https://www.python.org/downloads/
    pause
    exit /b 1
)

node --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Node.js n'est pas installe ou pas dans le PATH
    echo Telechargez Node.js depuis: https://nodejs.org/
    pause
    exit /b 1
)

echo [2/5] Verification de la structure du projet...
if not exist "backend" (
    echo ERREUR: Dossier backend introuvable
    echo Assurez-vous d'etre dans le bon dossier
    pause
    exit /b 1
)

if not exist "frontend" (
    echo ERREUR: Dossier frontend introuvable
    echo Assurez-vous d'etre dans le bon dossier
    pause
    exit /b 1
)

echo [3/5] Configuration du backend...
cd backend
if not exist "venv" (
    echo Creation de l'environnement virtuel...
    python -m venv venv
)

echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

echo Installation des dependances Python...
pip install -r requirements.txt

echo Application des migrations...
python manage.py makemigrations
python manage.py migrate

echo [4/5] Configuration du frontend...
cd ..\frontend
if not exist "node_modules" (
    echo Installation des dependances Node.js...
    npm install
)

echo [5/5] Demarrage des serveurs...
cd ..
echo.
echo ========================================
echo   SERVEURS EN COURS DE DEMARRAGE...
echo ========================================
echo Backend Django: http://127.0.0.1:8000
echo Frontend React: http://localhost:3000
echo.
echo Appuyez sur Ctrl+C pour arreter les serveurs
echo.

start "Backend Django" cmd /k "cd backend && venv\Scripts\activate.bat && python manage.py runserver 127.0.0.1:8000"
timeout /t 3 /nobreak >nul
start "Frontend React" cmd /k "cd frontend && npm start"

echo.
echo ========================================
echo   DEMARRAGE TERMINE !
echo ========================================
echo.
echo Ouvrez votre navigateur sur: http://localhost:3000
echo.
echo Fonctionnalites disponibles:
echo - Assistant IA intelligent et deplagable
echo - Analyse de peau automatique
echo - Base de donnees de 112 produits
echo - Mode vocal integre
echo - Chat contextuel personnalise
echo.
echo Appuyez sur une touche pour fermer ce guide...
pause >nul


