"""
Script pour ajouter des produits de pharmacies et parfumeries françaises
"""

import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skin_ai.settings')
django.setup()

from recommendations.models import Product

def add_french_pharmacy_products():
    """Ajoute des produits de pharmacies et parfumeries françaises"""
    
    products_data = [
        # PHARMACIE.COM
        {
            'name': "La Roche-Posay Effaclar Duo+ Crème Anti-Imperfections",
            'brand': "La Roche-Posay",
            'price': 16.99,
            'description': "Crème traitante pour peaux à tendance acnéique avec niacinamide et acide salicylique",
            'category': 'TREATMENT',
            'target_skin_types': ['OILY', 'COMBINATION'],
            'target_issues': ['acne', 'imperfections'],
            'ingredients': "Niacinamide, Acide Salicylique, Procerad, Eau Thermale de La Roche-Posay",
            'source': 'Pharmacie.com'
        },
        {
            'name': "Avène Hydrance Optimale Crème Hydratante",
            'brand': "Avène",
            'price': 22.99,
            'description': "Crème hydratante apaisante pour peaux sensibles avec eau thermale d'Avène",
            'category': 'MOISTURIZER',
            'target_skin_types': ['SENSITIVE', 'DRY'],
            'target_issues': ['sensitivity', 'dryness'],
            'ingredients': "Eau Thermale d'Avène, Acide Hyaluronique, Vitamine E, Glycérine",
            'source': 'Pharmacie.com'
        },
        {
            'name': "Vichy LiftActiv Supreme Sérum Anti-Âge",
            'brand': "Vichy",
            'price': 29.99,
            'description': "Sérum anti-âge haute performance avec rhamnose et acide hyaluronique",
            'category': 'SERUM',
            'target_skin_types': ['NORMAL', 'DRY'],
            'target_issues': ['aging', 'wrinkles'],
            'ingredients': "Rhamnose, Acide Hyaluronique, Eau Thermale de Vichy, Vitamine C",
            'source': 'Pharmacie.com'
        },
        
        # SEPHORA.FR
        {
            'name': "The Ordinary Niacinamide 10% + Zinc 1%",
            'brand': "The Ordinary",
            'price': 6.90,
            'description': "Sérum purifiant avec niacinamide pour réduire les imperfections et contrôler le sébum",
            'category': 'SERUM',
            'target_skin_types': ['OILY', 'COMBINATION'],
            'target_issues': ['acne', 'oily_skin'],
            'ingredients': "Niacinamide 10%, Zinc PCA 1%, Acide Hyaluronique",
            'source': 'Sephora.fr'
        },
        {
            'name': "Drunk Elephant C-Firma Vitamin C Day Serum",
            'brand': "Drunk Elephant",
            'price': 78.00,
            'description': "Sérum vitaminé C pour éclaircir et uniformiser le teint",
            'category': 'SERUM',
            'target_skin_types': ['NORMAL', 'DRY', 'COMBINATION'],
            'target_issues': ['dark_spots', 'dullness'],
            'ingredients': "Vitamine C 15%, Acide Ferulique, Vitamine E, Acide Hyaluronique",
            'source': 'Sephora.fr'
        },
        {
            'name': "Fenty Skin Fat Water Pore-Refining Toner Serum",
            'brand': "Fenty Skin",
            'price': 32.00,
            'description': "Tonique-sérum pour affiner les pores et hydrater la peau",
            'category': 'TONER',
            'target_skin_types': ['OILY', 'COMBINATION'],
            'target_issues': ['large_pores', 'oily_skin'],
            'ingredients': "Niacinamide, Acide Hyaluronique, Extrait de Figue de Barbarie",
            'source': 'Sephora.fr'
        },
        
        # NOCIBÉ.FR
        {
            'name': "L'Oréal Paris Revitalift Laser X3 Anti-Âge",
            'brand': "L'Oréal Paris",
            'price': 24.99,
            'description': "Routine anti-âge complète avec sérum et crème pour réduire les rides",
            'category': 'TREATMENT',
            'target_skin_types': ['NORMAL', 'DRY', 'COMBINATION'],
            'target_issues': ['aging', 'wrinkles'],
            'ingredients': "Pro-Rétinol, Acide Hyaluronique, Vitamine C, Peptides",
            'source': 'Nocibé.fr'
        },
        {
            'name': "Garnier SkinActive Hydra Bomb Crème Hydratante",
            'brand': "Garnier",
            'price': 6.99,
            'description': "Crème hydratante 24h avec acide hyaluronique pour une hydratation intense",
            'category': 'MOISTURIZER',
            'target_skin_types': ['DRY', 'NORMAL'],
            'target_issues': ['dryness'],
            'ingredients': "Acide Hyaluronique, Glycérine, Eau de Rose, Vitamine E",
            'source': 'Nocibé.fr'
        },
        
        # MARIONNAUD.FR
        {
            'name': "NIVEA Q10 Plus Crème Anti-Âge",
            'brand': "NIVEA",
            'price': 8.99,
            'description': "Crème anti-âge avec Q10 et créatine pour raffermir la peau",
            'category': 'MOISTURIZER',
            'target_skin_types': ['NORMAL', 'DRY'],
            'target_issues': ['aging', 'wrinkles'],
            'ingredients': "Q10, Créatine, Vitamine E, Acide Hyaluronique",
            'source': 'Marionnaud.fr'
        },
        {
            'name': "Maybelline New York Dream Fresh BB Cream",
            'brand': "Maybelline",
            'price': 9.99,
            'description': "BB crème hydratante avec protection SPF pour un teint unifié",
            'category': 'MOISTURIZER',
            'target_skin_types': ['NORMAL', 'DRY', 'COMBINATION'],
            'target_issues': ['dryness', 'uneven_skin_tone'],
            'ingredients': "SPF 30, Acide Hyaluronique, Vitamine E, Glycérine",
            'source': 'Marionnaud.fr'
        },
        
        # DOUGLAS.FR
        {
            'name': "Estée Lauder Advanced Night Repair Synchronized Multi-Recovery Complex",
            'brand': "Estée Lauder",
            'price': 95.00,
            'description': "Sérum de nuit réparateur pour tous types de peau",
            'category': 'SERUM',
            'target_skin_types': ['NORMAL', 'DRY', 'COMBINATION', 'SENSITIVE'],
            'target_issues': ['aging', 'wrinkles', 'dullness'],
            'ingredients': "Chronolux Power Signal Technology, Acide Hyaluronique, Peptides",
            'source': 'Douglas.fr'
        },
        {
            'name': "Clinique Dramatically Different Moisturizing Lotion+",
            'brand': "Clinique",
            'price': 32.00,
            'description': "Lotion hydratante légère pour peaux mixtes à grasses",
            'category': 'MOISTURIZER',
            'target_skin_types': ['OILY', 'COMBINATION'],
            'target_issues': ['oily_skin', 'dryness'],
            'ingredients': "Glycérine, Acide Hyaluronique, Vitamine E, Extrait d'Aloe Vera",
            'source': 'Douglas.fr'
        },
        
        # LOOKFANTASTIC.FR
        {
            'name': "The Ordinary Hyaluronic Acid 2% + B5",
            'brand': "The Ordinary",
            'price': 6.80,
            'description': "Sérum hydratant avec acide hyaluronique pour une hydratation intense",
            'category': 'SERUM',
            'target_skin_types': ['DRY', 'NORMAL', 'SENSITIVE'],
            'target_issues': ['dryness'],
            'ingredients': "Acide Hyaluronique 2%, Vitamine B5, Glycérine",
            'source': 'Lookfantastic.fr'
        },
        {
            'name': "Paula's Choice Skin Perfecting 2% BHA Liquid Exfoliant",
            'brand': "Paula's Choice",
            'price': 32.00,
            'description': "Exfoliant liquide avec acide salicylique pour unifier le teint",
            'category': 'EXFOLIANT',
            'target_skin_types': ['OILY', 'COMBINATION'],
            'target_issues': ['acne', 'large_pores', 'blackheads'],
            'ingredients': "Acide Salicylique 2%, Acide Hyaluronique, Extrait de Thé Vert",
            'source': 'Lookfantastic.fr'
        },
        
        # FEELUNIQUE.COM
        {
            'name': "CeraVe Foaming Facial Cleanser",
            'brand': "CeraVe",
            'price': 12.99,
            'description': "Nettoyant moussant pour peaux normales à grasses",
            'category': 'CLEANSER',
            'target_skin_types': ['OILY', 'COMBINATION', 'NORMAL'],
            'target_issues': ['oily_skin', 'acne'],
            'ingredients': "Céramides, Acide Hyaluronique, Niacinamide, Acide Salicylique",
            'source': 'Feelunique.com'
        },
        {
            'name': "The Inkey List Retinol Anti-Aging Serum",
            'brand': "The Inkey List",
            'price': 9.99,
            'description': "Sérum anti-âge avec rétinol pour réduire les rides",
            'category': 'SERUM',
            'target_skin_types': ['NORMAL', 'DRY', 'COMBINATION'],
            'target_issues': ['aging', 'wrinkles'],
            'ingredients': "Rétinol 1%, Acide Hyaluronique, Squalane, Peptides",
            'source': 'Feelunique.com'
        },
        
        # NOTINO.FR
        {
            'name': "Olay Regenerist Micro-Sculpting Cream",
            'brand': "Olay",
            'price': 18.99,
            'description': "Crème anti-âge avec peptides et niacinamide",
            'category': 'MOISTURIZER',
            'target_skin_types': ['NORMAL', 'DRY'],
            'target_issues': ['aging', 'wrinkles'],
            'ingredients': "Peptides, Niacinamide, Acide Hyaluronique, Vitamine E",
            'source': 'Notino.fr'
        },
        {
            'name': "Neutrogena Hydro Boost Water Gel",
            'brand': "Neutrogena",
            'price': 14.99,
            'description': "Gel hydratant avec acide hyaluronique pour une hydratation 24h",
            'category': 'MOISTURIZER',
            'target_skin_types': ['DRY', 'NORMAL', 'SENSITIVE'],
            'target_issues': ['dryness'],
            'ingredients': "Acide Hyaluronique, Glycérine, Vitamine E, Extrait d'Aloe Vera",
            'source': 'Notino.fr'
        }
    ]
    
    print("Ajout des produits de pharmacies et parfumeries françaises...")
    print("=" * 60)
    
    added_count = 0
    skipped_count = 0
    
    for product_data in products_data:
        try:
            # Vérifier si le produit existe déjà
            existing_product = Product.objects.filter(
                name=product_data['name'],
                brand=product_data['brand']
            ).first()
            
            if existing_product:
                print(f"Produit deja existant: {product_data['name'][:40]}...")
                skipped_count += 1
                continue
            
            # Créer le nouveau produit
            product = Product.objects.create(
                name=product_data['name'],
                brand=product_data['brand'],
                price=product_data['price'],
                description=product_data['description'],
                ingredients=product_data['ingredients'],
                category=product_data['category'],
                target_skin_types=product_data['target_skin_types'],
                target_issues=product_data['target_issues']
            )
            
            print(f"Produit ajoute ({product_data['source']}): {product.name[:40]}...")
            added_count += 1
            
        except Exception as e:
            print(f"Erreur lors de l'ajout du produit {product_data['name']}: {e}")
            continue
    
    print("=" * 60)
    print(f"Resume: {added_count} produits ajoutes, {skipped_count} produits ignores")
    print(f"Total produits dans la base: {Product.objects.count()}")
    
    # Afficher la répartition par source
    print("\nRepartition par source:")
    sources = {}
    for product in Product.objects.all():
        # Pour les produits existants, on ne peut pas déterminer la source
        # mais on peut afficher les nouvelles sources
        pass
    
    return added_count, skipped_count

if __name__ == "__main__":
    add_french_pharmacy_products()


