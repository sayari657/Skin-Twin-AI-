# 📤 Guide pour Partager le Projet avec vos Amis

## 🎯 Méthode 1 : Partager le Code Source (Recommandé)

### Pour vous (exporter) :

1. **Créer une archive du projet** :
   - Clic droit sur le dossier `skin-twin-ai`
   - Sélectionnez "Envoyer vers" → "Dossier compressé"
   - Ou utilisez WinRAR/7-Zip pour créer une archive ZIP

2. **Exclure les fichiers inutiles** :
   - `node_modules/` (trop gros, sera réinstallé)
   - `venv/` (environnement virtuel local)
   - `backend/__pycache__/` (fichiers Python compilés)
   - `backend/db.sqlite3` (base de données locale)
   - `.git/` (si vous utilisez Git)

3. **Partager l'archive** :
   - Via Google Drive, Dropbox, WeTransfer, etc.
   - Ou via GitHub (si vous avez un compte)

### Pour vos amis (importer) :

1. **Télécharger et extraire l'archive**

2. **Ouvrir PowerShell** dans le dossier `skin-twin-ai`

3. **Exécuter** :
   ```powershell
   .\DEMARRER.bat
   ```

4. **Attendre** que Docker construise les images (10-20 minutes la première fois)

5. **Accéder à l'application** :
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000/api

---

## 🐳 Méthode 2 : Partager avec Docker (Images pré-construites)

### Pour vous (exporter) :

1. **Construire les images Docker** :
   ```powershell
   docker-compose -f docker/docker-compose.yml build
   ```

2. **Sauvegarder les images** :
   ```powershell
   docker save docker-backend docker-frontend -o skin-twin-ai-images.tar
   ```

3. **Créer une archive avec** :
   - Le code source (sans node_modules, venv, etc.)
   - Le fichier `skin-twin-ai-images.tar` (les images Docker)
   - Les instructions dans `INSTRUCTIONS_IMPORT.txt`

4. **Partager l'archive**

### Pour vos amis (importer) :

1. **Extraire l'archive**

2. **Charger les images Docker** :
   ```powershell
   docker load -i skin-twin-ai-images.tar
   ```

3. **Démarrer le projet** :
   ```powershell
   docker-compose -f docker/docker-compose.yml up -d
   ```

---

## 📋 Méthode 3 : Utiliser le Script d'Export Automatique

### Pour vous :

```powershell
.\EXPORTER_DOCKER.ps1
```

Ce script va créer :
- Une archive ZIP avec le projet
- Les images Docker sauvegardées
- Un fichier d'instructions

### Pour vos amis :

1. Extraire l'archive
2. Exécuter `.\IMPORTER_DOCKER.ps1`

---

## ✅ Checklist avant de Partager

- [ ] Le projet fonctionne sur votre machine
- [ ] Les images Docker sont construites
- [ ] Le fichier `.env` n'est PAS inclus (contient des secrets)
- [ ] Les gros dossiers sont exclus (`node_modules/`, `venv/`, etc.)
- [ ] Un fichier `README.md` avec les instructions est inclus

---

## 🔒 Sécurité - Fichiers à NE PAS Partager

- `docker/.env` (contient vos clés API)
- `backend/db.sqlite3` (base de données avec vos données)
- `backend/config_local.py` (configuration locale)
- Tout fichier contenant des mots de passe ou clés API

---

## 📝 Fichiers à Inclure

- ✅ Tout le code source (`backend/`, `frontend/`, `docker/`)
- ✅ `requirements.txt` et `package.json`
- ✅ Les fichiers Docker (`Dockerfile.*`, `docker-compose.yml`)
- ✅ Les scripts de démarrage (`DEMARRER.bat`, etc.)
- ✅ `README.md` et la documentation

---

## 🚀 Méthode Rapide (Recommandée)

1. **Créez une archive ZIP** du dossier `skin-twin-ai` (sans `node_modules/`, `venv/`, `.git/`)

2. **Partagez-la** via Google Drive, Dropbox, ou autre

3. **Vos amis** :
   - Téléchargent et extraient
   - Exécutent `.\DEMARRER.bat`
   - Attendent la construction Docker
   - Utilisent l'application !

---

## 💡 Astuce : Créer un Fichier .zipignore

Créez un fichier `.zipignore` (ou utilisez WinRAR/7-Zip avec exclusions) :

```
node_modules/
venv/
__pycache__/
*.pyc
.git/
.env
db.sqlite3
*.log
```

---

## 📞 Support

Si vos amis ont des problèmes :
1. Vérifiez qu'ils ont Docker Desktop installé
2. Vérifiez qu'ils sont dans le bon dossier
3. Vérifiez les logs : `docker logs skin_twin_backend`





