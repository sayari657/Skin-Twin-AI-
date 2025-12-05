"""
Chargement et gestion des données pour le training
"""
import os
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Tuple, Optional, List
import logging

logger = logging.getLogger(__name__)

class DataLoader:
    """Classe pour charger et préparer les données"""
    
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def load_images(self, image_paths: List[str]) -> np.ndarray:
        """Charger une liste d'images"""
        import cv2
        images = []
        
        for img_path in image_paths:
            try:
                img = cv2.imread(str(img_path))
                if img is not None:
                    images.append(img)
                else:
                    logger.warning(f"Could not load image: {img_path}")
            except Exception as e:
                logger.error(f"Error loading image {img_path}: {e}")
        
        return np.array(images)
    
    def load_labels(self, labels_path: str) -> pd.DataFrame:
        """Charger les labels depuis un fichier CSV"""
        try:
            labels = pd.read_csv(labels_path)
            logger.info(f"Loaded {len(labels)} labels from {labels_path}")
            return labels
        except Exception as e:
            logger.error(f"Error loading labels: {e}")
            return pd.DataFrame()
    
    def split_data(
        self, 
        X: np.ndarray, 
        y: np.ndarray, 
        train_ratio: float = 0.7,
        val_ratio: float = 0.15,
        test_ratio: float = 0.15,
        shuffle: bool = True
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Diviser les données en train/val/test"""
        from sklearn.model_selection import train_test_split
        
        assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-6, "Ratios must sum to 1"
        
        # Première division : train vs (val + test)
        X_train, X_temp, y_train, y_temp = train_test_split(
            X, y, test_size=(val_ratio + test_ratio), random_state=42, shuffle=shuffle
        )
        
        # Deuxième division : val vs test
        val_size = val_ratio / (val_ratio + test_ratio)
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=(1 - val_size), random_state=42, shuffle=shuffle
        )
        
        logger.info(f"Data split - Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")
        
        return X_train, X_val, X_test, y_train, y_val, y_test

