"""
Intégration MLOps avec Django
"""
import logging
import numpy as np
from typing import Optional, Dict
import os
import sys
from pathlib import Path

# Ajouter le répertoire mlops au path
BASE_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

try:
    from mlops.deployment.model_registry import ModelRegistry
    from mlops.deployment.model_loader import ModelLoader
    from mlops.monitoring.model_monitor import ModelMonitor
    from mlops.monitoring.performance_tracker import PerformanceTracker
    from mlops.monitoring.alerting import AlertingSystem
    MLOPS_AVAILABLE = True
except ImportError as e:
    MLOPS_AVAILABLE = False
    logging.getLogger(__name__).warning(f"MLOps modules not available: {e}")

logger = logging.getLogger(__name__)

class DjangoMLOpsIntegration:
    """Intégration MLOps avec Django"""
    
    _instance = None
    
    def __new__(cls, use_registry: bool = False):
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, use_registry: bool = False):
        if not MLOPS_AVAILABLE:
            self.enabled = False
            logger.warning("MLOps not available, monitoring disabled")
            return
        
        if hasattr(self, 'initialized'):
            return
        
        self.use_registry = use_registry
        self.enabled = True
        
        try:
            self.registry = ModelRegistry() if use_registry else None
            self.model_loader = ModelLoader(use_registry=use_registry)
            self.monitor = ModelMonitor()
            self.performance_tracker = PerformanceTracker()
            self.alerting = AlertingSystem()
            self.initialized = True
            logger.info("MLOps integration initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing MLOps: {e}")
            self.enabled = False
    
    def initialize_models(self):
        """Initialiser les modèles pour Django"""
        if not self.enabled:
            return None
        
        try:
            logger.info("Initializing models for Django...")
            models = self.model_loader.load_all_models()
            
            if all(models.values()):
                logger.info("All models loaded successfully")
                return models
            else:
                logger.warning("Some models failed to load")
                return models
        except Exception as e:
            logger.error(f"Error initializing models: {e}")
            return None
    
    def log_prediction_for_monitoring(
        self, 
        prediction: Dict, 
        input_data: Optional[np.ndarray] = None,
        model_name: str = "ensemble"
    ):
        """Logger une prédiction pour le monitoring"""
        if not self.enabled:
            return
        
        try:
            self.monitor.log_prediction(prediction, input_data=input_data, model_name=model_name)
        except Exception as e:
            logger.error(f"Error logging prediction: {e}")
    
    def track_inference_performance(self, model_name: str, inference_time: float):
        """Tracker les performances d'inférence"""
        if not self.enabled:
            return
        
        try:
            self.performance_tracker.track_inference_time(model_name, inference_time)
        except Exception as e:
            logger.error(f"Error tracking performance: {e}")
    
    def check_model_health(self) -> Dict:
        """Vérifier la santé des modèles"""
        if not self.enabled:
            return {'enabled': False}
        
        try:
            health_status = {
                'enabled': True,
                'models_loaded': all(self.model_loader.models.values()) if self.model_loader.models else False,
                'monitoring_active': len(self.monitor.predictions_history) > 0,
                'recent_errors': self.performance_tracker.get_error_summary()
            }
            return health_status
        except Exception as e:
            logger.error(f"Error checking health: {e}")
            return {'enabled': True, 'error': str(e)}
    
    def get_production_models(self) -> Dict:
        """Obtenir les modèles de production depuis le registry"""
        if not self.enabled:
            return {}
        
        if not self.use_registry or not self.registry:
            logger.warning("Model registry not enabled, using local models")
            return self.model_loader.models if self.model_loader else {}
        
        try:
            models = {}
            
            # Charger depuis le registry
            yolo_info = self.registry.get_latest_model('YOLO-SkinDetection', 'Production')
            eff_info = self.registry.get_latest_model('EfficientNet-SkinType', 'Production')
            xgb_info = self.registry.get_latest_model('XGBoost-ContextCorrection', 'Production')
            
            if yolo_info:
                models['yolo'] = self.registry.load_model('YOLO-SkinDetection', 'Production')
            if eff_info:
                models['efficientnet'] = self.registry.load_model('EfficientNet-SkinType', 'Production')
            if xgb_info:
                models['xgboost'] = self.registry.load_model('XGBoost-ContextCorrection', 'Production')
            
            return models
        except Exception as e:
            logger.error(f"Error getting production models: {e}")
            return {}


# Instance globale pour Django
mlops_integration = DjangoMLOpsIntegration(use_registry=False)

