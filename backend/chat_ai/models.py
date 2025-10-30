from django.db import models
from users.models import User


class ChatSession(models.Model):
    """Modèle pour les sessions de chat avec l'IA"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions')
    session_id = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Chat Session {self.session_id} - {self.user.username}"
    
    class Meta:
        db_table = 'chat_sessions'
        ordering = ['-updated_at']


class ChatMessage(models.Model):
    """Modèle pour les messages du chat IA"""
    
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(
        max_length=20,
        choices=[
            ('user', 'Utilisateur'),
            ('assistant', 'Assistant IA'),
            ('system', 'Système')
        ]
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    tokens_used = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."
    
    class Meta:
        db_table = 'chat_messages'
        ordering = ['timestamp']


class ChatContext(models.Model):
    """Modèle pour le contexte du chat (profil utilisateur, analyses, etc.)"""
    
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='contexts')
    context_type = models.CharField(
        max_length=50,
        choices=[
            ('user_profile', 'Profil utilisateur'),
            ('skin_analysis', 'Analyse de peau'),
            ('product_recommendation', 'Recommandation produit'),
            ('skin_history', 'Historique de peau')
        ]
    )
    context_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.context_type} - {self.session.session_id}"
    
    class Meta:
        db_table = 'chat_contexts'


