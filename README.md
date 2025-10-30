# Skin-Twin-AI

Une application intelligente d'analyse de la peau utilisant l'IA pour fournir des recommandations personnalisées de soins de la peau.

## 🚀 Fonctionnalités

- 🤖 Assistant IA conversationnel avec Groq API
- 🎤 Reconnaissance vocale pour interagir avec le chat
- 📸 Analyse de peau via upload d'images
- 📊 Dashboard avec statistiques et graphiques
- 💬 Système de témoignages utilisateurs
- 🔐 Authentification JWT sécurisée
- 📱 Interface moderne et responsive

## 🛠️ Technologies

### Frontend
- React + TypeScript
- Material-UI (MUI)
- React Router
- Axios
- Web Speech API

### Backend
- Django + Django REST Framework
- SQLite (développement)
- JWT Authentication
- Groq API pour l'IA

## 📦 Installation

### Prérequis
- Python 3.10+
- Node.js 16+
- npm ou yarn

### Backend

```bash
cd skin-twin-ai/backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend

```bash
cd skin-twin-ai/frontend
npm install
npm start
```

## 🔧 Configuration

### Configuration Groq API (Backend)

**Option 1 : Fichier local (recommandé pour développement)**
Créez le fichier `backend/config_local.py` (ignoré par Git) :
```python
GROQ_API_KEY_LOCAL = 'votre_cle_groq_ici'
GROQ_MODEL_LOCAL = 'llama-3.1-8b-instant'
```

**Option 2 : Variables d'environnement**
```bash
export GROQ_API_KEY=votre_cle_groq
export GROQ_MODEL=llama-3.1-8b-instant
```

**Note :** Le fichier `config_local.py` est ignoré par Git pour la sécurité. Utilisez `config_local.example.py` comme modèle.

### Variables d'environnement Frontend

Créez un fichier `.env` dans `frontend/` :
```
REACT_APP_API_URL=http://127.0.0.1:8000/api
```

## 📝 Structure du projet

```
skin-twin-ai/
├── backend/
│   ├── chat_ai/          # Module chat IA
│   ├── detection/        # Module détection de problèmes cutanés
│   ├── users/            # Module utilisateurs
│   ├── products/        # Module produits
│   └── recommendations/ # Module recommandations
├── frontend/
│   ├── src/
│   │   ├── components/  # Composants React
│   │   ├── pages/       # Pages de l'application
│   │   ├── services/    # Services API
│   │   └── utils/       # Utilitaires
└── README.md
```

## 🎯 Utilisation

1. Démarrez le backend Django sur `http://127.0.0.1:8000`
2. Démarrez le frontend React sur `http://localhost:3000`
3. Créez un compte ou connectez-vous
4. Utilisez l'assistant IA pour obtenir des conseils personnalisés
5. Uploadez une photo pour analyser votre peau

## 📄 Licence

MIT License

## 👥 Auteurs

- Mohamed Sayari

## 🙏 Remerciements

- Groq pour l'API IA
- Material-UI pour les composants UI
- Django et React pour les frameworks
