from rest_framework import serializers
from .models import ScrapedProduct, ScrapingSession, ScrapingLog


class ScrapedProductSerializer(serializers.ModelSerializer):
    """Serializer pour les produits scrapés"""
    
    target_skin_types_display = serializers.SerializerMethodField()
    target_issues_display = serializers.SerializerMethodField()
    category_display = serializers.SerializerMethodField()
    
    class Meta:
        model = ScrapedProduct
        fields = [
            'id', 'name', 'brand', 'description', 'ingredients',
            'price', 'size', 'category', 'category_display',
            'target_skin_types', 'target_skin_types_display',
            'target_issues', 'target_issues_display',
            'image', 'url', 'source_site', 'source_url',
            'is_active', 'created_at', 'updated_at', 'scraped_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_target_skin_types_display(self, obj):
        return obj.get_target_skin_types_display()
    
    def get_target_issues_display(self, obj):
        return obj.get_target_issues_display()
    
    def get_category_display(self, obj):
        return obj.get_category_display()


class ScrapedProductCreateSerializer(serializers.ModelSerializer):
    """Serializer pour créer des produits scrapés"""
    
    class Meta:
        model = ScrapedProduct
        fields = [
            'name', 'brand', 'description', 'ingredients',
            'price', 'size', 'category', 'target_skin_types',
            'target_issues', 'image', 'url', 'source_site',
            'source_url', 'scraped_by'
        ]
    
    def create(self, validated_data):
        # Créer le produit scrapé
        product = ScrapedProduct.objects.create(**validated_data)
        return product


class ScrapingSessionSerializer(serializers.ModelSerializer):
    """Serializer pour les sessions de scraping"""
    
    duration = serializers.SerializerMethodField()
    logs_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ScrapingSession
        fields = [
            'id', 'session_name', 'source_sites', 'total_products_found',
            'total_products_saved', 'total_products_skipped', 'status',
            'started_at', 'completed_at', 'created_by', 'duration', 'logs_count'
        ]
        read_only_fields = ['id', 'started_at', 'completed_at']
    
    def get_duration(self, obj):
        duration = obj.get_duration()
        if duration:
            return str(duration)
        return None
    
    def get_logs_count(self, obj):
        return obj.logs.count()


class ScrapingLogSerializer(serializers.ModelSerializer):
    """Serializer pour les logs de scraping"""
    
    class Meta:
        model = ScrapingLog
        fields = [
            'id', 'session', 'log_type', 'message', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ScrapingStatsSerializer(serializers.Serializer):
    """Serializer pour les statistiques de scraping"""
    
    total_products = serializers.IntegerField()
    total_sessions = serializers.IntegerField()
    active_sessions = serializers.IntegerField()
    products_by_category = serializers.DictField()
    products_by_source = serializers.DictField()
    recent_products = ScrapedProductSerializer(many=True)
    recent_sessions = ScrapingSessionSerializer(many=True)




