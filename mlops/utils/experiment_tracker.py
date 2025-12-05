"""
Tracking des expériences ML
"""
import mlflow
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class ExperimentTracker:
    """Tracker pour les expériences ML"""
    
    def __init__(self, experiment_name: str):
        mlflow.set_experiment(experiment_name)
        self.experiment_name = experiment_name
    
    def start_run(self, run_name: Optional[str] = None):
        """Démarrer une nouvelle run"""
        return mlflow.start_run(run_name=run_name)
    
    def log_params(self, params: Dict):
        """Logger des paramètres"""
        mlflow.log_params(params)
    
    def log_metrics(self, metrics: Dict, step: Optional[int] = None):
        """Logger des métriques"""
        mlflow.log_metrics(metrics, step=step)
    
    def log_artifacts(self, local_dir: str, artifact_path: Optional[str] = None):
        """Logger des artefacts"""
        mlflow.log_artifacts(local_dir, artifact_path)
    
    def log_model(self, model, artifact_path: str, registered_model_name: Optional[str] = None):
        """Logger un modèle"""
        # Détecter le type de modèle et utiliser la méthode appropriée
        if hasattr(model, 'predict_proba'):  # Scikit-learn/XGBoost
            mlflow.sklearn.log_model(model, artifact_path, registered_model_name=registered_model_name)
        elif hasattr(model, 'forward'):  # PyTorch
            mlflow.pytorch.log_model(model, artifact_path, registered_model_name=registered_model_name)
        else:
            mlflow.log_artifact(model, artifact_path)

