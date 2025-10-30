@echo off
echo ========================================
echo CONFIGURATION GROQ API KEY
echo ========================================
echo.
echo La clé Groq est configurée dans backend/config_local.py
echo (ce fichier est ignoré par Git pour la sécurité)
echo.
set GROQ_MODEL=llama-3.1-8b-instant
echo Modèle : %GROQ_MODEL%
echo.
echo ========================================
echo DEMARRAGE SERVEUR DJANGO
echo ========================================
cd /d "%~dp0"
python manage.py runserver 127.0.0.1:8000

