# 🗄️ Guide pour Visualiser la Base de Données SQLite

## 📋 Vue d'ensemble

Ce guide explique comment visualiser et gérer la base de données SQLite de l'application Skin Twin AI en utilisant XAMPP et d'autres outils.

## 🔧 Méthode 1 : XAMPP avec SQLite Support

### 1. **Installer SQLite Support dans XAMPP**

1. **Télécharger SQLite Browser** :
   - Aller sur : https://sqlitebrowser.org/
   - Télécharger "DB Browser for SQLite"
   - Installer l'application

2. **Alternative - SQLite Extension pour XAMPP** :
   - Télécharger l'extension SQLite pour PHP
   - Ajouter dans `php.ini` : `extension=sqlite3`

### 2. **Localiser le Fichier de Base de Données**

Le fichier SQLite se trouve dans :
```
skin-twin-ai/backend/db.sqlite3
```

### 3. **Ouvrir avec DB Browser for SQLite**

1. **Lancer DB Browser for SQLite**
2. **Cliquer sur "Open Database"**
3. **Naviguer vers** : `C:\Users\Mohamed\Desktop\skin twin ai\skin-twin-ai\backend\db.sqlite3`
4. **Ouvrir le fichier**

### 4. **Explorer les Tables**

Vous verrez les tables suivantes :
- `scraped_products_scrapedproduct` - Produits scrapés
- `scraped_products_scrapingsession` - Sessions de scraping
- `scraped_products_scrapinglog` - Logs de scraping
- `users_user` - Utilisateurs
- `detection_analysis` - Analyses de peau
- Et d'autres tables Django...

## 🔧 Méthode 2 : Interface Web Django Admin

### 1. **Démarrer le Serveur Django**

```bash
cd "skin-twin-ai\backend"
python manage.py runserver
```

### 2. **Accéder à l'Interface Admin**

1. **Ouvrir le navigateur**
2. **Aller sur** : `http://127.0.0.1:8000/admin/`
3. **Se connecter** avec un superutilisateur

### 3. **Créer un Superutilisateur (si nécessaire)**

```bash
cd "skin-twin-ai\backend"
python manage.py createsuperuser
```

### 4. **Explorer les Données**

- **Scraped products** : Produits scrapés
- **Scraping sessions** : Sessions de scraping
- **Scraping logs** : Logs d'activité
- **Users** : Utilisateurs
- **Analyses** : Analyses de peau

## 🔧 Méthode 3 : Utiliser SQLite Browser Directement

### 1. **Télécharger SQLite Browser**

- **Site officiel** : https://sqlitebrowser.org/
- **Télécharger** : DB Browser for SQLite
- **Installer** l'application

### 2. **Ouvrir la Base de Données**

1. **Lancer DB Browser for SQLite**
2. **File → Open Database**
3. **Sélectionner** : `skin-twin-ai\backend\db.sqlite3`

### 3. **Explorer les Données**

- **Onglet "Database Structure"** : Voir les tables
- **Onglet "Browse Data"** : Voir les données
- **Onglet "Execute SQL"** : Exécuter des requêtes

## 🔧 Méthode 4 : Interface Web Personnalisée

### 1. **Créer une Interface Web Simple**

Créer un fichier `view_database.html` :

```html
<!DOCTYPE html>
<html>
<head>
    <title>Base de Données Skin Twin AI</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h1>🗄️ Base de Données Skin Twin AI</h1>
    
    <h2>📊 Statistiques</h2>
    <ul>
        <li><strong>Produits scrapés</strong> : [Nombre]</li>
        <li><strong>Sessions de scraping</strong> : [Nombre]</li>
        <li><strong>Utilisateurs</strong> : [Nombre]</li>
        <li><strong>Analyses</strong> : [Nombre]</li>
    </ul>
    
    <h2>🕷️ Produits Scrapés</h2>
    <table>
        <tr>
            <th>ID</th>
            <th>Nom</th>
            <th>Marque</th>
            <th>Prix</th>
            <th>Catégorie</th>
            <th>Source</th>
            <th>Date</th>
        </tr>
        <!-- Données des produits scrapés -->
    </table>
    
    <h2>📈 Sessions de Scraping</h2>
    <table>
        <tr>
            <th>ID</th>
            <th>Nom</th>
            <th>Statut</th>
            <th>Produits trouvés</th>
            <th>Produits sauvegardés</th>
            <th>Date de début</th>
        </tr>
        <!-- Données des sessions -->
    </table>
</body>
</html>
```

## 🔧 Méthode 5 : Utiliser Python pour Explorer

### 1. **Script Python pour Explorer la Base**

Créer un fichier `explore_database.py` :

