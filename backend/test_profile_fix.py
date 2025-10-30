#!/usr/bin/env python3
"""
Script de test pour vérifier que le profil utilisateur fonctionne correctement
"""

import requests
import json

def test_profile_system():
    base_url = "http://127.0.0.1:8000/api"
    
    print("🔍 Test du système de profil utilisateur")
    print("=" * 50)
    
    # 1. Test de l'endpoint profile-simple
    print("\n1. Test de l'endpoint profile-simple...")
    try:
        response = requests.get(f"{base_url}/users/profile-simple/?user_id=33")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Utilisateur trouvé: {data.get('username')}")
            print(f"   📧 Email: {data.get('email')}")
            print(f"   👤 Âge: {data.get('age')}")
            print(f"   🏷️ Type de peau: {data.get('skin_type')}")
            print(f"   🌍 Pays: {data.get('location_country')}")
            print(f"   🏘️ Région: {data.get('location_region')}")
        else:
            print(f"   ❌ Erreur: {response.text}")
    except Exception as e:
        print(f"   ❌ Erreur de connexion: {e}")
    
    # 2. Test de création d'un nouvel utilisateur
    print("\n2. Test de création d'un nouvel utilisateur...")
    try:
        new_user_data = {
            "username": "testprofile",
            "email": "testprofile@example.com",
            "password": "testprofile123",
            "password_confirm": "testprofile123",
            "first_name": "Test",
            "last_name": "Profile",
            "age": 25,
            "gender": "F",
            "skin_type": "NORMAL",
            "location_country": "France",
            "location_region": "Île-de-France"
        }
        
        response = requests.post(f"{base_url}/users/register/", json=new_user_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            data = response.json()
            user_id = data['user']['id']
            print(f"   ✅ Utilisateur créé avec ID: {user_id}")
            
            # Test de récupération du profil du nouvel utilisateur
            print(f"\n3. Test de récupération du profil du nouvel utilisateur (ID: {user_id})...")
            profile_response = requests.get(f"{base_url}/users/profile-simple/?user_id={user_id}")
            print(f"   Status: {profile_response.status_code}")
            if profile_response.status_code == 200:
                profile_data = profile_response.json()
                print(f"   ✅ Profil récupéré:")
                print(f"      - Nom: {profile_data.get('first_name')} {profile_data.get('last_name')}")
                print(f"      - Âge: {profile_data.get('age')}")
                print(f"      - Type de peau: {profile_data.get('skin_type')}")
                print(f"      - Pays: {profile_data.get('location_country')}")
                print(f"      - Région: {profile_data.get('location_region')}")
            else:
                print(f"   ❌ Erreur lors de la récupération du profil: {profile_response.text}")
        else:
            print(f"   ❌ Erreur lors de la création: {response.text}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Test terminé !")
    print("\n📋 Instructions pour tester dans le navigateur:")
    print("1. Allez sur http://localhost:3000/signup")
    print("2. Créez un compte avec vos informations")
    print("3. Connectez-vous sur http://localhost:3000/login")
    print("4. Allez sur le dashboard - vos informations devraient s'afficher")
    print("5. Cliquez sur 'Modifier le profil' - vos données devraient être pré-remplies")

if __name__ == '__main__':
    test_profile_system()


