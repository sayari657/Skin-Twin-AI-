"""
YOLOv8 pour la segmentation des problèmes de peau
"""
import torch
import cv2
import numpy as np
from ultralytics import YOLO
from typing import List, Dict, Any, Tuple


class SkinSegmentationYOLO:
    """Classe pour la segmentation des problèmes de peau avec YOLOv8"""
    
    def __init__(self, model_path: str, device: str = 'cpu'):
        self.device = device
        self.model = YOLO(model_path)
        self.model.to(device)
        
        # Classes de problèmes de peau
        self.class_names = {
            0: 'acne',
            1: 'wrinkles', 
            2: 'dark_spots',
            3: 'redness',
            4: 'scars',
            5: 'pores'
        }
        
        # Couleurs pour la visualisation
        self.colors = {
            'acne': (255, 0, 0),      # Rouge
            'wrinkles': (0, 255, 0),  # Vert
            'dark_spots': (0, 0, 255), # Bleu
            'redness': (255, 255, 0),  # Cyan
            'scars': (255, 0, 255),    # Magenta
            'pores': (0, 255, 255)     # Jaune
        }
    
    def predict(self, image: np.ndarray, conf_threshold: float = 0.5) -> Dict[str, Any]:
        """
        Prédire les problèmes de peau sur une image
        
        Args:
            image: Image d'entrée (BGR)
            conf_threshold: Seuil de confiance minimum
            
        Returns:
            Dictionnaire contenant les détections
        """
        # Exécuter la prédiction
        results = self.model(image, conf=conf_threshold)
        
        # Traiter les résultats
        detections = {
            'acne': {'detected': False, 'severity': 'NONE', 'confidence': 0.0, 'masks': []},
            'wrinkles': {'detected': False, 'severity': 'NONE', 'confidence': 0.0, 'masks': []},
            'dark_spots': {'detected': False, 'confidence': 0.0, 'masks': []},
            'redness': {'detected': False, 'severity': 'NONE', 'confidence': 0.0, 'masks': []},
            'scars': {'detected': False, 'confidence': 0.0, 'masks': []},
            'pores': {'detected': False, 'confidence': 0.0, 'masks': []}
        }
        
        for result in results:
            if result.masks is not None:
                # Traiter les masques de segmentation
                masks = result.masks.data.cpu().numpy()
                boxes = result.boxes.data.cpu().numpy()
                
                for i, (box, mask) in enumerate(zip(boxes, masks)):
                    class_id = int(box[5])
                    confidence = float(box[4])
                    class_name = self.class_names.get(class_id, 'unknown')
                    
                    if class_name in detections and confidence > conf_threshold:
                        detections[class_name]['detected'] = True
                        detections[class_name]['confidence'] = max(
                            detections[class_name]['confidence'], 
                            confidence
                        )
                        detections[class_name]['masks'].append(mask)
                        
                        # Déterminer la sévérité
                        if class_name in ['acne', 'wrinkles', 'redness']:
                            detections[class_name]['severity'] = self._get_severity(confidence)
        
        return detections
    
    def _get_severity(self, confidence: float) -> str:
        """Déterminer la sévérité basée sur la confiance"""
        if confidence >= 0.8:
            return 'HIGH'
        elif confidence >= 0.6:
            return 'MODERATE'
        else:
            return 'LOW'
    
    def visualize_results(self, image: np.ndarray, detections: Dict[str, Any]) -> np.ndarray:
        """
        Visualiser les résultats de segmentation
        
        Args:
            image: Image originale
            detections: Résultats de détection
            
        Returns:
            Image avec les masques superposés
        """
        result_image = image.copy()
        
        for class_name, detection in detections.items():
            if detection['detected'] and detection['masks']:
                color = self.colors.get(class_name, (128, 128, 128))
                
                # Superposer tous les masques pour cette classe
                combined_mask = np.zeros(image.shape[:2], dtype=np.uint8)
                for mask in detection['masks']:
                    # Redimensionner le masque si nécessaire
                    if mask.shape != image.shape[:2]:
                        mask = cv2.resize(mask, (image.shape[1], image.shape[0]))
                    
                    combined_mask = np.maximum(combined_mask, (mask * 255).astype(np.uint8))
                
                # Appliquer le masque coloré
                mask_colored = np.zeros_like(result_image)
                mask_colored[combined_mask > 0] = color
                
                # Superposer avec transparence
                result_image = cv2.addWeighted(result_image, 0.7, mask_colored, 0.3, 0)
        
        return result_image
    
    def get_face_region(self, image: np.ndarray) -> Tuple[int, int, int, int]:
        """
        Détecter la région du visage
        
        Args:
            image: Image d'entrée
            
        Returns:
            Coordonnées (x1, y1, x2, y2) de la région du visage
        """
        # Utiliser un détecteur de visage simple (peut être amélioré avec MTCNN ou RetinaFace)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) > 0:
            # Prendre le plus grand visage
            largest_face = max(faces, key=lambda x: x[2] * x[3])
            x, y, w, h = largest_face
            return (x, y, x + w, y + h)
        else:
            # Si aucun visage détecté, utiliser toute l'image
            return (0, 0, image.shape[1], image.shape[0])


def create_skin_yolo_model(model_path: str = None) -> SkinSegmentationYOLO:
    """
    Créer une instance du modèle YOLO pour la segmentation de peau
    
    Args:
        model_path: Chemin vers le modèle pré-entraîné
        
    Returns:
        Instance de SkinSegmentationYOLO
    """
    if model_path is None:
        # Utiliser un modèle YOLOv8 par défaut
        model_path = 'yolov8n-seg.pt'
    
    return SkinSegmentationYOLO(model_path)


# Fonction utilitaire pour prétraiter les images
def preprocess_image(image_path: str, target_size: Tuple[int, int] = (640, 640)) -> np.ndarray:
    """
    Prétraiter une image pour l'analyse YOLO
    
    Args:
        image_path: Chemin vers l'image
        target_size: Taille cible pour le redimensionnement
        
    Returns:
        Image prétraitée
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Impossible de charger l'image: {image_path}")
    
    # Redimensionner en gardant le ratio d'aspect
    h, w = image.shape[:2]
    target_w, target_h = target_size
    
    # Calculer le ratio de redimensionnement
    ratio = min(target_w / w, target_h / h)
    new_w = int(w * ratio)
    new_h = int(h * ratio)
    
    # Redimensionner
    image_resized = cv2.resize(image, (new_w, new_h))
    
    # Ajouter du padding si nécessaire
    pad_w = (target_w - new_w) // 2
    pad_h = (target_h - new_h) // 2
    
    image_padded = cv2.copyMakeBorder(
        image_resized, 
        pad_h, pad_h, pad_w, pad_w, 
        cv2.BORDER_CONSTANT, 
        value=(114, 114, 114)
    )
    
    return image_padded




