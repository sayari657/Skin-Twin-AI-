"""
Monitoring des modèles en production
"""
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging
from collections import deque
from scipy import stats
import json
from pathlib import Path

logger = logging.getLogger(__name__)

class ModelMonitor:
    """Monitoring des modèles en production"""
    
    def __init__(self, max_history: int = 10000):
        self.predictions_history = deque(maxlen=max_history)
        self.performance_metrics = {}
        self.drift_threshold = 0.1
        self.reference_data = None
        self.monitoring_dir = Path('.monitoring')
        self.monitoring_dir.mkdir(parents=True, exist_ok=True)
    
    def log_prediction(
        self, 
        prediction: Dict, 
        actual: Optional[Dict] = None,
        input_data: Optional[np.ndarray] = None,
        model_name: str = "unknown"
    ):
        """Logger une prédiction"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'model_name': model_name,
            'prediction': prediction,
            'actual': actual,
            'input_shape': input_data.shape if input_data is not None else None
        }
        
        self.predictions_history.append(log_entry)
        
        # Sauvegarder périodiquement
        if len(self.predictions_history) % 100 == 0:
            self._save_history()
    
    def set_reference_data(self, reference_data: np.ndarray):
        """Définir les données de référence pour la détection de dérive"""
        self.reference_data = reference_data
        logger.info(f"Reference data set with shape: {reference_data.shape}")
    
    def detect_data_drift(
        self, 
        current_data: np.ndarray, 
        reference_data: Optional[np.ndarray] = None
    ) -> Optional[Dict]:
        """Détecter la dérive des données"""
        if reference_data is None:
            reference_data = self.reference_data
        
        if reference_data is None:
            logger.warning("No reference data available for drift detection")
            return None
        
        try:
            # Test de Kolmogorov-Smirnov pour détecter la dérive
            statistic, p_value = stats.ks_2samp(
                reference_data.flatten(), 
                current_data.flatten()
            )
            
            drift_detected = p_value < 0.05
            
            result = {
                'drift_detected': drift_detected,
                'p_value': float(p_value),
                'statistic': float(statistic),
                'severity': self._calculate_severity(p_value),
                'timestamp': datetime.now().isoformat()
            }
            
            if drift_detected:
                logger.warning(f"Data drift detected! p-value: {p_value:.4f}")
                self._save_drift_alert(result)
            
            return result
        except Exception as e:
            logger.error(f"Error detecting data drift: {e}")
            return None
    
    def _calculate_severity(self, p_value: float) -> str:
        """Calculer la sévérité de la dérive"""
        if p_value < 0.01:
            return 'high'
        elif p_value < 0.05:
            return 'medium'
        else:
            return 'low'
    
    def calculate_performance_metrics(
        self, 
        predictions: List, 
        actuals: List
    ) -> Dict:
        """Calculer les métriques de performance"""
        try:
            from sklearn.metrics import (
                accuracy_score, precision_score, 
                recall_score, f1_score, confusion_matrix
            )
            
            metrics = {
                'accuracy': float(accuracy_score(actuals, predictions)),
                'precision': float(precision_score(actuals, predictions, average='weighted', zero_division=0)),
                'recall': float(recall_score(actuals, predictions, average='weighted', zero_division=0)),
                'f1_score': float(f1_score(actuals, predictions, average='weighted', zero_division=0))
            }
            
            # Matrice de confusion
            cm = confusion_matrix(actuals, predictions)
            metrics['confusion_matrix'] = cm.tolist()
            
            self.performance_metrics = metrics
            self._save_metrics(metrics)
            
            return metrics
        except Exception as e:
            logger.error(f"Error calculating performance metrics: {e}")
            return {}
    
    def get_prediction_stats(self, hours: int = 24) -> Dict:
        """Obtenir les statistiques des prédictions sur une période"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        recent_predictions = [
            p for p in self.predictions_history
            if datetime.fromisoformat(p['timestamp']) > cutoff_time
        ]
        
        if not recent_predictions:
            return {}
        
        return {
            'total_predictions': len(recent_predictions),
            'time_period_hours': hours,
            'predictions_per_hour': len(recent_predictions) / hours,
            'timestamp': datetime.now().isoformat()
        }
    
    def _save_history(self):
        """Sauvegarder l'historique"""
        try:
            history_file = self.monitoring_dir / 'predictions_history.json'
            with open(history_file, 'w') as f:
                json.dump(list(self.predictions_history), f, indent=2)
        except Exception as e:
            logger.error(f"Error saving history: {e}")
    
    def _save_drift_alert(self, drift_result: Dict):
        """Sauvegarder une alerte de dérive"""
        try:
            alert_file = self.monitoring_dir / f"drift_alert_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(alert_file, 'w') as f:
                json.dump(drift_result, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving drift alert: {e}")
    
    def _save_metrics(self, metrics: Dict):
        """Sauvegarder les métriques"""
        try:
            metrics_file = self.monitoring_dir / 'performance_metrics.json'
            with open(metrics_file, 'w') as f:
                json.dump(metrics, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving metrics: {e}")

