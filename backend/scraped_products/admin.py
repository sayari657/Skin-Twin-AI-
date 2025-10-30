from django.contrib import admin
from .models import ScrapedProduct, ScrapingSession, ScrapingLog


@admin.register(ScrapedProduct)
class ScrapedProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'brand', 'category', 'price', 'source_site', 
        'is_active', 'created_at'
    ]
    list_filter = [
        'category', 'source_site', 'is_active', 'created_at'
    ]
    search_fields = ['name', 'brand', 'description']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 25
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('name', 'brand', 'description', 'ingredients')
        }),
        ('Prix et taille', {
            'fields': ('price', 'size')
        }),
        ('Catégorie et ciblage', {
            'fields': ('category', 'target_skin_types', 'target_issues')
        }),
        ('Images et liens', {
            'fields': ('image', 'url')
        }),
        ('Source', {
            'fields': ('source_site', 'source_url', 'scraped_by')
        }),
        ('Métadonnées', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )


@admin.register(ScrapingSession)
class ScrapingSessionAdmin(admin.ModelAdmin):
    list_display = [
        'session_name', 'status', 'total_products_found', 
        'total_products_saved', 'started_at', 'created_by'
    ]
    list_filter = ['status', 'started_at', 'created_by']
    search_fields = ['session_name']
    readonly_fields = ['started_at', 'completed_at']
    list_per_page = 25


@admin.register(ScrapingLog)
class ScrapingLogAdmin(admin.ModelAdmin):
    list_display = ['session', 'log_type', 'message', 'created_at']
    list_filter = ['log_type', 'created_at']
    search_fields = ['message']
    readonly_fields = ['created_at']
    list_per_page = 50




