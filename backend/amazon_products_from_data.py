"""
Script pour ajouter les produits Amazon basés sur les données fournies
"""

import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skin_ai.settings')
django.setup()

from recommendations.models import Product

def add_amazon_products_from_data():
    """Ajoute les produits Amazon basés sur les données fournies"""
    
    products_data = [
        # Produits sponsorisés
        {
            'name': "Tiege Hanley Ensemble de soins de la peau pour homme - Routine de rajeunissement (niveau 5)",
            'brand': "Tiege Hanley",
            'price': 0.0,  # Prix non spécifié
            'description': "Ensemble complet de soins pour homme avec lavage, gommage, hydratant, crème yeux, sérum, masque argile et bâton rétinol",
            'category': 'TREATMENT',
            'target_skin_types': ['NORMAL', 'DRY', 'COMBINATION'],
            'target_issues': ['aging', 'wrinkles'],
            'ingredients': "Rétinol, Acide Hyaluronique, Argile, Vitamines",
            'source': 'Amazon.fr'
        },
        {
            'name': "NIVEA MEN Active Age Soin de Jour Anti-Âge Complet (1 x 50 ml)",
            'brand': "NIVEA MEN",
            'price': 11.99,
            'description': "Soin visage enrichi en créatine et caféine, crème homme 6-en-1 hydratant & anti-âge à la texture légère",
            'category': 'MOISTURIZER',
            'target_skin_types': ['NORMAL', 'DRY', 'COMBINATION'],
            'target_issues': ['aging', 'wrinkles'],
            'ingredients': "Créatine, Caféine, Acide Hyaluronique, Vitamine E",
            'source': 'Amazon.fr'
        },
        {
            'name': "NIVEA Luminous 630 - Serum Visage Anti-Âge & Anti-Taches",
            'brand': "NIVEA",
            'price': 17.71,
            'description': "Combleur de rides profond & booster de collagène avec Thiamidol breveté & acide hyaluronique pour tous types de peaux",
            'category': 'SERUM',
            'target_skin_types': ['NORMAL', 'DRY', 'COMBINATION', 'SENSITIVE'],
            'target_issues': ['aging', 'wrinkles', 'dark_spots'],
            'ingredients': "Thiamidol, Acide Hyaluronique, Collagène, Vitamine C",
            'source': 'Amazon.fr'
        },
        {
            'name': "Sérum Visage Vitamine C 20% – Format XL 50ml avec Acide Hyaluronique et Vitamine E",
            'brand': "KLEEM ORGANICS",
            'price': 0.0,  # Prix non spécifié
            'description': "Anti-âge, anti-rides, anti-taches, hydratant éclaircissant pour peaux sensibles & tous types de peaux",
            'category': 'SERUM',
            'target_skin_types': ['NORMAL', 'DRY', 'SENSITIVE'],
            'target_issues': ['aging', 'wrinkles', 'dark_spots', 'dullness'],
            'ingredients': "Vitamine C 20%, Acide Hyaluronique, Vitamine E",
            'source': 'Amazon.fr'
        },
        {
            'name': "Brickell Men's Products Nettoyant Visage Purifiant au Charbon",
            'brand': "Brickell Men's Products",
            'price': 0.0,  # Prix non spécifié
            'description': "Nettoyant visage naturel et bio au charbon pour hommes",
            'category': 'CLEANSER',
            'target_skin_types': ['OILY', 'COMBINATION'],
            'target_issues': ['oily_skin', 'large_pores'],
            'ingredients': "Charbon Actif, Extrait d'Aloe Vera, Vitamine E",
            'source': 'Amazon.fr'
        },
        {
            'name': "L'OCCITANE - Crème Ultra Riche Corps Karité - Peaux sèches et sensibles",
            'brand': "L'OCCITANE",
            'price': 0.0,  # Prix non spécifié
            'description': "Crème ultra riche au karité pour peaux sèches et sensibles, fabriquée en France",
            'category': 'MOISTURIZER',
            'target_skin_types': ['DRY', 'SENSITIVE'],
            'target_issues': ['dryness', 'sensitivity'],
            'ingredients': "Beurre de Karité, Vitamine E, Extrait de Lavande",
            'source': 'Amazon.fr'
        },
        
        # Produits populaires
        {
            'name': "GARNIER Skin Active - Solution Micellaire Tout-En-1",
            'brand': "Garnier",
            'price': 3.03,
            'description': "Nettoie, démaquille & hydrate avec micelles & glycérine hydratante, sans parfum, pour peaux sèches & sensibles",
            'category': 'CLEANSER',
            'target_skin_types': ['DRY', 'SENSITIVE'],
            'target_issues': ['dryness', 'sensitivity'],
            'ingredients': "Micelles, Glycérine, Eau Thermale",
            'source': 'Amazon.fr'
        },
        {
            'name': "Mixa Expert Peau Sensible - Crème Cica Réparation",
            'brand': "Mixa",
            'price': 6.33,
            'description': "Réparation effet longue durée pour peaux très sèches et rugueuses, hypoallergénique",
            'category': 'MOISTURIZER',
            'target_skin_types': ['DRY', 'SENSITIVE'],
            'target_issues': ['dryness', 'sensitivity'],
            'ingredients': "Cica, Acide Hyaluronique, Vitamine E, Glycérine",
            'source': 'Amazon.fr'
        },
        {
            'name': "GARNIER Skin Active - Sérum Éclat - Anti-Tache Brunes",
            'brand': "Garnier",
            'price': 9.68,
            'description': "Soin visage enrichi en 3.5-4% niacinamide, vitamine C & acide salicylique, vegan & cruelty free",
            'category': 'SERUM',
            'target_skin_types': ['NORMAL', 'DRY', 'COMBINATION'],
            'target_issues': ['dark_spots', 'dullness'],
            'ingredients': "Niacinamide 3.5-4%, Vitamine C, Acide Salicylique",
            'source': 'Amazon.fr'
        },
        {
            'name': "Mixa Intensif Peaux Sèches - La Crème des Peaux Très Sèches et Ternes",
            'brand': "Mixa",
            'price': 5.09,
            'description': "Multi usages visage, corps, mains, pieds - nourrit 48h et ravive l'éclat, hypoallergénique",
            'category': 'MOISTURIZER',
            'target_skin_types': ['DRY'],
            'target_issues': ['dryness', 'dullness'],
            'ingredients': "Glycérine, Acide Hyaluronique, Vitamine E, Huiles Nourrissantes",
            'source': 'Amazon.fr'
        },
        {
            'name': "L'Oréal Paris - Revitalift - Soin Anti-Âge Hydratant & Raffermissant",
            'brand': "L'Oréal Paris",
            'price': 6.11,
            'description': "Crème de jour anti-rides & extra-fermeté enrichie en pro-rétinol pour tous types de peaux",
            'category': 'MOISTURIZER',
            'target_skin_types': ['NORMAL', 'DRY', 'COMBINATION'],
            'target_issues': ['aging', 'wrinkles'],
            'ingredients': "Pro-Rétinol, Acide Hyaluronique, Vitamine E",
            'source': 'Amazon.fr'
        },
        {
            'name': "Mixa - Sérum Booster d'Hydratation Hyalurogel",
            'brand': "Mixa",
            'price': 6.00,
            'description': "Pour peaux sensibles déshydratées - hydratant 24h, repulpant à l'acide hyaluronique pur, vitamines B3 + B5",
            'category': 'SERUM',
            'target_skin_types': ['DRY', 'SENSITIVE'],
            'target_issues': ['dryness'],
            'ingredients': "Acide Hyaluronique Pur, Vitamine B3, Vitamine B5, Glycérine",
            'source': 'Amazon.fr'
        },
        {
            'name': "Topicrem - Ultra Hydratant Lait Corps",
            'brand': "Topicrem",
            'price': 8.89,
            'description': "Hydrate 48h, relipide, protège la peau - texture onctueuse, odeur délicate pour peaux sensibles, fabrication française",
            'category': 'MOISTURIZER',
            'target_skin_types': ['DRY', 'SENSITIVE'],
            'target_issues': ['dryness', 'sensitivity'],
            'ingredients': "Acide Hyaluronique, Glycérine, Vitamine E, Extrait d'Aloe Vera",
            'source': 'Amazon.fr'
        },
        {
            'name': "Cattier gommage argile blanche aloe vera",
            'brand': "Cattier",
            'price': 3.90,
            'description': "Gommage à l'argile blanche et aloe vera pour tous types de peaux",
            'category': 'EXFOLIANT',
            'target_skin_types': ['NORMAL', 'DRY', 'OILY', 'COMBINATION'],
            'target_issues': ['dullness', 'large_pores'],
            'ingredients': "Argile Blanche, Extrait d'Aloe Vera, Vitamine E",
            'source': 'Amazon.fr'
        },
        
        # Produits de traitement
        {
            'name': "GARNIER Pure Active - Patch Bouton Pack XXL",
            'brand': "Garnier",
            'price': 11.99,
            'description': "Réduit l'apparence des boutons en 8H, cliniquement prouvé, invisible & ultra-fin, technologie hydrocolloïde",
            'category': 'TREATMENT',
            'target_skin_types': ['OILY', 'COMBINATION'],
            'target_issues': ['acne'],
            'ingredients': "Technologie Hydrocolloïde, Acide Salicylique",
            'source': 'Amazon.fr'
        },
        {
            'name': "Hero Cosmetics Mighty Patch Original – Patch Bouton Nuit",
            'brand': "Hero Cosmetics",
            'price': 10.50,
            'description': "Résultats en 6H, technologie hydrocolloïde, absorbe les impuretés & réduit les boutons",
            'category': 'TREATMENT',
            'target_skin_types': ['OILY', 'COMBINATION'],
            'target_issues': ['acne'],
            'ingredients': "Technologie Hydrocolloïde, Acide Salicylique",
            'source': 'Amazon.fr'
        },
        {
            'name': "L'Oréal Paris - CC Crème 5-en-1 - Crème Universelle Anti-Rougeurs",
            'brand': "L'Oréal Paris",
            'price': 11.09,
            'description': "Enrichie en vitamines B5 et E, hydratation 24H, pour peaux sensibles et peaux grasses",
            'category': 'MOISTURIZER',
            'target_skin_types': ['SENSITIVE', 'OILY', 'COMBINATION'],
            'target_issues': ['redness', 'sensitivity'],
            'ingredients': "Vitamine B5, Vitamine E, Acide Hyaluronique, SPF",
            'source': 'Amazon.fr'
        },
        {
            'name': "Dr. Althea 345 Relief Cream, Gel Crème Hydratant à la Niacinamide et au Panthénol",
            'brand': "Dr. Althea",
            'price': 31.28,
            'description': "Gel crème hydratant à la niacinamide et au panthénol pour peaux sensibles",
            'category': 'MOISTURIZER',
            'target_skin_types': ['SENSITIVE', 'DRY'],
            'target_issues': ['sensitivity', 'dryness'],
            'ingredients': "Niacinamide, Panthénol, Acide Hyaluronique, Glycérine",
            'source': 'Amazon.fr'
        },
        {
            'name': "Garnier Pure Active - Nettoyant 3 En 1",
            'brand': "Garnier",
            'price': 4.35,
            'description': "Nettoyant, exfoliant, masque - réduit les points noirs & prévient leur apparition avec BHA & charbon",
            'category': 'CLEANSER',
            'target_skin_types': ['OILY', 'COMBINATION'],
            'target_issues': ['acne', 'large_pores', 'blackheads'],
            'ingredients': "BHA, Charbon, Acide Salicylique, Glycérine",
            'source': 'Amazon.fr'
        },
        {
            'name': "Topicrem - CICA+, Crème Apaisante au Zinc et à l'Acide Hyaluronique",
            'brand': "Topicrem",
            'price': 4.89,
            'description': "Apaise les irritations cutanées, soin pour peau sensible, bébé, enfant, adulte, fondante, sans parfum",
            'category': 'MOISTURIZER',
            'target_skin_types': ['SENSITIVE'],
            'target_issues': ['sensitivity', 'redness'],
            'ingredients': "Zinc, Acide Hyaluronique, Cica, Glycérine",
            'source': 'Amazon.fr'
        }
    ]
    
    print("Ajout des produits Amazon soins du visage...")
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
    add_amazon_products_from_data()


