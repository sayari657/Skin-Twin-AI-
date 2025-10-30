#!/usr/bin/env python
"""
Script pour explorer la base de donnees SQLite3 de Skin Twin AI
Usage: python explore_database.py
"""

import sqlite3
import os

def explore_database():
    """Explore la base de donnees et affiche les informations principales"""
    
    # Chemin vers la base de donnees
    db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite3')
    
    if not os.path.exists(db_path):
        print("ERREUR: Base de donnees non trouvee!")
        print(f"   Chemin attendu: {db_path}")
        return
    
    print("EXPLORATION DE LA BASE DE DONNEES SKIN TWIN AI")
    print("=" * 60)
    
    try:
        # Connexion a la base
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Voir toutes les tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"\nTABLES DISPONIBLES ({len(tables)}):")
        for table in tables:
            print(f"   - {table[0]}")
        
        # Initialiser les compteurs
        user_count = 0
        session_count = 0
        message_count = 0
        product_count = 0
        analysis_count = 0
        scraped_count = 0
        
        # Informations sur les utilisateurs
        try:
            cursor.execute("SELECT COUNT(*) FROM users;")
            user_count = cursor.fetchone()[0]
            print(f"\nUTILISATEURS: {user_count}")
            
            if user_count > 0:
                cursor.execute("SELECT id, username, email, first_name, last_name FROM users LIMIT 5;")
                users = cursor.fetchall()
                print("   Derniers utilisateurs:")
                for user in users:
                    print(f"     ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Name: {user[3]} {user[4]}")
        except Exception as e:
            print(f"   Erreur utilisateurs: {e}")
        
        # Informations sur les sessions de chat
        try:
            cursor.execute("SELECT COUNT(*) FROM chat_sessions;")
            session_count = cursor.fetchone()[0]
            print(f"\nSESSIONS DE CHAT: {session_count}")
            
            if session_count > 0:
                cursor.execute("SELECT id, session_id, user_id, created_at FROM chat_sessions ORDER BY created_at DESC LIMIT 3;")
                sessions = cursor.fetchall()
                print("   Dernieres sessions:")
                for session in sessions:
                    print(f"     ID: {session[0]}, Session: {session[1]}, User: {session[2]}, Date: {session[3]}")
        except Exception as e:
            print(f"   Erreur sessions: {e}")
        
        # Informations sur les messages de chat
        try:
            cursor.execute("SELECT COUNT(*) FROM chat_messages;")
            message_count = cursor.fetchone()[0]
            print(f"\nMESSAGES DE CHAT: {message_count}")
            
            if message_count > 0:
                cursor.execute("SELECT id, role, content, timestamp FROM chat_messages ORDER BY timestamp DESC LIMIT 3;")
                messages = cursor.fetchall()
                print("   Derniers messages:")
                for message in messages:
                    content = message[2][:50] + "..." if len(message[2]) > 50 else message[2]
                    print(f"     ID: {message[0]}, Role: {message[1]}, Content: {content}, Time: {message[3]}")
        except Exception as e:
            print(f"   Erreur messages: {e}")
        
        # Informations sur les produits
        try:
            cursor.execute("SELECT COUNT(*) FROM products;")
            product_count = cursor.fetchone()[0]
            print(f"\nPRODUITS: {product_count}")
            
            if product_count > 0:
                cursor.execute("SELECT id, name, brand, price FROM products LIMIT 5;")
                products = cursor.fetchall()
                print("   Quelques produits:")
                for product in products:
                    print(f"     ID: {product[0]}, Name: {product[1]}, Brand: {product[2]}, Price: {product[3]}")
        except Exception as e:
            print(f"   Erreur produits: {e}")
        
        # Informations sur les analyses de peau
        try:
            cursor.execute("SELECT COUNT(*) FROM skin_analyses;")
            analysis_count = cursor.fetchone()[0]
            print(f"\nANALYSES DE PEAU: {analysis_count}")
            
            if analysis_count > 0:
                cursor.execute("SELECT id, user_id, detected_problems, overall_score, created_at FROM skin_analyses ORDER BY created_at DESC LIMIT 3;")
                analyses = cursor.fetchall()
                print("   Dernieres analyses:")
                for analysis in analyses:
                    print(f"     ID: {analysis[0]}, User: {analysis[1]}, Problems: {analysis[2]}, Score: {analysis[3]}, Date: {analysis[4]}")
        except Exception as e:
            print(f"   Erreur analyses: {e}")
        
        # Informations sur les produits scrapes
        try:
            cursor.execute("SELECT COUNT(*) FROM scraped_products_scrapedproduct;")
            scraped_count = cursor.fetchone()[0]
            print(f"\nPRODUITS SCRAPES: {scraped_count}")
            
            if scraped_count > 0:
                cursor.execute("SELECT id, name, brand, price FROM scraped_products_scrapedproduct LIMIT 5;")
                scraped = cursor.fetchall()
                print("   Quelques produits scrapes:")
                for item in scraped:
                    print(f"     ID: {item[0]}, Name: {item[1]}, Brand: {item[2]}, Price: {item[3]}")
        except Exception as e:
            print(f"   Erreur produits scrapes: {e}")
        
        # Statistiques generales
        print(f"\nSTATISTIQUES GENERALES:")
        print(f"   - Tables: {len(tables)}")
        print(f"   - Utilisateurs: {user_count}")
        print(f"   - Sessions chat: {session_count}")
        print(f"   - Messages: {message_count}")
        print(f"   - Produits: {product_count}")
        print(f"   - Analyses: {analysis_count}")
        print(f"   - Produits scrapes: {scraped_count}")
        
        print(f"\nEXPLORATION TERMINEE!")
        print(f"   Base de donnees: {db_path}")
        print(f"   Taille: {os.path.getsize(db_path) / 1024:.1f} KB")
        
    except Exception as e:
        print(f"ERREUR: {e}")
    
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    explore_database()