from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ScrapedProduct(models.Model):
    """Modèle pour stocker les produits scrapés depuis des sites web"""
    
    # Informations de base
    name = models.CharField(max_length=255, verbose_name="Nom du produit")
    brand = models.CharField(max_length=100, verbose_name="Marque")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    ingredients = models.TextField(blank=True, null=True, verbose_name="Ingrédients")
    
    # Prix et taille
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix")
    size = models.CharField(max_length=50, blank=True, null=True, verbose_name="Taille")
    
    # Catégorie et ciblage
    category = models.CharField(
        max_length=50,
        choices=[
            ('CLEANSER', 'Nettoyant'),
            ('MOISTURIZER', 'Hydratant'),
            ('SERUM', 'Sérum'),
            ('SUNSCREEN', 'Crème solaire'),
            ('MASK', 'Masque'),
            ('TONER', 'Tonique'),
            ('EXFOLIANT', 'Exfoliant'),
            ('TREATMENT', 'Traitement'),
        ],
        verbose_name="Catégorie"
    )
    
    # Types de peau ciblés
    target_skin_types = models.JSONField(
        default=list,
        verbose_name="Types de peau ciblés",
        help_text="Liste des types de peau (SENSITIVE, DRY, OILY, COMBINATION, NORMAL)"
    )
    
    # Problèmes ciblés
    target_issues = models.JSONField(
        default=list,
        verbose_name="Problèmes ciblés",
        help_text="Liste des problèmes (acne, wrinkles, dark_spots, redness, dryness, oiliness)"
    )
    
    # Images et liens
    image = models.URLField(blank=True, null=True, verbose_name="Image")
    url = models.URLField(blank=True, null=True, verbose_name="URL du produit")
    
    # Source de scraping
    source_site = models.CharField(max_length=100, verbose_name="Site source")
    source_url = models.URLField(blank=True, null=True, verbose_name="URL source")
    
    # Métadonnées
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de mise à jour")
    
    # Utilisateur qui a scrapé (optionnel)
    scraped_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Scrapé par"
    )
    
    class Meta:
        verbose_name = "Produit Scrapé"
        verbose_name_plural = "Produits Scrapés"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.brand} - {self.name}"
    
    def get_target_skin_types_display(self):
        """Retourne les types de peau ciblés sous forme de chaîne"""
        if not self.target_skin_types:
            return "Non spécifié"
        return ", ".join(self.target_skin_types)
    
    def get_target_issues_display(self):
        """Retourne les problèmes ciblés sous forme de chaîne"""
        if not self.target_issues:
            return "Non spécifié"
        return ", ".join(self.target_issues)
    
    def get_category_display(self):
        """Retourne le nom de la catégorie"""
        category_dict = dict(self._meta.get_field('category').choices)
        return category_dict.get(self.category, self.category)


class ScrapingSession(models.Model):
    """Modèle pour tracker les sessions de scraping"""
    
    # Informations de la session
    session_name = models.CharField(max_length=255, verbose_name="Nom de la session")
    source_sites = models.JSONField(
        default=list,
        verbose_name="Sites sources",
        help_text="Liste des sites scrapés"
    )
    
    # Statistiques
    total_products_found = models.IntegerField(default=0, verbose_name="Total produits trouvés")
    total_products_saved = models.IntegerField(default=0, verbose_name="Total produits sauvegardés")
    total_products_skipped = models.IntegerField(default=0, verbose_name="Total produits ignorés")
    
    # Statut
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'En attente'),
            ('RUNNING', 'En cours'),
            ('COMPLETED', 'Terminé'),
            ('FAILED', 'Échoué'),
        ],
        default='PENDING',
        verbose_name="Statut"
    )
    
    # Métadonnées
    started_at = models.DateTimeField(auto_now_add=True, verbose_name="Début")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Fin")
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Créé par"
    )
    
    class Meta:
        verbose_name = "Session de Scraping"
        verbose_name_plural = "Sessions de Scraping"
        ordering = ['-started_at']
    
    def __str__(self):
        return f"Session {self.session_name} - {self.get_status_display()}"
    
    def get_duration(self):
        """Retourne la durée de la session"""
        if self.completed_at and self.started_at:
            return self.completed_at - self.started_at
        return None


class ScrapingLog(models.Model):
    """Modèle pour logger les activités de scraping"""
    
    # Session associée
    session = models.ForeignKey(
        ScrapingSession,
        on_delete=models.CASCADE,
        related_name='logs',
        verbose_name="Session"
    )
    
    # Type de log
    log_type = models.CharField(
        max_length=20,
        choices=[
            ('INFO', 'Information'),
            ('WARNING', 'Avertissement'),
            ('ERROR', 'Erreur'),
            ('SUCCESS', 'Succès'),
        ],
        verbose_name="Type de log"
    )
    
    # Message
    message = models.TextField(verbose_name="Message")
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    
    class Meta:
        verbose_name = "Log de Scraping"
        verbose_name_plural = "Logs de Scraping"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_log_type_display()} - {self.message[:50]}..."




