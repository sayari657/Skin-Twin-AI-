from django.contrib import admin
from .models import ChatSession, ChatMessage, ChatContext


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'user', 'title', 'created_at', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['session_id', 'user__username', 'title']
    readonly_fields = ['session_id', 'created_at', 'updated_at']


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'role', 'content_preview', 'timestamp', 'tokens_used']
    list_filter = ['role', 'timestamp']
    search_fields = ['content', 'session__session_id']
    readonly_fields = ['timestamp']
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Contenu'


@admin.register(ChatContext)
class ChatContextAdmin(admin.ModelAdmin):
    list_display = ['session', 'context_type', 'created_at']
    list_filter = ['context_type', 'created_at']
    search_fields = ['session__session_id']
    readonly_fields = ['created_at']


