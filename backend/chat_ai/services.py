import requests
import json
import uuid
from datetime import datetime
from django.conf import settings
from .models import ChatSession, ChatMessage, ChatContext
from users.models import User
from detection.models import SkinAnalysis
from recommendations.models import Product
import os


class ChatAIService:
    """Service pour l'intégration avec l'API de chat IA gratuite"""
    
    def __init__(self):
        # Utilisation de l'API Hugging Face gratuite
        self.api_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
        # Clé API publique pour les tests (gratuite)
        self.headers = {
            "Authorization": "Bearer hf_YourPublicTokenHere",  # Token public pour les tests
            "Content-Type": "application/json"
        }
    
    def get_skin_context(self, user):
        """Récupère le contexte de peau de l'utilisateur"""
        context = {
            "user_profile": {
                "age": user.age,
                "skin_type": user.skin_type,
                "location": f"{user.location_country}, {user.location_region}",
                "health_conditions": {
                    "diabetes": user.diabetes,
                    "hypertension": user.hypertension,
                    "blood_disorders": user.blood_disorders,
                    "autoimmune_diseases": user.autoimmune_diseases,
                    "pregnancy": user.pregnancy
                },
                "lifestyle": {
                    "smoking": user.smoking,
                    "alcohol": user.alcohol,
                    "sun_exposure": user.sun_exposure,
                    "sunscreen_usage": user.sunscreen_usage
                },
                "skin_problems": getattr(user, 'current_skin_problems', []),
                "skin_goals": getattr(user, 'skin_goals', [])
            }
        }
        
        # Ajouter les analyses récentes
        recent_analyses = SkinAnalysis.objects.filter(user=user).order_by('-created_at')[:3]
        if recent_analyses:
            context["recent_analyses"] = []
            for analysis in recent_analyses:
                context["recent_analyses"].append({
                    "date": analysis.created_at.isoformat(),
                    "skin_type": analysis.skin_type,
                    "issues": analysis.issues,
                    "recommendations": analysis.recommendations
                })
        
        return context
    
    def build_system_prompt(self, user):
        """Construit le prompt système pour l'IA"""
        context = self.get_skin_context(user)
        
        system_prompt = f"""Tu es Skin Twin AI, un assistant dermatologique intelligent spécialisé dans les soins de la peau.

CONTEXTE UTILISATEUR:
- Âge: {context['user_profile']['age']} ans
- Type de peau: {context['user_profile']['skin_type']}
- Localisation: {context['user_profile']['location']}
- Problèmes de peau actuels: {', '.join(context['user_profile']['skin_problems']) if context['user_profile']['skin_problems'] else 'Aucun'}
- Objectifs de peau: {', '.join(context['user_profile']['skin_goals']) if context['user_profile']['skin_goals'] else 'Non spécifiés'}

TON RÔLE:
1. Conseiller sur les soins de la peau adaptés au profil utilisateur
2. Recommander des produits cosmétiques appropriés
3. Expliquer les ingrédients et leurs bénéfices
4. Proposer des routines de soins personnalisées
5. Répondre aux questions dermatologiques de manière professionnelle
6. Adapter tes conseils selon l'âge, le type de peau et les problèmes spécifiques

RÈGLES IMPORTANTES:
- Toujours adapter tes conseils au profil utilisateur
- Être précis et professionnel
- Recommander des produits de la base de données Skin Twin AI
- Expliquer les ingrédients actifs
- Proposer des routines matin/soir
- Mentionner l'importance de la protection solaire
- Être encourageant et positif

Réponds en français de manière naturelle et professionnelle."""

        return system_prompt
    
    def call_ai_api(self, messages):
        """Appelle l'API IA gratuite"""
        try:
            # Formatage des messages pour l'API
            formatted_messages = []
            for msg in messages:
                formatted_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
            
            payload = {
                "inputs": {
                    "past_user_inputs": [msg["content"] for msg in messages if msg["role"] == "user"][-5:],
                    "generated_responses": [msg["content"] for msg in messages if msg["role"] == "assistant"][-5:],
                    "text": messages[-1]["content"] if messages else ""
                },
                "parameters": {
                    "max_length": 200,
                    "temperature": 0.7,
                    "do_sample": True
                }
            }
            
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get("generated_text", "Désolé, je n'ai pas pu générer de réponse.")
                elif isinstance(result, dict) and "generated_text" in result:
                    return result["generated_text"]
                else:
                    return "Désolé, je n'ai pas pu générer de réponse."
            else:
                # Fallback: réponse générique intelligente
                return "Désolé, je rencontre un problème technique. Veuillez réessayer."
                
        except Exception as e:
            print(f"Erreur API IA: {e}")
            return "Désolé, je rencontre un problème technique. Veuillez réessayer."
    
    def generate_fallback_response(self, user_message, user_context=None):
        """Génère une réponse de fallback intelligente et contextuelle (FR)
        - Tolérant aux fautes (ex: "ancre" pour "acné")
        - Donne des conseils concrets, routines matin/soir, ingrédients clés
        - Utilise le contexte utilisateur si disponible (type de peau, âge)
        """
        def normalize(text: str) -> str:
            try:
                import unicodedata
                text = text.lower().strip()
                text = ''.join(
                    c for c in unicodedata.normalize('NFD', text)
                    if unicodedata.category(c) != 'Mn'
                )
                return text
            except Exception:
                return (text or '').lower().strip()

        msg = normalize(user_message or '')

        # Contexte utilisateur simplifié
        skin_type = 'votre type de peau'
        age = 'votre âge'
        problems = 'vos problèmes de peau'
        if user_context and 'user_profile' in user_context:
            profile = user_context['user_profile']
            skin_type = profile.get('skin_type') or skin_type
            age = profile.get('age') or age
            if profile.get('skin_problems'):
                problems = ', '.join(profile.get('skin_problems'))

        def routine_block(morning_steps, night_steps):
            return (
                "\n\nRoutine proposée:" \
                "\n• Matin:" + ''.join(f"\n  - {s}" for s in morning_steps) + \
                "\n• Soir:" + ''.join(f"\n  - {s}" for s in night_steps)
            )

        # Jeux de mots-clés (normalisés, sans accents)
        kw_acne = ['acne', 'acnee', 'acnee', 'acnes', 'bouton', 'boutons', 'imperfection', 'imperfections', 'ancre']
        kw_wrinkles = ['ride', 'rides', 'antiride', 'anti-age', 'antiage', 'vieillissement']
        kw_dry = ['seche', 'deshydratee', 'deshydratation', 'tiraille', 'tiraillements', 'peau seche']
        kw_oily = ['grasse', 'seborrhee', 'sebum', 'brillante', 'peau grasse']
        kw_spots = ['tache', 'taches', 'hyperpigmentation', 'pigmentation', 'melasma']
        kw_redness = ['rougeur', 'rougeurs', 'erytheme', 'rosacee']
        kw_routine = ['routine', 'soins', 'etapes', 'conseil', 'conseils']

        def contains_any(text, words):
            return any(w in text for w in words)

        # Réponses spécialisées
        if contains_any(msg, kw_acne):
            reply = (
                "Pour l'acné, privilégiez une approche douce et régulière." \
                "\nIngrédients clés: acide salicylique (BHA), niacinamide, peroxyde de benzoyle (faible dose), adapalène (si toléré)." \
                f"\nAdaptation à votre peau ({skin_type}): commencez lentement, évitez d'agresser la barrière cutanée."
            )
            reply += routine_block(
                [
                    "Nettoyant doux (pH ~5.5)",
                    "Tonique/essence hydratante (facultatif)",
                    "Sérum niacinamide 5%",
                    "Crème hydratante non comédogène",
                    "Écran solaire SPF 50"
                ],
                [
                    "Nettoyant doux",
                    "Traitement ciblé: acide salicylique 2% ou peroxyde de benzoyle (2.5%) en fine couche",
                    "Hydratant réparateur (ex: céramides)"
                ]
            )
            reply += (
                "\n\nAstuces: évitez de toucher les lésions, changez taie d'oreiller régulièrement, privilégiez une routine simple."
                "\nEscalade: si acné modérée à sévère, consultez un dermatologue (rétinoïdes, antibiotiques, isotréinoïne selon cas)."
            )
            return reply

        if contains_any(msg, kw_wrinkles):
            reply = (
                "Pour les rides, pensez protection solaire quotidienne + actifs anti-âge." \
                "\nIngrédients clés: vitamine C (matin), rétinol/rétinoïdes (soir, progressif), peptides, acide hyaluronique."
            )
            reply += routine_block(
                [
                    "Nettoyant doux",
                    "Vitamine C (antioxydant)",
                    "Hydratant",
                    "SPF 50"
                ],
                [
                    "Nettoyant",
                    "Rétinol (2-3 soirs/sem au départ)",
                    "Crème nourrissante/réparatrice"
                ]
            )
            reply += "\nNote: introduisez les actifs progressivement pour limiter l'irritation."
            return reply

        if contains_any(msg, kw_dry):
            reply = (
                "Pour la peau sèche/déshydratée: restaurer la barrière cutanée et limiter la perte d'eau." \
                "\nIngrédients clés: céramides, acide hyaluronique, glycérine, squalane."
            )
            reply += routine_block(
                [
                    "Nettoyant crème sans sulfate",
                    "Essence/sérum acide hyaluronique",
                    "Crème riche céramides",
                    "SPF 50"
                ],
                [
                    "Nettoyant doux",
                    "Huile/sérum nourrissant (squalane)",
                    "Baume réparateur"
                ]
            )
            reply += "\nÉvitez l'eau très chaude et les nettoyants décapants."
            return reply

        if contains_any(msg, kw_oily):
            reply = (
                "Pour la peau grasse: réguler le sébum sans sur-assécher." \
                "\nIngrédients clés: niacinamide, acide salicylique (BHA), zinc, textures légères non comédogènes."
            )
            reply += routine_block(
                [
                    "Nettoyant gel doux",
                    "Sérum niacinamide",
                    "Hydratant léger gel-crème",
                    "SPF 50 matifiant"
                ],
                [
                    "Nettoyant",
                    "BHA 2% (2-4 soirs/sem)",
                    "Hydratant léger"
                ]
            )
            return reply

        if contains_any(msg, kw_spots):
            reply = (
                "Pour les taches/hyperpigmentation: constance + protection solaire stricte." \
                "\nIngrédients clés: vitamine C, niacinamide, acide azélaïque, acide tranexamique, rétinoïdes."
            )
            reply += routine_block(
                [
                    "Nettoyant",
                    "Vitamine C",
                    "Hydratant",
                    "SPF 50 (renouveler)"
                ],
                [
                    "Nettoyant",
                    "Sérum acide azélaïque ou niacinamide",
                    "Rétinoïde (progressif)",
                    "Crème hydratante"
                ]
            )
            reply += "\nEscalade: dermatologue pour peelings, hydroquinone ou laser si nécessaire."
            return reply

        if contains_any(msg, kw_redness):
            reply = (
                "Pour les rougeurs/rosacée: apaiser et renforcer la barrière cutanée." \
                "\nIngrédients: niacinamide, panthénol, céramides; éviter alcool parfum/irritants."
            )
            reply += routine_block(
                [
                    "Nettoyant doux",
                    "Sérum apaisant (niacinamide/panthénol)",
                    "Crème réparatrice",
                    "SPF 50"
                ],
                [
                    "Nettoyant",
                    "Crème apaisante",
                    "Baume barrière (si besoin)"
                ]
            )
            reply += "\nÉvitez les températures extrêmes et les actifs trop forts."
            return reply

        if contains_any(msg, kw_routine):
            return (
                f"Routine de base pour {skin_type}:" +
                routine_block(
                    ["Nettoyant doux", "Sérum ciblé", "Hydratant", "SPF 50"],
                    ["Nettoyant", "Actif ciblé (selon besoin)", "Crème réparatrice"]
                ) +
                "\nAjustez les actifs selon vos objectifs (acné, taches, rides, sécheresse, rougeurs)."
            )

        # Réponse générale améliorée
        return (
            "Je suis là pour vous aider avec vos soins de la peau." \
            f"\nProfil: peau {skin_type}, âge {age}, préoccupations: {problems}." \
            "\nDites-moi votre priorité (acné, taches, rides, sécheresse, rougeurs) et je vous propose une routine précise."
        )
    
    def create_session(self, user):
        """Crée une nouvelle session de chat"""
        session_id = str(uuid.uuid4())
        session = ChatSession.objects.create(
            user=user,
            session_id=session_id,
            title="Nouvelle conversation"
        )
        return session
    
    def get_or_create_session(self, user, session_id=None):
        """Récupère ou crée une session de chat"""
        if session_id:
            try:
                return ChatSession.objects.get(session_id=session_id, user=user)
            except ChatSession.DoesNotExist:
                pass
        
        return self.create_session(user)
    
    def save_message(self, session, role, content, tokens_used=0):
        """Sauvegarde un message dans la session"""
        return ChatMessage.objects.create(
            session=session,
            role=role,
            content=content,
            tokens_used=tokens_used
        )
    
    def get_session_messages(self, session, limit=20):
        """Récupère les messages d'une session"""
        return ChatMessage.objects.filter(session=session).order_by('timestamp')[:limit]
    
    def _call_gemini_api(self, prompt):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise Exception("Pas de clé Google Gemini API détectée.")
        endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + api_key
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{
                "role": "user",
                "parts": [{"text": prompt}]
            }]
        }
        res = requests.post(endpoint, json=payload, headers=headers, timeout=20)
        if res.status_code == 200:
            data = res.json()
            candidates = data.get("candidates", [])
            if candidates and candidates[0]["content"]["parts"]:
                return candidates[0]["content"]["parts"][0]["text"]
            return data.get('text', "[Gemini: pas de contenu AI généré]")
        raise Exception(f"Gemini API Error: {res.status_code} - {res.text}")

    def _call_ollama_chat(self, messages, model_name=None):
        """Call local Ollama chat API.
        messages: list of {role: 'system'|'user'|'assistant', content: str}
        """
        model = model_name or os.environ.get('OLLAMA_MODEL') or 'llama3'
        endpoint = os.environ.get('OLLAMA_URL') or 'http://localhost:11434/api/chat'
        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
        }
        res = requests.post(endpoint, json=payload, timeout=60)
        if res.status_code != 200:
            raise Exception(f"Ollama API Error: {res.status_code} - {res.text}")
        data = res.json()
        # Some Ollama builds return { message: { role, content } }
        if isinstance(data, dict) and 'message' in data and 'content' in data['message']:
            return data['message']['content']
        # Some return { messages: [ ... ] }
        if isinstance(data, dict) and 'messages' in data and data['messages']:
            last = data['messages'][-1]
            return last.get('content', '')
        return str(data)

    def chat(self, user, message, session_id=None, include_context=True):
        """Fonction principale de chat"""
        # Récupérer ou créer la session
        session = self.get_or_create_session(user, session_id)
        
        # Sauvegarder le message utilisateur
        user_message = self.save_message(session, "user", message)
        
        # Construire l'historique des messages
        messages = []
        
        # Ajouter le contexte système si demandé
        if include_context:
            system_prompt = self.build_system_prompt(user)
            messages.append({"role": "system", "content": system_prompt})
        
        # Ajouter l'historique de la session
        session_messages = self.get_session_messages(session, limit=10)
        for msg in session_messages:
            if msg.role != "system":  # Éviter les doublons
                messages.append({"role": msg.role, "content": msg.content})
        
        context = self.get_skin_context(user)
        ai_reply = None
        token = self.headers.get('Authorization')
        gemini_key = os.environ.get("GEMINI_API_KEY")
        chat_engine = (os.environ.get('CHAT_ENGINE') or '').upper()

        # 0. OLLAMA first if requested
        if chat_engine == 'OLLAMA':
            try:
                # Build chat messages for Ollama (system + user/assistant history + new user message)
                ollama_messages = messages + [{"role": "user", "content": message}]
                ai_reply = self._call_ollama_chat(ollama_messages, os.environ.get('OLLAMA_MODEL'))
            except Exception as exc:
                print(f"Erreur Ollama: {exc}")
                ai_reply = None

        # 1. Gemini AI
        if not ai_reply and gemini_key:
            try:
                prompt = message
                if include_context:
                    prompt = f"Profil utilisateur: {context}\nQuestion: {message}"
                ai_reply = self._call_gemini_api(prompt)
            except Exception as exc:
                print(f"Erreur Gemini AI: {exc}")

        # 2. HuggingFace fallback
        if not ai_reply and token and 'YourPublicTokenHere' not in token:
            try:
                # Reuse last content
                hf_msgs = messages + [{"role": "user", "content": message}]
                ai_reply = self.call_ai_api(hf_msgs)
            except Exception as exc:
                print(f"Erreur IA HuggingFace: {exc}")

        # 3. Local fallback
        if not ai_reply:
            ai_reply = self.generate_fallback_response(message, context)
        
        # Sauvegarder la réponse de l'IA
        ai_message = self.save_message(session, "assistant", ai_reply)
        
        # Mettre à jour la session
        session.updated_at = datetime.now()
        session.save()
        
        return {
            "response": ai_reply,
            "session_id": session.session_id,
            "tokens_used": 0,
            "timestamp": ai_message.timestamp
        }
