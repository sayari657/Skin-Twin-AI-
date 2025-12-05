"""
Pipeline de training complet pour DVC
Ce fichier est appelé par dvc.yaml pour exécuter le training
"""
import sys
from pathlib import Path

# Ajouter le chemin du projet au PYTHONPATH
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from mlops.training.train_pipeline import TrainingPipeline
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Point d'entrée principal pour le pipeline DVC"""
    logger.info("Starting DVC training pipeline...")
    
    # Chemin des données préprocessées (depuis dvc.yaml)
    data_path = project_root / "data" / "processed"
    
    if not data_path.exists():
        logger.error(f"Data path does not exist: {data_path}")
        logger.info("Please run 'dvc repro prepare_data' first")
        sys.exit(1)
    
    # Créer le pipeline de training
    pipeline = TrainingPipeline()
    
    # Exécuter le pipeline complet
    try:
        results = pipeline.run_full_pipeline(str(data_path))
        logger.info("Training pipeline completed successfully!")
        logger.info(f"Results: {results}")
        return 0
    except Exception as e:
        logger.error(f"Training pipeline failed: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())

