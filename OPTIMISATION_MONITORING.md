# ⚡ Optimisation du Workflow ML Monitoring

## Problème identifié

Le workflow prenait **plus d'1 heure** à cause de l'installation de dépendances très lourdes :
- **PyTorch** (~2-3 GB) : `torch>=2.0.0`, `torchvision>=0.15.0`
- **Ultralytics YOLO** (~500 MB) : `ultralytics>=8.0.0`
- **DVC avec S3** (~200 MB) : `dvc[s3]>=3.0.0`
- **Evidently/Whylogs** (~300 MB) : outils de monitoring lourds
- **Great Expectations** (~400 MB) : validation de données

**Total estimé : ~4-5 GB de téléchargements** pour un simple monitoring qui ne fait que vérifier des fichiers JSON !

## Solution implémentée

### 1. Fichier de dépendances minimales

Création de `mlops_requirements_monitoring.txt` avec **seulement** les dépendances nécessaires :
- MLflow (léger, sans extras)
- scipy, scikit-learn, numpy, pandas (bibliothèques de base)
- pyyaml, python-dotenv, joblib (utilitaires)

**Réduction : ~4-5 GB → ~50-100 MB** 🎉

### 2. Cache GitHub Actions

- Cache pip activé pour réutiliser les packages entre les runs
- Cache basé sur le hash du fichier requirements
- **Gain : 80-90% de temps en moins** sur les runs suivants

### 3. Timeout configuré

- Timeout de 10 minutes pour éviter les runs qui traînent
- Le workflow échouera rapidement si quelque chose bloque

### 4. Script optimisé

- Le script `run_monitoring.py` ne charge plus les modèles ML
- Vérifie seulement les fichiers de monitoring existants
- Pas d'imports lourds (PyTorch, Ultralytics, etc.)

## Résultats attendus

| Métrique | Avant | Après | Amélioration |
|----------|-------|-------|--------------|
| Temps d'installation | 45-60 min | 2-5 min | **90% plus rapide** |
| Taille téléchargée | ~4-5 GB | ~50-100 MB | **98% plus léger** |
| Temps total workflow | 60+ min | 5-10 min | **85% plus rapide** |

## Utilisation

Le workflow utilise maintenant automatiquement `mlops_requirements_monitoring.txt` au lieu de `mlops_requirements.txt`.

Pour le training complet, utilisez toujours `mlops_requirements.txt` localement.

## Vérification

Pour tester localement :

```bash
# Installer les dépendances minimales
pip install -r mlops_requirements_monitoring.txt

# Exécuter le monitoring
python mlops/scripts/run_monitoring.py

# Devrait prendre quelques secondes, pas des heures !
```

## Notes importantes

- Les modèles ML ne sont **pas** nécessaires pour le monitoring GitHub Actions
- Le monitoring vérifie seulement :
  - Existence des fichiers de monitoring
  - Présence d'alertes récentes
  - Configuration MLflow (sans charger les modèles)
- Pour le training réel, utilisez `mlops_requirements.txt` complet

