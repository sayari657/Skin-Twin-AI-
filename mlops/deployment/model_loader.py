"""
Chargement des modèles depuis le registry pour la production
"""
import logging
from typing import Optional, Dict
from pathlib import Path
import torch
import joblib
from ultralytics import YOLO
from mlops.deployment.model_registry import ModelRegistry
from mlops.config.mlflow_config import (
    YOLO_MODEL_PATH, EFFICIENTNET_MODEL_PATH, XGBOOST_MODEL_PATH,
    PREPROC_MODEL_PATH, LABEL_ENC_MODEL_PATH
)

logger = logging.getLogger(__name__)

class ModelLoader:
    """Charger les modèles pour l'inférence"""
    
    def __init__(self, use_registry: bool = False):
        self.use_registry = use_registry
        self.registry = ModelRegistry() if use_registry else None
        self.models = {}
    
    def load_yolo_model(self, model_path: Optional[str] = None) -> Optional[YOLO]:
        """Charger le modèle YOLO"""
        try:
            if self.use_registry and self.registry:
                model_info = self.registry.get_latest_model('YOLO-SkinDetection', 'Production')
                if model_info:
                    # Télécharger depuis MLflow
                    model_path = self.registry.registry.download_artifacts(
                        model_info['run_id'], 'models/yolo'
                    )
            
            if model_path is None:
                model_path = YOLO_MODEL_PATH
            
            if not Path(model_path).exists():
                logger.error(f"YOLO model not found at {model_path}")
                return None
            
            model = YOLO(str(model_path))
            self.models['yolo'] = model
            logger.info(f"YOLO model loaded from {model_path}")
            return model
        except Exception as e:
            logger.error(f"Error loading YOLO model: {e}")
            return None
    
    def load_efficientnet_model(self, model_path: Optional[str] = None):
        """Charger le modèle EfficientNet"""
        try:
            if self.use_registry and self.registry:
                model = self.registry.load_model('EfficientNet-SkinType', 'Production')
                if model:
                    self.models['efficientnet'] = model
                    return model
            
            if model_path is None:
                model_path = EFFICIENTNET_MODEL_PATH
            
            if not Path(model_path).exists():
                logger.error(f"EfficientNet model not found at {model_path}")
                return None
            
            from torchvision.models import efficientnet_b0
            model = efficientnet_b0(pretrained=False)
            num_features = model.classifier[1].in_features
            model.classifier[1] = torch.nn.Linear(num_features, 3)
            state = torch.load(model_path, map_location='cpu')
            model.load_state_dict(state)
            model.eval()
            
            self.models['efficientnet'] = model
            logger.info(f"EfficientNet model loaded from {model_path}")
            return model
        except Exception as e:
            logger.error(f"Error loading EfficientNet model: {e}")
            return None
    
    def load_xgboost_model(self, model_path: Optional[str] = None):
        """Charger le modèle XGBoost"""
        try:
            if self.use_registry and self.registry:
                model = self.registry.load_model('XGBoost-ContextCorrection', 'Production')
                if model:
                    self.models['xgboost'] = model
                    return model
            
            if model_path is None:
                model_path = XGBOOST_MODEL_PATH
            
            if not Path(model_path).exists():
                logger.error(f"XGBoost model not found at {model_path}")
                return None
            
            model = joblib.load(model_path)
            self.models['xgboost'] = model
            logger.info(f"XGBoost model loaded from {model_path}")
            return model
        except Exception as e:
            logger.error(f"Error loading XGBoost model: {e}")
            return None
    
    def load_preprocessing_model(self, model_path: Optional[str] = None):
        """Charger le modèle de preprocessing"""
        try:
            if model_path is None:
                model_path = PREPROC_MODEL_PATH
            
            if not Path(model_path).exists():
                logger.error(f"Preprocessing model not found at {model_path}")
                return None
            
            model = joblib.load(model_path)
            self.models['preprocessing'] = model
            logger.info(f"Preprocessing model loaded from {model_path}")
            return model
        except Exception as e:
            logger.error(f"Error loading preprocessing model: {e}")
            return None
    
    def load_label_encoder(self, model_path: Optional[str] = None):
        """Charger le label encoder"""
        try:
            if model_path is None:
                model_path = LABEL_ENC_MODEL_PATH
            
            if not Path(model_path).exists():
                logger.warning(f"Label encoder not found at {model_path} (optional)")
                return None
            
            encoder = joblib.load(model_path)
            self.models['label_encoder'] = encoder
            logger.info(f"Label encoder loaded from {model_path}")
            return encoder
        except Exception as e:
            logger.warning(f"Error loading label encoder: {e} (optional)")
            return None
    
    def load_all_models(self) -> Dict:
        """Charger tous les modèles"""
        return {
            'yolo': self.load_yolo_model(),
            'efficientnet': self.load_efficientnet_model(),
            'xgboost': self.load_xgboost_model(),
            'preprocessing': self.load_preprocessing_model(),
            'label_encoder': self.load_label_encoder(),
        }

