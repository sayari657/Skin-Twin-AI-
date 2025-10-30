from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from recommendations.models import Product
from recommendations.serializers import ProductSerializer


@api_view(['GET'])
@permission_classes([AllowAny])  # Public pour permettre l'accès sans authentification
def get_products(request):
    """Obtenir tous les produits"""
    try:
        products = Product.objects.filter(is_active=True)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    except Exception as e:
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












