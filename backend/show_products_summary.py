"""
Script pour afficher un résumé de tous les produits par source
"""

import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skin_ai.settings')
django.setup()

from recommendations.models import Product

def show_products_summary():
    """Affiche un résumé de tous les produits par source et catégorie"""
    
    print("RESUME DES PRODUITS DANS LA BASE DE DONNEES")
    print("=" * 60)
    
    total_products = Product.objects.count()
    print(f"Total des produits: {total_products}")
    print()
    
    # Répartition par catégorie
    categories = {}
    for product in Product.objects.all():
        category = product.category
        if category not in categories:
            categories[category] = 0
        categories[category] += 1
    
    print("REPARTITION PAR CATEGORIE:")
    for category, count in sorted(categories.items()):
        print(f"  {category}: {count} produits")
    print()
    
    # Répartition par marque
    brands = {}
    for product in Product.objects.all():
        brand = product.brand
        if brand not in brands:
            brands[brand] = 0
        brands[brand] += 1
    
    print("TOP 10 DES MARQUES:")
    sorted_brands = sorted(brands.items(), key=lambda x: x[1], reverse=True)
    for brand, count in sorted_brands[:10]:
        print(f"  {brand}: {count} produits")
    print()
    
    # Répartition par type de peau
    skin_types = {}
    for product in Product.objects.all():
        for skin_type in product.target_skin_types:
            if skin_type not in skin_types:
                skin_types[skin_type] = 0
            skin_types[skin_type] += 1
    
    print("REPARTITION PAR TYPE DE PEAU:")
    for skin_type, count in sorted(skin_types.items()):
        print(f"  {skin_type}: {count} produits")
    print()
    
    # Répartition par problème ciblé
    issues = {}
    for product in Product.objects.all():
        for issue in product.target_issues:
            if issue not in issues:
                issues[issue] = 0
            issues[issue] += 1
    
    print("REPARTITION PAR PROBLEME CIBLE:")
    for issue, count in sorted(issues.items()):
        print(f"  {issue}: {count} produits")
    print()
    
    # Gamme de prix
    prices = [float(product.price) for product in Product.objects.all() if product.price]
    if prices:
        min_price = min(prices)
        max_price = max(prices)
        avg_price = sum(prices) / len(prices)
        
        print("GAMME DE PRIX:")
        print(f"  Prix minimum: {min_price:.2f}€")
        print(f"  Prix maximum: {max_price:.2f}€")
        print(f"  Prix moyen: {avg_price:.2f}€")
        print()
    
    # Afficher quelques exemples de produits
    print("EXEMPLES DE PRODUITS:")
    for i, product in enumerate(Product.objects.all()[:5]):
        print(f"  {i+1}. {product.brand} - {product.name[:50]}...")
        print(f"     Prix: {product.price}€ | Catégorie: {product.category}")
        print(f"     Types de peau: {', '.join(product.target_skin_types)}")
        print(f"     Problèmes ciblés: {', '.join(product.target_issues)}")
        print()
    
    print("=" * 60)
    print("Base de donnees locale avec produits francais complete!")

if __name__ == "__main__":
    show_products_summary()


