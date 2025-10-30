"""
Script pour ajouter des images aux produits existants
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
        print(f"Erreur lors du telechargement de l'image pour {product_name}: {e}")
        return None

def add_images_to_existing_products():
    """Ajoute des images aux produits existants"""
    
    # Mapping des produits existants avec leurs URLs d'images
    product_images = {
        "NIVEA MEN Active Age Soin de Jour Anti-Âge Complet (1 x 50 ml)": "https://m.media-amazon.com/images/I/61Q8Q8Q8Q8L._AC_SL1500_.jpg",
        "NIVEA Luminous 630 - Serum Visage Anti-Âge & Anti-Taches": "https://m.media-amazon.com/images/I/51Q8Q8Q8Q8L._AC_SL1500_.jpg",
        "GARNIER Skin Active - Solution Micellaire Tout-En-1": "https://m.media-amazon.com/images/I/01Q8Q8Q8Q8L._AC_SL1500_.jpg",
        "Mixa Expert Peau Sensible - Crème Cica Réparation": "https://m.media-amazon.com/images/I/91Q8Q8Q8Q8L._AC_SL1500_.jpg",
        "GARNIER Skin Active - Sérum Éclat - Anti-Tache Brunes": "https://m.media-amazon.com/images/I/81Q8Q8Q8Q8L._AC_SL1500_.jpg",
        "Mixa Intensif Peaux Sèches - La Crème des Peaux Très Sèches et Ternes": "https://m.media-amazon.com/images/I/71Q8Q8Q8Q8L._AC_SL1500_.jpg",
        "L'Oréal Paris - Revitalift - Soin Anti-Âge Hydratant & Raffermissant": "https://m.media-amazon.com/images/I/61Q8Q8Q8Q8L._AC_SL1500_.jpg",
        "Mixa - Sérum Booster d'Hydratation Hyalurogel": "https://m.media-amazon.com/images/I/51Q8Q8Q8Q8L._AC_SL1500_.jpg",
        "CeraVe - Lait Hydratant Corps et Visage - Peau Sèche à Très Sèche": "https://m.media-amazon.com/images/I/11Q8Q8Q8Q8L._AC_SL1500_.jpg",
        "CeraVe - Crème Réparatrice Contour des Yeux": "https://m.media-amazon.com/images/I/01Q8Q8Q8Q8L._AC_SL1500_.jpg"
    }
    
    print("Ajout d'images aux produits existants...")
    print("=" * 60)
    
    updated_count = 0
    images_downloaded = 0
    
    for product_name, image_url in product_images.items():
        try:
            # Trouver le produit
            product = Product.objects.filter(name=product_name).first()
            
            if not product:
                print(f"[ERREUR] Produit non trouve: {product_name[:50]}...")
                continue
                
            if product.image:
                print(f"[EXISTANT] Produit deja avec image: {product_name[:50]}...")
                continue
            
            print(f"[TRAITEMENT] {product_name[:50]}...")
            
            # Télécharger l'image
            print(f"  [IMAGE] Telechargement de l'image...")
            image_path = download_and_save_image(image_url, product_name)
            
            if image_path:
                # Mettre à jour le produit avec l'image
                product.image = image_path
                product.save()
                
                print(f"  [OK] Image ajoutee: {image_path}")
                images_downloaded += 1
                updated_count += 1
            else:
                print(f"  [ERREUR] Echec du telechargement de l'image")
                
        except Exception as e:
            print(f"  [ERREUR] Erreur lors de la mise a jour du produit {product_name}: {e}")
            continue
    
    print("\n" + "=" * 60)
    print(f"Resume final:")
    print(f"  [OK] {updated_count} produits mis a jour avec images")
    print(f"  [IMAGE] {images_downloaded} images telechargees")
    print("=" * 60)
    
    return updated_count, images_downloaded

def add_new_products_with_images():
    """Ajoute de nouveaux produits avec images"""
    
    new_products = [
        {
            'name': "La Roche-Posay Effaclar Duo+ Crème Anti-Imperfections",
            'brand': "La Roche-Posay",
            'price': 15.90,
            'description': "Crème anti-imperfections pour peaux grasses et mixtes, avec niacinamide et acide salicylique",
            'category': 'TREATMENT',
            'target_skin_types': ['OILY', 'COMBINATION'],
            'target_issues': ['acne', 'large_pores'],
            'ingredients': "Niacinamide, Acide Salicylique, Glycérine",
            'image_url': 'https://m.media-amazon.com/images/I/71Q8Q8Q8Q8L._AC_SL1500_.jpg',
            'source': 'Amazon.fr'
        },
        {
            'name': "Vichy LiftActiv Supreme Crème Anti-Âge",
            'brand': "Vichy",
            'price': 24.99,
            'description': "Crème anti-âge avec rétinol et acide hyaluronique pour tous types de peaux",
            'category': 'MOISTURIZER',
            'target_skin_types': ['NORMAL', 'DRY', 'COMBINATION'],
            'target_issues': ['aging', 'wrinkles'],
            'ingredients': "Rétinol, Acide Hyaluronique, Vitamine E",
            'image_url': 'https://m.media-amazon.com/images/I/61Q8Q8Q8Q8L._AC_SL1500_.jpg',
            'source': 'Amazon.fr'
        },
        {
            'name': "Avène Cicalfate+ Crème Réparatrice Protectrice",
            'brand': "Avène",
            'price': 12.50,
            'description': "Crème réparatrice pour peaux sensibles et irritées, avec eau thermale d'Avène",
            'category': 'MOISTURIZER',
            'target_skin_types': ['SENSITIVE'],
            'target_issues': ['sensitivity', 'redness'],
            'ingredients': "Eau Thermale d'Avène, Cuivre, Zinc, Vitamine E",
            'image_url': 'https://m.media-amazon.com/images/I/51Q8Q8Q8Q8L._AC_SL1500_.jpg',
            'source': 'Amazon.fr'
        },
        {
            'name': "Eucerin Hyaluron-Filler Sérum Anti-Âge",
            'brand': "Eucerin",
            'price': 18.99,
            'description': "Sérum anti-âge avec acide hyaluronique et acide glycolique pour une peau plus ferme",
            'category': 'SERUM',
            'target_skin_types': ['NORMAL', 'DRY', 'COMBINATION'],
            'target_issues': ['aging', 'wrinkles', 'dryness'],
            'ingredients': "Acide Hyaluronique, Acide Glycolique, Vitamine C",
            'image_url': 'https://m.media-amazon.com/images/I/41Q8Q8Q8Q8L._AC_SL1500_.jpg',
            'source': 'Amazon.fr'
        },
        {
            'name': "Bioderma Sébium Pore Refiner Sérum",
            'brand': "Bioderma",
            'price': 16.80,
            'description': "Sérum pour affiner les pores et réguler la production de sébum",
            'category': 'SERUM',
            'target_skin_types': ['OILY', 'COMBINATION'],
            'target_issues': ['large_pores', 'oily_skin'],
            'ingredients': "Acide Salicylique, Niacinamide, Glycérine",
            'image_url': 'https://m.media-amazon.com/images/I/31Q8Q8Q8Q8L._AC_SL1500_.jpg',
            'source': 'Amazon.fr'
        }
    ]
    
    print("Ajout de nouveaux produits avec images...")
    print("=" * 60)
    
    added_count = 0
    images_downloaded = 0
    
    for i, product_data in enumerate(new_products, 1):
        try:
            print(f"\n[{i}/{len(new_products)}] Traitement: {product_data['name'][:50]}...")
            
            # Vérifier si le produit existe déjà
            existing_product = Product.objects.filter(
                name=product_data['name'],
                brand=product_data['brand']
            ).first()
            
            if existing_product:
                print(f"  [EXISTANT] Produit deja existant: {product_data['name'][:30]}...")
                continue
            
            # Télécharger l'image
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
                image=image_path
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
    print(f"  [OK] {added_count} nouveaux produits ajoutes")
    print(f"  [IMAGE] {images_downloaded} images telechargees")
    print(f"  [TOTAL] Total produits dans la base: {Product.objects.count()}")
    print("=" * 60)
    
    return added_count, images_downloaded

if __name__ == "__main__":
    print("=== AJOUT D'IMAGES AUX PRODUITS EXISTANTS ===")
    add_images_to_existing_products()
    
    print("\n=== AJOUT DE NOUVEAUX PRODUITS AVEC IMAGES ===")
    add_new_products_with_images()


