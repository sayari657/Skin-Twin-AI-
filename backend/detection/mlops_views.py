"""
Vues Django pour les fonctionnalités MLOps
"""
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)

# Import MLOps (optionnel)
try:
    import sys
    from pathlib import Path
    BASE_DIR = Path(__file__).parent.parent.parent.parent
    sys.path.insert(0, str(BASE_DIR))
    from mlops.integration.django_integration import mlops_integration
    MLOPS_ENABLED = True
except ImportError:
    MLOPS_ENABLED = False
    mlops_integration = None


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def mlops_health_check(request):
    """Vérifier la santé du système MLOps"""
    if not MLOPS_ENABLED:
        return Response({
            'enabled': False,
            'message': 'MLOps not available'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    try:
        health = mlops_integration.check_model_health()
        return Response(health, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error checking MLOps health: {e}")
        return Response({
            'enabled': True,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def mlops_model_stats(request):
    """Obtenir les statistiques des modèles"""
    if not MLOPS_ENABLED:
        return Response({
            'error': 'MLOps not available'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    try:
        stats = {
            'prediction_stats': mlops_integration.monitor.get_prediction_stats(hours=24),
            'performance_metrics': mlops_integration.performance_tracker.get_latest_metrics('ensemble'),
            'average_inference_time': mlops_integration.performance_tracker.get_average_inference_time('ensemble'),
            'error_summary': mlops_integration.performance_tracker.get_error_summary()
        }
        return Response(stats, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error getting model stats: {e}")
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

