# 🚀 Guide de Setup MLOps pour Skin-Twin-AI

## 📋 Vue d'ensemble

L'architecture MLOps complète a été créée pour votre projet Skin-Twin-AI. Elle inclut :

- ✅ **Model Registry** avec MLflow
- ✅ **Monitoring en production**
- ✅ **Pipelines de training automatisés**
- ✅ **Détection de dérive des données**
- ✅ **Intégration Django**
- ✅ **CI/CD avec GitHub Actions**
- ✅ **Versioning des données avec DVC**

## 📁 Structure créée

```
skin-twin-ai/
├── mlops/
│   ├── config/              # Configuration (MLflow, modèles, training)
│   ├── data/               # Gestion des données
│   ├── training/           # Modules de training
│   ├── evaluation/         # Évaluation des modèles
│   ├── deployment/         # Déploiement et registry
│   ├── monitoring/         # Monitoring en production
│   ├── pipelines/          # Pipelines ML
│   ├── utils/              # Utilitaires
│   ├── integration/        # Intégration Django
│   ├── scripts/            # Scripts de setup
│   └── tests/              # Tests MLOps
├── mlops_requirements.txt   # Dépendances MLOps
├── dvc.yaml                # Configuration DVC
└── .github/workflows/       # CI/CD GitHub Actions
```

## 🔧 Installation

### 1. Installer les dépendances MLOps

```bash
cd skin-twin-ai
pip install -r mlops_requirements.txt
```

### 2. Initialiser l'environnement MLOps

```bash
python mlops/scripts/setup_mlops.py
```

Cette commande va :
- Créer les répertoires nécessaires (`.mlflow`, `.monitoring`, `logs/mlops`)
- Configurer MLflow avec l'expérience `skin-twin-ai`
- Vérifier la présence des modèles

### 3. Vérifier l'intégration Django

L'intégration MLOps est déjà configurée dans :
- `backend/detection/views.py` : Logging automatique des prédictions
- `backend/detection/mlops_views.py` : Endpoints MLOps
- `backend/detection/urls.py` : Routes MLOps ajoutées

## 📊 Utilisation

### Enregistrer un modèle dans MLflow

```python
from mlops.deployment.model_registry import ModelRegistry

registry = ModelRegistry()
registry.register_yolo_model(
    model_path='ml_models/model skin/models/modéle skinTwin2 .pt',
    metrics={'mAP': 0.85, 'precision': 0.82},
    tags={'version': '1.0'}
)
```

### Monitoring en production

Le monitoring est automatique ! Chaque prédiction est loggée via `mlops_integration` dans `views.py`.

Pour vérifier la santé du système :

```bash
curl http://localhost:8000/api/detection/mlops/health/
```

Pour obtenir les statistiques :

```bash
curl http://localhost:8000/api/detection/mlops/stats/
```

### Pipeline de training

```python
from mlops.pipelines.training_pipeline import TrainingPipeline

pipeline = TrainingPipeline()
results = pipeline.run_full_pipeline(data_path='data/processed')
```

## 🔍 Monitoring

Les métriques sont sauvegardées dans :
- `.monitoring/predictions_history.json` : Historique des prédictions
- `.monitoring/performance_metrics.json` : Métriques de performance
- `.monitoring/alerts/` : Alertes de dérive et erreurs

## 🔄 CI/CD

Les workflows GitHub Actions sont configurés dans `.github/workflows/` :
- `ml_training.yml` : Training automatique (dimanche à 2h)
- `ml_monitoring.yml` : Monitoring périodique (toutes les 6h)

## 📝 Configuration

### MLflow

Modifier `mlops/config/mlflow_config.py` pour :
- Changer l'URI de tracking MLflow
- Modifier le nom de l'expérience
- Ajuster les chemins des modèles

### Monitoring

Modifier `mlops/config/mlflow_config.py` → `MONITORING_CONFIG` pour :
- Ajuster le seuil de dérive
- Configurer les alertes email
- Modifier l'intervalle de vérification

## 🧪 Tests

```bash
pytest mlops/tests/
```

## 📚 Documentation

Voir `mlops/README.md` pour plus de détails.

## ⚠️ Notes importantes

1. **MLOps est optionnel** : Le système fonctionne même si MLOps n'est pas installé (grace aux imports optionnels)

2. **Premier démarrage** : Exécutez `python mlops/scripts/setup_mlops.py` avant d'utiliser MLOps

3. **MLflow UI** : Pour visualiser les expériences :
   ```bash
   mlflow ui --backend-store-uri file:./.mlflow
   ```
   Puis ouvrir http://localhost:5000

4. **Production** : Pour utiliser le Model Registry en production, configurez `MLFLOW_TRACKING_URI` dans les variables d'environnement

## 🎯 Prochaines étapes

1. ✅ Architecture créée
2. ⏳ Installer les dépendances : `pip install -r mlops_requirements.txt`
3. ⏳ Initialiser MLOps : `python mlops/scripts/setup_mlops.py`
4. ⏳ Tester l'intégration : Vérifier les endpoints `/api/detection/mlops/health/`
5. ⏳ (Optionnel) Configurer MLflow remote tracking pour la production