```python
import sqlite3
import json
from datetime import datetime

def explore_database():
    # Connexion à la base de données
    conn = sqlite3.connect('skin-twin-ai/backend/db.sqlite3')
    cursor = conn.cursor()
    
    print("🗄️ EXPLORATION DE LA BASE DE DONNÉES SKIN TWIN AI")
    print("=" * 60)
    
    # Lister toutes les tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print(f"\n📋 TABLES DISPONIBLES ({len(tables)}):")
    for table in tables:
        print(f"  - {table[0]}")
    
    # Statistiques générales
    print(f"\n📊 STATISTIQUES GÉNÉRALES:")
    
    # Produits scrapés
    try:
        cursor.execute("SELECT COUNT(*) FROM scraped_products_scrapedproduct")
        scraped_count = cursor.fetchone()[0]
        print(f"  - Produits scrapés : {scraped_count}")
    except:
        print("  - Produits scrapés : 0")
    
    # Sessions de scraping
    try:
        cursor.execute("SELECT COUNT(*) FROM scraped_products_scrapingsession")
        sessions_count = cursor.fetchone()[0]
        print(f"  - Sessions de scraping : {sessions_count}")
    except:
        print("  - Sessions de scraping : 0")
    
    # Utilisateurs
    try:
        cursor.execute("SELECT COUNT(*) FROM users_user")
        users_count = cursor.fetchone()[0]
        print(f"  - Utilisateurs : {users_count}")
    except:
        print("  - Utilisateurs : 0")
    
    # Analyses
    try:
        cursor.execute("SELECT COUNT(*) FROM detection_analysis")
        analyses_count = cursor.fetchone()[0]
        print(f"  - Analyses : {analyses_count}")
    except:
        print("  - Analyses : 0")
    
    # Derniers produits scrapés
    print(f"\n🕷️ DERNIERS PRODUITS SCRAPÉS:")
    try:
        cursor.execute("""
            SELECT name, brand, price, category, source_site, created_at 
            FROM scraped_products_scrapedproduct 
            ORDER BY created_at DESC 
            LIMIT 5
        """)
        products = cursor.fetchall()
        
        for product in products:
            print(f"  - {product[1]} - {product[0]} ({product[2]}€) - {product[3]} - {product[4]}")
    except Exception as e:
        print(f"  - Erreur : {e}")
    
    # Sessions récentes
    print(f"\n📈 SESSIONS RÉCENTES:")
    try:
        cursor.execute("""
            SELECT session_name, status, total_products_found, total_products_saved, started_at 
            FROM scraped_products_scrapingsession 
            ORDER BY started_at DESC 
            LIMIT 3
        """)
        sessions = cursor.fetchall()
        
        for session in sessions:
            print(f"  - {session[0]} - {session[1]} - {session[2]} trouvés, {session[3]} sauvegardés")
    except Exception as e:
        print(f"  - Erreur : {e}")
    
    conn.close()
    print(f"\n✅ Exploration terminée !")

if __name__ == "__main__":
    explore_database()
```

### 2. **Exécuter le Script**

```bash
cd "skin-twin-ai\backend"
python explore_database.py
```

## 🔧 Méthode 6 : Interface Web avec Flask

### 1. **Créer une Interface Web Simple**

Créer un fichier `web_database_viewer.py` :

```python
from flask import Flask, render_template_string
import sqlite3
import json

app = Flask(__name__)

def get_database_stats():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    stats = {}
    
    # Compter les produits scrapés
    try:
        cursor.execute("SELECT COUNT(*) FROM scraped_products_scrapedproduct")
        stats['scraped_products'] = cursor.fetchone()[0]
    except:
        stats['scraped_products'] = 0
    
    # Compter les sessions
    try:
        cursor.execute("SELECT COUNT(*) FROM scraped_products_scrapingsession")
        stats['sessions'] = cursor.fetchone()[0]
    except:
        stats['sessions'] = 0
    
    # Compter les utilisateurs
    try:
        cursor.execute("SELECT COUNT(*) FROM users_user")
        stats['users'] = cursor.fetchone()[0]
    except:
        stats['users'] = 0
    
    conn.close()
    return stats

@app.route('/')
def index():
    stats = get_database_stats()
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Base de Données Skin Twin AI</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }
            .stat-card { background: #e3f2fd; padding: 20px; border-radius: 8px; text-align: center; }
            .stat-number { font-size: 2em; font-weight: bold; color: #1976d2; }
            .stat-label { color: #666; margin-top: 5px; }
            h1 { color: #1976d2; text-align: center; }
            h2 { color: #333; border-bottom: 2px solid #1976d2; padding-bottom: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🗄️ Base de Données Skin Twin AI</h1>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">{{ stats.scraped_products }}</div>
                    <div class="stat-label">Produits Scrapés</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ stats.sessions }}</div>
                    <div class="stat-label">Sessions de Scraping</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ stats.users }}</div>
                    <div class="stat-label">Utilisateurs</div>
                </div>
            </div>
            
            <h2>📋 Informations</h2>
            <p>Cette interface vous permet de visualiser les statistiques de votre base de données SQLite.</p>
            <p><strong>Fichier de base de données :</strong> skin-twin-ai/backend/db.sqlite3</p>
            <p><strong>Interface Django Admin :</strong> <a href="http://127.0.0.1:8000/admin/">http://127.0.0.1:8000/admin/</a></p>
        </div>
    </body>
    </html>
    """, stats=stats)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### 2. **Démarrer l'Interface Web**

```bash
cd "skin-twin-ai\backend"
pip install flask
python web_database_viewer.py
```

### 3. **Accéder à l'Interface**

Ouvrir : `http://localhost:5000`

## 🎯 **Recommandations**

### **Pour Débuter (Facile)**
1. **DB Browser for SQLite** - Interface graphique simple
2. **Django Admin** - Interface web intégrée

### **Pour Développeurs (Avancé)**
1. **Scripts Python** - Exploration programmatique
2. **Interface Flask** - Interface web personnalisée

### **Pour Production (Professionnel)**
1. **phpMyAdmin** avec SQLite support
2. **Outils de monitoring** spécialisés

## 📝 **Notes Importantes**

1. **Sauvegarde** : Toujours sauvegarder `db.sqlite3` avant modifications
2. **Permissions** : Vérifier les permissions d'accès au fichier
3. **Concurrence** : Éviter les accès simultanés à la base
4. **Sécurité** : Ne pas exposer la base en production sans protection

## 🚀 **Prochaines Étapes**

1. **Choisir une méthode** selon vos besoins
2. **Installer les outils** nécessaires
3. **Explorer la base** de données
4. **Configurer des sauvegardes** automatiques
5. **Mettre en place un monitoring** régulier




