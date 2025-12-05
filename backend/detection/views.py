from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import SkinAnalysis, SegmentationResult
from .services import skin_analysis_service
from .serializers import SkinAnalysisSerializer, SegmentationResultSerializer
import time
import logging

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

logger = logging.getLogger(__name__)


class SkinAnalysisUploadView(APIView):
    """Vue pour uploader et analyser une image de peau"""
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request):
        """Analyser une image de peau"""
        try:
            if 'image' not in request.FILES:
                return Response(
                    {'error': 'Aucune image fournie'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            image_file = request.FILES['image']
            
            # Valider le type de fichier
            allowed_types = ['image/jpeg', 'image/png', 'image/jpg']
            if image_file.content_type not in allowed_types:
                return Response(
                    {'error': 'Type de fichier non supporté'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Créer l'analyse
            skin_analysis = SkinAnalysis.objects.create(
                user=request.user,
                image=image_file
            )
            
            # Analyser l'image
            start_time = time.time()
            results = skin_analysis_service.analyze_skin(
                skin_analysis.image.path, 
                user=request.user
            )
            processing_time = time.time() - start_time
            
            # MLOps: Logger la prédiction et tracker les performances
            if MLOPS_ENABLED and mlops_integration:
                try:
                    mlops_integration.track_inference_performance('ensemble', processing_time)
                    mlops_integration.log_prediction_for_monitoring(
                        prediction={
                            'skin_type': results['skin_type']['prediction'],
                            'confidence': results['skin_type']['confidence'],
                            'detections': results['detections'],
                            'analysis_id': skin_analysis.id
                        },
                        model_name='ensemble'
                    )
                except Exception as e:
                    logger.warning(f"MLOps logging failed: {e}")
            
            # Mettre à jour l'analyse avec les résultats
            skin_analysis.skin_type_prediction = results['skin_type']['prediction']
            skin_analysis.skin_type_confidence = results['skin_type']['confidence']
            skin_analysis.processing_time = processing_time
            
            # Mettre à jour les détections
            detections = results['detections']
            skin_analysis.acne_detected = detections['acne']['detected']
            skin_analysis.acne_severity = detections['acne']['severity']
            skin_analysis.acne_confidence = detections['acne']['confidence']
            
            skin_analysis.wrinkles_detected = detections['wrinkles']['detected']
            skin_analysis.wrinkles_severity = detections['wrinkles']['severity']
            skin_analysis.wrinkles_confidence = detections['wrinkles']['confidence']
            
            skin_analysis.dark_spots_detected = detections['dark_spots']['detected']
            skin_analysis.dark_spots_severity = detections['dark_spots']['severity']
            skin_analysis.dark_spots_confidence = detections['dark_spots']['confidence']
            
            skin_analysis.redness_detected = detections['redness']['detected']
            skin_analysis.redness_severity = detections['redness']['severity']
            skin_analysis.redness_confidence = detections['redness']['confidence']
            
            # Sauvegarder les résultats bruts
            skin_analysis.raw_cnn_results = results['skin_type']
            # Stocker les détections agrégées ET les détections individuelles avec coordonnées
            raw_yolo_data = {
                'aggregated': detections,  # Détections agrégées par type de problème
                'detections': results.get('raw_results', {}).get('detections', [])  # Détections individuelles avec coordonnées
            }
            skin_analysis.raw_yolo_results = raw_yolo_data
            
            skin_analysis.save()
            
            # Sérialiser et retourner les résultats
            serializer = SkinAnalysisSerializer(skin_analysis)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': f'Erreur lors de l\'analyse: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_analysis(request, analysis_id):
    """Récupérer une analyse spécifique"""
    analysis = get_object_or_404(SkinAnalysis, id=analysis_id, user=request.user)
    serializer = SkinAnalysisSerializer(analysis)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])  # Temporaire : permettre l'accès sans authentification
def get_user_analyses(request):
    """Récupérer toutes les analyses d'un utilisateur"""
    # Solution temporaire : récupérer l'utilisateur par ID depuis les paramètres
    user_id = request.GET.get('user_id')
    if user_id:
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            user = User.objects.get(id=user_id)
            analyses = SkinAnalysis.objects.filter(user=user).order_by('-analysis_date')
            serializer = SkinAnalysisSerializer(analyses, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            # Retourner une liste vide plutôt qu'une 404 pour éviter les erreurs bruyantes côté client
            return Response([], status=status.HTTP_200_OK)
    else:
        # Fallback vers l'utilisateur authentifié si disponible
        if hasattr(request, 'user') and request.user.is_authenticated:
            analyses = SkinAnalysis.objects.filter(user=request.user).order_by('-analysis_date')
            serializer = SkinAnalysisSerializer(analyses, many=True)
            return Response(serializer.data)
        else:
            return Response([], status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_analysis(request, analysis_id):
    """Supprimer une analyse"""
    analysis = get_object_or_404(SkinAnalysis, id=analysis_id, user=request.user)
    analysis.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_user_analyses_simple(request):
    """Endpoint simple pour récupérer les analyses d'un utilisateur sans authentification JWT"""
    user_id = request.GET.get('user_id')
    if not user_id:
        return Response({'error': 'user_id requis'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.get(id=user_id)
        analyses = SkinAnalysis.objects.filter(user=user).order_by('-created_at')
        serializer = SkinAnalysisSerializer(analyses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'Utilisateur non trouvé'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': f'Erreur serveur: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
