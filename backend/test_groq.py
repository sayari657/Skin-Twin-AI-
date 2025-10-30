"""
Script de test pour vérifier que Groq API fonctionne correctement
IMPORTANT: Configurez votre clé dans les variables d'environnement
Exemple: set GROQ_API_KEY=votre_cle_ici
"""
import os
import requests

GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
if not GROQ_API_KEY:
    print("ERREUR: GROQ_API_KEY non configurée!")
    print("Configurez-la avec: set GROQ_API_KEY=votre_cle_ici")
    exit(1)

GROQ_MODEL = 'llama-3.1-8b-instant'
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

