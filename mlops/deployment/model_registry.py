"""
Model Registry avec MLflow pour versioning et gestion des modèles
"""
import mlflow
import mlflow.pytorch
import mlflow.sklearn
from pathlib import Path
from typing import Dict, Optional, List
import joblib
import torch
import logging
from mlops.config.mlflow_config import (
    MLFLOW_TRACKING_URI, MLFLOW_EXPERIMENT_NAME,
    YOLO_MODEL_PATH, EFFICIENTNET_MODEL_PATH, XGBOOST_MODEL_PATH,
    REGISTERED_MODEL_NAMES
)

logger = logging.getLogger(__name__)

class ModelRegistry:
    """Registry pour gérer les versions des modèles ML"""
    
    def __init__(self, tracking_uri: Optional[str] = None):
        self.tracking_uri = tracking_uri or MLFLOW_TRACKING_URI
        mlflow.set_tracking_uri(self.tracking_uri)
        mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)
        logger.info(f"MLflow tracking URI: {self.tracking_uri}")
        logger.info(f"MLflow experiment: {MLFLOW_EXPERIMENT_NAME}")
    
    def register_yolo_model(
        self, 
        model_path: str, 
        metrics: Dict, 
        tags: Optional[Dict] = None,
        description: str = ""
    ) -> Optional[str]:
        """Enregistrer un modèle YOLO dans MLflow"""
        try:
            with mlflow.start_run(run_name="yolo_model"):
                # Enregistrer le modèle comme artefact
                mlflow.log_artifact(model_path, "models/yolo")
                
                # Enregistrer les métriques
                mlflow.log_metrics(metrics)
                
                # Enregistrer les tags
                if tags:
                    mlflow.set_tags(tags)
                
                # Paramètres du modèle
                mlflow.log_param("model_type", "yolo")
                mlflow.log_param("model_path", str(model_path))
                mlflow.log_param("framework", "ultralytics")
                
                if description:
                    mlflow.set_tag("description", description)
                
                # Enregistrer dans le model registry
                model_name = REGISTERED_MODEL_NAMES['yolo']
                mlflow.register_model(
                    f"runs:/{mlflow.active_run().info.run_id}/models/yolo",
                    model_name
                )
                
                logger.info(f"YOLO model registered: {model_path}")
                return mlflow.active_run().info.run_id
        except Exception as e:
            logger.error(f"Error registering YOLO model: {e}")
            raise
    
    def register_efficientnet_model(
        self, 
        model_path: str, 
        metrics: Dict, 
        tags: Optional[Dict] = None,
        description: str = ""
    ) -> Optional[str]:
        """Enregistrer un modèle EfficientNet dans MLflow"""
        try:
            model = torch.load(model_path, map_location='cpu')
            
            with mlflow.start_run(run_name="efficientnet_model"):
                mlflow.pytorch.log_model(
                    pytorch_model=model,
                    artifact_path="efficientnet_model",
                    registered_model_name=REGISTERED_MODEL_NAMES['efficientnet']
                )
                mlflow.log_metrics(metrics)
                
                if tags:
                    mlflow.set_tags(tags)
                
                mlflow.log_param("model_type", "efficientnet")
                mlflow.log_param("model_path", str(model_path))
                mlflow.log_param("architecture", "efficientnet_b0")
                
                if description:
                    mlflow.set_tag("description", description)
                
                logger.info(f"EfficientNet model registered: {model_path}")
                return mlflow.active_run().info.run_id
        except Exception as e:
            logger.error(f"Error registering EfficientNet model: {e}")
            raise
    
    def register_xgboost_model(
        self, 
        model_path: str, 
        metrics: Dict, 
        tags: Optional[Dict] = None,
        description: str = ""
    ) -> Optional[str]:
        """Enregistrer un modèle XGBoost dans MLflow"""
        try:
            model = joblib.load(model_path)
            
            with mlflow.start_run(run_name="xgboost_model"):
                mlflow.sklearn.log_model(
                    sk_model=model,
                    artifact_path="xgboost_model",
                    registered_model_name=REGISTERED_MODEL_NAMES['xgboost']
                )
                mlflow.log_metrics(metrics)
                
                if tags:
                    mlflow.set_tags(tags)
                
                mlflow.log_param("model_type", "xgboost")
                mlflow.log_param("model_path", str(model_path))
                
                if description:
                    mlflow.set_tag("description", description)
                
                logger.info(f"XGBoost model registered: {model_path}")
                return mlflow.active_run().info.run_id
        except Exception as e:
            logger.error(f"Error registering XGBoost model: {e}")
            raise
    
    def get_latest_model(self, model_name: str, stage: str = "Production") -> Optional[Dict]:
        """Récupérer la dernière version d'un modèle"""
        try:
            client = mlflow.tracking.MlflowClient()
            latest_versions = client.get_latest_versions(model_name, stages=[stage])
            
            if latest_versions:
                version = latest_versions[0]
                return {
                    'name': version.name,
                    'version': version.version,
                    'stage': version.current_stage,
                    'run_id': version.run_id,
                    'source': version.source
                }
            else:
                # Essayer sans stage spécifique
                latest_versions = client.get_latest_versions(model_name)
                if latest_versions:
                    version = latest_versions[0]
                    return {
                        'name': version.name,
                        'version': version.version,
                        'stage': version.current_stage,
                        'run_id': version.run_id,
                        'source': version.source
                    }
            
            logger.warning(f"No model found for {model_name} in stage {stage}")
            return None
        except Exception as e:
            logger.error(f"Error getting latest model: {e}")
            return None
    
    def load_model(self, model_name: str, stage: str = "Production"):
        """Charger un modèle depuis le registry"""
        try:
            model_info = self.get_latest_model(model_name, stage)
            if model_info:
                if 'pytorch' in model_info['source']:
                    return mlflow.pytorch.load_model(model_info['source'])
                elif 'sklearn' in model_info['source']:
                    return mlflow.sklearn.load_model(model_info['source'])
                else:
                    # Pour YOLO, charger manuellement
                    return mlflow.artifacts.download_artifacts(model_info['source'])
            return None
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return None
    
    def transition_model_stage(self, model_name: str, version: int, stage: str):
        """Changer le stage d'un modèle (Staging -> Production)"""
        try:
            client = mlflow.tracking.MlflowClient()
            client.transition_model_version_stage(
                name=model_name,
                version=version,
                stage=stage
            )
            logger.info(f"Model {model_name} v{version} transitioned to {stage}")
        except Exception as e:
            logger.error(f"Error transitioning model: {e}")
            raise
    
    def list_all_models(self) -> List[Dict]:
        """Lister tous les modèles enregistrés"""
        try:
            client = mlflow.tracking.MlflowClient()
            models = client.search_registered_models()
            return [
                {
                    'name': m.name,
                    'latest_versions': [v.version for v in m.latest_versions],
                    'description': m.description
                }
                for m in models
            ]
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []

