"""
Système d'alertes pour le monitoring
"""
import logging
from typing import Dict, Optional
from datetime import datetime
import json
from pathlib import Path

logger = logging.getLogger(__name__)

class AlertingSystem:
    """Système d'alertes pour le monitoring"""
    
    def __init__(self, alert_dir: str = '.monitoring/alerts'):
        self.alert_dir = Path(alert_dir)
        self.alert_dir.mkdir(parents=True, exist_ok=True)
    
    def send_drift_alert(self, drift_info: Dict):
        """Envoyer une alerte de dérive"""
        alert = {
            'type': 'data_drift',
            'severity': drift_info.get('severity', 'medium'),
            'message': f"Data drift detected: p-value={drift_info.get('p_value', 0):.4f}",
            'timestamp': datetime.now().isoformat(),
            'details': drift_info
        }
        
        self._save_alert(alert)
        logger.warning(f"DRIFT ALERT: {alert['message']}")
    
    def send_performance_alert(self, model_name: str, metric_name: str, value: float, threshold: float):
        """Envoyer une alerte de performance"""
        alert = {
            'type': 'performance_degradation',
            'model': model_name,
            'metric': metric_name,
            'value': value,
            'threshold': threshold,
            'message': f"{model_name} {metric_name} ({value:.4f}) below threshold ({threshold:.4f})",
            'timestamp': datetime.now().isoformat()
        }
        
        self._save_alert(alert)
        logger.warning(f"PERFORMANCE ALERT: {alert['message']}")
    
    def send_error_alert(self, model_name: str, error_type: str, error_message: str):
        """Envoyer une alerte d'erreur"""
        alert = {
            'type': 'error',
            'model': model_name,
            'error_type': error_type,
            'message': error_message,
            'timestamp': datetime.now().isoformat()
        }
        
        self._save_alert(alert)
        logger.error(f"ERROR ALERT: {model_name} - {error_type}: {error_message}")
    
    def _save_alert(self, alert: Dict):
        """Sauvegarder une alerte"""
        try:
            alert_file = self.alert_dir / f"alert_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(alert_file, 'w') as f:
                json.dump(alert, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving alert: {e}")

