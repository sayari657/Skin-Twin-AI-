@echo off
echo ========================================
echo CONFIGURATION GROQ API KEY
echo ========================================
echo.
echo Configuration de la clé Groq API...
echo ATTENTION: Configurez votre clé dans les variables d'environnement
echo Exemple: set GROQ_API_KEY=votre_cle_ici
echo.
set GROQ_MODEL=llama-3.1-8b-instant
echo.
echo Modèle : %GROQ_MODEL%
echo.
echo ========================================
echo DEMARRAGE SERVEUR DJANGO
echo ========================================
cd /d "%~dp0"
python manage.py runserver 127.0.0.1:8000

