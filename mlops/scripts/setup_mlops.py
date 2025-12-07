"""
Script pour initialiser l'environnement MLOps
"""
import os
import sys
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    import mlflow
    MLFLOW_AVAILABLE = True
except ImportError:
    MLFLOW_AVAILABLE = False
    print("⚠️  MLflow not available, some features will be disabled")

try:
    from mlops.config.mlflow_config import MLFLOW_TRACKING_URI, MLFLOW_EXPERIMENT_NAME
except ImportError:
    MLFLOW_TRACKING_URI = os.getenv('MLFLOW_TRACKING_URI', 'file:./.mlflow')
    MLFLOW_EXPERIMENT_NAME = 'skin-twin-ai'
    print("⚠️  Using default MLflow config")

try:
    from mlops.utils.logger import setup_mlops_logger
    logger = setup_mlops_logger()
except ImportError:
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

def setup_mlflow():
    """Configurer MLflow"""
    if not MLFLOW_AVAILABLE:
        logger.warning("⚠️  MLflow not available, skipping MLflow setup")
        return
    
    try:
        tracking_uri = MLFLOW_TRACKING_URI
        mlflow.set_tracking_uri(tracking_uri)
        
        # Créer l'expérience si elle n'existe pas
        try:
            experiment_id = mlflow.create_experiment(MLFLOW_EXPERIMENT_NAME)
            logger.info(f"✅ Created experiment: {MLFLOW_EXPERIMENT_NAME} (ID: {experiment_id})")
        except Exception:
            mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)
            logger.info(f"✅ Using existing experiment: {MLFLOW_EXPERIMENT_NAME}")
    except Exception as e:
        logger.warning(f"⚠️  Error setting up MLflow: {e}")

def setup_directories():
    """Créer les répertoires nécessaires"""
    directories = [
        '.mlflow',
        '.monitoring',
        '.monitoring/alerts',
        'data/raw',
        'data/processed',
        'models',
        'mlruns',
        'logs/mlops'
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        logger.info(f"✅ Created directory: {dir_path}")

def verify_models():
    """Vérifier que les modèles existent"""
    try:
        from mlops.config.mlflow_config import (
            YOLO_MODEL_PATH, EFFICIENTNET_MODEL_PATH, XGBOOST_MODEL_PATH
        )
        
        models_status = {
            'yolo': YOLO_MODEL_PATH.exists(),
            'efficientnet': EFFICIENTNET_MODEL_PATH.exists(),
            'xgboost': XGBOOST_MODEL_PATH.exists(),
        }
        
        for model_name, exists in models_status.items():
            if exists:
                logger.info(f"✅ {model_name} model found")
            else:
                model_path = globals().get(f'{model_name.upper()}_MODEL_PATH', 'unknown')
                logger.warning(f"⚠️  {model_name} model not found at {model_path}")
        
        return models_status
    except ImportError as e:
        logger.warning(f"⚠️  Could not import model config: {e}")
        return {}

if __name__ == "__main__":
    print("🚀 Setting up MLOps environment...")
    print("=" * 60)
    
    setup_directories()
    setup_mlflow()
    models_status = verify_models()
    
    print("=" * 60)
    print("✅ MLOps environment ready!")
    print(f"📊 MLflow tracking URI: {MLFLOW_TRACKING_URI}")
    print(f"🔬 Experiment: {MLFLOW_EXPERIMENT_NAME}")
    print(f"📁 Monitoring directory: .monitoring/")
    print(f"📝 Logs directory: logs/mlops/")

