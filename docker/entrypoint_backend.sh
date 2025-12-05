#!/bin/bash
set -e

echo "🚀 Démarrage du backend Skin Twin AI..."

# Attendre que la base de données soit prête (si MySQL utilisé)
if [ "$DATABASE_URL" != "" ]; then
    echo "⏳ Attente de la base de données..."
    while ! python -c "import django; django.setup(); from django.db import connection; connection.ensure_connection()" 2>/dev/null; do
        echo "⏳ Base de données non disponible, attente..."
        sleep 2
    done
    echo "✅ Base de données disponible"
fi

# Exécuter les migrations
echo "📦 Exécution des migrations..."
python manage.py migrate --noinput

# Collecter les fichiers statiques
echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput || true

# Créer un superutilisateur si nécessaire (optionnel)
# python manage.py createsuperuser --noinput || true

# Démarrer le serveur
echo "✅ Démarrage du serveur Django..."
exec gunicorn --bind 0.0.0.0:8000 --workers 2 --timeout 120 skin_ai.wsgi:application

