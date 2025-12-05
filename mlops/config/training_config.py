"""
Configuration du training des modèles
"""
import os
from typing import Dict

# Configuration générale du training
TRAINING_CONFIG: Dict = {
    'batch_size': 32,
    'epochs': 50,
    'learning_rate': 0.001,
    'validation_split': 0.2,
    'test_split': 0.1,
    'early_stopping_patience': 5,
    'device': os.getenv('DEVICE', 'cpu'),
    'num_workers': int(os.getenv('NUM_WORKERS', '4')),
    'seed': 42,
}

# Configuration spécifique YOLO
YOLO_TRAINING_CONFIG: Dict = {
    'img_size': 640,
    'batch': 16,
    'epochs': 100,
    'patience': 50,
    'save_period': 10,
    'device': TRAINING_CONFIG['device'],
}

# Configuration spécifique EfficientNet
EFFICIENTNET_TRAINING_CONFIG: Dict = {
    'img_size': 224,
    'batch_size': 32,
    'epochs': 50,
    'learning_rate': 0.001,
    'weight_decay': 1e-4,
    'device': TRAINING_CONFIG['device'],
}

# Configuration spécifique XGBoost
XGBOOST_TRAINING_CONFIG: Dict = {
    'n_estimators': 100,
    'max_depth': 6,
    'learning_rate': 0.1,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'random_state': 42,
}

