"""
Services pour la simulation GAN
"""
import os
import cv2
import numpy as np
import torch
from PIL import Image
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class GANSimulationService:
    """Service pour la simulation GAN"""
    
    def __init__(self):
        self.models_path = settings.ML_MODELS_PATH
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.gan_model = None
    
    def load_gan_model(self, model_type='pix2pix'):
        """Charger le modèle GAN"""
        try:
            if model_type == 'pix2pix':
                model_path = os.path.join(self.models_path, 'gan', 'pix2pix_skin.pt')
            elif model_type == 'stylegan2':
                model_path = os.path.join(self.models_path, 'gan', 'stylegan2_skin.pt')
            else:
                raise ValueError(f"Type de modèle GAN non supporté: {model_type}")
            
            if os.path.exists(model_path):
                self.gan_model = torch.load(model_path, map_location=self.device)
                self.gan_model.eval()
                logger.info(f"Modèle GAN {model_type} chargé avec succès")
            else:
                logger.warning(f"Modèle GAN {model_type} non trouvé à {model_path}")
                
        except Exception as e:
            logger.error(f"Erreur lors du chargement du modèle GAN: {e}")
    
    def preprocess_for_gan(self, image_path, target_size=(512, 512)):
        """Préprocesser l'image pour le GAN"""
        try:
            # Charger l'image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError("Impossible de charger l'image")
            
            # Redimensionner
            image = cv2.resize(image, target_size)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Normaliser entre -1 et 1
            image = image.astype(np.float32) / 255.0
            image = (image - 0.5) * 2.0
            
            # Convertir en tensor
            image_tensor = torch.from_numpy(image.transpose(2, 0, 1)).unsqueeze(0)
            
            return image_tensor
            
        except Exception as e:
            logger.error(f"Erreur lors du préprocessing GAN: {e}")
            raise
    
    def postprocess_gan_output(self, output_tensor):
        """Postprocesser la sortie du GAN"""
        try:
            # Dénormaliser
            output = output_tensor.squeeze(0).cpu().numpy()
            output = (output + 1.0) / 2.0
            output = np.clip(output, 0, 1)
            
            # Convertir en image
            output = (output * 255).astype(np.uint8)
            output = output.transpose(1, 2, 0)
            output = cv2.cvtColor(output, cv2.COLOR_RGB2BGR)
            
            return output
            
        except Exception as e:
            logger.error(f"Erreur lors du postprocessing GAN: {e}")
            raise
    
    def simulate_skin_improvement(self, image_path, simulation_type, analysis_results):
        """Simuler l'amélioration de la peau"""
        try:
            # Charger le modèle si nécessaire
            if self.gan_model is None:
                self.load_gan_model('pix2pix')
            
            if self.gan_model is None:
                # Mode simulation simple (sans GAN réel)
                return self._simple_simulation(image_path, simulation_type, analysis_results)
            
            # Préprocesser l'image
            input_tensor = self.preprocess_for_gan(image_path)
            input_tensor = input_tensor.to(self.device)
            
            # Générer la simulation
            with torch.no_grad():
                # Ajouter des conditions selon le type de simulation
                conditions = self._prepare_conditions(simulation_type, analysis_results)
                simulated_tensor = self.gan_model(input_tensor, conditions)
            
            # Postprocesser
            simulated_image = self.postprocess_gan_output(simulated_tensor)
            
            # Calculer les scores
            improvement_score = self._calculate_improvement_score(analysis_results, simulation_type)
            confidence_score = self._calculate_confidence_score(simulated_tensor)
            
            return {
                'simulated_image': simulated_image,
                'improvement_score': improvement_score,
                'confidence_score': confidence_score,
                'simulation_type': simulation_type
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la simulation: {e}")
            # Fallback vers simulation simple
            return self._simple_simulation(image_path, simulation_type, analysis_results)
    
    def _simple_simulation(self, image_path, simulation_type, analysis_results):
        """Simulation simple sans GAN (fallback)"""
        try:
            # Charger l'image originale
            original = cv2.imread(image_path)
            simulated = original.copy()
            
            # Appliquer des filtres selon le type de simulation
            if simulation_type == 'ACNE_TREATMENT':
                # Flou gaussien léger pour simuler la réduction d'acné
                simulated = cv2.GaussianBlur(simulated, (5, 5), 0)
                simulated = cv2.addWeighted(original, 0.7, simulated, 0.3, 0)
                
            elif simulation_type == 'WRINKLE_REDUCTION':
                # Filtre de lissage pour réduire les rides
                kernel = np.ones((3, 3), np.float32) / 9
                simulated = cv2.filter2D(simulated, -1, kernel)
                simulated = cv2.addWeighted(original, 0.6, simulated, 0.4, 0)
                
            elif simulation_type == 'DARK_SPOT_REMOVAL':
                # Éclaircissement pour réduire les taches
                simulated = cv2.convertScaleAbs(simulated, alpha=1.1, beta=10)
                
            elif simulation_type == 'SKIN_SMOOTHING':
                # Lissage général
                simulated = cv2.bilateralFilter(simulated, 9, 75, 75)
                
            else:  # COMPLETE_TREATMENT
                # Combinaison de plusieurs effets
                simulated = cv2.bilateralFilter(simulated, 9, 75, 75)
                simulated = cv2.GaussianBlur(simulated, (3, 3), 0)
                simulated = cv2.addWeighted(original, 0.5, simulated, 0.5, 0)
            
            # Calculer des scores approximatifs
            improvement_score = self._estimate_improvement(analysis_results, simulation_type)
            confidence_score = 0.7  # Score fixe pour la simulation simple
            
            return {
                'simulated_image': simulated,
                'improvement_score': improvement_score,
                'confidence_score': confidence_score,
                'simulation_type': simulation_type
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la simulation simple: {e}")
            raise
    
    def _prepare_conditions(self, simulation_type, analysis_results):
        """Préparer les conditions pour le GAN"""
        conditions = {
            'acne_severity': analysis_results.get('acne_severity', 'NONE'),
            'wrinkles_severity': analysis_results.get('wrinkles_severity', 'NONE'),
            'dark_spots_severity': analysis_results.get('dark_spots_severity', 'NONE'),
            'skin_type': analysis_results.get('skin_type', 'NORMAL')
        }
        return conditions
    
    def _calculate_improvement_score(self, analysis_results, simulation_type):
        """Calculer le score d'amélioration"""
        base_score = 50.0
        
        # Ajuster selon les problèmes détectés
        if simulation_type == 'ACNE_TREATMENT' and analysis_results.get('acne_detected'):
            base_score += 30
        if simulation_type == 'WRINKLE_REDUCTION' and analysis_results.get('wrinkles_detected'):
            base_score += 25
        if simulation_type == 'DARK_SPOT_REMOVAL' and analysis_results.get('dark_spots_detected'):
            base_score += 20
        
        return min(base_score, 100.0)
    
    def _calculate_confidence_score(self, output_tensor):
        """Calculer le score de confiance"""
        # Calculer la variance comme indicateur de confiance
        variance = torch.var(output_tensor).item()
        confidence = max(0.0, min(1.0, 1.0 - variance))
        return confidence
    
    def _estimate_improvement(self, analysis_results, simulation_type):
        """Estimer l'amélioration pour la simulation simple"""
        score = 40.0  # Score de base
        
        if simulation_type == 'ACNE_TREATMENT' and analysis_results.get('acne_detected'):
            score += 35
        elif simulation_type == 'WRINKLE_REDUCTION' and analysis_results.get('wrinkles_detected'):
            score += 30
        elif simulation_type == 'DARK_SPOT_REMOVAL' and analysis_results.get('dark_spots_detected'):
            score += 25
        elif simulation_type == 'COMPLETE_TREATMENT':
            score += 20
        
        return min(score, 95.0)
    
    def create_comparison_image(self, original_path, simulated_image, output_path):
        """Créer une image de comparaison côte à côte"""
        try:
            original = cv2.imread(original_path)
            original_resized = cv2.resize(original, (512, 512))
            simulated_resized = cv2.resize(simulated_image, (512, 512))
            
            # Créer l'image de comparaison
            comparison = np.hstack([original_resized, simulated_resized])
            
            # Ajouter des labels
            cv2.putText(comparison, 'AVANT', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(comparison, 'APRES', (562, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            # Sauvegarder
            cv2.imwrite(output_path, comparison)
            
            return comparison
            
        except Exception as e:
            logger.error(f"Erreur lors de la création de la comparaison: {e}")
            raise


# Instance globale du service
gan_simulation_service = GANSimulationService()




