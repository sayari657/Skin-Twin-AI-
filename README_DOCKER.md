# 🐳 Skin Twin AI - Guide Docker Rapide

## 🚀 Démarrage Rapide dans Docker Desktop

### Méthode 1 : Script automatique (Recommandé)

1. **Ouvrir Docker Desktop** et s'assurer qu'il est démarré ✅

2. **Ouvrir PowerShell** dans le dossier `skin-twin-ai`

3. **Exécuter le script de démarrage :**
```powershell
.\DEMARRER_DOCKER.ps1
```

Le script va automatiquement :
- ✅ Vérifier que Docker Desktop est démarré
- ✅ Créer le fichier `.env` si nécessaire
- ✅ Construire les images Docker
- ✅ Démarrer les conteneurs
- ✅ Appliquer les migrations de la base de données

4. **Accéder à l'application :**
   - 🌐 Frontend: http://localhost:3000
   - 🔧 Backend API: http://localhost:8000/api
   - 👤 Admin Django: http://localhost:8000/admin

### Méthode 2 : Commandes manuelles

```powershell
# 1. Aller dans le dossier du projet
cd "C:\Users\Mohamed\Desktop\skin twin ai\skin-twin-ai"

# 2. Créer le fichier .env (si pas déjà fait)
copy docker\env.example docker\.env

# 3. Construire les images Docker
docker-compose -f docker/docker-compose.yml build

# 4. Démarrer les conteneurs
docker-compose -f docker/docker-compose.yml up -d

# 5. Appliquer les migrations
docker exec -it skin_twin_backend python manage.py migrate

# 6. Vérifier les logs
docker-compose -f docker/docker-compose.yml logs -f
```

---

## 📤 Pour exporter le projet (vous)

1. **Ouvrir PowerShell dans le dossier `skin-twin-ai`**

2. **Exécuter le script d'export :**
```powershell
.\EXPORTER_DOCKER.ps1
```

3. **Le script va :**
   - Construire les images Docker
   - Sauvegarder les images dans `skin-twin-ai-images.tar`
   - Créer une archive ZIP avec tout le projet

4. **Partager l'archive ZIP avec vos camarades**

## 📥 Pour importer le projet (vos camarades)

1. **Extraire l'archive ZIP**

2. **Ouvrir PowerShell dans le dossier extrait**

3. **Exécuter le script d'import :**
```powershell
.\IMPORTER_DOCKER.ps1
```

4. **Le script va :**
   - Charger les images Docker
   - Créer le fichier `.env` si nécessaire
   - Démarrer les conteneurs

5. **Accéder à l'application :**
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000/api
   - Admin: http://localhost:8000/admin

## 🚀 Méthode manuelle (sans scripts)

### Export :
```powershell
# Construire les images
docker-compose -f docker/docker-compose.yml build

# Sauvegarder les images
docker save skin-twin-ai_backend:latest skin-twin-ai_frontend:latest -o skin-twin-ai-images.tar
```

### Import :
```powershell
# Charger les images
docker load -i skin-twin-ai-images.tar

# Démarrer
docker-compose -f docker/docker-compose.yml up -d
```

## 📋 Prérequis

- Docker Desktop installé et démarré
- PowerShell (sur Windows)

## 🛠️ Commandes utiles

```powershell
# Voir les logs
docker-compose -f docker/docker-compose.yml logs -f

# Arrêter
docker-compose -f docker/docker-compose.yml down

# Redémarrer
docker-compose -f docker/docker-compose.yml restart

# Créer un superutilisateur Django
docker exec -it skin_twin_backend python manage.py createsuperuser
```

## ⚙️ Configuration

Éditez `docker/.env` pour ajouter vos clés API :
- `GROQ_API_KEY` : Pour le chat AI
- `SECRET_KEY` : Clé secrète Django

## 📚 Documentation complète

Voir `DOCKER_EXPORT_GUIDE.md` pour plus de détails.

