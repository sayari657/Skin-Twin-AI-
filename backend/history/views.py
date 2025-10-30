from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from detection.models import SkinAnalysis
from detection.serializers import SkinAnalysisSerializer
from gan.models import GANSimulation
from gan.serializers import GANSimulationSerializer


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_history(request):
    """Obtenir l'historique complet de l'utilisateur"""
    try:
        # Récupérer les analyses
        analyses = SkinAnalysis.objects.filter(user=request.user).order_by('-analysis_date')
        analyses_data = SkinAnalysisSerializer(analyses, many=True).data
        
        # Récupérer les simulations
        simulations = GANSimulation.objects.filter(user=request.user).order_by('-created_at')
        simulations_data = GANSimulationSerializer(simulations, many=True).data
        
        # Combiner les données
        history = {
            'analyses': analyses_data,
            'simulations': simulations_data,
            'total_analyses': analyses.count(),
            'total_simulations': simulations.count()
        }
        
        return Response(history)
        
    except Exception as e:
        return Response(
            {'error': f'Erreur lors du chargement de l\'historique: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )












