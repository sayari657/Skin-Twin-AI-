# MLOps pour Skin-Twin-AI

Architecture MLOps complète pour le projet Skin-Twin-AI.

## 📁 Structure

```
mlops/
├── config/              # Configuration (MLflow, modèles, training)
├── data/               # Gestion des données (loader, preprocessor, validator)
├── training/           # Modules de training
├── evaluation/         # Évaluation des modèles
├── deployment/         # Déploiement et registry
├── monitoring/         # Monitoring en production
├── pipelines/          # Pipelines ML
├── utils/              # Utilitaires (logger, tracker)
├── integration/        # Intégration Django
├── scripts/            # Scripts de setup
└── tests/              # Tests MLOps
```

## 🚀 Installation

```bash
# Installer les dépendances MLOps
pip install -r mlops_requirements.txt

# Initialiser l'environnement MLOps
python mlops/scripts/setup_mlops.py
```

## 📊 Utilisation

### 1. Enregistrer un modèle dans MLflow

```python
from mlops.deployment.model_registry import ModelRegistry

registry = ModelRegistry()
registry.register_yolo_model(
    model_path='models/yolo.pt',
    metrics={'mAP': 0.85, 'precision': 0.82},
    tags={'version': '1.0'}
)
```

### 2. Charger un modèle depuis le registry

```python
from mlops.deployment.model_loader import ModelLoader

loader = ModelLoader(use_registry=True)
models = loader.load_all_models()
```

### 3. Monitoring en production

```python
from mlops.monitoring.model_monitor import ModelMonitor

monitor = ModelMonitor()
monitor.log_prediction(prediction_dict, input_data=image_array)
drift_result = monitor.detect_data_drift(current_data, reference_data)
```

### 4. Pipeline de training

```python
from mlops.pipelines.training_pipeline import TrainingPipeline

pipeline = TrainingPipeline()
results = pipeline.run_full_pipeline(data_path='data/processed')
```

## 🔧 Configuration

Les configurations sont dans `mlops/config/`:
- `mlflow_config.py`: Configuration MLflow
- `model_config.py`: Configuration des modèles
- `training_config.py`: Configuration du training

## 📈 Monitoring

Les métriques et alertes sont sauvegardées dans `.monitoring/`:
- `predictions_history.json`: Historique des prédictions
- `performance_metrics.json`: Métriques de performance
- `alerts/`: Alertes de dérive et erreurs

## 🔄 CI/CD

Les workflows GitHub Actions sont dans `.github/workflows/`:
- `ml_training.yml`: Pipeline de training automatisé
- `ml_monitoring.yml`: Monitoring périodique

## 📝 Notes

- Les modèles sont versionnés avec MLflow
- Les données peuvent être versionnées avec DVC
- Le monitoring détecte automatiquement la dérive des données
- Les alertes sont générées pour les problèmes critiques

