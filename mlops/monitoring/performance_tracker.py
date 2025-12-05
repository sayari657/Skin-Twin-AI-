"""
Suivi des performances des modèles en production
"""
import time
from typing import Dict, List
from datetime import datetime
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

class PerformanceTracker:
    """Tracker pour suivre les performances des modèles"""
    
    def __init__(self):
        self.metrics_history = defaultdict(list)
        self.inference_times = []
        self.error_counts = defaultdict(int)
    
    def track_inference_time(self, model_name: str, inference_time: float):
        """Tracker le temps d'inférence"""
        self.inference_times.append({
            'model': model_name,
            'time': inference_time,
            'timestamp': datetime.now().isoformat()
        })
    
    def track_metric(self, model_name: str, metric_name: str, value: float):
        """Tracker une métrique"""
        self.metrics_history[f"{model_name}_{metric_name}"].append({
            'value': value,
            'timestamp': datetime.now().isoformat()
        })
    
    def track_error(self, model_name: str, error_type: str):
        """Tracker une erreur"""
        self.error_counts[f"{model_name}_{error_type}"] += 1
    
    def get_average_inference_time(self, model_name: str, last_n: int = 100) -> float:
        """Obtenir le temps d'inférence moyen"""
        model_times = [
            t['time'] for t in self.inference_times 
            if t['model'] == model_name
        ][-last_n:]
        
        if not model_times:
            return 0.0
        
        return sum(model_times) / len(model_times)
    
    def get_latest_metrics(self, model_name: str) -> Dict:
        """Obtenir les dernières métriques pour un modèle"""
        metrics = {}
        for key, values in self.metrics_history.items():
            if key.startswith(model_name):
                if values:
                    metrics[key.replace(f"{model_name}_", "")] = values[-1]['value']
        return metrics
    
    def get_error_summary(self) -> Dict:
        """Obtenir un résumé des erreurs"""
        return dict(self.error_counts)

