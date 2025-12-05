# 🧹 Guide de Nettoyage - Skin Twin AI

## 📋 Deux Types de Nettoyage

### 1. Nettoyage Léger (Recommandé)

**Script :** `NETTOYER_FICHIERS_INUTILES.bat`

**Supprime :**
- ✅ Archives ZIP de partage (déjà créées)
- ✅ Dossiers temporaires (temp_export_*)
- ✅ Fichiers temporaires (*.tmp, *.temp)
- ✅ Fichiers de cache (.cache/)

**Conserve :**
- ✅ Code source complet
- ✅ Modèles ML
- ✅ Dépendances (node_modules, venv)
- ✅ Configuration Docker

**Quand utiliser :** Après avoir créé et partagé vos archives

---

### 2. Nettoyage Complet

**Script :** `NETTOYER_COMPLET.bat`

**Supprime :**
- ✅ node_modules/ (~500 MB)
- ✅ venv/ (~500 MB)
- ✅ __pycache__/ (fichiers Python compilés)
- ✅ Archives ZIP
- ✅ Fichiers temporaires

**Conserve :**
- ✅ Code source
- ✅ Modèles ML
- ✅ Configuration Docker

**Quand utiliser :** 
- Si vous manquez d'espace disque
- Si vous ne modifiez plus le code localement
- Docker fonctionnera toujours (utilise ses propres dépendances)

**⚠️ Attention :** Après ce nettoyage, vous devrez réinstaller les dépendances si vous modifiez le code localement.

---

## 🎯 Recommandation

**Après avoir partagé votre projet :**

1. Utilisez `NETTOYER_FICHIERS_INUTILES.bat` pour supprimer les archives et fichiers temporaires
2. Gardez les dépendances (node_modules, venv) si vous continuez à développer
3. Utilisez `NETTOYER_COMPLET.bat` seulement si vous manquez d'espace disque

---

## 💾 Espace Libéré

- **Nettoyage léger :** ~100-500 MB (archives + temporaires)
- **Nettoyage complet :** ~1-2 GB (dépendances incluses)

---

## 🔄 Réinstallation des Dépendances (si nécessaire)

### Frontend :
```powershell
cd frontend
npm install
```

### Backend :
```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## ✅ Checklist de Nettoyage

Avant de nettoyer, assurez-vous :
- [ ] Vous avez créé et sauvegardé vos archives de partage
- [ ] Vous avez sauvegardé vos modifications importantes
- [ ] Docker fonctionne correctement
- [ ] Vous n'avez pas besoin des dépendances locales immédiatement

---

## 🚀 Résumé Rapide

**Pour nettoyer après partage :**
```batch
.\NETTOYER_FICHIERS_INUTILES.bat
```

**Pour nettoyer complètement (libérer de l'espace) :**
```batch
.\NETTOYER_COMPLET.bat
```





