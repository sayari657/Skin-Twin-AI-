"""
Configuration MLflow pour le tracking et le registry des modèles
"""
import os
from pathlib import Path
from typing import Optional

# Configuration MLflow
MLFLOW_TRACKING_URI = os.getenv('MLFLOW_TRACKING_URI', 'file:./.mlflow')
MLFLOW_EXPERIMENT_NAME = 'skin-twin-ai'
MLFLOW_MODEL_REGISTRY = os.getenv('MLFLOW_MODEL_REGISTRY', './mlruns')

# Chemins des modèles (relatifs au projet)
BASE_DIR = Path(__file__).parent.parent.parent
MODELS_BASE_PATH = BASE_DIR / 'ml_models' / 'model skin' / 'models'

# Chemins des modèles individuels
YOLO_MODEL_PATH = MODELS_BASE_PATH / 'modéle skinTwin2 .pt'
EFFICIENTNET_MODEL_PATH = MODELS_BASE_PATH / 'modele_peau.pth'
XGBOOST_MODEL_PATH = MODELS_BASE_PATH / 'context_correction_xgb.joblib'
PREPROC_MODEL_PATH = MODELS_BASE_PATH / 'Modelefusion_preproc.joblib'
LABEL_ENC_MODEL_PATH = MODELS_BASE_PATH / 'context_correction_label_encoder.joblib'

# Configuration du training
TRAINING_CONFIG = {
    'batch_size': 32,
    'epochs': 50,
    'learning_rate': 0.001,
    'validation_split': 0.2,
    'early_stopping_patience': 5,
    'device': 'cuda' if os.getenv('CUDA_AVAILABLE', 'false').lower() == 'true' else 'cpu',
}

# Configuration du monitoring
MONITORING_CONFIG = {
    'drift_threshold': 0.1,
    'performance_check_interval': 100,  # nombre de prédictions
    'alert_email': os.getenv('ALERT_EMAIL', ''),
    'max_history_size': 10000,
}

# Configuration des modèles enregistrés
REGISTERED_MODEL_NAMES = {
    'yolo': 'YOLO-SkinDetection',
    'efficientnet': 'EfficientNet-SkinType',
    'xgboost': 'XGBoost-ContextCorrection',
}

