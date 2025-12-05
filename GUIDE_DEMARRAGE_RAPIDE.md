# 🚀 Guide de Démarrage Rapide - Docker Desktop

## ⚡ Démarrage en 3 étapes

### 1️⃣ Ouvrir Docker Desktop
- Assurez-vous que **Docker Desktop** est installé et **démarré**
- Vous devriez voir l'icône Docker dans la barre des tâches

### 2️⃣ Exécuter le script
Ouvrez **PowerShell** dans le dossier `skin-twin-ai` et exécutez :

```powershell
.\DEMARRER_DOCKER.ps1
```

### 3️⃣ Accéder à l'application
Une fois le script terminé, ouvrez votre navigateur :

- **Frontend** : http://localhost:3000
- **Backend API** : http://localhost:8000/api
- **Admin Django** : http://localhost:8000/admin

---

## 📋 Vérification

Pour vérifier que tout fonctionne :

```powershell
# Voir l'état des conteneurs
docker-compose -f docker/docker-compose.yml ps

# Voir les logs
docker-compose -f docker/docker-compose.yml logs -f
```

Vous devriez voir 2 conteneurs en cours d'exécution :
- `skin_twin_backend`
- `skin_twin_frontend`

---

## 🛑 Arrêter l'application

```powershell
docker-compose -f docker/docker-compose.yml down
```

---

## 🔄 Redémarrer l'application

```powershell
docker-compose -f docker/docker-compose.yml restart
```

---

## ⚙️ Configuration (Optionnel)

Si vous voulez utiliser le chat AI, éditez le fichier `docker\.env` et ajoutez votre clé API Groq :

```env
GROQ_API_KEY=votre-cle-api-ici
```

Puis redémarrez :
```powershell
docker-compose -f docker/docker-compose.yml restart
```

---

## ❓ Problèmes courants

### Docker Desktop n'est pas démarré
- Ouvrez Docker Desktop depuis le menu Démarrer
- Attendez que l'icône Docker apparaisse dans la barre des tâches

### Les ports 8000 ou 3000 sont déjà utilisés
Modifiez les ports dans `docker/docker-compose.yml` :
```yaml
ports:
  - "8001:8000"  # Au lieu de 8000:8000
  - "3001:3000"  # Au lieu de 3000:3000
```

### Erreur lors de la construction
```powershell
# Nettoyer et reconstruire
docker-compose -f docker/docker-compose.yml down
docker system prune -f
docker-compose -f docker/docker-compose.yml build --no-cache
```

---

## 📚 Documentation complète

Pour plus de détails, consultez :
- `GUIDE_DOCKER_ETAPES.md` - Guide étape par étape détaillé
- `README_DOCKER.md` - Guide Docker complet
- `docker/README.md` - Documentation technique Docker






