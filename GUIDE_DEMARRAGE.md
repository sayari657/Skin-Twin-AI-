# 🚀 GUIDE DE DÉMARRAGE - SKIN TWIN AI

## 📋 Prérequis

### Logiciels nécessaires :
- **Python 3.8+** : [Télécharger Python](https://www.python.org/downloads/)
- **Node.js 16+** : [Télécharger Node.js](https://nodejs.org/)
- **Git** : [Télécharger Git](https://git-scm.com/)

### Vérification des installations :
```bash
python --version
node --version
npm --version
```

## 🛠️ Installation du projet

### 1. Cloner le projet
```bash
git clone [URL_DU_REPO]
cd skin-twin-ai
```

### 2. Configuration du Backend (Django)

#### A. Naviguer vers le dossier backend
```bash
cd skin-twin-ai/backend
```

#### B. Créer l'environnement virtuel
```bash
python -m venv venv
```

#### C. Activer l'environnement virtuel
**Windows :**
```bash
venv\Scripts\activate
```

**Linux/Mac :**
```bash
source venv/bin/activate
```

#### D. Installer les dépendances
```bash
pip install -r requirements.txt
```

#### E. Appliquer les migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

#### F. Créer un superutilisateur (optionnel)
```bash
python manage.py createsuperuser
```

### 3. Configuration du Frontend (React)

#### A. Naviguer vers le dossier frontend
```bash
cd skin-twin-ai/frontend
```

#### B. Installer les dépendances
```bash
npm install
```

## 🚀 Démarrage du projet

### Méthode 1 : Script automatique (Recommandée)

#### A. Retourner à la racine du projet
```bash
cd skin-twin-ai
```

#### B. Exécuter le script de démarrage
```bash
.\start_servers.bat
```

### Méthode 2 : Démarrage manuel

#### A. Terminal 1 - Backend Django
```bash
cd skin-twin-ai/backend
venv\Scripts\activate
python manage.py runserver 127.0.0.1:8000
```

#### B. Terminal 2 - Frontend React
```bash
cd skin-twin-ai/frontend
npm start
```

## 🌐 Accès à l'application

### URLs principales :
- **Frontend React** : http://localhost:3000
- **Backend Django** : http://127.0.0.1:8000
- **Admin Django** : http://127.0.0.1:8000/admin

### Pages disponibles :
- **Dashboard** : http://localhost:3000/dashboard
- **Upload** : http://localhost:3000/upload
- **History** : http://localhost:3000/history
- **Products** : http://localhost:3000/products
- **Profile** : http://localhost:3000/profile

## 🔧 Configuration avancée

### Variables d'environnement (optionnel)
Créer un fichier `.env` dans `skin-twin-ai/backend/` :
```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Base de données
Le projet utilise SQLite par défaut. Pour utiliser PostgreSQL :
1. Installer PostgreSQL
2. Modifier `settings.py`
3. Créer la base de données
4. Exécuter les migrations

## 🎯 Fonctionnalités principales

### 1. Assistant IA Intelligent
- **Chat contextuel** : Réponses basées sur le profil utilisateur
- **Mode vocal** : Reconnaissance vocale intégrée
- **Déplaçable** : Glissez l'assistant partout sur l'écran
- **Historique** : Gestion des sessions de chat

### 2. Analyse de peau
- **Upload d'images** : Analyse automatique
- **Détection de problèmes** : Acné, rides, taches, etc.
- **Recommandations** : Produits adaptés

### 3. Base de données produits
- **112 produits** : Base complète de cosmétiques
- **Images** : Photos des produits
- **Recommandations** : Basées sur l'analyse

### 4. Interface utilisateur
- **Design moderne** : Interface Material-UI
- **Responsive** : Adapté à tous les écrans
- **Animations** : Transitions fluides

## 🐛 Résolution de problèmes

### Erreur "Port already in use"
```bash
# Tuer le processus sur le port 3000
npx kill-port 3000
# Tuer le processus sur le port 8000
npx kill-port 8000
```

### Erreur "Module not found"
```bash
# Réinstaller les dépendances
cd skin-twin-ai/frontend
rm -rf node_modules package-lock.json
npm install
```

### Erreur "Python not found"
```bash
# Vérifier l'installation Python
python --version
# Ou utiliser python3
python3 --version
```

### Erreur de base de données
```bash
# Supprimer et recréer la base
cd skin-twin-ai/backend
rm db.sqlite3
python manage.py migrate
```

## 📱 Utilisation de l'application

### 1. Première connexion
1. Aller sur http://localhost:3000
2. Cliquer sur "S'inscrire"
3. Remplir le formulaire
4. Se connecter

### 2. Utilisation de l'assistant IA
1. Cliquer sur "🎤 Parler à l'IA"
2. L'assistant s'ouvre en bas à droite
3. Glisser l'assistant où vous voulez
4. Taper ou parler votre question
5. Recevoir des conseils personnalisés

### 3. Analyse de peau
1. Aller sur "Upload"
2. Télécharger une photo de votre visage
3. Attendre l'analyse
4. Voir les résultats et recommandations

### 4. Navigation
- **Dashboard** : Vue d'ensemble
- **Upload** : Analyser une photo
- **History** : Historique des analyses
- **Products** : Catalogue de produits
- **Profile** : Gérer le profil

## 🎨 Personnalisation

### Modifier les couleurs
Éditer `skin-twin-ai/frontend/src/medical-theme.css`

### Ajouter des produits
Utiliser l'interface admin Django ou les scripts Python

### Modifier l'IA
Éditer `skin-twin-ai/backend/chat_ai/services.py`

## 📞 Support

### Logs de débogage
```bash
# Backend
cd skin-twin-ai/backend
python manage.py runserver --verbosity=2

# Frontend
cd skin-twin-ai/frontend
npm start --verbose
```

### Vérification de l'état
```bash
# Vérifier les ports
netstat -an | findstr :3000
netstat -an | findstr :8000
```

## 🚀 Déploiement

### Production
1. Configurer les variables d'environnement
2. Utiliser un serveur web (Nginx, Apache)
3. Configurer HTTPS
4. Utiliser une base de données PostgreSQL

### Docker (optionnel)
```bash
cd skin-twin-ai
docker-compose up -d
```

## 📚 Documentation technique

### Structure du projet
```
skin-twin-ai/
├── backend/          # Django API
├── frontend/          # React App
├── ml_models/         # Modèles IA
├── data/             # Données
└── docs/             # Documentation
```

### Technologies utilisées
- **Backend** : Django, Django REST Framework
- **Frontend** : React, TypeScript, Material-UI
- **IA** : Hugging Face API, Reconnaissance vocale
- **Base de données** : SQLite (dev), PostgreSQL (prod)

## ✅ Checklist de démarrage

- [ ] Python 3.8+ installé
- [ ] Node.js 16+ installé
- [ ] Projet cloné
- [ ] Environnement virtuel créé
- [ ] Dépendances backend installées
- [ ] Dépendances frontend installées
- [ ] Migrations appliquées
- [ ] Serveurs démarrés
- [ ] Application accessible sur http://localhost:3000

## 🎉 Félicitations !

Votre application Skin Twin AI est maintenant prête à l'emploi !

**URLs importantes :**
- Application : http://localhost:3000
- API : http://127.0.0.1:8000
- Admin : http://127.0.0.1:8000/admin

**Fonctionnalités disponibles :**
- ✅ Assistant IA intelligent et déplaçable
- ✅ Analyse de peau automatique
- ✅ Base de données de 112 produits
- ✅ Interface moderne et responsive
- ✅ Mode vocal intégré
- ✅ Chat contextuel personnalisé

**Bon développement ! 🚀**


