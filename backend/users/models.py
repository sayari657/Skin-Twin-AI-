from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Modèle utilisateur étendu avec informations dermatologiques"""
    
    # Résoudre les conflits de related_name
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set',
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',
        related_query_name='custom_user',
    )
    
    # Informations générales
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=[('M', 'Homme'), ('F', 'Femme'), ('O', 'Autre')],
        null=True, blank=True
    )
    location_country = models.CharField(max_length=100, null=True, blank=True)
    location_region = models.CharField(max_length=100, null=True, blank=True)
    
    # Type de peau
    skin_type = models.CharField(
        max_length=20,
        choices=[
            ('DRY', 'Sèche'),
            ('OILY', 'Grasse'),
            ('COMBINATION', 'Mixte'),
            ('NORMAL', 'Normale'),
            ('SENSITIVE', 'Sensible')
        ],
        null=True, blank=True
    )
    
    # Antécédents médicaux
    diabetes = models.BooleanField(default=False)
    hypertension = models.BooleanField(default=False)
    blood_disorders = models.BooleanField(default=False)
    autoimmune_diseases = models.BooleanField(default=False)
    pregnancy = models.BooleanField(default=False)
    
    # Habitudes de vie
    sun_exposure = models.CharField(
        max_length=20,
        choices=[
            ('LOW', 'Faible'),
            ('MODERATE', 'Modérée'),
            ('HIGH', 'Élevée')
        ],
        null=True, blank=True
    )
    sunscreen_usage = models.CharField(
        max_length=20,
        choices=[
            ('NEVER', 'Jamais'),
            ('SOMETIMES', 'Parfois'),
            ('DAILY', 'Quotidiennement')
        ],
        null=True, blank=True
    )
    diet = models.CharField(
        max_length=20,
        choices=[
            ('BALANCED', 'Équilibrée'),
            ('HIGH_FAT_SUGAR', 'Riche en graisses & sucres'),
            ('VEGETARIAN', 'Végétarienne')
        ],
        null=True, blank=True
    )
    hydration = models.CharField(
        max_length=20,
        choices=[
            ('LOW', '<1L'),
            ('MODERATE', '1-2L'),
            ('HIGH', '>2L')
        ],
        null=True, blank=True
    )
    smoking = models.BooleanField(default=False)
    alcohol = models.BooleanField(default=False)
    sleep_hours = models.CharField(
        max_length=20,
        choices=[
            ('LOW', '<5h'),
            ('MODERATE', '5-7h'),
            ('HIGH', '>7h')
        ],
        null=True, blank=True
    )
    
    # Antécédents dermatologiques
    family_dermatological_history = models.BooleanField(default=False)
    current_skin_problems = models.JSONField(default=list, blank=True)
    current_treatments = models.TextField(blank=True)
    current_cosmetics = models.TextField(blank=True)
    known_allergies = models.TextField(blank=True)
    
    # Objectifs
    skin_goals = models.JSONField(default=list, blank=True)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.email})"
    
    class Meta:
        db_table = 'users'


class UserTestimonial(models.Model):
    """Modèle pour stocker les témoignages des utilisateurs"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='testimonials')
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], help_text="Note de 1 à 5 étoiles")
    comment = models.TextField(blank=True, null=True, help_text="Commentaire optionnel")
    is_public = models.BooleanField(default=True, help_text="Afficher sur la page d'accueil")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Témoignage de {self.user.username} - {self.rating} étoiles"
    
    class Meta:
        db_table = 'user_testimonials'
        ordering = ['-created_at']
