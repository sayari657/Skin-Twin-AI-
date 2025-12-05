from rest_framework import serializers
from .models import SkinAnalysis, SegmentationResult


class SkinAnalysisSerializer(serializers.ModelSerializer):
    """Serializer pour les analyses de peau"""
    
    class Meta:
        model = SkinAnalysis
        fields = [
            'id', 'image', 'annotated_image', 'skin_type_prediction', 'skin_type_confidence',
            'acne_detected', 'acne_severity', 'acne_confidence',
            'wrinkles_detected', 'wrinkles_severity', 'wrinkles_confidence',
            'dark_spots_detected', 'dark_spots_severity', 'dark_spots_confidence',
            'redness_detected', 'redness_severity', 'redness_confidence',
            'analysis_date', 'processing_time', 'raw_cnn_results', 'raw_yolo_results'
        ]
        read_only_fields = ['id', 'analysis_date']


class SegmentationResultSerializer(serializers.ModelSerializer):
    """Serializer pour les résultats de segmentation"""
    
    class Meta:
        model = SegmentationResult
        fields = [
            'id', 'segmented_image', 'face_zone', 'acne_zones',
            'wrinkle_zones', 'dark_spot_zones', 'redness_zones', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']




