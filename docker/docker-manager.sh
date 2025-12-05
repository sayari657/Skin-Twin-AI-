#!/bin/bash
# Script Docker pour Skin Twin AI - Linux/Mac
# Usage: ./docker-manager.sh [command]

set -e

COMPOSE_FILE="docker/docker-compose.yml"

case "$1" in
  build)
    echo "🔨 Construction des images Docker..."
    docker-compose -f $COMPOSE_FILE build
    ;;
  start)
    echo "🚀 Démarrage des services..."
    docker-compose -f $COMPOSE_FILE up -d
    echo ""
    echo "✅ Services démarrés!"
    echo "Frontend: http://localhost:3000"
    echo "Backend API: http://localhost:8000/api"
    echo "Admin Django: http://localhost:8000/admin"
    ;;
  stop)
    echo "⏹️  Arrêt des services..."
    docker-compose -f $COMPOSE_FILE down
    ;;
  restart)
    echo "🔄 Redémarrage des services..."
    docker-compose -f $COMPOSE_FILE restart
    ;;
  logs)
    echo "📋 Affichage des logs (Ctrl+C pour quitter)..."
    docker-compose -f $COMPOSE_FILE logs -f
    ;;
  export)
    FILENAME=${2:-skin-twin-ai-images}
    echo "📦 Export des images Docker..."
    docker save skin-twin-ai_backend:latest skin-twin-ai_frontend:latest -o ${FILENAME}.tar
    echo "✅ Images exportées dans ${FILENAME}.tar"
    ;;
  clean)
    echo "⚠️  ATTENTION: Suppression des conteneurs et volumes..."
    read -p "Êtes-vous sûr? (oui/non): " confirm
    if [ "$confirm" = "oui" ]; then
      docker-compose -f $COMPOSE_FILE down -v
      echo "✅ Nettoyage terminé!"
    else
      echo "❌ Opération annulée"
    fi
    ;;
  shell-backend)
    echo "🐚 Accès au shell du backend..."
    docker exec -it skin_twin_backend bash
    ;;
  shell-frontend)
    echo "🐚 Accès au shell du frontend..."
    docker exec -it skin_twin_frontend sh
    ;;
  migrate)
    echo "📦 Exécution des migrations..."
    docker exec -it skin_twin_backend python manage.py migrate
    ;;
  createsuperuser)
    echo "👤 Création d'un superutilisateur..."
    docker exec -it skin_twin_backend python manage.py createsuperuser
    ;;
  *)
    echo "Usage: $0 {build|start|stop|restart|logs|export|clean|shell-backend|shell-frontend|migrate|createsuperuser}"
    echo ""
    echo "Commandes disponibles:"
    echo "  build            - Construire les images Docker"
    echo "  start            - Démarrer les services"
    echo "  stop             - Arrêter les services"
    echo "  restart          - Redémarrer les services"
    echo "  logs             - Voir les logs"
    echo "  export [name]    - Exporter les images (nom optionnel)"
    echo "  clean            - Supprimer conteneurs et volumes"
    echo "  shell-backend    - Accéder au shell du backend"
    echo "  shell-frontend   - Accéder au shell du frontend"
    echo "  migrate          - Exécuter les migrations"
    echo "  createsuperuser  - Créer un superutilisateur"
    exit 1
    ;;
esac

exit 0

