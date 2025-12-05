"""
Préprocessing des données pour le training
"""
import numpy as np
import cv2
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class DataPreprocessor:
    """Classe pour préprocesser les données d'images"""
    
    def __init__(self, target_size: Tuple[int, int] = (224, 224)):
        self.target_size = target_size
    
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Préprocesser une image pour EfficientNet"""
        # Redimensionner
        image = cv2.resize(image, self.target_size)
        
        # Normaliser les valeurs entre 0 et 1
        image = image.astype(np.float32) / 255.0
        
        # Convertir BGR vers RGB si nécessaire
        if len(image.shape) == 3 and image.shape[2] == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        return image
    
    def preprocess_batch(self, images: np.ndarray) -> np.ndarray:
        """Préprocesser un batch d'images"""
        processed = []
        for img in images:
            processed.append(self.preprocess_image(img))
        return np.array(processed)
    
    def augment_image(self, image: np.ndarray) -> np.ndarray:
        """Augmenter une image (rotation, flip, etc.)"""
        # Flip horizontal aléatoire
        if np.random.random() > 0.5:
            image = cv2.flip(image, 1)
        
        # Rotation aléatoire
        angle = np.random.uniform(-15, 15)
        h, w = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        image = cv2.warpAffine(image, M, (w, h))
        
        return image

