from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
import os
import requests
from .models import ChatSession
from .serializers import ChatSessionSerializer
from .services import ChatAIService

def generate_fallback_response(user_message):
    """Génère une réponse locale intelligente si Groq échoue"""
    msg_lower = user_message.lower()
    
    # Questions générales sur les soins de la peau
    if any(word in msg_lower for word in ['advice', 'conseil', 'aide', 'help', 'routine', 'soins', 'skin care', 'skincare']):
        return """Voici mes conseils généraux pour une routine de soins de la peau efficace :

**Routine de base quotidienne :**

1. **Matin :**
   - Nettoyage doux avec un nettoyant adapté à votre type de peau
   - Sérum antioxydant (vitamine C) pour protéger contre les radicaux libres
   - Crème hydratante légère
   - Protection solaire SPF 30-50 (ESSENTIEL même par temps nuageux)

2. **Soir :**
   - Démaquillage complet si vous portez du maquillage
   - Nettoyage en profondeur
   - Sérum actif selon vos besoins (rétinol pour l'anti-âge, niacinamide pour l'acné)
   - Crème hydratante plus riche

**Conseils généraux :**
- Buvez au moins 2 litres d'eau par jour
- Dormez 7-9 heures par nuit
- Mangez équilibré avec des fruits et légumes riches en antioxydants
- Évitez de toucher votre visage avec les mains sales
- Changez vos taies d'oreiller régulièrement

Pour des conseils plus personnalisés, pouvez-vous me dire votre type de peau (sèche, grasse, mixte, sensible) et vos préoccupations principales ?"""
    
    elif any(word in msg_lower for word in ['acné', 'acne', 'bouton', 'ancre', 'pimple', 'acré', 'acnee']):
        return """Pour l'acné, je recommande une routine douce mais efficace :

**Routine anti-acné :**

1. **Nettoyage :**
   - Nettoyant à l'acide salicylique (BHA) matin et soir
   - Évitez les produits trop agressifs qui peuvent irriter et aggraver l'acné
   - Nettoyez avec des mains propres et de l'eau tiède

2. **Sérum :**
   - Niacinamide (2-5%) pour réduire l'inflammation et réguler le sébum
   - Ou acide salicylique en sérum (2-3 fois par semaine)
   - Évitez d'utiliser plusieurs actifs acides en même temps

3. **Hydratation :**
   - Crème hydratante légère, non comédogène (gel ou lotion)
   - Évitez les crèmes trop riches qui peuvent boucher les pores

4. **Protection solaire :**
   - SPF 50, non comédogène, matifiant
   - ESSENTIEL car certains traitements contre l'acné rendent la peau plus sensible au soleil

**Conseils importants :**
- Ne touchez pas vos boutons avec les mains
- Changez vos taies d'oreiller tous les 2-3 jours
- Évitez les produits comédogènes (huiles lourdes, beurres)
- Soyez patient : les résultats prennent 4-8 semaines

**Si l'acné persiste :** Consultez un dermatologue pour des traitements plus forts (rétinoïdes, antibiotiques topiques).

Avez-vous un type d'acné spécifique ? (points noirs, boutons rouges, kystes ?)"""
    
    elif any(word in msg_lower for word in ['ride', 'anti-âge', 'vieillissement', 'wrinkle', 'aging']):
        return "Pour les rides, intégrez dans votre routine : vitamine C le matin (antioxydant), rétinol le soir (progressivement), hydratant riche et protection solaire quotidienne. La clé est la constance et la protection solaire."
    
    elif any(word in msg_lower for word in ['bonjour', 'salut', 'hi', 'hello']):
        return "Bonjour ! Je suis Skin Twin AI, votre assistant dermatologique. Je peux vous aider avec vos questions sur les soins de la peau, l'acné, les rides, les routines de soins et bien plus. Que souhaitez-vous savoir ?"
    
    elif any(word in msg_lower for word in ['sèche', 'dry', 'déshydratée', 'dehydrated', 'peaux séche', 'peau sèche', 'seche']):
        return """Ah parfait ! Pour une peau sèche, voici mes conseils personnalisés :

**Routine spécifique pour peau sèche :**

1. **Nettoyage :**
   - Utilisez des nettoyants sans savon (syndet ou huile nettoyante)
   - Évitez les produits contenant de l'alcool ou des sulfates
   - Nettoyez seulement matin et soir (pas plus)
   - Utilisez de l'eau tiède, jamais chaude

2. **Hydratation :**
   - Sérum à l'acide hyaluronique (matin et soir) - il retient jusqu'à 1000x son poids en eau
   - Crèmes riches en céramides, glycérine ou niacinamide
   - Évitez les formules avec alcool qui assèchent encore plus
   - Appliquez votre crème sur peau légèrement humide pour mieux retenir l'hydratation

3. **Protection :**
   - Crème solaire hydratante (cherchez "moisturizing sunscreen")
   - En hiver, pensez à un humidificateur d'air dans votre chambre

4. **À éviter :**
   - Produits trop agressifs
   - Douches trop chaudes
   - Exfoliation trop fréquente (max 1x/semaine, très douce)

**Astuce pro :** Essayez le "slugging" le soir : appliquez une fine couche d'huile ou de baume sur votre crème pour créer une barrière qui retient l'hydratation toute la nuit !

Avez-vous des préoccupations spécifiques avec votre peau sèche ? Rougeurs, tiraillements, desquamation ?"""
    
    elif any(word in msg_lower for word in ['grasse', 'oily', 'brillante', 'shiny']):
        return "Pour une peau grasse, utilisez des nettoyants doux deux fois par jour, des sérum à l'acide salicylique ou niacinamide, des hydratants légers sans huile (gel ou lotion) et n'oubliez pas la protection solaire matifiante."
    
    elif any(word in msg_lower for word in ['sensible', 'sensitive', 'irritée', 'irritated']):
        return "Pour une peau sensible, évitez les parfums, les alcools et les ingrédients actifs forts. Utilisez des produits hypoallergéniques, testez toujours les nouveaux produits sur une petite zone, et optez pour des formules minimalistes."
    
    elif any(word in msg_lower for word in ['comment', 'how', 'faire', 'do', 'tuto']):
        return """Je peux vous aider avec plein de questions "comment" sur les soins de la peau ! 

Par exemple :
- Comment traiter l'acné ?
- Comment hydrater une peau sèche ?
- Comment réduire les rides ?
- Comment choisir les bons produits ?
- Comment créer une routine de soins ?

Quelle question spécifique vous intéresse ? Dites-moi ce que vous voulez savoir et je vous donnerai des conseils détaillés !"""

