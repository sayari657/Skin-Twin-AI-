"""
Services pour l'analyse de peau avec IA
"""
import os
import cv2
import numpy as np
import torch
from PIL import Image
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class SkinAnalysisService:
    """Service principal pour l'analyse de peau"""
    
    def __init__(self):
        self.models_path = settings.ML_MODELS_PATH
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.cnn_model = None
        self.yolo_model = None
    
    def load_models(self):
        """Charger les modèles IA"""
        try:
            # Charger le modèle CNN pour la classification
            cnn_path = os.path.join(self.models_path, 'detection_cnn', 'skin_classifier.pth')
            if os.path.exists(cnn_path):
                self.cnn_model = torch.load(cnn_path, map_location=self.device)
                self.cnn_model.eval()
                logger.info("Modèle CNN chargé avec succès")
            
            # Charger le modèle YOLOv8 pour la segmentation
            yolo_path = os.path.join(self.models_path, 'segmentation_yolo', 'yolov8_skin.pt')
            if os.path.exists(yolo_path):
                from ultralytics import YOLO
                self.yolo_model = YOLO(yolo_path)
                logger.info("Modèle YOLOv8 chargé avec succès")
            
        except Exception as e:
            logger.error(f"Erreur lors du chargement des modèles: {e}")
    
    def preprocess_image(self, image_path):
        """Préprocesser l'image pour l'analyse"""
        try:
            # Charger l'image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError("Impossible de charger l'image")
            
            # Redimensionner pour CNN (224x224)
            cnn_image = cv2.resize(image, (224, 224))
            cnn_image = cv2.cvtColor(cnn_image, cv2.COLOR_BGR2RGB)
            cnn_image = cnn_image.astype(np.float32) / 255.0
            
            # Normaliser
            mean = np.array([0.485, 0.456, 0.406])
            std = np.array([0.229, 0.224, 0.225])
            cnn_image = (cnn_image - mean) / std
            
            # Convertir en tensor
            cnn_tensor = torch.from_numpy(cnn_image.transpose(2, 0, 1)).unsqueeze(0)
            
            return cnn_tensor, image
            
        except Exception as e:
            logger.error(f"Erreur lors du préprocessing: {e}")
            raise
    
    def classify_skin_type(self, image_tensor):
        """Classifier le type de peau avec CNN"""
        if self.cnn_model is None:
            return None, 0.0
        
        try:
            with torch.no_grad():
                image_tensor = image_tensor.to(self.device)
                outputs = self.cnn_model(image_tensor)
                probabilities = torch.softmax(outputs, dim=1)
                confidence, predicted = torch.max(probabilities, 1)
                
                skin_types = ['DRY', 'OILY', 'COMBINATION', 'NORMAL', 'SENSITIVE']
                predicted_type = skin_types[predicted.item()]
                confidence_score = confidence.item()
                
                return predicted_type, confidence_score
                
        except Exception as e:
            logger.error(f"Erreur lors de la classification: {e}")
            return None, 0.0
    
    def detect_skin_issues(self, image):
        """Détecter les problèmes de peau avec YOLOv8"""
        if self.yolo_model is None:
            return {}
        
        try:
            results = self.yolo_model(image)
            
            detections = {
                'acne': {'detected': False, 'severity': 'NONE', 'confidence': 0.0},
                'wrinkles': {'detected': False, 'severity': 'NONE', 'confidence': 0.0},
                'dark_spots': {'detected': False, 'severity': 'NONE', 'confidence': 0.0},
                'redness': {'detected': False, 'severity': 'NONE', 'confidence': 0.0}
            }
            
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        class_id = int(box.cls[0])
                        confidence = float(box.conf[0])
                        
                        # Mapping des classes (à adapter selon votre modèle)
                        class_names = ['acne', 'wrinkles', 'dark_spots', 'redness']
                        if class_id < len(class_names):
                            class_name = class_names[class_id]
                            
                            if confidence > 0.5:  # Seuil de confiance
                                detections[class_name]['detected'] = True
                                detections[class_name]['confidence'] = confidence
                                
                                # Déterminer la sévérité
                                if confidence > 0.8:
                                    detections[class_name]['severity'] = 'HIGH'
                                elif confidence > 0.6:
                                    detections[class_name]['severity'] = 'MODERATE'
                                else:
                                    detections[class_name]['severity'] = 'LOW'
            
            return detections
            
        except Exception as e:
            logger.error(f"Erreur lors de la détection: {e}")
            return {}
    
    def analyze_skin(self, image_path):
        """Analyser complètement la peau"""
        try:
            # Charger les modèles si nécessaire
            if self.cnn_model is None or self.yolo_model is None:
                self.load_models()
            
            # Préprocesser l'image
            cnn_tensor, original_image = self.preprocess_image(image_path)
            
            # Classification du type de peau
            skin_type, skin_confidence = self.classify_skin_type(cnn_tensor)
            
            # Détection des problèmes
            detections = self.detect_skin_issues(original_image)
            
            # Préparer les résultats
            results = {
                'skin_type': {
                    'prediction': skin_type,
                    'confidence': skin_confidence
                },
                'detections': detections,
                'processing_time': 0.0  # À calculer
            }
            
            return results
            
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse: {e}")
            raise


# Instance globale du service
skin_analysis_service = SkinAnalysisService()




