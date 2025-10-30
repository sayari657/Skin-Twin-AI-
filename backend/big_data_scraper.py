"""
Système de scraping Big Data pour collecter des milliers de produits avec images
"""

import os
import sys
import django
import requests
import time
import random
import concurrent.futures
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import json
from datetime import datetime
import threading

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skin_ai.settings')
django.setup()

from recommendations.models import Product

class BigDataScraper:
    def __init__(self):
        self.base_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        # Sources de scraping
        self.sources = {
            'amazon': {
                'base_url': 'https://www.amazon.fr',
                'search_urls': [
                    'https://www.amazon.fr/s?k=crème+visage&ref=sr_pg_1',
                    'https://www.amazon.fr/s?k=sérum+visage&ref=sr_pg_1',
                    'https://www.amazon.fr/s?k=nettoyant+visage&ref=sr_pg_1',
                    'https://www.amazon.fr/s?k=masque+visage&ref=sr_pg_1',
                    'https://www.amazon.fr/s?k=anti-âge&ref=sr_pg_1',
                    'https://www.amazon.fr/s?k=hydratant+visage&ref=sr_pg_1',
                    'https://www.amazon.fr/s?k=exfoliant+visage&ref=sr_pg_1',
                    'https://www.amazon.fr/s?k=tonique+visage&ref=sr_pg_1'
                ],
                'max_pages': 20  # 20 pages par recherche
            },
            'sephora': {
                'base_url': 'https://www.sephora.fr',
                'search_urls': [
                    'https://www.sephora.fr/recherche?q=crème+visage',
                    'https://www.sephora.fr/recherche?q=sérum+visage',
                    'https://www.sephora.fr/recherche?q=nettoyant+visage',
                    'https://www.sephora.fr/recherche?q=masque+visage',
                    'https://www.sephora.fr/recherche?q=anti-âge',
                    'https://www.sephora.fr/recherche?q=hydratant+visage'
                ],
                'max_pages': 15
            },
            'nocibe': {
                'base_url': 'https://www.nocibe.fr',
                'search_urls': [
                    'https://www.nocibe.fr/recherche?q=crème+visage',
                    'https://www.nocibe.fr/recherche?q=sérum+visage',
                    'https://www.nocibe.fr/recherche?q=nettoyant+visage',
                    'https://www.nocibe.fr/recherche?q=masque+visage',
                    'https://www.nocibe.fr/recherche?q=anti-âge'
                ],
                'max_pages': 10
            },
            'marionnaud': {
                'base_url': 'https://www.marionnaud.fr',
                'search_urls': [
                    'https://www.marionnaud.fr/recherche?q=crème+visage',
                    'https://www.marionnaud.fr/recherche?q=sérum+visage',
                    'https://www.marionnaud.fr/recherche?q=nettoyant+visage',
                    'https://www.marionnaud.fr/recherche?q=masque+visage'
                ],
                'max_pages': 10
            },
            'douglas': {
                'base_url': 'https://www.douglas.fr',
                'search_urls': [
                    'https://www.douglas.fr/recherche?q=crème+visage',
                    'https://www.douglas.fr/recherche?q=sérum+visage',
                    'https://www.douglas.fr/recherche?q=nettoyant+visage',
                    'https://www.douglas.fr/recherche?q=masque+visage'
                ],
                'max_pages': 10
            }
        }
        
        self.scraped_products = []
        self.images_downloaded = 0
        self.products_saved = 0
        self.lock = threading.Lock()
        
        # Créer le dossier media/products
        self.media_dir = os.path.join(os.path.dirname(__file__), 'media', 'products')
        os.makedirs(self.media_dir, exist_ok=True)
    
    def download_image(self, image_url, product_name, source):
        """Télécharge et sauvegarde une image"""
        try:
            if not image_url or image_url == '':
                return None
                
            # Nettoyer le nom du produit
            safe_name = "".join(c for c in product_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_name = safe_name.replace(' ', '_')[:50]
            
            # Nom du fichier avec source
            filename = f"{source}_{safe_name}.jpg"
            filepath = os.path.join(self.media_dir, filename)
            
            # Télécharger l'image
            response = requests.get(image_url, headers=self.base_headers, timeout=15)
            response.raise_for_status()
            
            # Sauvegarder l'image
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            with self.lock:
                self.images_downloaded += 1
            
            return f"products/{filename}"
            
        except Exception as e:
            print(f"Erreur téléchargement image {product_name}: {e}")
            return None
    
    def extract_amazon_products(self, soup, page_url):
        """Extrait les produits Amazon"""
        products = []
        
        try:
            # Sélecteurs Amazon
            product_elements = soup.find_all('div', {'data-component-type': 's-search-result'})
            
            for element in product_elements:
                try:
                    # Titre
                    title_elem = element.find('h2', {'class': 's-size-mini'}) or \
                               element.find('h2', {'class': 'a-size-mini'}) or \
                               element.find('span', {'class': 'a-size-medium'})
                    
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    
                    # Lien
                    link_elem = element.find('a', {'class': 'a-link-normal'})
                    product_url = urljoin(self.sources['amazon']['base_url'], link_elem.get('href', '')) if link_elem else ''
                    
                    # Prix
                    price_elem = element.find('span', {'class': 'a-price-whole'}) or \
                               element.find('span', {'class': 'a-offscreen'})
                    price = 0.0
                    if price_elem:
                        price_text = price_elem.get_text(strip=True).replace('€', '').replace(',', '.')
                        try:
                            price = float(re.findall(r'\d+\.?\d*', price_text)[0])
                        except:
                            price = 0.0
                    
                    # Image
                    img_elem = element.find('img', {'class': 's-image'})
                    image_url = img_elem.get('src', '') if img_elem else ''
                    
                    # Rating
                    rating_elem = element.find('span', {'class': 'a-icon-alt'})
                    rating = 0.0
                    if rating_elem:
                        rating_text = rating_elem.get_text(strip=True)
                        try:
                            rating = float(re.findall(r'\d+\.?\d*', rating_text)[0])
                        except:
                            rating = 0.0
                    
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
                        'rating': rating,
                        'url': product_url
                    }
                    
                    products.append(product_data)
                    
                except Exception as e:
                    print(f"Erreur extraction produit Amazon: {e}")
                    continue
        
        except Exception as e:
            print(f"Erreur extraction Amazon: {e}")
        
        return products
    
    def extract_sephora_products(self, soup, page_url):
        """Extrait les produits Sephora"""
        products = []
        
        try:
            # Sélecteurs Sephora
            product_elements = soup.find_all('div', {'class': 'product-tile'}) or \
                             soup.find_all('div', {'class': 'product-item'}) or \
                             soup.find_all('article', {'class': 'product'})
            
            for element in product_elements:
                try:
                    # Titre
                    title_elem = element.find('h3') or element.find('h2') or element.find('a', {'class': 'product-name'})
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    
                    # Prix
                    price_elem = element.find('span', {'class': 'price'}) or \
                               element.find('div', {'class': 'price'}) or \
                               element.find('span', {'class': 'amount'})
                    price = 0.0
                    if price_elem:
                        price_text = price_elem.get_text(strip=True).replace('€', '').replace(',', '.')
                        try:
                            price = float(re.findall(r'\d+\.?\d*', price_text)[0])
                        except:
                            price = 0.0
                    
                    # Image
                    img_elem = element.find('img')
                    image_url = img_elem.get('src', '') or img_elem.get('data-src', '') if img_elem else ''
                    if image_url and not image_url.startswith('http'):
                        image_url = urljoin(self.sources['sephora']['base_url'], image_url)
                    
                    # Marque
                    brand_elem = element.find('span', {'class': 'brand'}) or \
                               element.find('div', {'class': 'brand'}) or \
                               element.find('a', {'class': 'brand'})
                    brand = brand_elem.get_text(strip=True) if brand_elem else self.extract_brand_from_title(title)
                    
                    product_data = {
                        'name': title,
                        'brand': brand,
                        'price': price,
                        'image_url': image_url,
                        'description': f"Produit Sephora - {title}",
                        'category': self.determine_category(title),
                        'target_skin_types': self.determine_skin_types(title),
                        'target_issues': self.determine_target_issues(title),
                        'ingredients': "Ingrédients non spécifiés",
                        'source': 'Sephora.fr'
                    }
                    
                    products.append(product_data)
                    
                except Exception as e:
                    print(f"Erreur extraction produit Sephora: {e}")
                    continue
        
        except Exception as e:
            print(f"Erreur extraction Sephora: {e}")
        
        return products
    
    def extract_brand_from_title(self, title):
        """Extrait la marque du titre"""
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
            "Glow Recipe", "The Inkey List", "Uriage", "Vichy", "L'Oréal Paris"
        ]
        
        for brand in brands:
            if brand.lower() in title.lower():
                return brand
        
        return title.split()[0] if title.split() else "Marque inconnue"
    
    def determine_category(self, title):
        """Détermine la catégorie du produit"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['crème', 'cream', 'moisturizer', 'hydratant']):
            return 'MOISTURIZER'
        elif any(word in title_lower for word in ['sérum', 'serum']):
            return 'SERUM'
        elif any(word in title_lower for word in ['nettoyant', 'cleanser', 'gel', 'micellaire', 'solution']):
            return 'CLEANSER'
        elif any(word in title_lower for word in ['masque', 'mask']):
            return 'MASK'
        elif any(word in title_lower for word in ['tonique', 'toner']):
            return 'TONER'
        elif any(word in title_lower for word in ['exfoliant', 'scrub', 'gommage']):
            return 'EXFOLIANT'
        elif any(word in title_lower for word in ['solaire', 'sunscreen', 'spf']):
            return 'SUNSCREEN'
        elif any(word in title_lower for word in ['patch', 'bouton']):
            return 'TREATMENT'
        else:
            return 'MOISTURIZER'
    
    def determine_skin_types(self, title):
        """Détermine les types de peau ciblés"""
        title_lower = title.lower()
        skin_types = []
        
        if any(word in title_lower for word in ['sèche', 'dry', 'hydratant', 'hydratation']):
            skin_types.append('DRY')
        if any(word in title_lower for word in ['grasse', 'oily', 'séborrhée', 'mixtes']):
            skin_types.append('OILY')
        if any(word in title_lower for word in ['mixte', 'combination']):
            skin_types.append('COMBINATION')
        if any(word in title_lower for word in ['sensible', 'sensitive']):
            skin_types.append('SENSITIVE')
        if any(word in title_lower for word in ['normale', 'normal', 'tous types']):
            skin_types.append('NORMAL')
        
        if not skin_types:
            skin_types = ['DRY', 'OILY', 'COMBINATION', 'NORMAL', 'SENSITIVE']
        
        return skin_types
    
    def determine_target_issues(self, title):
        """Détermine les problèmes ciblés"""
        title_lower = title.lower()
        issues = []
        
        if any(word in title_lower for word in ['anti-âge', 'anti-age', 'rides', 'wrinkles', 'jeunesse']):
            issues.append('aging')
        if any(word in title_lower for word in ['acné', 'acne', 'boutons', 'imperfections', 'patch']):
            issues.append('acne')
        if any(word in title_lower for word in ['taches', 'spots', 'pigmentation', 'éclat']):
            issues.append('dark_spots')
        if any(word in title_lower for word in ['rougeurs', 'redness', 'irritation']):
            issues.append('redness')
        if any(word in title_lower for word in ['hydratation', 'moisturizing', 'sècheresse']):
            issues.append('dryness')
        if any(word in title_lower for word in ['éclat', 'brightening', 'luminosité']):
            issues.append('dullness')
        if any(word in title_lower for word in ['pores', 'points noirs']):
            issues.append('large_pores')
        
        if not issues:
            issues = ['dryness']
        
        return issues
    
    def scrape_page(self, url, source):
        """Scrape une page spécifique"""
        try:
            print(f"Scraping {source}: {url}")
            
            response = requests.get(url, headers=self.base_headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            if source == 'amazon':
                return self.extract_amazon_products(soup, url)
            elif source == 'sephora':
                return self.extract_sephora_products(soup, url)
            else:
                # Pour les autres sources, utiliser la même logique que Sephora
                return self.extract_sephora_products(soup, url)
                
        except Exception as e:
            print(f"Erreur scraping {source} {url}: {e}")
            return []
    
    def scrape_source(self, source_name, source_config):
        """Scrape une source complète"""
        print(f"\n=== SCRAPING {source_name.upper()} ===")
        
        all_products = []
        
        for search_url in source_config['search_urls']:
            print(f"\nRecherche: {search_url}")
            
            for page in range(1, source_config['max_pages'] + 1):
                try:
                    # Construire l'URL de la page
                    if 'amazon' in source_name:
                        page_url = f"{search_url}&page={page}"
                    else:
                        page_url = f"{search_url}&page={page}"
                    
                    # Scraper la page
                    products = self.scrape_page(page_url, source_name)
                    all_products.extend(products)
                    
                    print(f"  Page {page}: {len(products)} produits trouvés")
                    
                    # Pause entre les pages
                    time.sleep(random.uniform(1, 3))
                    
                except Exception as e:
                    print(f"  Erreur page {page}: {e}")
                    continue
        
        print(f"Total {source_name}: {len(all_products)} produits")
        return all_products
    
    def save_products_to_database(self, products):
        """Sauvegarde les produits dans la base de données"""
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
                
                # Télécharger l'image
                image_path = None
                if product_data.get('image_url'):
                    image_path = self.download_image(
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
                
                if saved_count % 10 == 0:
                    print(f"  {saved_count} produits sauvegardés...")
                
            except Exception as e:
                print(f"Erreur sauvegarde produit {product_data['name']}: {e}")
                continue
        
        return saved_count, skipped_count
    
    def run_big_data_scraping(self):
        """Lance le scraping Big Data complet"""
        print("=== DÉMARRAGE DU SCRAPING BIG DATA ===")
        print(f"Sources: {list(self.sources.keys())}")
        print(f"Total pages estimées: {sum(len(s['search_urls']) * s['max_pages'] for s in self.sources.values())}")
        print("=" * 60)
        
        start_time = datetime.now()
        
        # Scraper toutes les sources
        all_products = []
        
        for source_name, source_config in self.sources.items():
            try:
                products = self.scrape_source(source_name, source_config)
                all_products.extend(products)
                
                # Sauvegarder immédiatement pour éviter la perte de données
                if products:
                    saved, skipped = self.save_products_to_database(products)
                    print(f"{source_name}: {saved} ajoutés, {skipped} ignorés")
                
            except Exception as e:
                print(f"Erreur scraping {source_name}: {e}")
                continue
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        print("\n" + "=" * 60)
        print("=== RÉSULTATS DU SCRAPING BIG DATA ===")
        print(f"Durée totale: {duration}")
        print(f"Produits collectés: {len(all_products)}")
        print(f"Produits sauvegardés: {self.products_saved}")
        print(f"Images téléchargées: {self.images_downloaded}")
        print(f"Total produits en base: {Product.objects.count()}")
        print("=" * 60)
        
        return all_products

def main():
    """Fonction principale"""
    scraper = BigDataScraper()
    scraper.run_big_data_scraping()

if __name__ == "__main__":
    main()


