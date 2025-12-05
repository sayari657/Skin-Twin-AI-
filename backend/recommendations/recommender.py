"""
Moteur de recommandation de produits cosmétiques
"""
import logging
from typing import List, Dict, Any
from .models import Product, Recommendation
from detection.models import SkinAnalysis
from scraped_products.models import ScrapedProduct

logger = logging.getLogger(__name__)


def convert_scraped_to_product(scraped_product):
    """Convertit un ScrapedProduct en format Product pour le système de recommandation"""
    # Créer un objet Product factice avec les mêmes attributs
    class FakeProduct:
        def __init__(self, scraped):
            self.id = scraped.id + 1000000  # Offset pour éviter les conflits
            self.name = scraped.name
            self.brand = scraped.brand
            self.description = scraped.description or scraped.name
            self.ingredients = scraped.ingredients or ''
            self.price = scraped.price
            self.size = scraped.size
            self.category = scraped.category
            self.target_skin_types = scraped.target_skin_types or ['NORMAL']
            self.target_issues = scraped.target_issues or []
            self.image = scraped.image
            self.is_active = scraped.is_active
    
    return FakeProduct(scraped_product)


class ProductRecommender:
    """Moteur de recommandation de produits"""
    
    def __init__(self):
        self._load_products()
    
    def _load_products(self):
        """Recharger les produits depuis la base de données et les produits scrapés"""
        # Charger les produits de la base de données
        self.db_products = Product.objects.filter(is_active=True)
        # Charger les produits scrapés
        self.scraped_products = ScrapedProduct.objects.filter(is_active=True)
        
        # Convertir les produits scrapés en format Product
        self.products = list(self.db_products) + [
            convert_scraped_to_product(sp) for sp in self.scraped_products
        ]
    
    def get_recommendations(self, skin_analysis: SkinAnalysis, limit: int = 10) -> List[Dict[str, Any]]:
        """Obtenir des recommandations basées sur l'analyse de peau"""
        try:
            # Recharger les produits pour avoir les plus récents
            self._load_products()
            
            recommendations = []
            seen_products = set()  # Pour éviter les doublons basés sur nom+marque
            
            for product in self.products:
                # Créer une clé unique pour éviter les doublons exacts
                product_key = (
                    (product.name or '').lower().strip(),
                    (product.brand or '').lower().strip(),
                    product.category or ''
                )
                
                # Si on a déjà vu ce produit exact, passer au suivant
                if product_key in seen_products:
                    continue
                
                score, reasons = self._calculate_relevance_score(skin_analysis, product)
                
                if score > 30:  # Seuil minimum de pertinence
                    recommendations.append({
                        'product': product,
                        'relevance_score': score,
                        'confidence_score': self._calculate_confidence_score(skin_analysis, product),
                        'reasons': reasons
                    })
                    seen_products.add(product_key)
            
            # Trier par score de pertinence
            recommendations.sort(key=lambda x: x['relevance_score'], reverse=True)
            
            # Diversifier les sources : essayer d'avoir des produits de différents sites
            # Grouper par nom+marque pour diversifier
            diversified_recommendations = []
            product_groups = {}
            
            for rec in recommendations:
                product = rec['product']
                # Créer une clé de groupe basée sur nom+marque (sans tenir compte du site)
                group_key = (
                    (product.name or '').lower().strip()[:50],  # Limiter la longueur
                    (product.brand or '').lower().strip()
                )
                
                if group_key not in product_groups:
                    product_groups[group_key] = []
                product_groups[group_key].append(rec)
            
            # Prendre le meilleur produit de chaque groupe, mais aussi diversifier les sources
            source_count = {}
            for group_key, group_recs in product_groups.items():
                # Trier les produits du groupe par score
                group_recs.sort(key=lambda x: x['relevance_score'], reverse=True)
                
                # Prendre le meilleur produit du groupe
                best_rec = group_recs[0]
                diversified_recommendations.append(best_rec)
                
                # Si on a encore de la place, ajouter d'autres produits du même groupe mais de sites différents
                if len(diversified_recommendations) < limit * 2:  # Prendre 2x plus pour avoir du choix
                    for rec in group_recs[1:]:
                        product = rec['product']
                        # Vérifier si c'est un produit scrapé pour obtenir son source_site
                        source = 'unknown'
                        if hasattr(product, 'id') and product.id >= 1000000:
                            try:
                                from scraped_products.models import ScrapedProduct
                                scraped_id = product.id - 1000000
                                scraped_product = ScrapedProduct.objects.get(id=scraped_id)
                                source = scraped_product.source_site or 'unknown'
                            except:
                                pass
                        
                        # Ajouter si c'est d'un site différent ou si on n'a pas encore assez de produits
                        if source not in source_count or source_count[source] < 3:
                            diversified_recommendations.append(rec)
                            source_count[source] = source_count.get(source, 0) + 1
                            if len(diversified_recommendations) >= limit * 2:
                                break
            
            # Trier à nouveau et limiter
            diversified_recommendations.sort(key=lambda x: x['relevance_score'], reverse=True)
            return diversified_recommendations[:limit]
            
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




