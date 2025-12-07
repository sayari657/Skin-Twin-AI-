#!/usr/bin/env python
"""
Script d'entrée pour le pipeline de training dans GitHub Actions
Gère les erreurs et les cas où les modèles n'existent pas encore
"""
import sys
import logging
from pathlib import Path

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Point d'entrée principal"""
    try:
        # Importer le pipeline de training
        from mlops.training.train_pipeline import TrainingPipeline
        
        logger.info("=" * 60)
        logger.info("Starting ML Training Pipeline")
        logger.info("=" * 60)
        
        # Créer le pipeline
        pipeline = TrainingPipeline()
        
        # Chemin des données (par défaut)
        data_path = "data/processed"
        
        # Vérifier si le répertoire existe
        if not Path(data_path).exists():
            logger.warning(f"Data directory {data_path} does not exist, using placeholder data")
            data_path = "data/raw"  # Fallback
        
        # Exécuter le pipeline
        logger.info(f"Running pipeline with data path: {data_path}")
        results = pipeline.run_full_pipeline(data_path)
        
        logger.info("=" * 60)
        logger.info("Training pipeline completed successfully!")
        logger.info(f"Run ID: {results.get('run_id', 'N/A')}")
        logger.info("=" * 60)
        
        return 0
        
    except ImportError as e:
        logger.error(f"Import error: {e}")
        logger.error("Make sure all dependencies are installed")
        return 1
    except Exception as e:
        logger.error(f"Training pipeline failed: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

