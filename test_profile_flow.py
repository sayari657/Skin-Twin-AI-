#!/usr/bin/env python3
"""
Script de test pour vérifier le flux d'inscription et de récupération du profil
"""
import requests
import json

# Configuration
BASE_URL = "http://127.0.0.1:8000/api"
HEADERS = {"Content-Type": "application/json"}

def test_registration_and_profile():
    """Test complet du flux d'inscription et de récupération du profil"""
    
    print("🧪 Test du flux d'inscription et de profil")
    print("=" * 50)
    
    # 1. Test d'inscription
    print("\n1️⃣ Test d'inscription...")
    registration_data = {
        "username": "testuser_profile",
        "email": "testuser_profile@example.com",
        "password": "test123456",
        "password_confirm": "test123456",
        "age": 25,
        "gender": "F",
        "location_country": "France",
        "location_region": "Île-de-France",
        "skin_type": "COMBINATION",
        "diabetes": False,
        "hypertension": False,
        "smoking": False,
        "alcohol": False,
        "current_skin_problems": ["acne", "dark_spots"],
        "skin_goals": ["prevent_acne", "hydrate_skin"]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/users/register/", 
                               json=registration_data, 
                               headers=HEADERS)
        
        if response.status_code == 201:
            print("✅ Inscription réussie!")
            data = response.json()
            user = data.get('user', {})
            tokens = data.get('tokens', {})
            
            print(f"   - Utilisateur: {user.get('username')}")
            print(f"   - Email: {user.get('email')}")
            print(f"   - Âge: {user.get('age')}")
            print(f"   - Pays: {user.get('location_country')}")
            print(f"   - Type de peau: {user.get('skin_type')}")
            print(f"   - Problèmes de peau: {user.get('current_skin_problems')}")
            
            # 2. Test de récupération du profil avec authentification
            print("\n2️⃣ Test de récupération du profil...")
            access_token = tokens.get('access')
            if access_token:
                auth_headers = {
                    **HEADERS,
                    "Authorization": f"Bearer {access_token}"
                }
                
                profile_response = requests.get(f"{BASE_URL}/users/profile/", 
                                              headers=auth_headers)
                
                if profile_response.status_code == 200:
                    print("✅ Profil récupéré avec succès!")
                    profile_data = profile_response.json()
                    
                    print(f"   - Utilisateur: {profile_data.get('username')}")
                    print(f"   - Email: {profile_data.get('email')}")
                    print(f"   - Âge: {profile_data.get('age')}")
                    print(f"   - Pays: {profile_data.get('location_country')}")
                    print(f"   - Région: {profile_data.get('location_region')}")
                    print(f"   - Type de peau: {profile_data.get('skin_type')}")
                    print(f"   - Problèmes de peau: {profile_data.get('current_skin_problems')}")
                    print(f"   - Objectifs: {profile_data.get('skin_goals')}")
                    
                    # Vérifier que les données sont identiques
                    if (profile_data.get('age') == registration_data['age'] and
                        profile_data.get('location_country') == registration_data['location_country'] and
                        profile_data.get('skin_type') == registration_data['skin_type']):
                        print("✅ Les données du profil correspondent aux données d'inscription!")
                    else:
                        print("❌ Les données du profil ne correspondent pas aux données d'inscription!")
                        
                else:
                    print(f"❌ Erreur lors de la récupération du profil: {profile_response.status_code}")
                    print(f"   Réponse: {profile_response.text}")
            else:
                print("❌ Pas de token d'accès reçu")
                
        else:
            print(f"❌ Erreur d'inscription: {response.status_code}")
            print(f"   Réponse: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter au serveur Django")
        print("   Vérifiez que le serveur est en cours d'exécution sur le port 8000")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")

if __name__ == "__main__":
    test_registration_and_profile()






