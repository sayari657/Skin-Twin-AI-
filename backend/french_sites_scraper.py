#!/usr/bin/env python3
"""
Scraper pour les sites français de cosmétiques
Sephora, Nocibé, Marionnaud, Douglas
"""

import os
import sys
import django
import requests
from bs4 import BeautifulSoup
import time
import random
from urllib.parse import urljoin, urlparse
import re
from multiprocessing import Pool
import json

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skin_ai.settings')
django.setup()

from recommendations.models import Product

def get_random_user_agent():
    """Génère un User-Agent aléatoire"""
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59'
    ]
    return random.choice(user_agents)

def fetch_page(url, max_retries=3):
    """Récupère une page avec gestion d'erreurs"""
    headers = {
        'User-Agent': get_random_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code == 200:
                return response
            elif response.status_code == 403:
                print(f"Accès refusé pour {url}, tentative {attempt + 1}")
                time.sleep(random.uniform(2, 5))
            else:
                print(f"Erreur {response.status_code} pour {url}")
                time.sleep(random.uniform(1, 3))
        except requests.exceptions.RequestException as e:
            print(f"Erreur de requête pour {url}: {e}")
            time.sleep(random.uniform(1, 3))
    
    return None

def scrape_sephora_page(url):
    """Scrape une page Sephora"""
    print(f"Scraping Sephora: {url}")
    
    response = fetch_page(url)
    if not response:
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    products = []
    
    # Sélecteurs Sephora
    product_cards = soup.find_all('div', class_=['product-item', 'product-tile'])
    
    for card in product_cards:
        try:
            # Nom du produit
            name_elem = card.find(['h3', 'h4', 'a'], class_=['product-name', 'product-title'])
            if not name_elem:
                continue
            name = name_elem.get_text(strip=True)
            
            # Prix
            price_elem = card.find(['span', 'div'], class_=['price', 'product-price'])
            price = "0.00"
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                price_match = re.search(r'(\d+[,.]?\d*)', price_text.replace(',', '.'))
                if price_match:
                    price = price_match.group(1)
            
            # Image
            img_elem = card.find('img')
            image_url = ""
            if img_elem and img_elem.get('src'):
                image_url = urljoin(url, img_elem['src'])
            
            # Lien produit
            link_elem = card.find('a', href=True)
            product_url = ""
            if link_elem:
                product_url = urljoin(url, link_elem['href'])
            
            # Marque
            brand_elem = card.find(['span', 'div'], class_=['brand', 'product-brand'])
            brand = brand_elem.get_text(strip=True) if brand_elem else "Sephora"
            
            if name and name != "Sephora":
                products.append({
                    'name': name,
                    'brand': brand,
                    'price': float(price),
                    'image_url': image_url,
                    'url': product_url,
                    'source': 'Sephora'
                })
                
        except Exception as e:
            print(f"Erreur lors du parsing d'un produit Sephora: {e}")
            continue
    
    print(f"Sephora: {len(products)} produits trouvés")
    return products

def scrape_nocibe_page(url):
    """Scrape une page Nocibé"""
    print(f"Scraping Nocibé: {url}")
    
    response = fetch_page(url)
    if not response:
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    products = []
    
    # Sélecteurs Nocibé
    product_cards = soup.find_all('div', class_=['product-item', 'product-card'])
    
    for card in product_cards:
        try:
            # Nom du produit
            name_elem = card.find(['h3', 'h4', 'a'], class_=['product-name', 'product-title'])
            if not name_elem:
                continue
            name = name_elem.get_text(strip=True)
            
            # Prix
            price_elem = card.find(['span', 'div'], class_=['price', 'product-price'])
            price = "0.00"
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                price_match = re.search(r'(\d+[,.]?\d*)', price_text.replace(',', '.'))
                if price_match:
                    price = price_match.group(1)
            
            # Image
            img_elem = card.find('img')
            image_url = ""
            if img_elem and img_elem.get('src'):
                image_url = urljoin(url, img_elem['src'])
            
            # Lien produit
            link_elem = card.find('a', href=True)
            product_url = ""
            if link_elem:
                product_url = urljoin(url, link_elem['href'])
            
            # Marque
            brand_elem = card.find(['span', 'div'], class_=['brand', 'product-brand'])
            brand = brand_elem.get_text(strip=True) if brand_elem else "Nocibé"
            
            if name and name != "Nocibé":
                products.append({
                    'name': name,
                    'brand': brand,
                    'price': float(price),
                    'image_url': image_url,
                    'url': product_url,
                    'source': 'Nocibé'
                })
                
        except Exception as e:
            print(f"Erreur lors du parsing d'un produit Nocibé: {e}")
            continue
    
    print(f"Nocibé: {len(products)} produits trouvés")
    return products

def scrape_marionnaud_page(url):
    """Scrape une page Marionnaud"""
    print(f"Scraping Marionnaud: {url}")
    
    response = fetch_page(url)
    if not response:
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    products = []
    
    # Sélecteurs Marionnaud
    product_cards = soup.find_all('div', class_=['product-item', 'product-card'])
    
    for card in product_cards:
        try:
            # Nom du produit
            name_elem = card.find(['h3', 'h4', 'a'], class_=['product-name', 'product-title'])
            if not name_elem:
                continue
            name = name_elem.get_text(strip=True)
            
            # Prix
            price_elem = card.find(['span', 'div'], class_=['price', 'product-price'])
            price = "0.00"
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                price_match = re.search(r'(\d+[,.]?\d*)', price_text.replace(',', '.'))
                if price_match:
                    price = price_match.group(1)
            
            # Image
            img_elem = card.find('img')
            image_url = ""
            if img_elem and img_elem.get('src'):
                image_url = urljoin(url, img_elem['src'])
            
            # Lien produit
            link_elem = card.find('a', href=True)
            product_url = ""
            if link_elem:
                product_url = urljoin(url, link_elem['href'])
            
            # Marque
            brand_elem = card.find(['span', 'div'], class_=['brand', 'product-brand'])
            brand = brand_elem.get_text(strip=True) if brand_elem else "Marionnaud"
            
            if name and name != "Marionnaud":
                products.append({
                    'name': name,
                    'brand': brand,
                    'price': float(price),
                    'image_url': image_url,
                    'url': product_url,
                    'source': 'Marionnaud'
                })
                
        except Exception as e:
            print(f"Erreur lors du parsing d'un produit Marionnaud: {e}")
            continue
    
    print(f"Marionnaud: {len(products)} produits trouvés")
    return products

def scrape_douglas_page(url):
    """Scrape une page Douglas"""
    print(f"Scraping Douglas: {url}")
    
    response = fetch_page(url)
    if not response:
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    products = []
    
    # Sélecteurs Douglas
    product_cards = soup.find_all('div', class_=['product-item', 'product-card'])
    
    for card in product_cards:
        try:
            # Nom du produit
            name_elem = card.find(['h3', 'h4', 'a'], class_=['product-name', 'product-title'])
            if not name_elem:
                continue
            name = name_elem.get_text(strip=True)
            
            # Prix
            price_elem = card.find(['span', 'div'], class_=['price', 'product-price'])
            price = "0.00"
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                price_match = re.search(r'(\d+[,.]?\d*)', price_text.replace(',', '.'))
                if price_match:
                    price = price_match.group(1)
            
            # Image
            img_elem = card.find('img')
            image_url = ""
            if img_elem and img_elem.get('src'):
                image_url = urljoin(url, img_elem['src'])
            
            # Lien produit
            link_elem = card.find('a', href=True)
            product_url = ""
            if link_elem:
                product_url = urljoin(url, link_elem['href'])
            
            # Marque
            brand_elem = card.find(['span', 'div'], class_=['brand', 'product-brand'])
            brand = brand_elem.get_text(strip=True) if brand_elem else "Douglas"
            
            if name and name != "Douglas":
                products.append({
                    'name': name,
                    'brand': brand,
                    'price': float(price),
                    'image_url': image_url,
                    'url': product_url,
                    'source': 'Douglas'
                })
                
        except Exception as e:
            print(f"Erreur lors du parsing d'un produit Douglas: {e}")
            continue
    
    print(f"Douglas: {len(products)} produits trouvés")
    return products

def download_and_save_image(image_url, product_name):
    """Télécharge et sauvegarde une image"""
    if not image_url:
        return None
    
    try:
        response = requests.get(image_url, timeout=30)
        if response.status_code == 200:
            # Créer le dossier media/products s'il n'existe pas
            media_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'media', 'products')
            os.makedirs(media_dir, exist_ok=True)
            
            # Nom de fichier sécurisé
            safe_name = re.sub(r'[^\w\-_\.]', '_', product_name)[:50]
            filename = f"{safe_name}_{int(time.time())}.jpg"
            filepath = os.path.join(media_dir, filename)
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            return f"products/{filename}"
    except Exception as e:
        print(f"Erreur lors du téléchargement de l'image {image_url}: {e}")
    
    return None

