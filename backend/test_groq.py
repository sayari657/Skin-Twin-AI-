"""
Script de test pour vérifier que Groq API fonctionne correctement
Utilise config_local.py pour la clé API (ignoré par Git)
"""
import os
import requests

# Essaie d'abord le fichier local, puis les variables d'environnement
try:
    from config_local import GROQ_API_KEY_LOCAL, GROQ_MODEL_LOCAL
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY') or GROQ_API_KEY_LOCAL
    GROQ_MODEL = os.environ.get('GROQ_MODEL') or GROQ_MODEL_LOCAL
except ImportError:
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
    GROQ_MODEL = os.environ.get('GROQ_MODEL', 'llama-3.1-8b-instant')
    if not GROQ_API_KEY:
        print("ERREUR: GROQ_API_KEY non configurée!")
        print("Créez le fichier backend/config_local.py avec votre clé")
        exit(1)

GROQ_URL = 'https://api.groq.com/openai/v1/chat/completions'

def test_groq():
    print("="*60)
    print("TEST GROQ API")
    print("="*60)
    
    headers = {
        'Authorization': f'Bearer {GROQ_API_KEY}',
        'Content-Type': 'application/json',
    }
    
    payload = {
        'model': GROQ_MODEL,
        'messages': [
            {"role": "system", "content": "Tu es un assistant dermatologique amical."},
            {"role": "user", "content": "Bonjour, comment vas-tu ?"}
        ],
        'temperature': 0.8,
        'max_tokens': 100,
    }
    
    try:
        print(f"Envoi de la requête à Groq...")
        print(f"URL: {GROQ_URL}")
        print(f"Model: {GROQ_MODEL}")
        print(f"API Key: {GROQ_API_KEY[:20]}...")
        print()
        
        res = requests.post(GROQ_URL, json=payload, headers=headers, timeout=30)
        
        print(f"Status Code: {res.status_code}")
        print(f"Response Headers: {dict(res.headers)}")
        print()
        
        if res.status_code == 200:
            data = res.json()
            print("✅ SUCCESS!")
            print(f"Response: {data}")
            if 'choices' in data and len(data['choices']) > 0:
                ai_text = data['choices'][0]['message']['content']
                print(f"\nRéponse de l'IA: {ai_text}")
        else:
            print(f"❌ ERROR: {res.status_code}")
            print(f"Response: {res.text}")
            
    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_groq()

