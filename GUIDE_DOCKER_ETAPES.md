# 🐳 Guide Étape par Étape - Mettre le Projet dans Docker

## 📋 Prérequis

Avant de commencer, assurez-vous d'avoir :
- ✅ Docker Desktop installé et démarré
- ✅ PowerShell ou Terminal ouvert
- ✅ Le projet `skin-twin-ai` disponible

---

## 🚀 ÉTAPE 1 : Vérifier Docker Desktop

1. **Ouvrir Docker Desktop**
2. **Vérifier que Docker fonctionne :**
```powershell
docker --version
docker ps
```
Si vous voyez la version et une liste (même vide), Docker fonctionne ✅

---

## 🚀 ÉTAPE 2 : Préparer la Configuration

1. **Aller dans le dossier du projet :**
```powershell
cd "C:\Users\Mohamed\Desktop\skin twin ai\skin-twin-ai"
```

2. **Vérifier que les fichiers Docker existent :**
```powershell
# Vérifier les fichiers
dir docker\docker-compose.yml
dir docker\Dockerfile.backend
dir docker\Dockerfile.frontend
```

3. **Créer le fichier .env (si pas déjà créé) :**
```powershell
# Copier le fichier exemple
copy docker\env.example docker\.env

# Éditer le fichier .env avec Notepad ou votre éditeur préféré
notepad docker\.env
```

**Contenu recommandé pour `.env` :**
```env
DEBUG=1
SECRET_KEY=django-insecure-changez-moi-en-production-avec-une-cle-secrete
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,backend
GROQ_API_KEY=votre-cle-groq-api-ici
GROQ_MODEL=llama-3.1-8b-instant
REACT_APP_API_URL=http://localhost:8000/api
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

---

## 🚀 ÉTAPE 3 : Construire les Images Docker

1. **Construire les images (cela peut prendre 5-10 minutes) :**
```powershell
docker-compose -f docker/docker-compose.yml build
```

**Ce qui se passe :**
- Le backend Django est construit avec Python 3.11
- Le frontend React est construit avec Node.js 20
- Les dépendances sont installées

**⚠️ Si vous avez des erreurs :**
- Vérifiez que Docker Desktop est bien démarré
- Vérifiez votre connexion Internet (pour télécharger les images de base)
- Vérifiez que les ports 8000 et 3000 ne sont pas déjà utilisés

---

## 🚀 ÉTAPE 4 : Démarrer les Conteneurs

1. **Démarrer les services en arrière-plan :**
```powershell
docker-compose -f docker/docker-compose.yml up -d
```

**Ce qui se passe :**
- Le backend Django démarre sur le port 8000
- Le frontend React démarre sur le port 3000
- Les conteneurs sont créés et démarrés

2. **Vérifier que les conteneurs sont en cours d'exécution :**
```powershell
docker ps
```

Vous devriez voir deux conteneurs :
- `skin_twin_backend`
- `skin_twin_frontend`

---

## 🚀 ÉTAPE 5 : Vérifier les Logs

1. **Voir les logs du backend :**
```powershell
docker-compose -f docker/docker-compose.yml logs backend
```

2. **Voir les logs du frontend :**
```powershell
docker-compose -f docker/docker-compose.yml logs frontend
```

3. **Voir tous les logs en temps réel :**
```powershell
docker-compose -f docker/docker-compose.yml logs -f
```

**Appuyez sur `Ctrl+C` pour quitter les logs**

---

## 🚀 ÉTAPE 6 : Initialiser la Base de Données

1. **Appliquer les migrations Django :**
```powershell
docker exec -it skin_twin_backend python manage.py migrate
```

2. **Créer un superutilisateur (optionnel) :**
```powershell
docker exec -it skin_twin_backend python manage.py createsuperuser
```

Suivez les instructions pour créer un compte admin.

---

## 🚀 ÉTAPE 7 : Accéder à l'Application

Une fois tout démarré, accédez à :

- 🌐 **Frontend** : http://localhost:3000
- 🔧 **Backend API** : http://localhost:8000/api
- 👤 **Admin Django** : http://localhost:8000/admin

---

## 🛠️ Commandes Utiles

### Voir l'état des conteneurs :
```powershell
docker-compose -f docker/docker-compose.yml ps
```

### Arrêter les conteneurs :
```powershell
docker-compose -f docker/docker-compose.yml down
```

### Redémarrer les conteneurs :
```powershell
docker-compose -f docker/docker-compose.yml restart
```

### Reconstruire les images (après modification du code) :
```powershell
docker-compose -f docker/docker-compose.yml build --no-cache
docker-compose -f docker/docker-compose.yml up -d
```

### Accéder au shell du backend :
```powershell
docker exec -it skin_twin_backend bash
```

### Accéder au shell du frontend :
```powershell
docker exec -it skin_twin_frontend sh
```

### Voir l'utilisation des ressources :
```powershell
docker stats
```

---

## 🐛 Dépannage

### Les conteneurs ne démarrent pas :

1. **Vérifier les logs d'erreur :**
```powershell
docker-compose -f docker/docker-compose.yml logs
```

2. **Vérifier que les ports ne sont pas utilisés :**
```powershell
# Windows PowerShell
netstat -ano | findstr :8000
netstat -ano | findstr :3000
```

3. **Arrêter et redémarrer :**
```powershell
docker-compose -f docker/docker-compose.yml down
docker-compose -f docker/docker-compose.yml up -d
```

### Erreur "port already in use" :

Si le port 8000 ou 3000 est déjà utilisé :

1. **Modifier le port dans `docker-compose.yml` :**
```yaml
ports:
  - "8001:8000"  # Au lieu de 8000:8000
  - "3001:3000"  # Au lieu de 3000:3000
