"""
Détection de dérive des données et des modèles
"""
import numpy as np
from typing import Dict, Optional
from scipy import stats
import logging

logger = logging.getLogger(__name__)

class DriftDetector:
    """Détecteur de dérive"""
    
    def __init__(self, threshold: float = 0.05):
        self.threshold = threshold
    
    def detect_distribution_drift(
        self, 
        reference_data: np.ndarray, 
        current_data: np.ndarray
    ) -> Dict:
        """Détecter la dérive de distribution avec KS test"""
        try:
            statistic, p_value = stats.ks_2samp(
                reference_data.flatten(),
                current_data.flatten()
            )
            
            drift_detected = p_value < self.threshold
            
            return {
                'drift_detected': drift_detected,
                'p_value': float(p_value),
                'statistic': float(statistic),
                'severity': self._calculate_severity(p_value)
            }
        except Exception as e:
            logger.error(f"Error detecting distribution drift: {e}")
            return {'drift_detected': False, 'error': str(e)}
    
    def detect_mean_drift(
        self,
        reference_data: np.ndarray,
        current_data: np.ndarray
    ) -> Dict:
        """Détecter la dérive de la moyenne"""
        try:
            ref_mean = np.mean(reference_data)
            curr_mean = np.mean(current_data)
            ref_std = np.std(reference_data)
            
            z_score = abs(curr_mean - ref_mean) / ref_std if ref_std > 0 else 0
            drift_detected = z_score > 2  # 2 écarts-types
            
            return {
                'drift_detected': drift_detected,
                'z_score': float(z_score),
                'reference_mean': float(ref_mean),
                'current_mean': float(curr_mean),
                'mean_difference': float(abs(curr_mean - ref_mean))
            }
        except Exception as e:
            logger.error(f"Error detecting mean drift: {e}")
            return {'drift_detected': False, 'error': str(e)}
    
    def _calculate_severity(self, p_value: float) -> str:
        """Calculer la sévérité"""
        if p_value < 0.01:
            return 'high'
        elif p_value < 0.05:
            return 'medium'
        else:
            return 'low'