# GROQ configuration via environment variables
# Fallback vers une clé par défaut pour le développement
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')  # Ne pas mettre de clé par défaut ici pour la sécurité
GROQ_MODEL = os.environ.get('GROQ_MODEL', 'llama-3.1-8b-instant')  # Modèle mis à jour (llama3-8b-8192 décommissionné)
GROQ_URL = 'https://api.groq.com/openai/v1/chat/completions'

@api_view(['POST'])
@permission_classes([AllowAny])
def chat_with_ai(request):
    try:
        user_msg = (request.data or {}).get('message', '')
        history = (request.data or {}).get('history', [])  # optional: [{role, content}]
        if not isinstance(history, list):
            history = []

        # Build messages for OpenAI-compatible Chat Completions API
        messages = []
        system_prompt = (request.data or {}).get('system') or """Tu es Skin Twin AI, un assistant dermatologique intelligent et amical. 
Tu parles de manière naturelle, conversationnelle et empathique en français.
Tu réponds librement aux questions sur les soins de la peau, comme un ami expert.
Sois chaleureux, professionnel mais accessible, et n'hésite pas à donner des conseils pratiques et détaillés."""
        messages.append({"role": "system", "content": system_prompt})
        for m in history:
            if isinstance(m, dict) and 'role' in m and 'content' in m:
                messages.append({"role": m['role'], "content": m['content']})
        messages.append({"role": "user", "content": user_msg})

        if not GROQ_API_KEY:
            return Response({
                "response": "Clé GROQ non configurée (GROQ_API_KEY). Ajoutez-la puis relancez le serveur.",
                "note": "missing_groq_api_key"
            }, status=status.HTTP_200_OK)

        headers = {
            'Authorization': f'Bearer {GROQ_API_KEY}',
            'Content-Type': 'application/json',
        }
        payload = {
            'model': GROQ_MODEL,
            'messages': messages,
            'temperature': 0.8,  # Plus créatif et conversationnel
            'max_tokens': 1000,
        }
        res = requests.post(GROQ_URL, json=payload, headers=headers, timeout=60)
        
        # Log pour debug
        print(f"\n{'='*60}")
        print(f"Groq API Request")
        print(f"{'='*60}")
        print(f"URL: {GROQ_URL}")
        print(f"Model: {GROQ_MODEL}")
        print(f"API Key: {GROQ_API_KEY[:20]}...")
        print(f"Status Code: {res.status_code}")
        print(f"Response: {res.text[:500]}")
        print(f"{'='*60}\n")
        
        if res.status_code != 200:
            error_msg = res.text[:300] if res.text else "Pas de réponse"
            print(f"Groq API Error: {res.status_code} - {error_msg}")
            # Fallback: réponse locale intelligente
            fallback_response = generate_fallback_response(user_msg)
            return Response({
                "response": fallback_response,
                "note": f"groq_error_{res.status_code}",
                "session_id": request.data.get('session_id', ''),
                "tokens_used": 0,
                "timestamp": None
            }, status=status.HTTP_200_OK)

        data = res.json()
        ai_text = ''
        # OpenAI-compatible: choices[0].message.content
        if isinstance(data, dict):
            choices = data.get('choices') or []
            if choices and len(choices) > 0 and 'message' in choices[0]:
                ai_text = choices[0]['message'].get('content', '')
            
            # Si pas de contenu, vérifier usage de tokens
            if not ai_text:
                print(f"Groq Response Structure: {data}")
                if 'error' in data:
                    print(f"Groq API Error in response: {data['error']}")
                    # Fallback si erreur dans la réponse
                    fallback_response = generate_fallback_response(user_msg)
                    return Response({
                        "response": fallback_response,
                        "note": f"groq_api_error: {data.get('error', 'unknown')}",
                        "session_id": request.data.get('session_id', ''),
                        "tokens_used": 0,
                        "timestamp": None
                    }, status=status.HTTP_200_OK)
        
        if not ai_text:
            print(f"Warning: No AI text generated, using fallback")
            ai_text = generate_fallback_response(user_msg)

        return Response({
            "response": ai_text,
            "session_id": request.data.get('session_id', ''),
            "tokens_used": 0,
            "timestamp": None
        }, status=status.HTTP_200_OK)
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Chat AI Exception: {error_trace}")
        return Response({
            "response": "Désolé, un problème technique est survenu. Réessayez dans quelques instants.",
            "note": str(e)
        }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chat_sessions(request):
    """Récupère les sessions de chat de l'utilisateur"""
    sessions = ChatSession.objects.filter(user=request.user, is_active=True).order_by('-updated_at')
    serializer = ChatSessionSerializer(sessions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chat_session(request, session_id):
    """Récupère une session de chat spécifique"""
    session = get_object_or_404(ChatSession, session_id=session_id, user=request.user)
    serializer = ChatSessionSerializer(session)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_chat_session(request, session_id):
    """Supprime une session de chat"""
    session = get_object_or_404(ChatSession, session_id=session_id, user=request.user)
    session.is_active = False
    session.save()
    return Response({"message": "Session supprimée avec succès"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_new_session(request):
    """Crée une nouvelle session de chat"""
    try:
        chat_service = ChatAIService()
        session = chat_service.create_session(request.user)
        serializer = ChatSessionSerializer(session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response(
            {"error": f"Erreur lors de la création de la session: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])  # Public pour que le frontend puisse charger les suggestions
def get_ai_suggestions(request):
    """Récupère des suggestions de questions pour l'IA"""
    suggestions = [
        "Quelle routine de soins me conseillez-vous ?",
        "Comment traiter l'acné naturellement ?",
        "Quels produits anti-âge recommandez-vous ?",
        "Comment hydrater une peau sèche ?",
        "Quelle protection solaire choisir ?",
        "Comment réduire les rides ?",
        "Quels ingrédients éviter pour ma peau ?",
        "Comment adapter ma routine selon les saisons ?"
    ]
    return Response({"suggestions": suggestions})


