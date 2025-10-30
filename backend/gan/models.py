from django.db import models
from users.models import User
from detection.models import SkinAnalysis


class GANSimulation(models.Model):
    """Modèle pour stocker les simulations GAN"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gan_simulations')
    original_analysis = models.ForeignKey(SkinAnalysis, on_delete=models.CASCADE, related_name='gan_simulations')
    
    # Images
    original_image = models.ImageField(upload_to='uploads/gan/original/')
    simulated_image = models.ImageField(upload_to='uploads/gan/simulated/')
    
    # Paramètres de simulation
    simulation_type = models.CharField(
        max_length=20,
        choices=[
            ('ACNE_TREATMENT', 'Traitement acné'),
            ('WRINKLE_REDUCTION', 'Réduction rides'),
            ('DARK_SPOT_REMOVAL', 'Suppression taches'),
            ('SKIN_SMOOTHING', 'Lissage peau'),
            ('COMPLETE_TREATMENT', 'Traitement complet')
        ]
    )
    
    # Résultats de la simulation
    improvement_score = models.FloatField(null=True, blank=True)  # Score d'amélioration 0-100
    confidence_score = models.FloatField(null=True, blank=True)  # Confiance du modèle
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    processing_time = models.FloatField(null=True, blank=True)  # en secondes
    
    # Résultats bruts
    raw_gan_results = models.JSONField(default=dict, blank=True)
    
    def __str__(self):
        return f"Simulation GAN {self.id} - {self.user.username} - {self.simulation_type}"
    
    class Meta:
        db_table = 'gan_simulations'
        ordering = ['-created_at']


class ComparisonResult(models.Model):
    """Modèle pour stocker les comparaisons avant/après"""
    
    gan_simulation = models.OneToOneField(GANSimulation, on_delete=models.CASCADE, related_name='comparison')
    
    # Images de comparaison
    before_image = models.ImageField(upload_to='uploads/gan/comparison/before/')
    after_image = models.ImageField(upload_to='uploads/gan/comparison/after/')
    side_by_side_image = models.ImageField(upload_to='uploads/gan/comparison/side_by_side/')
    
    # Métriques de comparaison
    similarity_score = models.FloatField(null=True, blank=True)
    improvement_metrics = models.JSONField(default=dict, blank=True)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comparaison pour simulation {self.gan_simulation.id}"
    
    class Meta:
        db_table = 'comparison_results'




