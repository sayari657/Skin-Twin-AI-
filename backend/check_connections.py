"""
Script de vérification professionnelle des connexions
Vérifie : Base de données, APIs, Routes Django
"""
# -*- coding: utf-8 -*-
import os
import sys
import django
import requests
from django.conf import settings

# Fix encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skin_ai.settings')
django.setup()

from django.db import connection
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.models import UserTestimonial
from detection.models import SkinAnalysis

User = get_user_model()

def check_database():
    """Vérifie la connexion à la base de données"""
    print("\n" + "="*60)
    print("[DB] VERIFICATION BASE DE DONNEES")
    print("="*60)
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result:
                print("[OK] Base de donnees SQLite : CONNECTEE")
                
                # Vérifier les tables
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = [row[0] for row in cursor.fetchall()]
                print(f"   Tables trouvees : {len(tables)}")
                print(f"   Tables : {', '.join(tables[:10])}")
                
                # Compter les utilisateurs
                user_count = User.objects.count()
                print(f"   Utilisateurs : {user_count}")
                
                # Compter les témoignages
                testimonial_count = UserTestimonial.objects.count()
                print(f"   Temoignages : {testimonial_count}")
                
                # Compter les analyses
                analysis_count = SkinAnalysis.objects.count()
                print(f"   Analyses de peau : {analysis_count}")
                
                return True
    except Exception as e:
        print(f"[ERROR] Erreur base de donnees : {str(e)}")
        return False

def check_api_endpoints():
    """Vérifie que tous les endpoints API sont accessibles"""
    print("\n" + "="*60)
    print("[API] VERIFICATION ENDPOINTS API")
    print("="*60)
    
    base_url = "http://127.0.0.1:8000"
    endpoints = [
        ("GET", "/api/users/test-no-auth/", "Test sans auth"),
        ("GET", "/api/users/testimonials/public/", "Témoignages publics"),
        ("POST", "/api/users/login/", "Login (400 attendu si pas de données)"),
        ("POST", "/api/users/register/", "Register (400 attendu si pas de données)"),
        ("GET", "/api/detection/analyses/", "Analyses (400/200 attendu)"),
        ("GET", "/api/products/", "Produits"),
        ("GET", "/api/chat-ai/suggestions/", "Suggestions chat"),
        ("GET", "/api/chat-ai/sessions/", "Sessions chat (401 attendu si pas auth)"),
    ]
    
    success_count = 0
    for method, endpoint, description in endpoints:
        try:
            url = base_url + endpoint
            if method == "GET":
                response = requests.get(url, timeout=5)
            else:
                response = requests.post(url, json={}, timeout=5)
            
            # Accepter 200, 400, 401 comme "endpoint existe"
            if response.status_code in [200, 400, 401, 403]:
                print(f"[OK] {description:30} {method:4} {endpoint:40} -> {response.status_code}")
                success_count += 1
            else:
                print(f"[WARN] {description:30} {method:4} {endpoint:40} -> {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"[ERROR] {description:30} {method:4} {endpoint:40} -> SERVEUR NON DEMARRE")
        except Exception as e:
            print(f"[ERROR] {description:30} {method:4} {endpoint:40} -> {str(e)[:50]}")
    
    print(f"\nResultat : {success_count}/{len(endpoints)} endpoints accessibles")
    return success_count == len(endpoints)

def check_groq_api():
    """Vérifie la configuration Groq API"""
    print("\n" + "="*60)
    print("[GROQ] VERIFICATION GROQ API")
    print("="*60)
    
    groq_key = os.environ.get('GROQ_API_KEY')
    if groq_key:
        print(f"[OK] GROQ_API_KEY trouvee : {groq_key[:20]}...")
        print(f"   Modele : {os.environ.get('GROQ_MODEL', 'llama3-8b-8192')}")
        return True
    else:
        print("[WARN] GROQ_API_KEY non configuree")
        print("   Pour activer : $env:GROQ_API_KEY = 'votre_cle'")
        return False

def check_django_settings():
    """Vérifie les paramètres Django"""
    print("\n" + "="*60)
    print("[CONFIG] VERIFICATION CONFIGURATION DJANGO")
    print("="*60)
    
    print(f"[OK] DEBUG : {settings.DEBUG}")
    print(f"[OK] ALLOWED_HOSTS : {settings.ALLOWED_HOSTS}")
    print(f"[OK] DATABASE : {settings.DATABASES['default']['ENGINE']}")
    print(f"[OK] INSTALLED_APPS : {len(settings.INSTALLED_APPS)} apps")
    
    # Vérifier CORS
    if 'corsheaders' in settings.INSTALLED_APPS:
        print(f"[OK] CORS active")
        print(f"   CORS_ALLOWED_ORIGINS : {getattr(settings, 'CORS_ALLOWED_ORIGINS', [])}")
    else:
        print("[WARN] CORS non active")
    
    return True

def main():
    """Fonction principale de vérification"""
    print("\n" + "="*60)
    print("SKIN TWIN AI - VERIFICATION SYSTEME")
    print("="*60)
    
    results = {
        "database": check_database(),
        "api_endpoints": check_api_endpoints(),
        "groq_api": check_groq_api(),
        "django_settings": check_django_settings(),
    }
    
    print("\n" + "="*60)
    print("RESUME DES VERIFICATIONS")
    print("="*60)
    
    for check_name, result in results.items():
        status = "[OK]" if result else "[ECHEC]"
        print(f"{status:10} {check_name.replace('_', ' ').title()}")
    
    all_ok = all(results.values())
    
    if all_ok:
        print("\n[SUCCESS] TOUS LES SYSTEMES SONT OPERATIONNELS !")
    else:
        print("\n[WARN] CERTAINS SYSTEMES NECESSITENT UNE ATTENTION")
    
    return all_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

