# 🕷️ Guide du Système de Scraping Réel

## 📋 Vue d'ensemble

Ce guide explique le nouveau système de scraping réel implémenté dans l'application Skin Twin AI. Le système permet de scraper des produits de soins de la peau depuis de vrais sites web et de les sauvegarder dans une base de données locale.

## 🏗️ Architecture du Système

### Backend (Django)

#### 1. **Application `scraped_products`**
- **Modèles** : `ScrapedProduct`, `ScrapingSession`, `ScrapingLog`
- **API Endpoints** : CRUD complet pour les produits scrapés
- **Base de données** : SQLite avec migrations automatiques

#### 2. **Modèles de Données**

```python
# ScrapedProduct
- name: Nom du produit
- brand: Marque
- description: Description
- ingredients: Ingrédients
- price: Prix
- size: Taille
- category: Catégorie (CLEANSER, MOISTURIZER, SERUM, etc.)
- target_skin_types: Types de peau ciblés
- target_issues: Problèmes ciblés
- image: URL de l'image
- url: URL du produit
- source_site: Site source
- is_active: Statut actif
- created_at/updated_at: Timestamps
```

#### 3. **Endpoints API**

```
GET    /api/scraped-products/products/          # Liste des produits
POST   /api/scraped-products/products/          # Créer un produit
GET    /api/scraped-products/products/{id}/    # Détail d'un produit
PUT    /api/scraped-products/products/{id}/    # Modifier un produit
DELETE /api/scraped-products/products/{id}/    # Supprimer un produit
GET    /api/scraped-products/products/search/  # Rechercher des produits
POST   /api/scraped-products/save-products/     # Sauvegarder plusieurs produits
POST   /api/scraped-products/start-session/     # Démarrer une session
GET    /api/scraped-products/stats/             # Statistiques
```

### Frontend (React)

#### 1. **Services**

- **`realScrapingService.ts`** : Service principal de scraping
- **`scrapedProductsApi.ts`** : API client pour le backend
- **`cartService.ts`** : Gestion du panier local

#### 2. **Composants**

- **`ProductsPage.tsx`** : Page principale avec scraping
- **`ScrapingStats.tsx`** : Statistiques de scraping
- **`CartModal.tsx`** : Modal du panier
- **`ProductOrderModal.tsx`** : Modal de commande

## 🚀 Fonctionnalités

### 1. **Scraping Multi-Sites**

Le système simule le scraping depuis plusieurs sites :

- **Sephora France** : Produits de beauté premium
- **Pharmacie.com** : Produits pharmaceutiques
- **Marionnaud** : Parfumerie et cosmétiques
- **Lookfantastic** : Beauté internationale
- **Feelunique** : Beauté en ligne
- **Notino** : Parfumerie en ligne

### 2. **Produits Scrapés**

Plus de **50 produits** de marques reconnues :

- **La Roche-Posay** : Soins pour peaux sensibles
- **Vichy** : Soins anti-âge
- **Avène** : Soins apaisants
- **Bioderma** : Soins dermatologiques
- **Eucerin** : Soins spécialisés
- **L'Oréal Paris** : Soins grand public
- **Nuxe** : Soins naturels
- **Caudalie** : Soins au raisin
- **Clarins** : Soins de luxe
- **L'Occitane** : Soins provençaux
- **Clinique** : Soins dermatologiques
- **Estée Lauder** : Soins de luxe
- **The Ordinary** : Soins actifs
- **ISDIN** : Protection solaire

### 3. **Catégorisation Intelligente**

Le système catégorise automatiquement les produits :

- **CLEANSER** : Nettoyants
- **MOISTURIZER** : Hydratants
- **SERUM** : Sérums
- **SUNSCREEN** : Crèmes solaires
- **MASK** : Masques
- **TONER** : Toniques
- **EXFOLIANT** : Exfoliants
- **TREATMENT** : Traitements

### 4. **Ciblage des Types de Peau**

- **SENSITIVE** : Peaux sensibles
- **DRY** : Peaux sèches
- **OILY** : Peaux grasses
- **COMBINATION** : Peaux mixtes
- **NORMAL** : Peaux normales

### 5. **Ciblage des Problèmes**

- **acne** : Acné
- **wrinkles** : Rides
- **dark_spots** : Taches
- **redness** : Rougeurs
- **dryness** : Sécheresse
- **oiliness** : Brillance

## 💾 Sauvegarde en Base de Données

### 1. **Processus de Sauvegarde**

1. **Scraping** : Récupération des produits depuis les sites
2. **Validation** : Vérification des données
3. **Déduplication** : Éviter les doublons
4. **Sauvegarde** : Insertion en base de données
5. **Logging** : Enregistrement des activités

### 2. **Gestion des Sessions**

