from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from recommendations.models import Product
from recommendations.serializers import ProductSerializer
from scraped_products.models import ScrapedProduct
from scraped_products.serializers import ScrapedProductSerializer


def convert_scraped_to_product(scraped_product):
    """Convertit un ScrapedProduct en format Product pour le frontend"""
    return {
        'id': scraped_product.id + 1000000,  # Ajouter un offset pour éviter les conflits d'ID
        'name': scraped_product.name,
        'brand': scraped_product.brand,
        'description': scraped_product.description or scraped_product.name,
        'ingredients': scraped_product.ingredients or '',
        'price': float(scraped_product.price) if scraped_product.price else 0,
        'size': scraped_product.size,
        'category': scraped_product.category,
        'target_skin_types': scraped_product.target_skin_types or ['NORMAL'],
        'target_issues': scraped_product.target_issues or [],
        'image': scraped_product.image,
        'url': scraped_product.url,  # Ajouter l'URL pour les produits scrapés
        'source_site': scraped_product.source_site,
        'is_active': scraped_product.is_active,
        'created_at': scraped_product.created_at.isoformat() if scraped_product.created_at else None,
        'updated_at': scraped_product.updated_at.isoformat() if scraped_product.updated_at else None,
    }


@api_view(['GET'])
@permission_classes([AllowAny])  # Public pour permettre l'accès sans authentification
def get_products(request):
    """Obtenir tous les produits (de la base de données + produits scrapés)"""
    try:
        all_products = []
        
        # Paramètre optionnel pour inclure les produits inactifs
        include_inactive = request.query_params.get('include_inactive', 'false').lower() == 'true'
        
        # Charger les produits de la base de données (recommendations)
        if include_inactive:
            products = Product.objects.all()
        else:
            products = Product.objects.filter(is_active=True)
        product_serializer = ProductSerializer(products, many=True)
        all_products.extend(product_serializer.data)
        print(f"📦 Produits de la base de données (recommendations): {len(all_products)}")
        
        # Charger les produits scrapés
        if include_inactive:
            scraped_products = ScrapedProduct.objects.all()
        else:
            scraped_products = ScrapedProduct.objects.filter(is_active=True)
        scraped_count = scraped_products.count()
        print(f"🕷️ Produits scrapés dans la base: {scraped_count}")
        
        # Compter aussi les produits inactifs pour le debug
        total_scraped = ScrapedProduct.objects.all().count()
        inactive_scraped = ScrapedProduct.objects.filter(is_active=False).count()
        active_scraped = ScrapedProduct.objects.filter(is_active=True).count()
        print(f"   Total produits scrapés (tous): {total_scraped}")
        print(f"   Produits scrapés actifs: {active_scraped}")
        print(f"   Produits scrapés inactifs: {inactive_scraped}")
        
        for scraped_product in scraped_products:
            converted_product = convert_scraped_to_product(scraped_product)
            all_products.append(converted_product)
        
        print(f"✅ Total produits retournés: {len(all_products)}")
        
        # Trier par date de création (plus récents en premier)
        all_products.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        return Response({
            'products': all_products,
            'stats': {
                'total': len(all_products),
                'from_database': len(product_serializer.data),
                'scraped_active': active_scraped,
                'scraped_total': total_scraped,
                'scraped_inactive': inactive_scraped,
            }
        })
    except Exception as e:
        import traceback
        print(f"❌ Erreur lors du chargement des produits: {str(e)}")
        print(traceback.format_exc())
        return Response(
            {'error': f'Erreur lors du chargement des produits: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])  # Public pour permettre l'accès sans authentification
def get_product(request, product_id):
    """Obtenir un produit spécifique"""
    try:
        product = Product.objects.get(id=product_id, is_active=True)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response(
            {'error': 'Produit non trouvé'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': f'Erreur lors du chargement du produit: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )












