from rest_framework import serializers
from .models import GANSimulation, ComparisonResult


class GANSimulationSerializer(serializers.ModelSerializer):
    """Serializer pour les simulations GAN"""
    
    class Meta:
        model = GANSimulation
        fields = [
            'id', 'original_analysis', 'original_image', 'simulated_image',
            'simulation_type', 'improvement_score', 'confidence_score',
            'created_at', 'processing_time', 'raw_gan_results'
        ]
        read_only_fields = ['id', 'created_at']


class ComparisonResultSerializer(serializers.ModelSerializer):
    """Serializer pour les résultats de comparaison"""
    
    class Meta:
        model = ComparisonResult
        fields = [
            'id', 'before_image', 'after_image', 'side_by_side_image',
            'similarity_score', 'improvement_metrics', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']












