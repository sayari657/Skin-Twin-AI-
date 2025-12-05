# 🐳 Guide d'Export Docker pour Skin Twin AI

Ce guide vous explique comment exporter et partager votre projet Skin Twin AI avec Docker Desktop.

## 📋 Prérequis

- Docker Desktop installé et démarré
- Git (optionnel, pour cloner le projet)

## 🚀 Méthode 1 : Exporter via Docker Compose (Recommandé)

### Pour l'expéditeur (vous) :

1. **Construire les images Docker :**
```bash
cd skin-twin-ai
docker-compose -f docker/docker-compose.yml build
```

2. **Sauvegarder les images Docker :**
```bash
docker save skin-twin-ai_backend:latest skin-twin-ai_frontend:latest -o skin-twin-ai-images.tar
```

3. **Créer une archive du projet :**
```bash
# Créer une archive avec le code et les images Docker
# Exclure node_modules, venv, __pycache__, etc.
tar -czf skin-twin-ai-project.tar.gz \
  --exclude='node_modules' \
  --exclude='venv' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='.git' \
  --exclude='media' \
  --exclude='db.sqlite3' \
  skin-twin-ai/ skin-twin-ai-images.tar
```

### Pour le destinataire (vos camarades) :

1. **Extraire l'archive :**
```bash
tar -xzf skin-twin-ai-project.tar.gz
```

2. **Charger les images Docker :**
```bash
docker load -i skin-twin-ai-images.tar
```

3. **Créer le fichier .env (optionnel) :**
```bash
cd skin-twin-ai/docker
cp env.example .env
# Éditer .env pour ajouter vos clés API si nécessaire
```

4. **Démarrer le projet :**
```bash
cd skin-twin-ai
docker-compose -f docker/docker-compose.yml up -d
```

5. **Vérifier que tout fonctionne :**
```bash
# Voir les logs
docker-compose -f docker/docker-compose.yml logs -f

# Vérifier les conteneurs
docker ps
```

6. **Accéder à l'application :**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api
- Admin Django: http://localhost:8000/admin

## 🚀 Méthode 2 : Via Git + Docker Build (Alternative)

### Pour l'expéditeur :

1. **Pousser le code sur Git (GitHub, GitLab, etc.) :**
```bash
git add .
git commit -m "Projet Skin Twin AI prêt pour Docker"
git push origin main
```

2. **Créer un fichier .dockerignore :**
```bash
# Créer .dockerignore à la racine du projet
echo "node_modules
venv
__pycache__
*.pyc
.git
.env
*.log
media
db.sqlite3" > .dockerignore
```

### Pour le destinataire :

1. **Cloner le projet :**
```bash
git clone <URL_DU_REPO>
cd skin-twin-ai
```

2. **Construire et démarrer :**
```bash
docker-compose -f docker/docker-compose.yml up --build -d
```

## 📦 Méthode 3 : Export complet avec volumes (Données incluses)

Si vous voulez inclure les données de la base de données :

```bash
# 1. Sauvegarder les volumes Docker
docker run --rm -v skin-twin-ai_backend_db:/data -v $(pwd):/backup alpine tar czf /backup/backend_db_backup.tar.gz /data
docker run --rm -v skin-twin-ai_backend_media:/data -v $(pwd):/backup alpine tar czf /backup/backend_media_backup.tar.gz /data

# 2. Créer l'archive complète
tar -czf skin-twin-ai-complete.tar.gz \
  skin-twin-ai/ \
  skin-twin-ai-images.tar \
  backend_db_backup.tar.gz \
  backend_media_backup.tar.gz
```

## 🛠️ Commandes utiles

### Gestion des conteneurs :
```bash
# Arrêter les conteneurs
docker-compose -f docker/docker-compose.yml down

# Redémarrer
docker-compose -f docker/docker-compose.yml restart

# Voir les logs
docker-compose -f docker/docker-compose.yml logs -f backend
docker-compose -f docker/docker-compose.yml logs -f frontend

# Accéder au shell du backend
docker exec -it skin_twin_backend bash

# Accéder au shell du frontend
docker exec -it skin_twin_frontend sh
```

### Base de données :
```bash
# Créer un superutilisateur Django
docker exec -it skin_twin_backend python manage.py createsuperuser

# Appliquer les migrations
docker exec -it skin_twin_backend python manage.py migrate

# Créer les migrations
docker exec -it skin_twin_backend python manage.py makemigrations
```

### Nettoyage :
```bash
# Arrêter et supprimer les conteneurs
docker-compose -f docker/docker-compose.yml down

# Supprimer les images
docker rmi skin-twin-ai_backend skin-twin-ai_frontend

# Nettoyer tout (attention : supprime aussi les volumes)
docker-compose -f docker/docker-compose.yml down -v
```

## ⚙️ Configuration

### Variables d'environnement

Créez un fichier `docker/.env` avec :

```env
SECRET_KEY=votre-secret-key-securisee
GROQ_API_KEY=votre-cle-api-groq
GROQ_MODEL=llama-3.1-8b-instant
DEBUG=1
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
```

### Ports

Par défaut :
- Frontend: `3000`
- Backend: `8000`

Pour changer les ports, modifiez `docker-compose.yml` :

```yaml
ports:
  - "VOTRE_PORT:8000"  # Backend
  - "VOTRE_PORT:3000"   # Frontend
```

## 🐛 Dépannage

### Les conteneurs ne démarrent pas :
```bash
# Vérifier les logs
docker-compose -f docker/docker-compose.yml logs

# Reconstruire les images
docker-compose -f docker/docker-compose.yml build --no-cache
```

### Erreur de port déjà utilisé :
```bash
# Vérifier quel processus utilise le port
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Mac/Linux

# Changer le port dans docker-compose.yml
```

### Problème de permissions :
```bash
# Sur Linux/Mac, donner les permissions
chmod +x docker/entrypoint.sh
chmod +x docker/entrypoint_backend.sh
```

## 📝 Checklist avant l'export

- [ ] Les images Docker sont construites avec succès
- [ ] Le fichier `.env.example` est présent
- [ ] Le fichier `docker-compose.yml` est configuré
- [ ] Les fichiers sensibles (.env, db.sqlite3) sont exclus
- [ ] Un README avec les instructions est inclus

## 🎯 Résumé rapide pour vos camarades

1. Extraire l'archive
2. Charger les images : `docker load -i skin-twin-ai-images.tar`
3. Démarrer : `docker-compose -f docker/docker-compose.yml up -d`
4. Accéder : http://localhost:3000

C'est tout ! 🎉






