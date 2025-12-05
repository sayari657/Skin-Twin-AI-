# 📤 Comment Partager le Projet avec vos Amis

## ✅ Oui, vos amis peuvent voir TOUT le code !

## 🚀 Méthode Simple (Recommandée)

### Pour vous (créer l'archive) :

1. **Clic droit** sur le dossier `skin-twin-ai`
2. Sélectionnez **"Envoyer vers"** → **"Dossier compressé"**
3. Attendez que l'archive ZIP soit créée
4. **Partagez** le fichier ZIP avec vos amis (Google Drive, Dropbox, WeTransfer, etc.)

### Pour vos amis (utiliser le projet) :

1. **Télécharger** et **extraire** l'archive ZIP
2. **Ouvrir PowerShell** dans le dossier `skin-twin-ai`
3. **Exécuter** :
   ```powershell
   .\DEMARRER.bat
   ```
4. **Attendre** 10-20 minutes (première fois)
5. **Accéder** à :
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000/api

---

## 📦 Ce qui sera inclus dans l'archive

✅ **Code source complet** (backend/, frontend/, docker/)
✅ **Modèles ML** (ml_models/)
✅ **Dépendances** (node_modules/, venv/)
✅ **Configuration Docker** (Dockerfile, docker-compose.yml)
✅ **Scripts de démarrage** (DEMARRER.bat, ARRETER.bat)
✅ **Documentation** (README.md, guides)

---

## 🔒 Fichiers à NE PAS partager (optionnel)

Si vous voulez protéger certaines informations :

- `docker/.env` (contient vos clés API Groq)
- `backend/db.sqlite3` (contient vos données)
- `backend/config_local.py` (configuration locale)

**Note :** Ces fichiers ne sont pas essentiels pour que vos amis utilisent le projet.

---

## 💡 Astuce : Taille de l'archive

L'archive sera **grosse** (plusieurs GB) car elle inclut :
- `node_modules/` (~500 MB)
- `venv/` (~500 MB)
- Modèles ML (plusieurs GB)

**Solutions pour réduire la taille :**
- Utilisez Google Drive (limite 15 GB)
- Partagez via plusieurs fichiers
- Utilisez Git/GitHub (meilleure solution pour le code)

---

## 🎯 Résumé Rapide

1. **Créez une archive ZIP** du dossier `skin-twin-ai`
2. **Partagez-la** avec vos amis
3. **Vos amis** extraient et exécutent `DEMARRER.bat`
4. **C'est tout !** 🎉

---

## 📝 Instructions pour vos amis

Envoyez ce message à vos amis :

```
Bonjour !

Voici le projet Skin Twin AI :

1. Téléchargez et extrayez l'archive ZIP
2. Ouvrez PowerShell dans le dossier skin-twin-ai
3. Exécutez: .\DEMARRER.bat
4. Attendez 10-20 minutes (première fois)
5. Ouvrez http://localhost:3000 dans votre navigateur

Prérequis: Docker Desktop doit être installé et démarré.

Bon développement ! 🚀
```





