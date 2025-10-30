from django.db import models
from users.models import User
from detection.models import SkinAnalysis


class Product(models.Model):
    """Modèle pour les produits cosmétiques"""
    
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    category = models.CharField(
        max_length=50,
        choices=[
            ('CLEANSER', 'Nettoyant'),
            ('MOISTURIZER', 'Hydratant'),
            ('SERUM', 'Sérum'),
            ('SUNSCREEN', 'Crème solaire'),
            ('TREATMENT', 'Traitement'),
            ('MASK', 'Masque'),
            ('TONER', 'Tonique'),
            ('EXFOLIANT', 'Exfoliant')
        ]
    )
    
    # Informations produit
    description = models.TextField()
    ingredients = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    size = models.CharField(max_length=50, null=True, blank=True)
    
    # Cibles
    target_skin_types = models.JSONField(default=list)  # ['DRY', 'OILY', etc.]
    target_issues = models.JSONField(default=list)  # ['acne', 'wrinkles', etc.]
    
    # Images
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.brand} - {self.name}"
    
    class Meta:
        db_table = 'products'


class Recommendation(models.Model):
    """Modèle pour les recommandations de produits"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    skin_analysis = models.ForeignKey(SkinAnalysis, on_delete=models.CASCADE, related_name='recommendations')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='recommendations')
    
    # Scores de recommandation
    relevance_score = models.FloatField()  # Score de pertinence 0-100
    confidence_score = models.FloatField()  # Score de confiance 0-100
    
    # Raisons de la recommandation
    reasons = models.JSONField(default=list)  # ['acne_treatment', 'skin_type_match', etc.]
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Recommandation {self.id} - {self.user.username} - {self.product.name}"
    
    class Meta:
        db_table = 'recommendations'
        ordering = ['-relevance_score']


class UserFeedback(models.Model):
    """Modèle pour les retours utilisateur sur les recommandations"""
    
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE, related_name='feedbacks')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    
    # Feedback
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 étoiles
    feedback_text = models.TextField(blank=True)
    
    # Utilisation du produit
    used_product = models.BooleanField(default=False)
    purchase_intent = models.BooleanField(default=False)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Feedback {self.id} - {self.user.username} - {self.rating} étoiles"
    
    class Meta:
        db_table = 'user_feedbacks'




