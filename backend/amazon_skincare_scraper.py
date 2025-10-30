"""
Script pour scraper les produits de soins du visage depuis Amazon.fr
URL: https://www.amazon.fr/soins-pour-le-visage-crèmes/b/?ie=UTF8&node=211020031&ref_=sv_beauty_5
"""

import os
import sys
import django
import requests
from bs4 import BeautifulSoup
import time
import random
import re
from urllib.parse import urljoin, urlparse

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skin_ai.settings')
django.setup()

from recommendations.models import Product

class AmazonSkincareScraper:
    def __init__(self):
        self.base_url = "https://www.amazon.fr"
        self.target_url = "https://www.amazon.fr/soins-pour-le-visage-crèmes/b/?ie=UTF8&node=211020031&ref_=sv_beauty_5"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    def get_page_content(self, url):
        """Récupère le contenu d'une page"""
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"Erreur lors de la recuperation de {url}: {e}")
            return None
    
    def extract_product_info(self, product_element):
        """Extrait les informations d'un produit Amazon"""
        try:
            # Titre du produit
            title_element = product_element.find('h2', {'class': 's-size-mini'}) or \
                          product_element.find('h2', {'class': 'a-size-mini'}) or \
                          product_element.find('span', {'class': 'a-size-medium'}) or \
                          product_element.find('span', {'class': 'a-size-base-plus'})
            
            if not title_element:
                return None
                
            title = title_element.get_text(strip=True)
            
            # Lien du produit
            link_element = product_element.find('a', {'class': 'a-link-normal'})
            product_url = urljoin(self.base_url, link_element.get('href', '')) if link_element else ''
            
            # Prix
            price_element = product_element.find('span', {'class': 'a-price-whole'}) or \
                          product_element.find('span', {'class': 'a-offscreen'}) or \
                          product_element.find('span', {'class': 'a-price'})
            price = 0.0
            if price_element:
                price_text = price_element.get_text(strip=True).replace('€', '').replace(',', '.')
                try:
                    price = float(re.findall(r'\d+\.?\d*', price_text)[0])
                except:
                    price = 0.0
            
            # Image
            img_element = product_element.find('img', {'class': 's-image'})
            image_url = img_element.get('src', '') if img_element else ''
            
            # Rating
            rating_element = product_element.find('span', {'class': 'a-icon-alt'}) or \
                           product_element.find('span', {'class': 'a-icon'})
            rating = 0.0
            if rating_element:
                rating_text = rating_element.get_text(strip=True)
                try:
                    rating = float(re.findall(r'\d+\.?\d*', rating_text)[0])
                except:
                    rating = 0.0
            
            # Nombre d'avis
            reviews_element = product_element.find('span', {'class': 'a-size-base'}) or \
                           product_element.find('span', {'class': 'a-size-small'})
            review_count = 0
            if reviews_element:
                review_text = reviews_element.get_text(strip=True)
                try:
                    review_count = int(re.findall(r'\d+', review_text)[0])
                except:
                    review_count = 0
            
            # Marque (extrait du titre)
            brand = self.extract_brand_from_title(title)
            
            # Catégorie (déterminée par les mots-clés)
            category = self.determine_category(title)
            
            # Type de peau ciblé
            skin_types = self.determine_skin_types(title)
            
            # Problèmes ciblés
            target_issues = self.determine_target_issues(title)
            
            # Description basée sur le titre
            description = f"Produit de soin du visage - {title}"
            
            return {
                'name': title,
                'brand': brand,
                'price': price,
                'image': image_url,
                'description': description,
                'category': category,
                'target_skin_types': skin_types,
                'target_issues': target_issues,
                'rating': rating,
                'review_count': review_count,
                'url': product_url
            }
            
        except Exception as e:
            print(f"Erreur lors de l'extraction des informations du produit: {e}")
            return None
    
    def extract_brand_from_title(self, title):
        """Extrait la marque du titre"""
        brands = [
            "L'Oréal Paris", "Garnier", "NIVEA", "Vichy", "La Roche-Posay", 
            "Avène", "Eucerin", "Bioderma", "CeraVe", "Cattier", "Topicrem",
            "Mixa", "L'OCCITANE", "Weleda", "Neutrogena", "Hero Cosmetics",
            "Dr. Althea", "Hada Labo", "DERMA E", "Scholl", "Felce Azzurra",
            "Demak'Up", "LABELLO", "Nip+Fab", "Braun", "Lavera", "Catrice",
            "AiQInu", "NOVA ENGEL", "Clinique", "KLEEM ORGANICS", "Brickell",
            "Tiege Hanley", "Dr. Organic", "Revlon", "I Heart Revolution"
        ]
        
        for brand in brands:
            if brand.lower() in title.lower():
                return brand
        
        # Si aucune marque connue, prendre le premier mot
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
            return 'MOISTURIZER'  # Par défaut
    
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
        
        # Si aucun type spécifique, ajouter tous les types
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
        
        # Si aucun problème spécifique, ajouter les problèmes courants
        if not issues:
            issues = ['dryness']
        
        return issues
    
    def scrape_products(self):
        """Scrape tous les produits de la page Amazon"""
        print("Debut du scraping des produits Amazon soins du visage...")
        
        soup = self.get_page_content(self.target_url)
        if not soup:
            print("Impossible de recuperer la page Amazon")
            return []
        
        # Trouver tous les produits
        products = []
        product_elements = soup.find_all('div', {'data-component-type': 's-search-result'})
        
        print(f"Trouve {len(product_elements)} produits sur la page")
        
        for i, product_element in enumerate(product_elements):
            print(f"Traitement du produit {i+1}/{len(product_elements)}")
            
            product_info = self.extract_product_info(product_element)
            if product_info:
                products.append(product_info)
                print(f"Produit ajoute: {product_info['name'][:50]}...")
            
            # Pause pour éviter d'être bloqué
            time.sleep(random.uniform(0.5, 1.5))
        
        print(f"Scraping termine! {len(products)} produits extraits")
        return products
    
    def save_products_to_database(self, products):
        """Sauvegarde les produits dans la base de données"""
        print("Sauvegarde des produits dans la base de donnees...")
        
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
                    print(f"Produit deja existant: {product_data['name'][:30]}...")
                    skipped_count += 1
                    continue
                
                # Créer le nouveau produit
                product = Product.objects.create(
                    name=product_data['name'],
                    brand=product_data['brand'],
                    price=product_data['price'],
                    image=product_data['image'],
                    description=product_data['description'],
                    ingredients="Ingrédients non spécifiés",  # Champ requis
                    category=product_data['category'],
                    target_skin_types=product_data['target_skin_types'],
                    target_issues=product_data['target_issues']
                )
                
                print(f"Produit sauvegarde: {product.name[:50]}...")
                saved_count += 1
                
            except Exception as e:
                print(f"Erreur lors de la sauvegarde du produit {product_data['name']}: {e}")
                continue
        
        print(f"Resume: {saved_count} produits ajoutes, {skipped_count} produits ignores")
        return saved_count, skipped_count

def main():
    """Fonction principale"""
    print("Importation des produits Amazon soins du visage")
    print("=" * 60)
    
    scraper = AmazonSkincareScraper()
    
    # Scraper les produits
    products = scraper.scrape_products()
    
    if not products:
        print("Aucun produit trouve")
        return
    
    # Sauvegarder dans la base de données
    saved, skipped = scraper.save_products_to_database(products)
    
    print("=" * 60)
    print(f"Importation terminee!")
    print(f"{saved} nouveaux produits ajoutes")
    print(f"{skipped} produits deja existants ignores")
    print(f"Total: {len(products)} produits traites")

if __name__ == "__main__":
    main()


