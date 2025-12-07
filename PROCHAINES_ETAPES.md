# 🚀 Prochaines Étapes - Correction du Workflow ML Monitoring

## ✅ Fichiers modifiés/créés

Les fichiers suivants ont été créés ou modifiés pour corriger le problème du workflow :

1. **`mlops/scripts/run_monitoring.py`** (NOUVEAU)
   - Script exécutable pour le monitoring
   - Vérifie la santé du système MLOps
   - Détecte les alertes

2. **`.github/workflows/ml_monitoring.yml`** (MODIFIÉ)
   - Ajout d'étapes de débogage
   - Configuration de PYTHONPATH
   - Gestion d'erreurs améliorée

3. **`mlops/scripts/setup_mlops.py`** (MODIFIÉ)
   - Gestion d'erreurs améliorée
   - Continue même si certains modules manquent

4. **`DEBUG_MONITORING.md`** (NOUVEAU)
   - Guide complet de débogage

## 📋 Étapes à suivre

### Étape 1 : Vérifier les fichiers localement

```bash
# Aller dans le répertoire du projet
cd skin-twin-ai

# Vérifier que les nouveaux fichiers existent
ls mlops/scripts/run_monitoring.py
ls .github/workflows/ml_monitoring.yml
ls DEBUG_MONITORING.md
```

### Étape 2 : Tester le script localement (optionnel mais recommandé)

```bash
# Installer les dépendances si nécessaire
pip install -r mlops_requirements.txt

# Tester le script de monitoring
python mlops/scripts/run_monitoring.py

# Vérifier le code de sortie (0 = succès)
echo $?  # Sur Linux/Mac
# ou
$LASTEXITCODE  # Sur PowerShell Windows
```

### Étape 3 : Commit et Push vers GitHub

```bash
# Vérifier les fichiers modifiés
git status

# Ajouter les fichiers modifiés
git add mlops/scripts/run_monitoring.py
git add .github/workflows/ml_monitoring.yml
git add mlops/scripts/setup_mlops.py
git add DEBUG_MONITORING.md
git add PROCHAINES_ETAPES.md

# Faire un commit
git commit -m "fix: Corriger le workflow ML Monitoring avec script exécutable et étapes de débogage"

# Push vers GitHub
git push origin main
# ou
git push origin master  # selon votre branche principale
```

### Étape 4 : Relancer le workflow sur GitHub

**Option A : Via l'interface GitHub**

1. Allez sur votre repository GitHub
2. Cliquez sur l'onglet **"Actions"**
3. Sélectionnez le workflow **"ML Monitoring"** dans la liste de gauche
4. Cliquez sur le dernier run qui a échoué
5. Cliquez sur le bouton **"Re-run jobs"** (en haut à droite)
6. Sélectionnez **"Re-run all jobs"**

**Option B : Via workflow_dispatch**

1. Allez sur l'onglet **"Actions"**
2. Sélectionnez **"ML Monitoring"**
3. Cliquez sur **"Run workflow"** (bouton en haut à droite)
4. Sélectionnez la branche (main/master)
5. Cliquez sur **"Run workflow"**

### Étape 5 : Consulter les logs

Une fois le workflow relancé :

1. Cliquez sur le nouveau run
2. Cliquez sur le job **"monitor-models"**
3. Consultez chaque étape :
   - ✅ **"Debug - Show Python version and paths"** : Vérifie l'environnement
   - ✅ **"Debug - Verify imports"** : Vérifie que les modules peuvent être importés
   - ✅ **"Initialize MLOps"** : Initialise l'environnement MLOps
   - ✅ **"Run monitoring checks"** : Exécute les vérifications de monitoring

### Étape 6 : Analyser les résultats

**Si le workflow réussit ✅ :**
- Vous verrez un checkmark vert
- Les artefacts seront uploadés dans l'onglet "Artifacts"
- Le monitoring fonctionne correctement

**Si le workflow échoue ❌ :**
- Consultez les logs de l'étape qui a échoué
- Les nouvelles étapes de débogage vous donneront plus d'informations
- Consultez `DEBUG_MONITORING.md` pour les solutions

## 🔍 Points à vérifier dans les logs

### Dans "Debug - Show Python version and paths"
- Version Python : devrait être 3.10.x
- Répertoire de travail : devrait être `/home/runner/work/[repo]/[repo]`
- PYTHONPATH : devrait être défini

### Dans "Debug - Verify imports"
- MLflow version : devrait s'afficher si installé
- ModelMonitor import : devrait réussir

### Dans "Run monitoring checks"
- Les messages de log devraient s'afficher
- Le code de sortie devrait être 0 (succès)

## 🐛 En cas de problème

Si le workflow échoue encore :

1. **Consultez les logs détaillés** de l'étape qui échoue
2. **Vérifiez les erreurs** dans les messages
3. **Consultez `DEBUG_MONITORING.md`** pour les solutions courantes
4. **Testez localement** avec les mêmes commandes que dans le workflow

## 📝 Commandes PowerShell (Windows)

Si vous êtes sur Windows PowerShell :

```powershell
# Aller dans le répertoire
cd "skin-twin-ai"

# Vérifier git status
git status

# Ajouter les fichiers
git add mlops/scripts/run_monitoring.py
git add .github/workflows/ml_monitoring.yml
git add mlops/scripts/setup_mlops.py
git add DEBUG_MONITORING.md
git add PROCHAINES_ETAPES.md

# Commit
git commit -m "fix: Corriger le workflow ML Monitoring"

# Push
git push origin main
```

## ✅ Checklist

- [ ] Les fichiers modifiés sont présents
- [ ] Le script `run_monitoring.py` fonctionne localement (optionnel)
- [ ] Les fichiers sont commités
- [ ] Les fichiers sont pushés vers GitHub
- [ ] Le workflow est relancé sur GitHub
- [ ] Les logs sont consultés
- [ ] Le workflow réussit ou les erreurs sont identifiées

## 🎯 Résultat attendu

Après ces étapes, le workflow **ML Monitoring** devrait :
- ✅ S'exécuter sans erreur
- ✅ Afficher des logs détaillés pour le débogage
- ✅ Uploader les artefacts de monitoring
- ✅ Fonctionner automatiquement toutes les 6 heures

---

**Note** : Si vous avez des questions ou rencontrez des problèmes, consultez `DEBUG_MONITORING.md` pour plus de détails.