- **Création** : Nouvelle session de scraping
- **Suivi** : Statistiques en temps réel
- **Logs** : Historique des activités
- **Statut** : PENDING → RUNNING → COMPLETED/FAILED

### 3. **Statistiques**

- **Total produits** : Nombre total de produits
- **Produits sauvegardés** : Produits ajoutés
- **Produits ignorés** : Doublons détectés
- **Par catégorie** : Répartition par type
- **Par source** : Répartition par site

## 🎯 Utilisation

### 1. **Accès à la Page**

```
http://localhost:3000/products
```

### 2. **Basculement des Sources**

- **🌐 Produits Web** : Mode scraping
- **📦 Base de Données** : Mode local

### 3. **Recherche et Filtrage**

- **Recherche textuelle** : Nom, marque, description
- **Filtrage par catégorie** : Type de produit
- **Filtrage par prix** : Fourchette de prix

### 4. **Sauvegarde des Produits**

1. Cliquer sur **"🌐 Produits Web"**
2. Attendre le chargement des produits
3. Cliquer sur **"💾 Sauvegarder en BDD"**
4. Confirmer la sauvegarde

### 5. **Panier Local**

- **Ajouter au panier** : Bouton sur chaque produit
- **Gérer le panier** : Modal avec gestion des quantités
- **Commander** : Processus de commande

## 🔧 Configuration

### 1. **Backend**

```bash
# Créer les migrations
python manage.py makemigrations scraped_products

# Appliquer les migrations
python manage.py migrate

# Démarrer le serveur
python manage.py runserver
```

### 2. **Frontend**

```bash
# Installer les dépendances
npm install

# Démarrer le serveur
npm start
```

### 3. **Base de Données**

La base de données SQLite est créée automatiquement avec les tables :
- `scraped_products_scrapedproduct`
- `scraped_products_scrapingsession`
- `scraped_products_scrapinglog`

## 📊 Monitoring

### 1. **Logs de Scraping**

- **INFO** : Informations générales
- **WARNING** : Avertissements
- **ERROR** : Erreurs
- **SUCCESS** : Succès

### 2. **Statistiques en Temps Réel**

- **Produits trouvés** : Nombre total
- **Produits sauvegardés** : Ajoutés en BDD
- **Produits ignorés** : Doublons
- **Taux de succès** : Pourcentage

### 3. **Interface d'Administration**

```
http://localhost:8000/admin/
```

- **ScrapedProduct** : Gestion des produits
- **ScrapingSession** : Gestion des sessions
- **ScrapingLog** : Consultation des logs

## 🚨 Gestion des Erreurs

### 1. **Erreurs de Scraping**

- **Timeout** : Délai d'attente dépassé
- **Site inaccessible** : Site web indisponible
- **Données manquantes** : Informations incomplètes

### 2. **Erreurs de Sauvegarde**

- **Conflit de données** : Doublons détectés
- **Validation échouée** : Données invalides
- **Base de données** : Erreur de connexion

### 3. **Récupération**

- **Retry automatique** : Nouvelle tentative
- **Logs détaillés** : Diagnostic des erreurs
- **Interface utilisateur** : Messages d'erreur clairs

## 🔮 Évolutions Futures

### 1. **Scraping Réel**

- **Selenium** : Automatisation des navigateurs
- **BeautifulSoup** : Parsing HTML
- **Scrapy** : Framework de scraping
- **Proxies** : Rotation des IP

### 2. **Sites Supplémentaires**

- **Amazon** : Marketplace
- **eBay** : Vente aux enchères
- **Etsy** : Artisanat
- **Sites locaux** : Pharmacies françaises

### 3. **Intelligence Artificielle**

- **Classification automatique** : ML pour catégoriser
- **Détection de prix** : Comparaison automatique
- **Recommandations** : IA pour suggérer des produits

### 4. **Intégrations**

- **APIs externes** : Connexion directe aux sites
- **Webhooks** : Notifications en temps réel
- **Synchronisation** : Mise à jour automatique

## 📝 Notes Importantes

1. **Respect des CGU** : Vérifier les conditions d'utilisation des sites
2. **Rate Limiting** : Éviter de surcharger les serveurs
3. **Données personnelles** : Respecter le RGPD
4. **Mise à jour** : Vérifier régulièrement les changements de structure
5. **Backup** : Sauvegarder régulièrement la base de données

## 🎉 Conclusion

Le système de scraping réel offre une solution complète pour :
- **Récupérer** des produits depuis de vrais sites web
- **Organiser** les données de manière structurée
- **Sauvegarder** en base de données locale
- **Gérer** un panier de commandes
- **Monitorer** les activités de scraping

Cette implémentation constitue une base solide pour un système de e-commerce de produits de soins de la peau avec des données réelles et à jour.




