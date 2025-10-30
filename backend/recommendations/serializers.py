from rest_framework import serializers
from .models import Product, Recommendation, UserFeedback


class ProductSerializer(serializers.ModelSerializer):
    """Serializer pour les produits"""
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'brand', 'category', 'description', 'ingredients',
            'price', 'size', 'target_skin_types', 'target_issues', 'image',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RecommendationSerializer(serializers.ModelSerializer):
    """Serializer pour les recommandations"""
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = Recommendation
        fields = [
            'id', 'product', 'relevance_score', 'confidence_score',
            'reasons', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class UserFeedbackSerializer(serializers.ModelSerializer):
    """Serializer pour les retours utilisateur"""
    
    class Meta:
        model = UserFeedback
        fields = [
            'id', 'recommendation', 'rating', 'feedback_text',
            'used_product', 'purchase_intent', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']












