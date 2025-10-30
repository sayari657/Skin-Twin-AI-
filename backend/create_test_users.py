#!/usr/bin/env python
"""
Script pour creer des utilisateurs de test dans Skin Twin AI
Usage: python create_test_users.py
"""

import os
import sys
import django
from datetime import datetime

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skin_ai.settings')
django.setup()

from users.models import User

def create_test_users():
    """Cree des utilisateurs de test pour Skin Twin AI"""
    
    print("CREATION D'UTILISATEURS DE TEST")
    print("=" * 40)
    
    # Utilisateurs de test a creer
    test_users = [
        {
            'username': 'admin',
            'email': 'admin@skintwin.com',
            'first_name': 'Admin',
            'last_name': 'SkinTwin',
            'password': 'admin123',
            'is_staff': True,
            'is_superuser': True,
            'age': 30,
            'skin_type': 'normal'
        },
        {
            'username': 'marie',
            'email': 'marie@example.com',
            'first_name': 'Marie',
            'last_name': 'Dubois',
            'password': 'marie123',
            'age': 28,
            'skin_type': 'combination'
        },
        {
            'username': 'sophie',
            'email': 'sophie@example.com',
            'first_name': 'Sophie',
            'last_name': 'Martin',
            'password': 'sophie123',
            'age': 32,
            'skin_type': 'dry'
        },
        {
            'username': 'lucas',
            'email': 'lucas@example.com',
            'first_name': 'Lucas',
            'last_name': 'Bernard',
            'password': 'lucas123',
            'age': 25,
            'skin_type': 'oily'
        },
        {
            'username': 'emma',
            'email': 'emma@example.com',
            'first_name': 'Emma',
            'last_name': 'Petit',
            'password': 'emma123',
            'age': 30,
            'skin_type': 'sensitive'
        }
    ]
    
    created_count = 0
    
    for user_data in test_users:
        try:
            # Verifier si l'utilisateur existe deja
            if User.objects.filter(username=user_data['username']).exists():
                print(f"   Utilisateur '{user_data['username']}' existe deja")
                continue
            
            # Creer l'utilisateur personnalise
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                is_staff=user_data.get('is_staff', False),
                is_superuser=user_data.get('is_superuser', False),
                age=user_data.get('age', 25),
                skin_type=user_data.get('skin_type', 'normal'),
                current_skin_problems=['acne', 'blackheads'] if user_data.get('skin_type') == 'oily' else [],
                skin_goals=['hydration', 'anti-aging'] if user_data.get('age', 25) > 30 else ['clear_skin']
            )
            
            print(f"   Utilisateur cree: {user_data['username']} ({user_data['first_name']} {user_data['last_name']})")
            created_count += 1
            
        except Exception as e:
            print(f"   Erreur pour {user_data['username']}: {e}")
    
    print(f"\nRESULTAT:")
    print(f"   - Utilisateurs crees: {created_count}")
    print(f"   - Total utilisateurs: {User.objects.count()}")
    
    print(f"\nIDENTIFIANTS DE CONNEXION:")
    print(f"   Admin: admin / admin123")
    print(f"   Marie: marie / marie123")
    print(f"   Sophie: sophie / sophie123")
    print(f"   Lucas: lucas / lucas123")
    print(f"   Emma: emma / emma123")
    
    print(f"\nURLS D'ACCES:")
    print(f"   - Application: http://localhost:3000")
    print(f"   - Admin Django: http://127.0.0.1:8000/admin")

if __name__ == "__main__":
    create_test_users()