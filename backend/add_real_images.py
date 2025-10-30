"""
Script pour ajouter des images réelles aux produits
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

def add_real_images_to_products():
    """Ajoute des images réelles aux produits"""
    
    # Images réelles de produits cosmétiques
    real_images = {
        "NIVEA MEN Active Age Soin de Jour Anti-Âge Complet (1 x 50 ml)": "https://images.unsplash.com/photo-1556228720-195c672ba8ee?w=500&h=500&fit=crop",
        "NIVEA Luminous 630 - Serum Visage Anti-Âge & Anti-Taches": "https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=500&h=500&fit=crop",
        "GARNIER Skin Active - Solution Micellaire Tout-En-1": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=500&h=500&fit=crop",
        "Mixa Expert Peau Sensible - Crème Cica Réparation": "https://images.unsplash.com/photo-1556228720-195c672ba8ee?w=500&h=500&fit=crop",
        "GARNIER Skin Active - Sérum Éclat - Anti-Tache Brunes": "https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=500&h=500&fit=crop",
        "Mixa Intensif Peaux Sèches - La Crème des Peaux Très Sèches et Ternes": "https://images.unsplash.com/photo-1556228720-195c672ba8ee?w=500&h=500&fit=crop",
        "L'Oréal Paris - Revitalift - Soin Anti-Âge Hydratant & Raffermissant": "https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=500&h=500&fit=crop",
        "Mixa - Sérum Booster d'Hydratation Hyalurogel": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=500&h=500&fit=crop",
        "CeraVe - Lait Hydratant Corps et Visage - Peau Sèche à Très Sèche": "https://images.unsplash.com/photo-1556228720-195c672ba8ee?w=500&h=500&fit=crop",
        "CeraVe - Crème Réparatrice Contour des Yeux": "https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=500&h=500&fit=crop",
        "Vichy LiftActiv Supreme Crème Anti-Âge": "https://images.unsplash.com/photo-1556228720-195c672ba8ee?w=500&h=500&fit=crop",
        "Avène Cicalfate+ Crème Réparatrice Protectrice": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=500&h=500&fit=crop",
        "Eucerin Hyaluron-Filler Sérum Anti-Âge": "https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=500&h=500&fit=crop",
        "Bioderma Sébium Pore Refiner Sérum": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=500&h=500&fit=crop"
    }
    
    print("Ajout d'images reelles aux produits...")
    print("=" * 60)
    
    updated_count = 0
    images_downloaded = 0
    
    for product_name, image_url in real_images.items():
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

def add_more_products_with_images():
    """Ajoute plus de produits avec images"""
    
    new_products = [
        {
            'name': "The Ordinary Niacinamide 10% + Zinc 1%",
            'brand': "The Ordinary",
            'price': 6.80,
            'description': "Sérum à la niacinamide pour réduire les imperfections et réguler la production de sébum",
            'category': 'SERUM',
            'target_skin_types': ['OILY', 'COMBINATION'],
            'target_issues': ['acne', 'large_pores', 'oily_skin'],
            'ingredients': "Niacinamide 10%, Zinc 1%, Acide Hyaluronique",
            'image_url': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=500&h=500&fit=crop',
            'source': 'Amazon.fr'
        },
        {
            'name': "Paula's Choice 2% BHA Liquid Exfoliant",
            'brand': "Paula's Choice",
            'price': 29.00,
            'description': "Exfoliant liquide avec acide salicylique pour unifier le teint et réduire les pores",
            'category': 'EXFOLIANT',
            'target_skin_types': ['OILY', 'COMBINATION'],
            'target_issues': ['large_pores', 'blackheads', 'acne'],
            'ingredients': "Acide Salicylique 2%, Acide Hyaluronique, Vitamine E",
            'image_url': 'https://images.unsplash.com/photo-1556228720-195c672ba8ee?w=500&h=500&fit=crop',
            'source': 'Amazon.fr'
        },
        {
            'name': "Lancôme Advanced Génifique Sérum Anti-Âge",
            'brand': "Lancôme",
            'price': 89.00,
            'description': "Sérum anti-âge avec probiotiques et acide hyaluronique pour une peau plus ferme",
            'category': 'SERUM',
            'target_skin_types': ['NORMAL', 'DRY', 'COMBINATION'],
            'target_issues': ['aging', 'wrinkles', 'dullness'],
            'ingredients': "Probiotiques, Acide Hyaluronique, Vitamine C",
            'image_url': 'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=500&h=500&fit=crop',
            'source': 'Amazon.fr'
        },
        {
            'name': "Estée Lauder Advanced Night Repair Sérum",
            'brand': "Estée Lauder",
            'price': 95.00,
            'description': "Sérum réparateur nocturne pour réduire les signes de l'âge et améliorer la texture de la peau",
            'category': 'SERUM',
            'target_skin_types': ['NORMAL', 'DRY', 'COMBINATION'],
            'target_issues': ['aging', 'wrinkles', 'dullness'],
            'ingredients': "Peptides, Acide Hyaluronique, Vitamines",
            'image_url': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=500&h=500&fit=crop',
            'source': 'Amazon.fr'
        },
        {
            'name': "Fresh Rose Deep Hydration Face Cream",
            'brand': "Fresh",
            'price': 45.00,
            'description': "Crème hydratante à l'extrait de rose pour une hydratation intense et durable",
            'category': 'MOISTURIZER',
            'target_skin_types': ['DRY', 'NORMAL'],
            'target_issues': ['dryness'],
            'ingredients': "Extrait de Rose, Acide Hyaluronique, Vitamine E",
            'image_url': 'https://images.unsplash.com/photo-1556228720-195c672ba8ee?w=500&h=500&fit=crop',
            'source': 'Amazon.fr'
        }
    ]
    
    print("Ajout de nouveaux produits avec images reelles...")
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
    print("=== AJOUT D'IMAGES REELLES AUX PRODUITS EXISTANTS ===")
    add_real_images_to_products()
    
    print("\n=== AJOUT DE NOUVEAUX PRODUITS AVEC IMAGES REELLES ===")
    add_more_products_with_images()


