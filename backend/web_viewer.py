from flask import Flask, render_template_string
import sqlite3
import os

app = Flask(__name__)

def get_db_data():
    """Récupérer les données de la base"""
    db_path = 'db.sqlite3'
    
    if not os.path.exists(db_path):
        return {"error": "Base de données non trouvée"}
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        data = {}
        
        # Compter les produits scrapés
        try:
            cursor.execute("SELECT COUNT(*) FROM scraped_products_scrapedproduct")
            data['scraped_products'] = cursor.fetchone()[0]
        except:
            data['scraped_products'] = 0
        
        # Compter les utilisateurs
        try:
            cursor.execute("SELECT COUNT(*) FROM users_user")
            data['users'] = cursor.fetchone()[0]
        except:
            data['users'] = 0
        
        # Derniers produits
        try:
            cursor.execute("""
                SELECT name, brand, price, category 
                FROM scraped_products_scrapedproduct 
                ORDER BY created_at DESC 
                LIMIT 10
            """)
            data['recent_products'] = cursor.fetchall()
        except:
            data['recent_products'] = []
        
        conn.close()
        return data
        
    except Exception as e:
        return {"error": str(e)}

@app.route('/')
def index():
    data = get_db_data()
    
    if "error" in data:
        return f"<h1>❌ Erreur: {data['error']}</h1>"
    
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Base de Données Skin Twin AI</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
            .container { max-width: 1000px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }
            .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }
            .stat-card { background: #e3f2fd; padding: 20px; border-radius: 8px; text-align: center; }
            .stat-number { font-size: 2em; font-weight: bold; color: #1976d2; }
            .stat-label { color: #666; }
            table { width: 100%; border-collapse: collapse; margin: 20px 0; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            h1 { color: #1976d2; text-align: center; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🗄️ Base de Données Skin Twin AI</h1>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">{{ data.scraped_products }}</div>
                    <div class="stat-label">Produits Scrapés</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ data.users }}</div>
                    <div class="stat-label">Utilisateurs</div>
                </div>
            </div>
            
            <h2>🕷️ Derniers Produits Scrapés</h2>
            {% if data.recent_products %}
            <table>
                <tr>
                    <th>Nom</th>
                    <th>Marque</th>
                    <th>Prix</th>
                    <th>Catégorie</th>
                </tr>
                {% for product in data.recent_products %}
                <tr>
                    <td>{{ product[0] }}</td>
                    <td>{{ product[1] }}</td>
                    <td>{{ product[2] }}€</td>
                    <td>{{ product[3] }}</td>
                </tr>
                {% endfor %}
            </table>
            {% else %}
            <p>Aucun produit scrapé trouvé</p>
            {% endif %}
            
            <h2>🔗 Liens Utiles</h2>
            <ul>
                <li><a href="http://127.0.0.1:8000/admin/">Interface Django Admin</a></li>
                <li><a href="http://localhost:3000/products">Page des Produits</a></li>
            </ul>
        </div>
    </body>
    </html>
    """, data=data)

if __name__ == '__main__':
    print("🌐 Démarrage du serveur web...")
    print("📱 Ouvrez: http://localhost:5000")
    app.run(debug=True, port=5000)