```

2. **Redémarrer :**
```powershell
docker-compose -f docker/docker-compose.yml up -d
```

### Erreur lors de la construction :

1. **Nettoyer et reconstruire :**
```powershell
docker-compose -f docker/docker-compose.yml down
docker system prune -f
docker-compose -f docker/docker-compose.yml build --no-cache
```

### Le backend ne répond pas :

1. **Vérifier que les migrations sont appliquées :**
```powershell
docker exec -it skin_twin_backend python manage.py migrate
```

2. **Vérifier les logs :**
```powershell
docker logs skin_twin_backend
```

---

## 📦 Exporter le Projet pour le Partager

Une fois que tout fonctionne, vous pouvez exporter le projet :

1. **Utiliser le script d'export :**
```powershell
.\EXPORTER_DOCKER.ps1
```

2. **Ou manuellement :**
```powershell
# Sauvegarder les images
docker save skin-twin-ai_backend:latest skin-twin-ai_frontend:latest -o skin-twin-ai-images.tar

# Créer une archive du projet
# (utiliser WinRAR, 7-Zip, ou PowerShell Compress-Archive)
```

---

## ✅ Checklist de Vérification

Avant de considérer que tout est prêt :

- [ ] Docker Desktop est démarré
- [ ] Les images sont construites (`docker images` montre les images)
- [ ] Les conteneurs sont en cours d'exécution (`docker ps` montre 2 conteneurs)
- [ ] Le frontend répond sur http://localhost:3000
- [ ] Le backend répond sur http://localhost:8000/api
- [ ] Les migrations sont appliquées
- [ ] Les logs ne montrent pas d'erreurs critiques

---

## 🎯 Résumé Rapide

```powershell
# 1. Aller dans le dossier du projet
cd "C:\Users\Mohamed\Desktop\skin twin ai\skin-twin-ai"

# 2. Construire les images
docker-compose -f docker/docker-compose.yml build

# 3. Démarrer les conteneurs
docker-compose -f docker/docker-compose.yml up -d

# 4. Appliquer les migrations
docker exec -it skin_twin_backend python manage.py migrate

# 5. Accéder à l'application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000/api
```

---

## 📚 Documentation Complète

Pour plus de détails, consultez :
- `DOCKER_EXPORT_GUIDE.md` - Guide d'export/import
- `README_DOCKER.md` - Guide rapide
- `docker/README.md` - Documentation Docker

---

**🎉 Félicitations ! Votre projet est maintenant dans Docker !**






