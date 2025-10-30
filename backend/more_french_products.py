"""
Script pour ajouter encore plus de produits de pharmacies et parfumeries françaises
"""

import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skin_ai.settings')
django.setup()

from recommendations.models import Product

def add_more_french_products():
    """Ajoute encore plus de produits de pharmacies et parfumeries françaises"""
    
    products_data = [
        # PHARMACIE.COM - Produits dermo-cosmétiques
        {
            'name': "Bioderma Sensibio H2O Eau Micellaire",
            'brand': "Bioderma",
            'price': 14.90,
            'description': "Eau micellaire démaquillante pour peaux sensibles",
            'category': 'CLEANSER',
            'target_skin_types': ['SENSITIVE', 'NORMAL'],
            'target_issues': ['sensitivity'],
            'ingredients': "Eau micellaire, Extrait de Cucumis Sativus, Acide Hyaluronique",
            'source': 'Pharmacie.com'
        },
        {
            'name': "Eucerin Hyaluron-Filler + Elasticity Crème Anti-Âge",
            'brand': "Eucerin",
            'price': 28.99,
            'description': "Crème anti-âge avec acide hyaluronique et élastine",
            'category': 'MOISTURIZER',
            'target_skin_types': ['DRY', 'NORMAL'],
            'target_issues': ['aging', 'wrinkles', 'dryness'],
            'ingredients': "Acide Hyaluronique, Élastine, Vitamine E, Glycérine",
            'source': 'Pharmacie.com'
        },
        {
            'name': "Uriage Hyséac Crème Hydratante Matifiante",
            'brand': "Uriage",
            'price': 16.99,
            'description': "Crème hydratante matifiante pour peaux mixtes à grasses",
            'category': 'MOISTURIZER',
            'target_skin_types': ['OILY', 'COMBINATION'],
            'target_issues': ['oily_skin', 'large_pores'],
            'ingredients': "Eau Thermale d'Uriage, Acide Salicylique, Niacinamide",
            'source': 'Pharmacie.com'
        },
        
        # SEPHORA.FR - Marques premium
        {
            'name': "Glow Recipe Watermelon Glow Niacinamide Dew Drops",
            'brand': "Glow Recipe",
            'price': 35.00,
            'description': "Sérum éclat avec niacinamide et extrait de pastèque",
            'category': 'SERUM',
            'target_skin_types': ['NORMAL', 'DRY', 'COMBINATION'],
            'target_issues': ['dullness', 'uneven_skin_tone'],
            'ingredients': "Niacinamide, Extrait de Pastèque, Acide Hyaluronique, Vitamine C",
            'source': 'Sephora.fr'
        },
        {
            'name': "Kiehl's Ultra Facial Cream",
            'brand': "Kiehl's",
            'price': 42.00,
            'description': "Crème hydratante 24h pour tous types de peau",
            'category': 'MOISTURIZER',
            'target_skin_types': ['DRY', 'NORMAL', 'SENSITIVE'],
            'target_issues': ['dryness'],
            'ingredients': "Glycérine, Acide Hyaluronique, Vitamine E, Extrait d'Aloe Vera",
            'source': 'Sephora.fr'
        },
        {
            'name': "Fresh Rose Deep Hydration Face Cream",
            'brand': "Fresh",
            'price': 58.00,
            'description': "Crème hydratante avec extrait de rose et acide hyaluronique",
            'category': 'MOISTURIZER',
            'target_skin_types': ['DRY', 'NORMAL', 'SENSITIVE'],
            'target_issues': ['dryness', 'sensitivity'],
            'ingredients': "Extrait de Rose, Acide Hyaluronique, Vitamine E, Glycérine",
            'source': 'Sephora.fr'
        },
        
        # NOCIBÉ.FR - Marques accessibles
        {
            'name': "L'Oréal Paris Age Perfect Rosy Tone Anti-Âge",
            'brand': "L'Oréal Paris",
            'price': 19.99,
            'description': "Crème anti-âge avec teinte rosée pour un teint éclatant",
            'category': 'MOISTURIZER',
            'target_skin_types': ['NORMAL', 'DRY'],
            'target_issues': ['aging', 'dullness'],
            'ingredients': "Pro-Rétinol, Acide Hyaluronique, Pigments Rosés, Vitamine E",
            'source': 'Nocibé.fr'
        },
        {
            'name': "Maybelline Fit Me Matte + Poreless Foundation",
            'brand': "Maybelline",
            'price': 12.99,
            'description': "Fond de teint matifiant pour peaux mixtes à grasses",
            'category': 'TREATMENT',
            'target_skin_types': ['OILY', 'COMBINATION'],
            'target_issues': ['oily_skin', 'large_pores'],
            'ingredients': "Pigments, Acide Hyaluronique, Vitamine E, SPF 18",
            'source': 'Nocibé.fr'
        },
        
        # MARIONNAUD.FR - Parfumerie
        {
            'name': "Lancôme Advanced Génifique Youth Activating Concentrate",
            'brand': "Lancôme",
            'price': 89.00,
            'description': "Sérum régénérant pour activer la jeunesse de la peau",
            'category': 'SERUM',
            'target_skin_types': ['NORMAL', 'DRY', 'COMBINATION'],
            'target_issues': ['aging', 'wrinkles', 'dullness'],
            'ingredients': "Probiotiques, Acide Hyaluronique, Vitamine C, Peptides",
            'source': 'Marionnaud.fr'
        },
        {
            'name': "Dior Capture Totale Super Potent Rich Cream",
            'brand': "Dior",
            'price': 125.00,
            'description': "Crème anti-âge luxueuse pour peaux matures",
            'category': 'MOISTURIZER',
            'target_skin_types': ['DRY', 'NORMAL'],
            'target_issues': ['aging', 'wrinkles', 'dryness'],
            'ingredients': "Extrait de Rose de Granville, Acide Hyaluronique, Vitamine E",
            'source': 'Marionnaud.fr'
        },
        
        # DOUGLAS.FR - Marques internationales
        {
            'name': "Shiseido Ultimune Power Infusing Concentrate",
            'brand': "Shiseido",
            'price': 95.00,
            'description': "Sérum concentré pour renforcer les défenses naturelles de la peau",
            'category': 'SERUM',
            'target_skin_types': ['NORMAL', 'DRY', 'SENSITIVE'],
            'target_issues': ['sensitivity', 'aging'],
            'ingredients': "Reishi, Gingko Biloba, Acide Hyaluronique, Vitamine E",
            'source': 'Douglas.fr'
        },
        {
            'name': "Chanel Le Lift Crème Anti-Âge",
            'brand': "Chanel",
            'price': 98.00,
            'description': "Crème anti-âge haute performance avec technologie 3D",
            'category': 'MOISTURIZER',
            'target_skin_types': ['NORMAL', 'DRY'],
            'target_issues': ['aging', 'wrinkles'],
            'ingredients': "Extrait de Vanille de Madagascar, Acide Hyaluronique, Peptides",
            'source': 'Douglas.fr'
        },
        
        # LOOKFANTASTIC.FR - Marques spécialisées
        {
            'name': "The Ordinary AHA 30% + BHA 2% Peeling Solution",
            'brand': "The Ordinary",
            'price': 7.20,
            'description': "Solution exfoliante avec AHA et BHA pour un teint lisse",
            'category': 'EXFOLIANT',
            'target_skin_types': ['NORMAL', 'OILY', 'COMBINATION'],
            'target_issues': ['acne', 'blackheads', 'dullness'],
            'ingredients': "AHA 30%, BHA 2%, Acide Hyaluronique, Vitamine B5",
            'source': 'Lookfantastic.fr'
        },
        {
            'name': "Paula's Choice Resist Intensive Repair Cream",
            'brand': "Paula's Choice",
            'price': 45.00,
            'description': "Crème réparatrice intensive pour peaux matures",
            'category': 'MOISTURIZER',
            'target_skin_types': ['DRY', 'NORMAL'],
            'target_issues': ['aging', 'wrinkles', 'dryness'],
            'ingredients': "Rétinol, Acide Hyaluronique, Peptides, Vitamine E",
            'source': 'Lookfantastic.fr'
        },
        
        # FEELUNIQUE.COM - Marques naturelles
        {
            'name': "The Body Shop Vitamin E Moisture Cream",
            'brand': "The Body Shop",
            'price': 18.00,
            'description': "Crème hydratante avec vitamine E pour tous types de peau",
            'category': 'MOISTURIZER',
            'target_skin_types': ['DRY', 'NORMAL', 'SENSITIVE'],
            'target_issues': ['dryness'],
            'ingredients': "Vitamine E, Extrait de Blé, Glycérine, Acide Hyaluronique",
            'source': 'Feelunique.com'
        },
        {
            'name': "Lush Angels On Bare Skin Cleanser",
            'brand': "Lush",
            'price': 15.50,
            'description': "Nettoyant exfoliant naturel avec lavande et amandes",
            'category': 'CLEANSER',
            'target_skin_types': ['NORMAL', 'DRY', 'SENSITIVE'],
            'target_issues': ['dullness', 'dryness'],
            'ingredients': "Amandes, Lavande, Kaolin, Glycérine",
            'source': 'Feelunique.com'
        },
        
        # NOTINO.FR - Marques populaires
        {
            'name': "Nivea Soft Crème Hydratante",
            'brand': "NIVEA",
            'price': 4.99,
            'description': "Crème hydratante douce pour le visage et le corps",
            'category': 'MOISTURIZER',
            'target_skin_types': ['DRY', 'NORMAL', 'SENSITIVE'],
            'target_issues': ['dryness'],
            'ingredients': "Vitamine E, Jojoba, Glycérine, Eau de Rose",
            'source': 'Notino.fr'
        },
        {
            'name': "L'Oréal Paris Pure Clay Masque Purifiant",
            'brand': "L'Oréal Paris",
            'price': 8.99,
            'description': "Masque purifiant à l'argile pour peaux mixtes à grasses",
            'category': 'MASK',
            'target_skin_types': ['OILY', 'COMBINATION'],
            'target_issues': ['oily_skin', 'large_pores', 'blackheads'],
            'ingredients': "Argile Blanche, Argile Rouge, Argile Verte, Eucalyptus",
            'source': 'Notino.fr'
        }
    ]
    
    print("Ajout de produits supplementaires de pharmacies francaises...")
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
    
    return added_count, skipped_count

if __name__ == "__main__":
    add_more_french_products()


