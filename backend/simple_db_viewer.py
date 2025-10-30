import sqlite3
import os

def view_database():
    """Afficher le contenu de la base de données"""
    
    db_path = 'db.sqlite3'
    
    if not os.path.exists(db_path):
        print("❌ Base de données non trouvée !")
        print(f"   Cherché dans : {os.path.abspath(db_path)}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🗄️ BASE DE DONNÉES SKIN TWIN AI")
        print("=" * 40)
        
        # Lister les tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"\n📋 TABLES ({len(tables)}):")
        for table in tables:
            print(f"  - {table[0]}")
        
        # Compter les produits scrapés
        try:
            cursor.execute("SELECT COUNT(*) FROM scraped_products_scrapedproduct")
            count = cursor.fetchone()[0]
            print(f"\n🕷️ PRODUITS SCRAPÉS: {count}")
            
            if count > 0:
                cursor.execute("SELECT name, brand, price FROM scraped_products_scrapedproduct LIMIT 5")
                products = cursor.fetchall()
                print("   Derniers produits:")
                for product in products:
                    print(f"   - {product[1]} - {product[0]} ({product[2]}€)")
        except:
            print("\n🕷️ PRODUITS SCRAPÉS: 0")
        
        # Compter les utilisateurs
        try:
            cursor.execute("SELECT COUNT(*) FROM users_user")
            count = cursor.fetchone()[0]
            print(f"\n👥 UTILISATEURS: {count}")
        except:
            print("\n👥 UTILISATEURS: 0")
        
        conn.close()
        print(f"\n✅ Exploration terminée !")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    view_database()




