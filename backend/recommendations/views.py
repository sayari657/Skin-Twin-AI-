from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Product, Recommendation
from .serializers import ProductSerializer, RecommendationSerializer
from detection.models import SkinAnalysis
from .recommender import product_recommender


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_recommendations(request, analysis_id):
    """Obtenir les recommandations pour une analyse"""
    try:
        analysis = SkinAnalysis.objects.get(id=analysis_id, user=request.user)
        
        # Générer les recommandations
        recommendations = product_recommender.get_recommendations(analysis, limit=10)
        
        # Sauvegarder les recommandations
        product_recommender.save_recommendations(analysis, recommendations)
        
        # Récupérer les recommandations sauvegardées
        saved_recommendations = Recommendation.objects.filter(
            skin_analysis=analysis
        ).order_by('-relevance_score')
        
        serializer = RecommendationSerializer(saved_recommendations, many=True)
        return Response(serializer.data)
        
    except SkinAnalysis.DoesNotExist:
        return Response(
            {'error': 'Analyse non trouvée'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': f'Erreur lors de la génération des recommandations: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
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












