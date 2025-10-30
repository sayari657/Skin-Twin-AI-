"""
Script pour ajouter manuellement des produits Amazon populaires
"""

import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skin_ai.settings')
django.setup()

from recommendations.models import Product

def add_amazon_products():
    """Ajoute des produits Amazon populaires manuellement"""
    
    products_data = [
        {
            'name': "L'Oréal Paris Revitalift Laser X3 Anti-Age Serum + Crème",
            'brand': "L'Oréal Paris",
            'price': 24.99,
            'description': "Routine anti-âge complète avec sérum et crème pour réduire les rides et raffermir la peau",
            'category': 'TREATMENT',
            'target_skin_types': ['NORMAL', 'DRY', 'COMBINATION'],
            'target_issues': ['aging', 'wrinkles'],
            'ingredients': "Pro-Rétinol, Acide Hyaluronique, Vitamine C"
        },
        {
            'name': "L'Oréal Paris Revitalift Filler Sérum Anti-Rides",
            'brand': "L'Oréal Paris", 
            'price': 19.99,
            'description': "Sérum anti-rides avec acide hyaluronique pour combler les rides et hydrater intensément",
            'category': 'SERUM',
            'target_skin_types': ['DRY', 'NORMAL'],
            'target_issues': ['aging', 'wrinkles', 'dryness'],
            'ingredients': "Acide Hyaluronique, Pro-Rétinol, Collagène"
        },
        {
            'name': "LA PROVENÇALE PEPTIDE-ÉCLAT Crème Rose Booster d'Éclat",
            'brand': "LA PROVENÇALE",
            'price': 15.99,
            'description': "Crème anti-fatigue avec peptides et extrait de rose pour un éclat naturel",
            'category': 'MOISTURIZER',
            'target_skin_types': ['NORMAL', 'SENSITIVE'],
            'target_issues': ['dullness', 'fatigue'],
            'ingredients': "Peptides, Extrait de Rose, Vitamine E"
        },
        {
            'name': "LA PROVENÇALE OLEO-JEUNESSE Crème Booster d'Hydratation",
            'brand': "LA PROVENÇALE",
            'price': 18.99,
            'description': "Crème hydratante anti-âge avec huile d'olive vierge et acide hyaluronique",
            'category': 'MOISTURIZER',
            'target_skin_types': ['DRY', 'NORMAL'],
            'target_issues': ['dryness', 'aging'],
            'ingredients': "Huile d'Olive Vierge, Acide Hyaluronique, Oméga 3"
        },
        {
            'name': "Circle FACE MOISTURISE Crème hydratante visage",
            'brand': "Circle",
            'price': 12.99,
            'description': "Crème hydratante quotidienne pour tous types de peau",
            'category': 'MOISTURIZER',
            'target_skin_types': ['DRY', 'NORMAL', 'OILY', 'COMBINATION'],
            'target_issues': ['dryness'],
            'ingredients': "Glycérine, Acide Hyaluronique, Vitamine E"
        },
        {
            'name': "NIVEA Q10 Plus Crème Anti-Âge",
            'brand': "NIVEA",
            'price': 8.99,
            'description': "Crème anti-âge avec Q10 et créatine pour raffermir la peau",
            'category': 'MOISTURIZER',
            'target_skin_types': ['NORMAL', 'DRY'],
            'target_issues': ['aging', 'wrinkles'],
            'ingredients': "Q10, Créatine, Vitamine E"
        },
        {
            'name': "Garnier SkinActive Hydra Bomb Crème Hydratante",
            'brand': "Garnier",
            'price': 6.99,
            'description': "Crème hydratante 24h avec acide hyaluronique pour une hydratation intense",
            'category': 'MOISTURIZER',
            'target_skin_types': ['DRY', 'NORMAL'],
            'target_issues': ['dryness'],
            'ingredients': "Acide Hyaluronique, Glycérine, Eau de Rose"
        },
        {
            'name': "Vichy LiftActiv Supreme Sérum Anti-Âge",
            'brand': "Vichy",
            'price': 29.99,
            'description': "Sérum anti-âge haute performance avec rhamnose et acide hyaluronique",
            'category': 'SERUM',
            'target_skin_types': ['NORMAL', 'DRY'],
            'target_issues': ['aging', 'wrinkles'],
            'ingredients': "Rhamnose, Acide Hyaluronique, Eau Thermale de Vichy"
        },
        {
            'name': "La Roche-Posay Effaclar Duo+ Crème Anti-Imperfections",
            'brand': "La Roche-Posay",
            'price': 16.99,
            'description': "Crème traitante pour peaux à tendance acnéique avec niacinamide",
            'category': 'TREATMENT',
            'target_skin_types': ['OILY', 'COMBINATION'],
            'target_issues': ['acne', 'imperfections'],
            'ingredients': "Niacinamide, Acide Salicylique, Procerad"
        },
        {
            'name': "Avène Hydrance Optimale Crème Hydratante",
            'brand': "Avène",
            'price': 22.99,
            'description': "Crème hydratante apaisante pour peaux sensibles avec eau thermale",
            'category': 'MOISTURIZER',
            'target_skin_types': ['SENSITIVE', 'DRY'],
            'target_issues': ['sensitivity', 'dryness'],
            'ingredients': "Eau Thermale d'Avène, Acide Hyaluronique, Vitamine E"
        }
    ]
    
    print("Ajout des produits Amazon populaires...")
    print("=" * 50)
    
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
            
            print(f"Produit ajoute: {product.name[:40]}...")
            added_count += 1
            
        except Exception as e:
            print(f"Erreur lors de l'ajout du produit {product_data['name']}: {e}")
            continue
    
    print("=" * 50)
    print(f"Resume: {added_count} produits ajoutes, {skipped_count} produits ignores")
    print(f"Total produits dans la base: {Product.objects.count()}")
    
    return added_count, skipped_count

if __name__ == "__main__":
    add_amazon_products()


