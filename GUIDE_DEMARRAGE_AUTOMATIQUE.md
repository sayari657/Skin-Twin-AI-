# 🚀 Guide de Démarrage Automatique - Skin Twin AI

## 🎯 Méthodes pour Démarrer Automatiquement

### Méthode 1 : Double-clic sur DEMARRER.bat ⭐ (La plus simple)

1. **Double-cliquez** sur le fichier `DEMARRER.bat` dans le dossier du projet
2. Le script démarre automatiquement tout le projet
3. C'est tout ! 🎉

**Avantages :**
- ✅ Simple : juste un double-clic
- ✅ Fonctionne même si PowerShell est bloqué
- ✅ Pas besoin de taper de commandes

---

### Méthode 2 : Raccourci sur le Bureau

1. **Exécutez** le script de création de raccourci :
   ```powershell
   .\CREER_RACCOURCI.ps1
   ```

2. Un raccourci **"Skin Twin AI - Démarrer"** sera créé sur votre Bureau

3. **Double-cliquez** sur le raccourci pour démarrer le projet

**Avantages :**
- ✅ Accès rapide depuis le Bureau
- ✅ Pas besoin d'ouvrir le dossier du projet
- ✅ Icône visible et facile à trouver

---

### Méthode 3 : Script PowerShell direct

1. **Clic droit** sur `DEMARRER_COMPLET.ps1`
2. Sélectionnez **"Exécuter avec PowerShell"**
3. Le projet démarre automatiquement

**Note :** Si vous avez une erreur de politique d'exécution, utilisez la Méthode 1 ou 2.

---

### Méthode 4 : Ajouter au Démarrage Windows (Avancé)

Pour démarrer automatiquement au démarrage de Windows :

1. **Appuyez sur** `Win + R`
2. Tapez `shell:startup` et appuyez sur Entrée
3. **Créez un raccourci** vers `DEMARRER.bat` dans ce dossier

**⚠️ Attention :** Cela démarrera le projet à chaque démarrage de Windows.

---

## 🛑 Arrêter le Projet

### Option 1 : Double-clic sur ARRETER.bat

Double-cliquez sur le fichier `ARRETER.bat` dans le dossier du projet.

### Option 2 : Raccourci sur le Bureau

Si vous avez créé le raccourci d'arrêt, double-cliquez dessus.

### Option 3 : Commande PowerShell

```powershell
docker-compose -f docker/docker-compose.yml down
```

---

## 📋 Résumé des Fichiers

| Fichier | Description | Usage |
|---------|-------------|-------|
| `DEMARRER.bat` | Script batch pour démarrer | Double-clic |
| `DEMARRER_COMPLET.ps1` | Script PowerShell complet | Exécution PowerShell |
| `ARRETER.bat` | Script batch pour arrêter | Double-clic |
| `CREER_RACCOURCI.ps1` | Crée des raccourcis sur le Bureau | Exécution PowerShell |

---

## 🎯 Recommandation

**Pour la plupart des utilisateurs :** Utilisez la **Méthode 1** (double-clic sur `DEMARRER.bat`)

C'est la méthode la plus simple et la plus fiable !

---

## 🔧 Dépannage

### Le fichier .bat ne s'ouvre pas

1. Clic droit sur `DEMARRER.bat`
2. Sélectionnez "Exécuter en tant qu'administrateur"

### Erreur de politique d'exécution PowerShell

1. Ouvrez PowerShell en tant qu'administrateur
2. Exécutez : `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`
3. Réessayez

### Docker Desktop n'est pas démarré

1. Ouvrez Docker Desktop manuellement
2. Attendez qu'il soit complètement démarré (icône dans la barre des tâches)
3. Relancez `DEMARRER.bat`

---

## 💡 Astuce

Créez un **raccourci** de `DEMARRER.bat` sur votre Bureau pour un accès encore plus rapide :

1. Clic droit sur `DEMARRER.bat`
2. Sélectionnez "Créer un raccourci"
3. Glissez le raccourci sur votre Bureau






