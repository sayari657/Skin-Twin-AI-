"""
Configuration des modèles ML
"""
from typing import Dict, List

# Labels des troubles de peau pour YOLO
YOLO_TROUBLE_LABELS = [
    'Acne', 'Blackheads', 'Dark-Spots', 'Dry-Skin', 'Englarged-Pores',
    'Eyebags', 'Oily-Skin', 'Skin-Redness', 'Whiteheads', 'Wrinkles'
]

# Labels des types de peau pour EfficientNet
SKIN_TYPE_LABELS = {
    0: "Dry",
    1: "Normal",
    2: "Oily"
}

# Mapping des problèmes détectés
PROBLEM_MAPPING = {
    'Acne': 'acne',
    'Wrinkles': 'wrinkles',
    'Dark-Spots': 'dark_spots',
    'Skin-Redness': 'redness',
    'Blackheads': 'acne',
    'Whiteheads': 'acne',
}

# Configuration des métriques à suivre
METRICS_TO_TRACK = {
    'yolo': ['mAP', 'precision', 'recall', 'f1_score'],
    'efficientnet': ['accuracy', 'precision', 'recall', 'f1_score'],
    'xgboost': ['accuracy', 'precision', 'recall', 'f1_score', 'roc_auc'],
}

