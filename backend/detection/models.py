from django.db import models
from users.models import User


class SkinAnalysis(models.Model):
    """Modèle pour stocker les analyses de peau"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skin_analyses')
    image = models.ImageField(upload_to='uploads/skin_analyses/')
    
    # Résultats de l'analyse CNN
    skin_type_prediction = models.CharField(max_length=20, null=True, blank=True)
    skin_type_confidence = models.FloatField(null=True, blank=True)
    
    # Détections YOLOv8
    acne_detected = models.BooleanField(default=False)
    acne_severity = models.CharField(max_length=20, null=True, blank=True)
    acne_confidence = models.FloatField(null=True, blank=True)
    
    wrinkles_detected = models.BooleanField(default=False)
    wrinkles_severity = models.CharField(max_length=20, null=True, blank=True)
    wrinkles_confidence = models.FloatField(null=True, blank=True)
    
    dark_spots_detected = models.BooleanField(default=False)
    dark_spots_severity = models.CharField(max_length=20, null=True, blank=True)
    dark_spots_confidence = models.FloatField(null=True, blank=True)
    
    redness_detected = models.BooleanField(default=False)
    redness_severity = models.CharField(max_length=20, null=True, blank=True)
    redness_confidence = models.FloatField(null=True, blank=True)
    
    # Métadonnées
    analysis_date = models.DateTimeField(auto_now_add=True)
    processing_time = models.FloatField(null=True, blank=True)  # en secondes
    
    # Résultats bruts JSON
    raw_cnn_results = models.JSONField(default=dict, blank=True)
    raw_yolo_results = models.JSONField(default=dict, blank=True)
    
    def __str__(self):
        return f"Analyse {self.id} - {self.user.username} - {self.analysis_date}"
    
    class Meta:
        db_table = 'skin_analyses'
        ordering = ['-analysis_date']


class SegmentationResult(models.Model):
    """Modèle pour stocker les résultats de segmentation"""
    
    skin_analysis = models.OneToOneField(SkinAnalysis, on_delete=models.CASCADE, related_name='segmentation')
    segmented_image = models.ImageField(upload_to='uploads/segmented/')
    
    # Zones segmentées
    face_zone = models.JSONField(default=dict, blank=True)
    acne_zones = models.JSONField(default=list, blank=True)
    wrinkle_zones = models.JSONField(default=list, blank=True)
    dark_spot_zones = models.JSONField(default=list, blank=True)
    redness_zones = models.JSONField(default=list, blank=True)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Segmentation pour analyse {self.skin_analysis.id}"
    
    class Meta:
        db_table = 'segmentation_results'




