from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Configuration admin pour le modèle User étendu"""
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'age', 'skin_type', 'is_staff')
    list_filter = ('skin_type', 'gender', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informations personnelles', {
            'fields': ('age', 'gender', 'location_country', 'location_region')
        }),
        ('Informations dermatologiques', {
            'fields': ('skin_type', 'current_skin_problems', 'skin_goals')
        }),
        ('Antécédents médicaux', {
            'fields': ('diabetes', 'hypertension', 'blood_disorders', 'autoimmune_diseases', 'pregnancy')
        }),
        ('Habitudes de vie', {
            'fields': ('sun_exposure', 'sunscreen_usage', 'diet', 'hydration', 'smoking', 'alcohol', 'sleep_hours')
        }),
        ('Antécédents dermatologiques', {
            'fields': ('family_dermatological_history', 'current_treatments', 'current_cosmetics', 'known_allergies')
        }),
    )




