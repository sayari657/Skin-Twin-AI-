"""
Système de scraping Big Data simplifié sans dépendances externes
"""

import os
import sys
import django
import requests
import time
import random
import concurrent.futures
from urllib.parse import urljoin, urlparse, quote
from bs4 import BeautifulSoup
import json
from datetime import datetime
import threading
import re

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skin_ai.settings')
django.setup()

from recommendations.models import Product

class SimpleBigDataScraper:
    def __init__(self, max_workers=3):
        self.max_workers = max_workers
        
        # Headers rotatifs pour éviter la détection
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ]
        
        self.get_headers = lambda: {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        }
        
        # Sources optimisées pour le scraping
        self.sources = {
            'amazon': {
                'base_url': 'https://www.amazon.fr',
                'search_terms': [
                    'crème visage', 'sérum visage', 'nettoyant visage', 'masque visage',
                    'anti-âge', 'hydratant visage', 'exfoliant visage', 'tonique visage'
                ],
                'max_pages': 3,  # Réduit pour éviter les blocages
                'delay': (3, 8)  # Délai entre les requêtes
            }
        }
        
        self.scraped_products = []
        self.images_downloaded = 0
        self.products_saved = 0
        self.lock = threading.Lock()
        
        # Créer le dossier media/products
        self.media_dir = os.path.join(os.path.dirname(__file__), 'media', 'products')
        os.makedirs(self.media_dir, exist_ok=True)
    
    def smart_request(self, url, max_retries=2):
        """Requête intelligente avec retry et rotation d'headers"""
        for attempt in range(max_retries):
            try:
                headers = self.get_headers()
                response = requests.get(url, headers=headers, timeout=25)
                
                if response.status_code == 200:
                    return response
                elif response.status_code == 403:
                    # Attendre plus longtemps en cas de blocage
                    time.sleep(random.uniform(15, 25))
                    continue
                else:
                    time.sleep(random.uniform(5, 10))
                    continue
                    
            except Exception as e:
                print(f"Tentative {attempt + 1} échouée pour {url}: {e}")
                time.sleep(random.uniform(10, 15))
                continue
        
        return None
    
    def download_image_smart(self, image_url, product_name, source):
        """Télécharge une image avec gestion intelligente des erreurs"""
        try:
            if not image_url or image_url == '':
                return None
                
            # Nettoyer le nom du produit
            safe_name = "".join(c for c in product_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_name = safe_name.replace(' ', '_')[:50]
            
            # Nom du fichier avec source et timestamp
            timestamp = int(time.time())
            filename = f"{source}_{safe_name}_{timestamp}.jpg"
            filepath = os.path.join(self.media_dir, filename)
            
            # Télécharger l'image avec headers rotatifs
            headers = self.get_headers()
            response = requests.get(image_url, headers=headers, timeout=20)
            response.raise_for_status()
            
            # Vérifier que c'est bien une image
            if not response.headers.get('content-type', '').startswith('image/'):
                return None
            
            # Sauvegarder l'image
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            with self.lock:
                self.images_downloaded += 1
            
            return f"products/{filename}"
            
        except Exception as e:
            print(f"Erreur téléchargement image {product_name}: {e}")
            return None
    
    def extract_amazon_products_smart(self, soup, page_url):
        """Extraction Amazon avec sélecteurs robustes"""
        products = []
        
        try:
            # Sélecteurs multiples pour Amazon
            product_elements = (
                soup.find_all('div', {'data-component-type': 's-search-result'}) or
                soup.find_all('div', {'class': 's-result-item'}) or
                soup.find_all('div', {'class': 's-widget-container'}) or
                soup.find_all('div', {'class': 's-card-container'})
            )
            
            for element in product_elements:
                try:
                    # Titre avec sélecteurs multiples
                    title_elem = (
                        element.find('h2', {'class': 's-size-mini'}) or
                        element.find('h2', {'class': 'a-size-mini'}) or
                        element.find('span', {'class': 'a-size-medium'}) or
                        element.find('span', {'class': 'a-size-base-plus'}) or
                        element.find('h3', {'class': 'a-size-base'}) or
                        element.find('span', {'class': 'a-size-base'})
                    )
                    
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    if len(title) < 10:  # Filtrer les titres trop courts
                        continue
                    
                    # Lien
                    link_elem = element.find('a', {'class': 'a-link-normal'}) or element.find('a')
                    product_url = urljoin(self.sources['amazon']['base_url'], link_elem.get('href', '')) if link_elem else ''
                    
                    # Prix avec sélecteurs multiples
                    price_elem = (
                        element.find('span', {'class': 'a-price-whole'}) or
                        element.find('span', {'class': 'a-offscreen'}) or
                        element.find('span', {'class': 'a-price'}) or
                        element.find('span', {'class': 'a-price-range'}) or
                        element.find('span', {'class': 'a-size-base'})
                    )
                    price = 0.0
                    if price_elem:
                        price_text = price_elem.get_text(strip=True).replace('€', '').replace(',', '.')
                        try:
                            price = float(re.findall(r'\d+\.?\d*', price_text)[0])
                        except:
                            price = 0.0
                    
                    # Image avec sélecteurs multiples
                    img_elem = (
                        element.find('img', {'class': 's-image'}) or
                        element.find('img', {'class': 'a-dynamic-image'}) or
                        element.find('img')
                    )
                    image_url = ''
                    if img_elem:
                        image_url = img_elem.get('src', '') or img_elem.get('data-src', '') or img_elem.get('data-lazy', '')
                    
                    # Marque
                    brand = self.extract_brand_from_title(title)
                    
                    # Catégorie
                    category = self.determine_category(title)
                    
                    # Types de peau
                    skin_types = self.determine_skin_types(title)
                    
                    # Problèmes ciblés
                    target_issues = self.determine_target_issues(title)
                    
                    product_data = {
                        'name': title,
                        'brand': brand,
                        'price': price,
                        'image_url': image_url,
                        'description': f"Produit Amazon - {title}",
                        'category': category,
                        'target_skin_types': skin_types,
                        'target_issues': target_issues,
                        'ingredients': "Ingrédients non spécifiés",
                        'source': 'Amazon.fr',
                        'url': product_url
                    }
                    
                    products.append(product_data)
                    
                except Exception as e:
                    continue
        
        except Exception as e:
            print(f"Erreur extraction Amazon: {e}")
        
        return products
    
    def extract_brand_from_title(self, title):
        """Extrait la marque du titre avec une liste étendue"""
        brands = [
            "L'Oréal Paris", "Garnier", "NIVEA", "Vichy", "La Roche-Posay", 
            "Avène", "Eucerin", "Bioderma", "CeraVe", "Cattier", "Topicrem",
            "Mixa", "L'OCCITANE", "Weleda", "Neutrogena", "Hero Cosmetics",
            "Dr. Althea", "Hada Labo", "DERMA E", "Scholl", "Felce Azzurra",
            "Demak'Up", "LABELLO", "Nip+Fab", "Braun", "Lavera", "Catrice",
            "AiQInu", "NOVA ENGEL", "Clinique", "KLEEM ORGANICS", "Brickell",
            "Tiege Hanley", "Dr. Organic", "Revlon", "I Heart Revolution",
            "Lancôme", "Dior", "Estée Lauder", "Chanel", "Shiseido", "Fresh",
            "Kiehl's", "The Body Shop", "Lush", "Olay", "Maybelline", "L'Oréal",
            "Paula's Choice", "The Ordinary", "Drunk Elephant", "Fenty Skin",
            "Glow Recipe", "The Inkey List", "Uriage", "Vichy", "L'Oréal Paris",
            "Clinique", "MAC", "Urban Decay", "Too Faced", "Benefit", "NARS",
            "Bobbi Brown", "Smashbox", "Tarte", "Anastasia Beverly Hills",
            "Huda Beauty", "Fenty Beauty", "Rare Beauty", "Glossier", "Milk Makeup"
        ]
        
        for brand in brands:
            if brand.lower() in title.lower():
                return brand
        
        return title.split()[0] if title.split() else "Marque inconnue"
    
    def determine_category(self, title):
        """Détermine la catégorie du produit"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['crème', 'cream', 'moisturizer', 'hydratant', 'lotion']):
            return 'MOISTURIZER'
        elif any(word in title_lower for word in ['sérum', 'serum', 'concentrate', 'essence']):
            return 'SERUM'
        elif any(word in title_lower for word in ['nettoyant', 'cleanser', 'gel', 'micellaire', 'solution', 'wash']):
            return 'CLEANSER'
        elif any(word in title_lower for word in ['masque', 'mask', 'treatment']):
            return 'MASK'
        elif any(word in title_lower for word in ['tonique', 'toner', 'mist']):
            return 'TONER'
        elif any(word in title_lower for word in ['exfoliant', 'scrub', 'gommage', 'peeling']):
            return 'EXFOLIANT'
        elif any(word in title_lower for word in ['solaire', 'sunscreen', 'spf', 'sun']):
            return 'SUNSCREEN'
        elif any(word in title_lower for word in ['patch', 'bouton', 'spot', 'treatment']):
            return 'TREATMENT'
        else:
            return 'MOISTURIZER'
    
    def determine_skin_types(self, title):
        """Détermine les types de peau ciblés"""
        title_lower = title.lower()
        skin_types = []
        
        if any(word in title_lower for word in ['sèche', 'dry', 'hydratant', 'hydratation', 'nourrissant']):
            skin_types.append('DRY')
        if any(word in title_lower for word in ['grasse', 'oily', 'séborrhée', 'mixtes', 'matifiant']):
            skin_types.append('OILY')
        if any(word in title_lower for word in ['mixte', 'combination', 'mixtes']):
            skin_types.append('COMBINATION')
        if any(word in title_lower for word in ['sensible', 'sensitive', 'délicat', 'apaisant']):
            skin_types.append('SENSITIVE')
        if any(word in title_lower for word in ['normale', 'normal', 'tous types', 'universel']):
            skin_types.append('NORMAL')
        
        if not skin_types:
            skin_types = ['DRY', 'OILY', 'COMBINATION', 'NORMAL', 'SENSITIVE']
        
        return skin_types
    
    def determine_target_issues(self, title):
        """Détermine les problèmes ciblés"""
        title_lower = title.lower()
        issues = []
        
        if any(word in title_lower for word in ['anti-âge', 'anti-age', 'rides', 'wrinkles', 'jeunesse', 'firming']):
            issues.append('aging')
        if any(word in title_lower for word in ['acné', 'acne', 'boutons', 'imperfections', 'patch', 'spots']):
            issues.append('acne')
        if any(word in title_lower for word in ['taches', 'spots', 'pigmentation', 'éclat', 'brightening']):
            issues.append('dark_spots')
        if any(word in title_lower for word in ['rougeurs', 'redness', 'irritation', 'calming']):
            issues.append('redness')
        if any(word in title_lower for word in ['hydratation', 'moisturizing', 'sècheresse', 'hydration']):
            issues.append('dryness')
        if any(word in title_lower for word in ['éclat', 'brightening', 'luminosité', 'glow']):
            issues.append('dullness')
        if any(word in title_lower for word in ['pores', 'points noirs', 'blackheads', 'refining']):
            issues.append('large_pores')
        
        if not issues:
            issues = ['dryness']
        
        return issues
    
    def scrape_page_smart(self, url, source_name):
        """Scrape une page avec gestion intelligente des erreurs"""
        try:
            print(f"Scraping {source_name}: {url}")
            
            response = self.smart_request(url)
            if not response:
                return []
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            if source_name == 'amazon':
                return self.extract_amazon_products_smart(soup, url)
            else:
                return []
                
        except Exception as e:
            print(f"Erreur scraping {source_name} {url}: {e}")
            return []
    
    def generate_search_urls_smart(self, source_name, source_config):
        """Génère les URLs de recherche avec encodage intelligent"""
        urls = []
        base_url = source_config['base_url']
        
        for term in source_config['search_terms']:
            for page in range(1, source_config['max_pages'] + 1):
                if source_name == 'amazon':
                    # Encodage URL pour Amazon
                    encoded_term = quote(term, safe='')
                    url = f"{base_url}/s?k={encoded_term}&page={page}"
                else:
                    # Encodage URL pour autres sources
                    encoded_term = quote(term, safe='')
                    url = f"{base_url}/recherche?q={encoded_term}&page={page}"
                urls.append((url, source_name))
        
        return urls
    
    def save_products_batch_smart(self, products):
        """Sauvegarde un lot de produits avec gestion d'erreurs"""
        saved_count = 0
        skipped_count = 0
        
        for product_data in products:
            try:
                # Vérifier si le produit existe déjà
                existing_product = Product.objects.filter(
                    name=product_data['name'],
                    brand=product_data['brand']
                ).first()
                
                if existing_product:
                    skipped_count += 1
                    continue
                
                # Télécharger l'image en parallèle
                image_path = None
                if product_data.get('image_url'):
                    image_path = self.download_image_smart(
                        product_data['image_url'], 
                        product_data['name'], 
                        product_data.get('source', 'unknown')
                    )
                
                # Créer le produit
                product = Product.objects.create(
                    name=product_data['name'],
                    brand=product_data['brand'],
                    price=product_data['price'],
                    image=image_path,
                    description=product_data['description'],
                    ingredients=product_data['ingredients'],
                    category=product_data['category'],
                    target_skin_types=product_data['target_skin_types'],
                    target_issues=product_data['target_issues']
                )
                
                saved_count += 1
                self.products_saved += 1
                
            except Exception as e:
                print(f"Erreur sauvegarde produit {product_data['name']}: {e}")
                continue
        
        return saved_count, skipped_count
    
    def run_simple_big_data_scraping(self):
        """Lance le scraping Big Data simplifié"""
        print("=== DÉMARRAGE DU SCRAPING BIG DATA SIMPLIFIÉ ===")
        print(f"Workers parallèles: {self.max_workers}")
        print(f"Sources: {list(self.sources.keys())}")
        
        # Calculer le nombre total d'URLs
        total_urls = sum(len(s['search_terms']) * s['max_pages'] for s in self.sources.values())
        print(f"Total URLs à scraper: {total_urls}")
        print("=" * 60)
        
        start_time = datetime.now()
        
        # Générer toutes les URLs
        all_urls = []
        for source_name, source_config in self.sources.items():
            urls = self.generate_search_urls_smart(source_name, source_config)
            all_urls.extend(urls)
        
        print(f"URLs générées: {len(all_urls)}")
        
        # Scraper en parallèle avec gestion intelligente
        all_products = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Soumettre toutes les tâches
            future_to_url = {
                executor.submit(self.scrape_page_smart, url, source): (url, source) 
                for url, source in all_urls
            }
            
            # Traiter les résultats au fur et à mesure
            batch_size = 10
            current_batch = []
            
            for future in concurrent.futures.as_completed(future_to_url):
                url, source = future_to_url[future]
                try:
                    products = future.result()
                    if products:
                        current_batch.extend(products)
                        all_products.extend(products)
                        
                        # Sauvegarder par lots
                        if len(current_batch) >= batch_size:
                            saved, skipped = self.save_products_batch_smart(current_batch)
                            print(f"Lot sauvegardé: {saved} ajoutés, {skipped} ignorés")
                            current_batch = []
                            
                        # Délai intelligent entre les requêtes
                        delay = random.uniform(*self.sources[source]['delay'])
                        time.sleep(delay)
                            
                except Exception as e:
                    print(f"Erreur traitement {url}: {e}")
                    continue
        
        # Sauvegarder le dernier lot
        if current_batch:
            saved, skipped = self.save_products_batch_smart(current_batch)
            print(f"Dernier lot: {saved} ajoutés, {skipped} ignorés")
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        print("\n" + "=" * 60)
        print("=== RÉSULTATS DU SCRAPING BIG DATA SIMPLIFIÉ ===")
        print(f"Durée totale: {duration}")
        print(f"URLs traitées: {len(all_urls)}")
        print(f"Produits collectés: {len(all_products)}")
        print(f"Produits sauvegardés: {self.products_saved}")
        print(f"Images téléchargées: {self.images_downloaded}")
        print(f"Total produits en base: {Product.objects.count()}")
        print("=" * 60)
        
        return all_products

def main():
    """Fonction principale"""
    scraper = SimpleBigDataScraper(max_workers=2)  # 2 workers pour éviter les blocages
    scraper.run_simple_big_data_scraping()

if __name__ == "__main__":
    main()


