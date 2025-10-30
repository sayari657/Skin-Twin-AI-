"""
Script pour afficher les produits avec leurs images
"""

import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skin_ai.settings')
django.setup()

from recommendations.models import Product

def display_products_with_images():
    """Affiche tous les produits avec leurs images"""
    
    print("AFFICHAGE DES PRODUITS AVEC IMAGES")
    print("=" * 80)
    
    # Récupérer tous les produits
    products = Product.objects.all().order_by('brand', 'name')
    
    total_products = products.count()
    products_with_images = products.exclude(image__isnull=True).exclude(image='').count()
    products_without_images = total_products - products_with_images
    
    print(f"TOTAL: {total_products} produits")
    print(f"AVEC IMAGES: {products_with_images} produits")
    print(f"SANS IMAGES: {products_without_images} produits")
    print("=" * 80)
    
    # Afficher les produits avec images
    print("\nPRODUITS AVEC IMAGES:")
    print("-" * 80)
    
    for i, product in enumerate(products.filter(image__isnull=False).exclude(image=''), 1):
        print(f"{i:2d}. {product.brand} - {product.name}")
        print(f"    Prix: {product.price}€ | Catégorie: {product.category}")
        print(f"    Image: {product.image}")
        print(f"    Types de peau: {', '.join(product.target_skin_types)}")
        print(f"    Problèmes ciblés: {', '.join(product.target_issues)}")
        print()
    
    # Afficher les produits sans images
    print("\nPRODUITS SANS IMAGES:")
    print("-" * 80)
    
    for i, product in enumerate(products.filter(image__isnull=True) | products.filter(image=''), 1):
        print(f"{i:2d}. {product.brand} - {product.name}")
        print(f"    Prix: {product.price}€ | Catégorie: {product.category}")
        print(f"    Types de peau: {', '.join(product.target_skin_types)}")
        print(f"    Problèmes ciblés: {', '.join(product.target_issues)}")
        print()
    
    # Statistiques par marque
    print("\nSTATISTIQUES PAR MARQUE:")
    print("-" * 80)
    
    brands = {}
    for product in products:
        brand = product.brand
        if brand not in brands:
            brands[brand] = {'total': 0, 'with_images': 0, 'without_images': 0}
        
        brands[brand]['total'] += 1
        if product.image and product.image != '':
            brands[brand]['with_images'] += 1
        else:
            brands[brand]['without_images'] += 1
    
    # Trier par nombre total de produits
    sorted_brands = sorted(brands.items(), key=lambda x: x[1]['total'], reverse=True)
    
    for brand, stats in sorted_brands[:10]:  # Top 10
        print(f"{brand}:")
        print(f"  Total: {stats['total']} produits")
        print(f"  Avec images: {stats['with_images']} ({stats['with_images']/stats['total']*100:.1f}%)")
        print(f"  Sans images: {stats['without_images']} ({stats['without_images']/stats['total']*100:.1f}%)")
        print()
    
    # Statistiques par catégorie
    print("\nSTATISTIQUES PAR CATEGORIE:")
    print("-" * 80)
    
    categories = {}
    for product in products:
        category = product.category
        if category not in categories:
            categories[category] = {'total': 0, 'with_images': 0, 'without_images': 0}
        
        categories[category]['total'] += 1
        if product.image and product.image != '':
            categories[category]['with_images'] += 1
        else:
            categories[category]['without_images'] += 1
    
    for category, stats in sorted(categories.items(), key=lambda x: x[1]['total'], reverse=True):
        print(f"{category}:")
        print(f"  Total: {stats['total']} produits")
        print(f"  Avec images: {stats['with_images']} ({stats['with_images']/stats['total']*100:.1f}%)")
        print(f"  Sans images: {stats['without_images']} ({stats['without_images']/stats['total']*100:.1f}%)")
        print()
    
    print("=" * 80)
    print("AFFICHAGE TERMINE")
    print("=" * 80)

if __name__ == "__main__":
    display_products_with_images()


