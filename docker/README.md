# 🐳 DOCKER - SKIN TWIN AI

Guide rapide pour utiliser Docker avec Skin Twin AI.

## 🚀 DÉMARRAGE RAPIDE

```bash
# 1. Construire les images
docker-compose -f docker/docker-compose.yml build

# 2. Démarrer les services
docker-compose -f docker/docker-compose.yml up -d

# 3. Voir les logs
docker-compose -f docker/docker-compose.yml logs -f
```

## 📍 ACCÈS

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000/api
- **Admin Django:** http://localhost:8000/admin

## 🛠️ COMMANDES UTILES

```bash
# Arrêter
docker-compose -f docker/docker-compose.yml down

# Redémarrer
docker-compose -f docker/docker-compose.yml restart

# Migrations DB
docker exec -it skin_twin_backend python manage.py migrate

# Créer superutilisateur
docker exec -it skin_twin_backend python manage.py createsuperuser
```

## 📦 EXPORTER LES IMAGES

```bash
# Sauvegarder les images
docker save skin-twin-ai_backend:latest skin-twin-ai_frontend:latest -o images.tar

# Charger les images
docker load -i images.tar
```

Voir `DOCKER_GUIDE.md` pour plus de détails.

