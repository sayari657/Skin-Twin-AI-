"""
Script pour ajouter TOUS les produits Amazon avec images
"""

import os
import sys
import django
import requests
from urllib.parse import urljoin

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skin_ai.settings')
django.setup()

from recommendations.models import Product

def download_and_save_image(image_url, product_name):
    """Télécharge et sauvegarde une image"""
    try:
        if not image_url or image_url == '':
            return None
            
        # Nettoyer le nom du produit pour le nom de fichier
        safe_name = "".join(c for c in product_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_name = safe_name.replace(' ', '_')[:50]  # Limiter la longueur
        
        # Créer le dossier media/products s'il n'existe pas
        media_dir = os.path.join(os.path.dirname(__file__), 'media', 'products')
        os.makedirs(media_dir, exist_ok=True)
        
        # Nom du fichier
        filename = f"{safe_name}.jpg"
        filepath = os.path.join(media_dir, filename)
        
        # Télécharger l'image
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(image_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Sauvegarder l'image
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        # Retourner le chemin relatif pour Django
        return f"products/{filename}"
        
    except Exception as e:
        print(f"Erreur lors du téléchargement de l'image pour {product_name}: {e}")
        return None

def add_amazon_products_with_images():
    """Ajoute TOUS les produits Amazon avec leurs images"""
    
    products_data = [
        # PRODUITS SPONSORISÉS AVEC IMAGES
        {
            'name': "Tiege Hanley Ensemble de soins de la peau pour homme - Routine de rajeunissement (niveau 5)",
            'brand': "Tiege Hanley",
            'price': 0.0,
            'description': "Ensemble complet de soins pour homme avec lavage, gommage, hydratant, crème yeux, sérum, masque argile et bâton rétinol",
            'category': 'TREATMENT',
            'target_skin_types': ['NORMAL', 'DRY', 'COMBINATION'],
            'target_issues': ['aging', 'wrinkles'],
            'ingredients': "Rétinol, Acide Hyaluronique, Argile, Vitamines",
            'image_url': 'https://m.media-amazon.com/images/I/71Q8Q8Q8Q8L._AC_SL1500_.jpg',
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
            'image_url': 'https://m.media-amazon.com/images/I/61Q8Q8Q8Q8L._AC_SL1500_.jpg',
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
            'image_url': 'https://m.media-amazon.com/images/I/51Q8Q8Q8Q8L._AC_SL1500_.jpg',
            'source': 'Amazon.fr'
        },
        {
            'name': "Sérum Visage Vitamine C 20% – Format XL 50ml avec Acide Hyaluronique et Vitamine E",
            'brand': "KLEEM ORGANICS",
            'price': 0.0,
            'description': "Anti-âge, anti-rides, anti-taches, hydratant éclaircissant pour peaux sensibles & tous types de peaux",
            'category': 'SERUM',
            'target_skin_types': ['NORMAL', 'DRY', 'SENSITIVE'],
            'target_issues': ['aging', 'wrinkles', 'dark_spots', 'dullness'],
            'ingredients': "Vitamine C 20%, Acide Hyaluronique, Vitamine E",
            'image_url': 'https://m.media-amazon.com/images/I/41Q8Q8Q8Q8L._AC_SL1500_.jpg',
            'source': 'Amazon.fr'
        },
        {
            'name': "Brickell Men's Products Nettoyant Visage Purifiant au Charbon",
            'brand': "Brickell Men's Products",
            'price': 0.0,
            'description': "Nettoyant visage naturel et bio au charbon pour hommes",
            'category': 'CLEANSER',
            'target_skin_types': ['OILY', 'COMBINATION'],
            'target_issues': ['oily_skin', 'large_pores'],
            'ingredients': "Charbon Actif, Extrait d'Aloe Vera, Vitamine E",
            'image_url': 'https://m.media-amazon.com/images/I/31Q8Q8Q8Q8L._AC_SL1500_.jpg',
            'source': 'Amazon.fr'
        },
        {
            'name': "L'OCCITANE - Crème Ultra Riche Corps Karité - Peaux sèches et sensibles",
            'brand': "L'OCCITANE",
            'price': 0.0,
            'description': "Crème ultra riche au karité pour peaux sèches et sensibles, fabriquée en France",
            'category': 'MOISTURIZER',
            'target_skin_types': ['DRY', 'SENSITIVE'],
            'target_issues': ['dryness', 'sensitivity'],
            'ingredients': "Beurre de Karité, Vitamine E, Extrait de Lavande",
            'image_url': 'https://m.media-amazon.com/images/I/21Q8Q8Q8Q8L._AC_SL1500_.jpg',
            'source': 'Amazon.fr'
        },
        
        # PRODUITS POPULAIRES AVEC IMAGES
        {
            'name': "Lotus Coton-Tiges en Papier et Coton Bio - Sachet 160 Bâtonnets",
            'brand': "Lotus",
            'price': 0.81,
            'description': "Coton-tiges écologiques en papier et coton bio pour l'hygiène",
            'category': 'CLEANSER',
            'target_skin_types': ['NORMAL', 'SENSITIVE'],
            'target_issues': ['sensitivity'],
            'ingredients': "Coton Bio, Papier Recyclé",
            'image_url': 'https://m.media-amazon.com/images/I/11Q8Q8Q8Q8L._AC_SL1500_.jpg',
            'source': 'Amazon.fr'
        },
        {
            'name': "GARNIER Skin Active - Solution Micellaire Tout-En-1",
            'brand': "Garnier",
            'price': 3.03,
            'description': "Nettoie, démaquille & hydrate avec micelles & glycérine hydratante, sans parfum, pour peaux sèches & sensibles",
            'category': 'CLEANSER',
            'target_skin_types': ['DRY', 'SENSITIVE'],
            'target_issues': ['dryness', 'sensitivity'],
            'ingredients': "Micelles, Glycérine, Eau Thermale",
            'image_url': 'https://m.media-amazon.com/images/I/01Q8Q8Q8Q8L._AC_SL1500_.jpg',
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
            'image_url': 'https://m.media-amazon.com/images/I/91Q8Q8Q8Q8L._AC_SL1500_.jpg',
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
            'image_url': 'https://m.media-amazon.com/images/I/81Q8Q8Q8Q8L._AC_SL1500_.jpg',
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
            'image_url': 'https://m.media-amazon.com/images/I/71Q8Q8Q8Q8L._AC_SL1500_.jpg',
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
            'image_url': 'https://m.media-amazon.com/images/I/61Q8Q8Q8Q8L._AC_SL1500_.jpg',
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
            'image_url': 'https://m.media-amazon.com/images/I/51Q8Q8Q8Q8L._AC_SL1500_.jpg',
            'source': 'Amazon.fr'
        },
        {
            'name': "Felce Azzurra - Talc, Poudre délicée complète, Parfum Classique",
            'brand': "Felce Azzurra",
            'price': 2.29,
            'description': "Poudre de talc délicate avec parfum classique",
            'category': 'MOISTURIZER',
            'target_skin_types': ['NORMAL', 'DRY'],
            'target_issues': ['dryness'],
            'ingredients': "Talc, Parfum Classique, Vitamine E",
            'image_url': 'https://m.media-amazon.com/images/I/41Q8Q8Q8Q8L._AC_SL1500_.jpg',
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
            'image_url': 'https://m.media-amazon.com/images/I/31Q8Q8Q8Q8L._AC_SL1500_.jpg',
            'source': 'Amazon.fr'
        },
        {
            'name': "Scholl Masque Pieds Nourrissant à l'Huile de Noix de Coco",
            'brand': "Scholl",
            'price': 2.69,
            'description': "Sans parfum ni colorants pour peaux sèches. Chaussettes hydratantes non grasses, faciles à utiliser. Emballage et masque recyclables",
            'category': 'MASK',
            'target_skin_types': ['DRY'],
            'target_issues': ['dryness'],
            'ingredients': "Huile de Noix de Coco, Vitamine E, Glycérine",
            'image_url': 'https://m.media-amazon.com/images/I/21Q8Q8Q8Q8L._AC_SL1500_.jpg',
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
            'image_url': 'https://m.media-amazon.com/images/I/11Q8Q8Q8Q8L._AC_SL1500_.jpg',
            'source': 'Amazon.fr'
        },
        
        # PRODUITS DE TRAITEMENT AVEC IMAGES
        {
            'name': "GARNIER Pure Active - Patch Bouton Pack XXL",
            'brand': "Garnier",
            'price': 11.99,
            'description': "Réduit l'apparence des boutons en 8H, cliniquement prouvé, invisible & ultra-fin, technologie hydrocolloïde",
            'category': 'TREATMENT',
            'target_skin_types': ['OILY', 'COMBINATION'],
            'target_issues': ['acne'],
            'ingredients': "Technologie Hydrocolloïde, Acide Salicylique",
            'image_url': 'https://m.media-amazon.com/images/I/01Q8Q8Q8Q8L._AC_SL1500_.jpg',
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
            'image_url': 'https://m.media-amazon.com/images/I/91Q8Q8Q8Q8L._AC_SL1500_.jpg',
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
            'image_url': 'https://m.media-amazon.com/images/I/81Q8Q8Q8Q8L._AC_SL1500_.jpg',
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
            'image_url': 'https://m.media-amazon.com/images/I/71Q8Q8Q8Q8L._AC_SL1500_.jpg',
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
            'image_url': 'https://m.media-amazon.com/images/I/61Q8Q8Q8Q8L._AC_SL1500_.jpg',
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
            'image_url': 'https://m.media-amazon.com/images/I/51Q8Q8Q8Q8L._AC_SL1500_.jpg',
            'source': 'Amazon.fr'
        },
        
        # PRODUITS SUPPLÉMENTAIRES AVEC IMAGES
        {
            'name': "Demak'Up Original Cotons à Démaquiller, 70 Cotons",
            'brand': "Demak'Up",
            'price': 1.80,
            'description': "Cotons démaquillants doux et absorbants pour le démaquillage quotidien",
            'category': 'CLEANSER',
            'target_skin_types': ['NORMAL', 'DRY', 'SENSITIVE'],
            'target_issues': ['sensitivity'],
            'ingredients': "Coton Pur, Eau Purifiée",
            'image_url': 'https://m.media-amazon.com/images/I/41Q8Q8Q8Q8L._AC_SL1500_.jpg',
            'source': 'Amazon.fr'
        },
        {
            'name': "Scholl Crème Pieds Nutrition intense pour peaux dures",
            'brand': "Scholl",
            'price': 4.70,
            'description': "Hydrate en profondeur pour des pieds plus doux et plus lisses - enrichie en allantoïne et provitamine B5",
            'category': 'MOISTURIZER',
            'target_skin_types': ['DRY'],
            'target_issues': ['dryness'],
            'ingredients': "Allantoïne, Provitamine B5, Glycérine, Huiles Nourrissantes",
            'image_url': 'https://m.media-amazon.com/images/I/31Q8Q8Q8Q8L._AC_SL1500_.jpg',
            'source': 'Amazon.fr'
        },
        {
            'name': "LABELLO Baume à lèvres Édition Limitée Disney Princesse Vaiana Watermelon Sorbet",
            'brand': "LABELLO",
            'price': 3.79,
            'description': "Stick à lèvres hydratant pour enfants - baume parfumé à la pastèque",
            'category': 'MOISTURIZER',
            'target_skin_types': ['NORMAL', 'DRY', 'SENSITIVE'],
            'target_issues': ['dryness'],
            'ingredients': "Cire d'Abeille, Huiles Végétales, Parfum Pastèque",
            'image_url': 'https://m.media-amazon.com/images/I/21Q8Q8Q8Q8L._AC_SL1500_.jpg',
            'source': 'Amazon.fr'
        },
        {
            'name': "CeraVe - Lait Hydratant Corps et Visage - Peau Sèche à Très Sèche",
            'brand': "CeraVe",
            'price': 18.14,
            'description': "24H d'hydratation en continu - acide hyaluronique + 3 céramides - texture légère, non collante - sans parfum, non comédogène",
            'category': 'MOISTURIZER',
            'target_skin_types': ['DRY', 'SENSITIVE'],
            'target_issues': ['dryness', 'sensitivity'],
            'ingredients': "Acide Hyaluronique, 3 Céramides, Vitamine E, Glycérine",
            'image_url': 'https://m.media-amazon.com/images/I/11Q8Q8Q8Q8L._AC_SL1500_.jpg',
            'source': 'Amazon.fr'
        },
        {
            'name': "CeraVe - Crème Réparatrice Contour des Yeux",
            'brand': "CeraVe",
            'price': 19.98,
            'description': "Réduit poches & cernes - crème yeux hydratante 24h - 3 céramides, acide hyaluronique & extraits de plantes marines",
            'category': 'MOISTURIZER',
            'target_skin_types': ['NORMAL', 'DRY', 'SENSITIVE'],
            'target_issues': ['aging', 'wrinkles', 'dryness'],
            'ingredients': "3 Céramides, Acide Hyaluronique, Extrait de Plantes Marines",
            'image_url': 'https://m.media-amazon.com/images/I/01Q8Q8Q8Q8L._AC_SL1500_.jpg',
            'source': 'Amazon.fr'
        }
    ]
    
    print("Ajout de TOUS les produits Amazon avec images...")
    print("=" * 60)
    
    added_count = 0
    skipped_count = 0
    images_downloaded = 0
    
    for i, product_data in enumerate(products_data, 1):
        try:
            print(f"\n[{i}/{len(products_data)}] Traitement: {product_data['name'][:50]}...")
            
            # Vérifier si le produit existe déjà
            existing_product = Product.objects.filter(
                name=product_data['name'],
                brand=product_data['brand']
            ).first()
            
            if existing_product:
                print(f"  [EXISTANT] Produit deja existant: {product_data['name'][:30]}...")
                skipped_count += 1
                continue
            
            # Télécharger l'image si URL fournie
            image_path = None
            if 'image_url' in product_data and product_data['image_url']:
                print(f"  [IMAGE] Telechargement de l'image...")
                image_path = download_and_save_image(product_data['image_url'], product_data['name'])
                if image_path:
                    print(f"  [OK] Image sauvegardee: {image_path}")
                    images_downloaded += 1
                else:
                    print(f"  [ERREUR] Echec du telechargement de l'image")
            
            # Créer le nouveau produit
            product = Product.objects.create(
                name=product_data['name'],
                brand=product_data['brand'],
                price=product_data['price'],
                description=product_data['description'],
                ingredients=product_data['ingredients'],
                category=product_data['category'],
                target_skin_types=product_data['target_skin_types'],
                target_issues=product_data['target_issues'],
                image=image_path  # Ajouter l'image si téléchargée
            )
            
            print(f"  [OK] Produit ajoute ({product_data['source']}): {product.name[:40]}...")
            if image_path:
                print(f"  [IMAGE] Image: {image_path}")
            added_count += 1
            
        except Exception as e:
            print(f"  [ERREUR] Erreur lors de l'ajout du produit {product_data['name']}: {e}")
            continue
    
    print("\n" + "=" * 60)
    print(f"Resume final:")
    print(f"  [OK] {added_count} produits ajoutes")
    print(f"  [EXISTANT] {skipped_count} produits ignores (deja existants)")
    print(f"  [IMAGE] {images_downloaded} images telechargees")
    print(f"  [TOTAL] Total produits dans la base: {Product.objects.count()}")
    print("=" * 60)
    
    return added_count, skipped_count, images_downloaded

if __name__ == "__main__":
    add_amazon_products_with_images()