def save_products_to_db(products):
    """Sauvegarde les produits en base de données"""
    saved_count = 0
    image_count = 0
    
    for product_data in products:
        try:
            # Vérifier si le produit existe déjà
            existing = Product.objects.filter(
                name=product_data['name'],
                brand=product_data['brand']
            ).first()
            
            if existing:
                continue
            
            # Télécharger l'image si disponible
            image_path = None
            if product_data.get('image_url'):
                image_path = download_and_save_image(
                    product_data['image_url'], 
                    product_data['name']
                )
                if image_path:
                    image_count += 1
            
            # Créer le produit
            product = Product.objects.create(
                name=product_data['name'],
                brand=product_data['brand'],
                price=product_data['price'],
                description=f"Produit {product_data['source']} - {product_data['name']}",
                category="MOISTURIZER",
                ingredients="Non spécifié",
                image=image_path
            )
            
            saved_count += 1
            print(f"Produit sauvegardé: {product.name}")
            
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du produit {product_data.get('name', 'Inconnu')}: {e}")
            continue
    
    return saved_count, image_count

def generate_french_urls():
    """Génère les URLs pour les sites français"""
    base_urls = {
        'Sephora': 'https://www.sephora.fr',
        'Nocibé': 'https://www.nocibe.fr',
        'Marionnaud': 'https://www.marionnaud.fr',
        'Douglas': 'https://www.douglas.fr'
    }
    
    keywords = [
        'creme-visage', 'serum-visage', 'nettoyant-visage',
        'masque-visage', 'anti-age', 'hydratant-visage',
        'exfoliant-visage', 'tonique-visage', 'soin-visage'
    ]
    
    urls = []
    
    for site, base_url in base_urls.items():
        for keyword in keywords:
            if site == 'Sephora':
                urls.append(f"{base_url}/recherche?q={keyword}")
            elif site == 'Nocibé':
                urls.append(f"{base_url}/recherche?q={keyword}")
            elif site == 'Marionnaud':
                urls.append(f"{base_url}/recherche?q={keyword}")
            elif site == 'Douglas':
                urls.append(f"{base_url}/recherche?q={keyword}")
    
    return urls

