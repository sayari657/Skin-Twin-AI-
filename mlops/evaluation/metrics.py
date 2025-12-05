"""
Métriques personnalisées pour l'évaluation
"""
import numpy as np
from typing import Dict, List

def calculate_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray, num_classes: int) -> np.ndarray:
    """Calculer la matrice de confusion"""
    from sklearn.metrics import confusion_matrix
    return confusion_matrix(y_true, y_pred, labels=list(range(num_classes)))

def calculate_classification_report(y_true: np.ndarray, y_pred: np.ndarray) -> Dict:
    """Calculer un rapport de classification détaillé"""
    from sklearn.metrics import classification_report
    report = classification_report(y_true, y_pred, output_dict=True)
    return report

def calculate_roc_auc(y_true: np.ndarray, y_pred_proba: np.ndarray, num_classes: int) -> float:
    """Calculer l'AUC-ROC"""
    from sklearn.metrics import roc_auc_score
    
    if num_classes == 2:
        return float(roc_auc_score(y_true, y_pred_proba[:, 1]))
    else:
        return float(roc_auc_score(y_true, y_pred_proba, multi_class='ovr'))

