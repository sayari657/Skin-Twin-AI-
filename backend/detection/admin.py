from django.contrib import admin
from .models import SkinAnalysis, SegmentationResult


@admin.register(SkinAnalysis)
class SkinAnalysisAdmin(admin.ModelAdmin):
    """Configuration admin pour SkinAnalysis"""
    
    list_display = ('id', 'user', 'skin_type_prediction', 'acne_detected', 'wrinkles_detected', 'analysis_date')
    list_filter = ('skin_type_prediction', 'acne_detected', 'wrinkles_detected', 'analysis_date')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('analysis_date', 'processing_time')
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('user', 'image', 'analysis_date', 'processing_time')
        }),
        ('Classification peau', {
            'fields': ('skin_type_prediction', 'skin_type_confidence')
        }),
        ('Détections', {
            'fields': (
                ('acne_detected', 'acne_severity', 'acne_confidence'),
                ('wrinkles_detected', 'wrinkles_severity', 'wrinkles_confidence'),
                ('dark_spots_detected', 'dark_spots_severity', 'dark_spots_confidence'),
                ('redness_detected', 'redness_severity', 'redness_confidence'),
            )
        }),
        ('Résultats bruts', {
            'fields': ('raw_cnn_results', 'raw_yolo_results'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SegmentationResult)
class SegmentationResultAdmin(admin.ModelAdmin):
    """Configuration admin pour SegmentationResult"""
    
    list_display = ('id', 'skin_analysis', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('skin_analysis__user__username',)
    readonly_fields = ('created_at',)




