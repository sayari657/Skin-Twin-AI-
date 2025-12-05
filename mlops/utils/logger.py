"""
Logging structuré pour MLOps
"""
import logging
import sys
from pathlib import Path
from datetime import datetime

def setup_mlops_logger(log_dir: str = 'logs/mlops', level: int = logging.INFO) -> logging.Logger:
    """Configurer le logger MLOps"""
    log_dir_path = Path(log_dir)
    log_dir_path.mkdir(parents=True, exist_ok=True)
    
    # Créer le logger
    logger = logging.getLogger('mlops')
    logger.setLevel(level)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler pour fichier
    file_handler = logging.FileHandler(
        log_dir_path / f'mlops_{datetime.now().strftime("%Y%m%d")}.log'
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    
    # Handler pour console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    
    # Ajouter les handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

