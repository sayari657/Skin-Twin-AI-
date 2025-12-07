# 🚀 Guide : Relancer le Workflow ML Monitoring

## ✅ Étape 1 : Commit et Push - TERMINÉ

Les changements ont été commités et pushés avec succès :
- Commit : `34c66b3`
- Branch : `main`
- Remote : `origin/main`

## 🔄 Étape 2 : Relancer le Workflow Manuellement

### Option A : Via l'interface GitHub (Recommandé)

1. **Aller sur GitHub** :
   - Ouvrez votre navigateur
   - Allez sur : https://github.com/sayari657/Skin-Twin-AI-

2. **Accéder aux Actions** :
   - Cliquez sur l'onglet **"Actions"** en haut du repository

3. **Sélectionner le workflow** :
   - Dans la liste à gauche, cliquez sur **"ML Monitoring"**

4. **Relancer manuellement** :
   - Cliquez sur le bouton **"Run workflow"** (en haut à droite)
   - Ou cliquez sur le dernier run qui a échoué
   - Cliquez sur **"Re-run jobs"** → **"Re-run failed jobs"**

### Option B : Via l'URL directe

Allez directement sur :
```
https://github.com/sayari657/Skin-Twin-AI-/actions/workflows/ml_monitoring.yml
```

Puis cliquez sur **"Run workflow"**.

## ⏱️ Étape 3 : Vérifier le Temps d'Exécution

### Ce qu'il faut surveiller :

1. **Temps d'installation des dépendances** :
   - Avant : 45-60 minutes
   - Attendu maintenant : **2-5 minutes** ⚡

2. **Temps total du workflow** :
   - Avant : 60+ minutes
   - Attendu maintenant : **5-10 minutes** ⚡

### Comment vérifier :

1. **Dans GitHub Actions** :
   - Cliquez sur le run en cours
   - Regardez le temps écoulé en haut à droite
   - Consultez chaque étape pour voir le temps pris

2. **Étapes à surveiller** :
   - ✅ `Install minimal dependencies` : devrait prendre 2-5 min (au lieu de 45-60 min)
   - ✅ `Run monitoring checks` : devrait prendre quelques secondes
   - ✅ Total : devrait être < 10 minutes

## 📊 Comparaison Avant/Après

| Étape | Avant | Après (Attendu) |
|-------|-------|-----------------|
| Installation dépendances | 45-60 min | 2-5 min |
| Setup MLOps | 5-10 min | 10-30 sec |
| Monitoring checks | 1-2 min | 10-30 sec |
| **TOTAL** | **60+ min** | **5-10 min** |

## 🔍 Vérifications à Faire

### ✅ Si le workflow réussit rapidement (< 10 min) :

1. Vérifier les logs pour confirmer :
   - Utilisation de `mlops_requirements_monitoring.txt`
   - Cache pip activé
   - Pas d'installation de PyTorch/Ultralytics

2. Vérifier les artefacts uploadés :
   - `.monitoring/` directory
   - `logs/mlops/` directory

### ⚠️ Si le workflow prend encore trop de temps :

1. Vérifier les logs de l'étape `Install minimal dependencies` :
   - Est-ce que `mlops_requirements_monitoring.txt` est utilisé ?
   - Y a-t-il des erreurs d'installation ?

2. Vérifier le cache :
   - Le cache pip est-il utilisé ?
   - Regardez dans les logs : "Cache restored from key: ..."

## 📝 Commandes Utiles pour Vérifier Localement

```bash
# Vérifier le temps d'installation localement
time pip install -r mlops_requirements_monitoring.txt

# Comparer avec l'ancien fichier (ne pas exécuter, juste voir la taille)
wc -l mlops_requirements.txt
wc -l mlops_requirements_monitoring.txt

# Tester le script de monitoring
time python mlops/scripts/run_monitoring.py
```

## 🎯 Résultat Attendu

Le workflow devrait maintenant :
- ✅ S'exécuter en **5-10 minutes** (au lieu de 60+ minutes)
- ✅ Installer seulement **~50-100 MB** de dépendances (au lieu de 4-5 GB)
- ✅ Utiliser le **cache pip** pour les runs suivants
- ✅ Avoir un **timeout de 10 minutes** pour éviter les runs bloqués

## 📞 En Cas de Problème

Si le workflow prend encore trop de temps :

1. Vérifier les logs GitHub Actions
2. Consulter `DEBUG_MONITORING.md` pour le débogage
3. Vérifier que `mlops_requirements_monitoring.txt` est bien utilisé
4. Vérifier que le cache pip fonctionne

---

**Prochaine étape** : Allez sur GitHub et relancez le workflow manuellement ! 🚀