def scrape_page(url):
    """Fonction wrapper pour le scraping parallèle"""
    try:
        if 'sephora.fr' in url:
            return scrape_sephora_page(url)
        elif 'nocibe.fr' in url:
            return scrape_nocibe_page(url)
        elif 'marionnaud.fr' in url:
            return scrape_marionnaud_page(url)
        elif 'douglas.fr' in url:
            return scrape_douglas_page(url)
        else:
            return []
    except Exception as e:
        print(f"Erreur lors du scraping de {url}: {e}")
        return []

def main():
    """Fonction principale"""
    print("=== SCRAPING SITES FRANÇAIS ===")
    print("Sites ciblés: Sephora, Nocibé, Marionnaud, Douglas")
    
    # Générer les URLs
    urls = generate_french_urls()
    print(f"URLs générées: {len(urls)}")
    
    # Scraping parallèle
    print("Démarrage du scraping parallèle...")
    with Pool(processes=4) as pool:
        results = pool.map(scrape_page, urls)
    
    # Aplatir les résultats
    all_products = []
    for product_list in results:
        all_products.extend(product_list)
    
    print(f"Total produits extraits: {len(all_products)}")
    
    # Sauvegarder en base
    if all_products:
        print("Sauvegarde en base de données...")
        saved_count, image_count = save_products_to_db(all_products)
        print(f"Produits sauvegardés: {saved_count}")
        print(f"Images téléchargées: {image_count}")
    
    print("Scraping terminé!")

if __name__ == "__main__":
    main()
