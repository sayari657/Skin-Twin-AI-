# 🐳 Commandes Docker Complètes - Skin Twin AI

## 🚀 DÉMARRAGE COMPLET (Première fois)

### Étape 1 : Aller dans le dossier du projet
```powershell
cd "C:\Users\Mohamed\Desktop\skin twin ai\skin-twin-ai"
```

### Étape 2 : Créer le fichier .env
```powershell
copy docker\env.example docker\.env
```

### Étape 3 : Construire les images Docker
```powershell
docker-compose -f docker/docker-compose.yml build
```

### Étape 4 : Démarrer les conteneurs
```powershell
docker-compose -f docker/docker-compose.yml up -d
```

### Étape 5 : Appliquer les migrations
```powershell
docker exec -it skin_twin_backend python manage.py migrate
```

### Étape 6 : Vérifier que tout fonctionne
```powershell
docker-compose -f docker/docker-compose.yml ps
```

---

## 📋 COMMANDES DE VÉRIFICATION

### Voir l'état des conteneurs
```powershell
docker-compose -f docker/docker-compose.yml ps
```

### Voir les logs en temps réel
```powershell
docker-compose -f docker/docker-compose.yml logs -f
```

### Voir les logs du backend uniquement
```powershell
docker-compose -f docker/docker-compose.yml logs -f backend
```

### Voir les logs du frontend uniquement
```powershell
docker-compose -f docker/docker-compose.yml logs -f frontend
```

### Voir les images Docker
```powershell
docker images
```

### Voir tous les conteneurs (y compris arrêtés)
```powershell
docker ps -a
```

### Voir l'utilisation des ressources
```powershell
docker stats
```

---

## 🛑 COMMANDES D'ARRÊT

### Arrêter les conteneurs
```powershell
docker-compose -f docker/docker-compose.yml down
```

### Arrêter les conteneurs (sans supprimer les volumes)
```powershell
docker-compose -f docker/docker-compose.yml stop
```

### Arrêter un conteneur spécifique
```powershell
docker stop skin_twin_backend
docker stop skin_twin_frontend
```

---

## 🔄 COMMANDES DE REDÉMARRAGE

### Redémarrer tous les conteneurs
```powershell
docker-compose -f docker/docker-compose.yml restart
```

### Redémarrer un conteneur spécifique
```powershell
docker restart skin_twin_backend
docker restart skin_twin_frontend
```

### Redémarrer après modification du code
```powershell
docker-compose -f docker/docker-compose.yml down
docker-compose -f docker/docker-compose.yml up -d --build
```

---

## 🔨 COMMANDES DE RECONSTRUCTION

### Reconstruire les images (après modification du code)
```powershell
docker-compose -f docker/docker-compose.yml build --no-cache
docker-compose -f docker/docker-compose.yml up -d
```

### Reconstruire un service spécifique
```powershell
docker-compose -f docker/docker-compose.yml build --no-cache backend
docker-compose -f docker/docker-compose.yml up -d backend
```

### Reconstruire avec logs détaillés
```powershell
docker-compose -f docker/docker-compose.yml build --progress=plain
```

---

## 🗄️ COMMANDES BASE DE DONNÉES

### Appliquer les migrations
```powershell
docker exec -it skin_twin_backend python manage.py migrate
```

### Créer un superutilisateur Django
```powershell
docker exec -it skin_twin_backend python manage.py createsuperuser
```

### Accéder au shell Django
```powershell
docker exec -it skin_twin_backend python manage.py shell
```

### Créer les migrations (si vous modifiez les models)
```powershell
docker exec -it skin_twin_backend python manage.py makemigrations
docker exec -it skin_twin_backend python manage.py migrate
```

---

## 🐚 COMMANDES SHELL

### Accéder au shell du backend
```powershell
docker exec -it skin_twin_backend bash
```

### Accéder au shell du frontend
```powershell
docker exec -it skin_twin_frontend sh
```

---

## 🧹 COMMANDES DE NETTOYAGE

### Arrêter et supprimer les conteneurs
```powershell
docker-compose -f docker/docker-compose.yml down
```

### Arrêter, supprimer les conteneurs ET les volumes
```powershell
docker-compose -f docker/docker-compose.yml down -v
```

### Supprimer les images Docker
```powershell
docker rmi skin-twin-ai_backend skin-twin-ai_frontend
```

### Nettoyer tout Docker (attention : supprime tout)
```powershell
docker system prune -a
```

### Nettoyer seulement les conteneurs arrêtés
```powershell
docker container prune
```

---

## 🔍 COMMANDES DE DÉPANNAGE

### Voir les logs d'erreur complets
```powershell
docker-compose -f docker/docker-compose.yml logs --tail=100
```

### Vérifier les ports utilisés (Windows)
```powershell
netstat -ano | findstr :8000
netstat -ano | findstr :3000
```

### Vérifier la configuration Docker Compose
```powershell
docker-compose -f docker/docker-compose.yml config
```

### Tester la connexion au backend
```powershell
curl http://localhost:8000/api
```

### Inspecter un conteneur
```powershell
docker inspect skin_twin_backend
```

---

## 📦 COMMANDES D'EXPORT/IMPORT

### Sauvegarder les images Docker
```powershell
docker save skin-twin-ai_backend:latest skin-twin-ai_frontend:latest -o skin-twin-ai-images.tar
```

### Charger les images Docker
```powershell
docker load -i skin-twin-ai-images.tar
```

---

## 🎯 COMMANDE TOUT-EN-UN (Script)

### Démarrer complètement le projet
```powershell
cd "C:\Users\Mohamed\Desktop\skin twin ai\skin-twin-ai"; copy docker\env.example docker\.env -ErrorAction SilentlyContinue; docker-compose -f docker/docker-compose.yml build; docker-compose -f docker/docker-compose.yml up -d; Start-Sleep -Seconds 10; docker exec -it skin_twin_backend python manage.py migrate --noinput; docker-compose -f docker/docker-compose.yml ps
```

### Arrêter complètement le projet
```powershell
cd "C:\Users\Mohamed\Desktop\skin twin ai\skin-twin-ai"; docker-compose -f docker/docker-compose.yml down
```

### Redémarrer complètement le projet
```powershell
cd "C:\Users\Mohamed\Desktop\skin twin ai\skin-twin-ai"; docker-compose -f docker/docker-compose.yml restart; docker exec -it skin_twin_backend python manage.py migrate --noinput
```

---

## 🌐 ACCÈS À L'APPLICATION

Une fois démarré, accédez à :
- **Frontend** : http://localhost:3000
- **Backend API** : http://localhost:8000/api
- **Admin Django** : http://localhost:8000/admin

---

## ⚡ COMMANDES RAPIDES (Les plus utilisées)

```powershell
# Démarrer
docker-compose -f docker/docker-compose.yml up -d

# Voir les logs
docker-compose -f docker/docker-compose.yml logs -f

# Arrêter
docker-compose -f docker/docker-compose.yml down

# Redémarrer
docker-compose -f docker/docker-compose.yml restart

# État
docker-compose -f docker/docker-compose.yml ps
```

---

## 📝 Notes

- Remplacez `docker-compose` par `docker compose` (sans tiret) si vous utilisez Docker Compose V2
- Toutes les commandes doivent être exécutées depuis le dossier `skin-twin-ai`
- Utilisez `Ctrl+C` pour quitter les logs en temps réel


