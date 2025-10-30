"""
Moteur de recommandation de produits cosmétiques
"""
import logging
from typing import List, Dict, Any
from .models import Product, Recommendation
from detection.models import SkinAnalysis

logger = logging.getLogger(__name__)


class ProductRecommender:
    """Moteur de recommandation de produits"""
    
    def __init__(self):
        self.products = Product.objects.filter(is_active=True)
    
    def get_recommendations(self, skin_analysis: SkinAnalysis, limit: int = 10) -> List[Dict[str, Any]]:
        """Obtenir des recommandations basées sur l'analyse de peau"""
        try:
            recommendations = []
            
            for product in self.products:
                score, reasons = self._calculate_relevance_score(skin_analysis, product)
                
                if score > 30:  # Seuil minimum de pertinence
                    recommendations.append({
                        'product': product,
                        'relevance_score': score,
                        'confidence_score': self._calculate_confidence_score(skin_analysis, product),
                        'reasons': reasons
                    })
            
            # Trier par score de pertinence
            recommendations.sort(key=lambda x: x['relevance_score'], reverse=True)
            
            # Limiter le nombre de recommandations
            return recommendations[:limit]
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération des recommandations: {e}")
            return []
    
    def _calculate_relevance_score(self, skin_analysis: SkinAnalysis, product: Product) -> tuple:
        """Calculer le score de pertinence d'un produit"""
        score = 0
        reasons = []
        
        # Score basé sur le type de peau
        skin_type_score = self._calculate_skin_type_score(skin_analysis, product)
        score += skin_type_score[0]
        if skin_type_score[1]:
            reasons.extend(skin_type_score[1])
        
        # Score basé sur les problèmes détectés
        issues_score = self._calculate_issues_score(skin_analysis, product)
        score += issues_score[0]
        if issues_score[1]:
            reasons.extend(issues_score[1])
        
        # Score basé sur la catégorie de produit
        category_score = self._calculate_category_score(skin_analysis, product)
        score += category_score[0]
        if category_score[1]:
            reasons.extend(category_score[1])
        
        # Normaliser le score entre 0 et 100
        score = min(score, 100)
        
        return score, reasons
    
    def _calculate_skin_type_score(self, skin_analysis: SkinAnalysis, product: Product) -> tuple:
        """Calculer le score basé sur le type de peau"""
        score = 0
        reasons = []
        
        predicted_skin_type = skin_analysis.skin_type_prediction
        target_skin_types = product.target_skin_types
        
        if predicted_skin_type in target_skin_types:
            score += 40
            reasons.append('skin_type_match')
        elif predicted_skin_type and target_skin_types:
            # Score partiel si le type de peau est compatible
            score += 20
            reasons.append('skin_type_compatible')
        
        return score, reasons
    
    def _calculate_issues_score(self, skin_analysis: SkinAnalysis, product: Product) -> tuple:
        """Calculer le score basé sur les problèmes détectés"""
        score = 0
        reasons = []
        
        target_issues = product.target_issues
        
        # Acné
        if skin_analysis.acne_detected and 'acne' in target_issues:
            score += 30
            reasons.append('acne_treatment')
        
        # Rides
        if skin_analysis.wrinkles_detected and 'wrinkles' in target_issues:
            score += 25
            reasons.append('wrinkle_treatment')
        
        # Taches sombres
        if skin_analysis.dark_spots_detected and 'dark_spots' in target_issues:
            score += 25
            reasons.append('dark_spot_treatment')
        
        # Rougeurs
        if skin_analysis.redness_detected and 'redness' in target_issues:
            score += 20
            reasons.append('redness_treatment')
        
        return score, reasons
    
    def _calculate_category_score(self, skin_analysis: SkinAnalysis, product: Product) -> tuple:
        """Calculer le score basé sur la catégorie de produit"""
        score = 0
        reasons = []
        
        category = product.category
        
        # Prioriser certaines catégories selon les problèmes
        if skin_analysis.acne_detected and category in ['CLEANSER', 'TREATMENT', 'EXFOLIANT']:
            score += 15
            reasons.append('acne_category_match')
        
        if skin_analysis.wrinkles_detected and category in ['SERUM', 'TREATMENT', 'MOISTURIZER']:
            score += 15
            reasons.append('anti_aging_category_match')
        
        if skin_analysis.dark_spots_detected and category in ['SERUM', 'TREATMENT', 'SUNSCREEN']:
            score += 15
            reasons.append('pigmentation_category_match')
        
        # Score de base pour les catégories essentielles
        if category in ['CLEANSER', 'MOISTURIZER', 'SUNSCREEN']:
            score += 10
            reasons.append('essential_category')
        
        return score, reasons
    
    def _calculate_confidence_score(self, skin_analysis: SkinAnalysis, product: Product) -> float:
        """Calculer le score de confiance de la recommandation"""
        confidence = 0.5  # Score de base
        
        # Augmenter la confiance si l'analyse est récente
        if skin_analysis.skin_type_confidence and skin_analysis.skin_type_confidence > 0.8:
            confidence += 0.2
        
        # Augmenter la confiance si plusieurs problèmes correspondent
        matching_issues = 0
        target_issues = product.target_issues
        
        if skin_analysis.acne_detected and 'acne' in target_issues:
            matching_issues += 1
        if skin_analysis.wrinkles_detected and 'wrinkles' in target_issues:
            matching_issues += 1
        if skin_analysis.dark_spots_detected and 'dark_spots' in target_issues:
            matching_issues += 1
        if skin_analysis.redness_detected and 'redness' in target_issues:
            matching_issues += 1
        
        confidence += matching_issues * 0.1
        
        return min(confidence, 1.0)
    
    def save_recommendations(self, skin_analysis: SkinAnalysis, recommendations: List[Dict[str, Any]]):
        """Sauvegarder les recommandations en base"""
        try:
            for rec in recommendations:
                Recommendation.objects.create(
                    user=skin_analysis.user,
                    skin_analysis=skin_analysis,
                    product=rec['product'],
                    relevance_score=rec['relevance_score'],
                    confidence_score=rec['confidence_score'],
                    reasons=rec['reasons']
                )
            
            logger.info(f"Recommandations sauvegardées pour l'analyse {skin_analysis.id}")
            
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde des recommandations: {e}")
            raise


# Instance globale du recommandateur
product_recommender = ProductRecommender()




