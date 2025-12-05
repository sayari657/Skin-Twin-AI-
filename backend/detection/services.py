"""
Services pour l'analyse de peau avec IA - Utilise les 5 modèles intégrés
"""
import os
import logging
from django.conf import settings

# Import optionnel pour permettre le démarrage sans dépendances ML
try:
    from .skin_diagnostic import SkinDiagnostic
    SKIN_DIAGNOSTIC_AVAILABLE = True
except ImportError as e:
    SKIN_DIAGNOSTIC_AVAILABLE = False
    SkinDiagnostic = None
    logging.getLogger(__name__).warning(f"SkinDiagnostic non disponible: {e}")

logger = logging.getLogger(__name__)


class SkinAnalysisService:
    """Service principal pour l'analyse de peau utilisant les 5 modèles"""
    
    def __init__(self):
        self.models_path = os.path.join(settings.ML_MODELS_PATH, 'model skin', 'models')
        self.diagnostic = None
        
        if SKIN_DIAGNOSTIC_AVAILABLE:
            try:
                self.diagnostic = SkinDiagnostic(models_dir=self.models_path)
                logger.info("✅ Système de diagnostic dermatologique initialisé avec succès")
            except Exception as e:
                logger.error(f"❌ Erreur lors de l'initialisation du système de diagnostic: {e}")
                self.diagnostic = None
        else:
            logger.warning("⚠️ SkinDiagnostic non disponible. Les fonctionnalités ML seront désactivées.")
    
    def _get_user_info(self, user):
        """Convertir les données utilisateur au format attendu par le modèle"""
        if not user:
            return None
        
        # Mapper les valeurs pour le modèle
        gender_map = {'M': 'Male', 'F': 'Female', 'O': 'Other'}
        diet_map = {
            'POOR': 'Poor',
            'AVERAGE': 'Average', 
            'GOOD': 'Good',
            'EXCELLENT': 'Excellent'
        }
        alcohol_map = {
            'NONE': 'No',
            'OCCASIONAL': 'Occasional',
            'MODERATE': 'Moderate',
            'HIGH': 'High'
        }
        
        user_info = {
            "age": user.age if user.age else 25,
            "gender": gender_map.get(user.gender, 'Female'),
            "sleep_hours": user.sleep_hours if user.sleep_hours else 7,
            "stress_level": user.stress_level if user.stress_level else 5,
            "diet_quality": diet_map.get(user.diet_quality, 'Average'),
            "smoker": "Yes" if user.smoking else "No",
            "alcohol_consumption": alcohol_map.get(user.alcohol_consumption, 'No')
        }
        
        return user_info
    
    def analyze_skin(self, image_path, user=None):
        """
        Analyser complètement la peau avec les 5 modèles
        
        Args:
            image_path: Chemin vers l'image à analyser
            user: Instance User Django (optionnel) pour utiliser les infos utilisateur
        
        Returns:
            Dictionnaire avec tous les résultats de l'analyse
        """
        if not SKIN_DIAGNOSTIC_AVAILABLE or self.diagnostic is None:
            logger.error("Système de diagnostic non disponible")
            return {
                'error': 'Système de diagnostic non disponible',
                'skin_type': {'prediction': None, 'confidence': 0.0},
                'detections': {}
            }
        
        try:
            # Préparer les infos utilisateur
            user_info = self._get_user_info(user) if user else None
            
            # Analyser l'image avec tous les modèles
            result = self.diagnostic.analyze_image(image_path, user_info=user_info)
            
            # Convertir les résultats au format attendu par Django
            skin_type_map = {
                'Dry': 'DRY',
                'Normal': 'NORMAL',
                'Oily': 'OILY'
            }
            
            # Mapper les troubles détectés
            trouble_map = {
                'Acne': 'acne',
                'Wrinkles': 'wrinkles',
                'Dark-Spots': 'dark_spots',
                'Skin-Redness': 'redness',
                'Blackheads': 'acne',
                'Whiteheads': 'acne',
                'Dry-Skin': None,  # Pas de mapping direct
                'Oily-Skin': None,  # Pas de mapping direct
                'Englarged-Pores': None,  # Pas de mapping direct
                'Eyebags': None  # Pas de mapping direct
            }
            
            # Préparer les détections
            detections = {
                'acne': {'detected': False, 'severity': 'NONE', 'confidence': 0.0},
                'wrinkles': {'detected': False, 'severity': 'NONE', 'confidence': 0.0},
                'dark_spots': {'detected': False, 'severity': 'NONE', 'confidence': 0.0},
                'redness': {'detected': False, 'severity': 'NONE', 'confidence': 0.0}
            }
            
            # Traiter les troubles détectés
            for trouble in result.get('detected_troubles', []):
                mapped_trouble = trouble_map.get(trouble)
                if mapped_trouble and mapped_trouble in detections:
                    confidence = result.get('yolo_probs', {}).get(trouble, 0.0)
                    detections[mapped_trouble]['detected'] = True
                    detections[mapped_trouble]['confidence'] = confidence
                    
                    # Déterminer la sévérité
                    if confidence > 0.8:
                        detections[mapped_trouble]['severity'] = 'HIGH'
                    elif confidence > 0.6:
                        detections[mapped_trouble]['severity'] = 'MODERATE'
                    else:
                        detections[mapped_trouble]['severity'] = 'LOW'
            
            # Résultats finaux
            skin_type = skin_type_map.get(result.get('skin_type', 'Normal'), 'NORMAL')
            skin_confidence = result.get('skin_probs', {}).get(result.get('skin_type', 'Normal'), 0.0)
            
            return {
                'skin_type': {
                    'prediction': skin_type,
                    'confidence': skin_confidence
                },
                'detections': detections,
                'annotated_image': result.get('annotated_image'),  # Image annotée avec les zones détectées
                'raw_results': result,  # Résultats bruts pour référence
                'processing_time': 0.0  # À calculer si nécessaire
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse: {e}", exc_info=True)
            return {
                'error': str(e),
                'skin_type': {'prediction': None, 'confidence': 0.0},
                'detections': {}
            }


# Instance globale du service
skin_analysis_service = SkinAnalysisService()
