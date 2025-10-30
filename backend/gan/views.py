from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import GANSimulation
from .serializers import GANSimulationSerializer
from detection.models import SkinAnalysis
from .services import gan_simulation_service
import time


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_simulation(request):
    """Créer une simulation GAN"""
    try:
        analysis_id = request.data.get('analysis_id')
        simulation_type = request.data.get('simulation_type', 'COMPLETE_TREATMENT')
        
        if not analysis_id:
            return Response(
                {'error': 'analysis_id requis'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Récupérer l'analyse
        try:
            analysis = SkinAnalysis.objects.get(id=analysis_id, user=request.user)
        except SkinAnalysis.DoesNotExist:
            return Response(
                {'error': 'Analyse non trouvée'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Créer la simulation
        start_time = time.time()
        results = gan_simulation_service.simulate_skin_improvement(
            analysis.image.path, 
            simulation_type,
            {
                'acne_detected': analysis.acne_detected,
                'acne_severity': analysis.acne_severity,
                'wrinkles_detected': analysis.wrinkles_detected,
                'wrinkles_severity': analysis.wrinkles_severity,
                'dark_spots_detected': analysis.dark_spots_detected,
                'dark_spots_severity': analysis.dark_spots_severity,
                'redness_detected': analysis.redness_detected,
                'redness_severity': analysis.redness_severity,
                'skin_type': analysis.skin_type_prediction
            }
        )
        processing_time = time.time() - start_time
        
        # Sauvegarder la simulation
        simulation = GANSimulation.objects.create(
            user=request.user,
            original_analysis=analysis,
            original_image=analysis.image,
            simulated_image=analysis.image,  # Temporaire, sera remplacé par l'image simulée
            simulation_type=simulation_type,
            improvement_score=results['improvement_score'],
            confidence_score=results['confidence_score'],
            processing_time=processing_time,
            raw_gan_results=results
        )
        
        serializer = GANSimulationSerializer(simulation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': f'Erreur lors de la simulation: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_simulation(request, simulation_id):
    """Récupérer une simulation spécifique"""
    try:
        simulation = GANSimulation.objects.get(id=simulation_id, user=request.user)
        serializer = GANSimulationSerializer(simulation)
        return Response(serializer.data)
    except GANSimulation.DoesNotExist:
        return Response(
            {'error': 'Simulation non trouvée'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_simulations(request):
    """Récupérer toutes les simulations d'un utilisateur"""
    simulations = GANSimulation.objects.filter(user=request.user).order_by('-created_at')
    serializer = GANSimulationSerializer(simulations, many=True)
    return Response(serializer.data)






