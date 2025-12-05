#!/bin/bash
set -e
echo "🚀 Démarrage du backend Skin Twin AI..."
echo "📦 Exécution des migrations..."
python manage.py migrate --noinput
echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput || true
echo "✅ Démarrage du serveur Django..."
exec gunicorn --bind 0.0.0.0:8000 --workers 2 --timeout 120 skin_ai.wsgi:application

