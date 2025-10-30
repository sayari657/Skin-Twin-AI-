# 🧬 Skin Twin AI - Version Professionnelle

## ✅ Vérification Complète des Connexions

Cette version inclut des outils de vérification pour s'assurer que :
- ✅ Backend Django est connecté
- ✅ Base de données SQLite fonctionne
- ✅ Toutes les APIs sont accessibles
- ✅ Groq API est configurée
- ✅ Frontend communique avec le backend

---

## 🚀 Démarrage Rapide

### Backend (Django)

```bash
cd skin-twin-ai/backend
start_backend_pro.bat
```

Ou manuellement :
```bash
python manage.py migrate
python check_connections.py  # Vérifie toutes les connexions
python manage.py runserver 127.0.0.1:8000
```

### Frontend (React)

```bash
cd skin-twin-ai/frontend
npm install
npm start
```

---

## 🔍 Outils de Vérification

### 1. Script de Vérification Backend (`check_connections.py`)

Vérifie automatiquement :
- ✅ Connexion base de données SQLite
- ✅ Tables et données
- ✅ Tous les endpoints API
- ✅ Configuration Groq
- ✅ Paramètres Django

**Utilisation :**
```bash
cd skin-twin-ai/backend
python check_connections.py
```

### 2. Monitor de Santé API (Frontend)

Un composant React qui vérifie en temps réel que toutes les APIs backend sont accessibles.

**Affichage :**
- ✅ Vert : API accessible
- ⚠️ Orange : API accessible mais avec warnings
- ❌ Rouge : API inaccessible

**Position :** Coin inférieur droit (dev mode uniquement)

---

## 🔧 Configuration

### Variables d'Environnement Backend

**Pour Groq API (Chat IA) :**
```powershell
$env:GROQ_API_KEY = "votre_cle_groq"
$env:GROQ_MODEL = "llama3-8b-8192"  # Optionnel
```

**Pour Ollama (Alternative) :**
```powershell
$env:CHAT_ENGINE = "OLLAMA"
$env:OLLAMA_MODEL = "llama3"
$env:OLLAMA_URL = "http://localhost:11434/api/chat"
```

### Variables d'Environnement Frontend

Créer `.env` dans `frontend/` :
```env
REACT_APP_API_URL=http://127.0.0.1:8000/api
```

---

## 📊 Endpoints API Vérifiés

| Endpoint | Méthode | Description | Auth |
|----------|---------|-------------|------|
| `/api/users/test-no-auth/` | GET | Test sans auth | ❌ |
| `/api/users/login/` | POST | Connexion | ❌ |
| `/api/users/register/` | POST | Inscription | ❌ |
| `/api/users/profile-simple/` | GET | Profil utilisateur | ❌ |
| `/api/users/testimonials/public/` | GET | Témoignages publics | ❌ |
| `/api/detection/analyses/` | GET | Analyses de peau | ✅ |
| `/api/detection/upload/` | POST | Upload image | ✅ |
| `/api/products/` | GET | Liste produits | ❌ |
| `/api/chat-ai/chat/` | POST | Chat IA | ❌ |
| `/api/chat-ai/sessions/` | GET | Sessions chat | ✅ |
| `/api/chat-ai/suggestions/` | GET | Suggestions | ✅ |

---

## 🗄️ Base de Données

**Type :** SQLite3 (développement)
**Fichier :** `backend/db.sqlite3`

**Tables principales :**
- `users` - Utilisateurs
- `user_testimonials` - Témoignages
- `skin_analysis` - Analyses de peau
- `chat_sessions` - Sessions de chat
- `chat_messages` - Messages de chat

**Vérification :**
```bash
python check_connections.py
```

---

## 🔐 Sécurité

- ✅ CORS configuré pour `localhost:3000`
- ✅ JWT Authentication pour endpoints protégés
- ✅ Variables d'environnement pour clés API
- ✅ Validation des données côté backend

---

## 🐛 Dépannage

### Erreur 404 sur les endpoints

1. Vérifier que le serveur Django tourne :
   ```bash
   python check_connections.py
   ```

2. Vérifier les URLs dans `backend/skin_ai/urls.py`

3. Redémarrer le serveur :
   ```bash
   python manage.py runserver 127.0.0.1:8000
   ```

### Erreur de connexion base de données

1. Vérifier que `db.sqlite3` existe dans `backend/`
2. Lancer les migrations :
   ```bash
   python manage.py migrate
   ```

### Chat IA ne répond pas

1. Vérifier Groq API Key :
   ```powershell
   $env:GROQ_API_KEY
   ```

2. Si vide, configurer :
   ```powershell
   $env:GROQ_API_KEY = "votre_cle"
   ```

3. Redémarrer Django

---

## 📝 Logs

**Backend :** `backend/logs/django.log`
**Console :** Vérifier les messages dans le terminal Django

---

## ✨ Fonctionnalités Pro

- ✅ Monitoring automatique des APIs
- ✅ Vérification complète au démarrage
- ✅ Scripts de démarrage robustes
- ✅ Gestion d'erreurs améliorée
- ✅ Documentation complète

---

## 🎯 Prochaines Étapes

1. Tester toutes les fonctionnalités
2. Configurer Groq API Key pour le chat
3. Vérifier que toutes les APIs répondent correctement
4. Tester l'upload d'images
5. Tester le chat IA

---

**Version :** Pro Edition
**Dernière mise à jour :** 2024
**Statut :** ✅ Toutes les connexions vérifiées

