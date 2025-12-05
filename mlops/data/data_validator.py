"""
Validation des données avant le training
"""
import numpy as np
import pandas as pd
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class DataValidator:
    """Valider la qualité des données avant le training"""
    
    def validate_images(self, images: np.ndarray) -> Dict[str, bool]:
        """Valider un batch d'images"""
        results = {
            'valid': True,
            'errors': []
        }
        
        if len(images) == 0:
            results['valid'] = False
            results['errors'].append("No images provided")
            return results
        
        # Vérifier la forme
        if len(images.shape) < 3:
            results['valid'] = False
            results['errors'].append(f"Invalid image shape: {images.shape}")
        
        # Vérifier les valeurs
        if images.min() < 0 or images.max() > 255:
            results['valid'] = False
            results['errors'].append("Image values out of range [0, 255]")
        
        # Vérifier les NaN
        if np.isnan(images).any():
            results['valid'] = False
            results['errors'].append("NaN values found in images")
        
        return results
    
    def validate_labels(self, labels: np.ndarray, num_classes: Optional[int] = None) -> Dict[str, bool]:
        """Valider les labels"""
        results = {
            'valid': True,
            'errors': []
        }
        
        if len(labels) == 0:
            results['valid'] = False
            results['errors'].append("No labels provided")
            return results
        
        # Vérifier les valeurs
        if labels.min() < 0:
            results['valid'] = False
            results['errors'].append("Negative label values found")
        
        if num_classes and labels.max() >= num_classes:
            results['valid'] = False
            results['errors'].append(f"Label values exceed number of classes ({num_classes})")
        
        return results
    
    def validate_data_split(
        self, 
        X_train: np.ndarray, 
        y_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray,
        X_test: np.ndarray,
        y_test: np.ndarray
    ) -> Dict[str, bool]:
        """Valider la division des données"""
        results = {
            'valid': True,
            'errors': []
        }
        
        # Vérifier que les tailles correspondent
        if len(X_train) != len(y_train):
            results['valid'] = False
            results['errors'].append("Train X and y sizes don't match")
        
        if len(X_val) != len(y_val):
            results['valid'] = False
            results['errors'].append("Val X and y sizes don't match")
        
        if len(X_test) != len(y_test):
            results['valid'] = False
            results['errors'].append("Test X and y sizes don't match")
        
        # Vérifier qu'il y a des données dans chaque split
        if len(X_train) == 0:
            results['valid'] = False
            results['errors'].append("No training data")
        
        if len(X_val) == 0:
            results['valid'] = False
            results['errors'].append("No validation data")
        
        if len(X_test) == 0:
            results['valid'] = False
            results['errors'].append("No test data")
        
        return results

