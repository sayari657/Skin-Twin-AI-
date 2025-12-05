#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script Python pour scraper tous les produits depuis pharma-shop.tn/839-visage
et les sauvegarder dans la base de données Django.

Usage:
    cd skin-twin-ai/backend
    python scrape_pharma_shop.py
    OU
    python manage.py shell < scrape_pharma_shop.py
    OU (Windows)
    double-cliquer sur scrape_pharma_shop.bat
"""

import os
import sys
import django
import requests
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime

# Fix encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Configuration Django
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skin_ai.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur lors de la configuration Django: {e}")
    print("Assurez-vous d'être dans le répertoire backend et que Django est installé.")
    sys.exit(1)

from scraped_products.models import ScrapedProduct

def scrape_pharma_shop_tn(base_url='https://pharma-shop.tn/839-visage', max_pages=None):
    """
    Scraper tous les produits depuis pharma-shop.tn
    
    Args:
        base_url: URL de base à scraper
        max_pages: Nombre maximum de pages à scraper (None = toutes les pages)
    
    Returns:
        Liste des produits scrapés
    """
    all_products = []
    
    # Headers pour éviter les blocages
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    print(f"🔍 Connexion à {base_url}...")
    
    try:
        # Charger la première page pour détecter le nombre total de produits
        first_response = requests.get(base_url, headers=headers, timeout=60)
        first_response.raise_for_status()
        print(f"✅ Page chargée avec succès (Status: {first_response.status_code})")
        first_soup = BeautifulSoup(first_response.content, 'html.parser')
        
        # Chercher le texte "Affichage 1-24 de X article(s)"
        pagination_text = first_soup.find(string=re.compile(r'Affichage.*de\s+(\d+)\s+article', re.I))
        total_products = 0
        estimated_pages = 1
        
        if pagination_text:
            match = re.search(r'de\s+(\d+)\s+article', pagination_text)
            if match:
                total_products = int(match.group(1))
                # Calculer le nombre de pages (24 produits par page généralement)
                estimated_pages = (total_products // 24) + 1
                print(f"📊 Total produits détectés: {total_products}")
                print(f"📄 Pages estimées: {estimated_pages}")
        
        # Chercher aussi dans la pagination
        pagination = first_soup.find('div', class_=re.compile(r'pagination', re.I))
        if pagination:
            page_links = pagination.find_all('a', href=True)
            if page_links:
                max_page_num = 1
                for link in page_links:
                    href = link.get('href', '')
                    page_match = re.search(r'[?&]p=(\d+)', href)
                    if page_match:
                        page_num = int(page_match.group(1))
                        max_page_num = max(max_page_num, page_num)
                if max_page_num > 1:
                    estimated_pages = max_page_num
                    print(f"📄 Pages détectées dans la pagination: {estimated_pages}")
        
        # Limiter le nombre de pages si spécifié
        if max_pages:
            estimated_pages = min(estimated_pages, max_pages)
        
        print(f"\n🚀 Début du scraping de {estimated_pages} pages...")
        print(f"⏱️ Temps estimé: ~{estimated_pages * 2} minutes\n")
        
        # Scraper chaque page
        for page in range(1, estimated_pages + 1):
            page_url = base_url
            if page > 1:
                if '?' in base_url:
                    page_url = f"{base_url}&p={page}"
                else:
                    page_url = f"{base_url}?p={page}"
            
            try:
                print(f"📄 Scraping page {page}/{estimated_pages}: {page_url}")
                response = requests.get(page_url, headers=headers, timeout=60)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Chercher les produits dans les divs avec classe "thumbnail-container"
                product_elements = soup.find_all('div', class_=re.compile(r'thumbnail-container', re.I))
                
                # Alternative: chercher aussi dans les articles
                if not product_elements:
                    product_elements = soup.find_all('article', class_=re.compile(r'product-miniature', re.I))
                    if product_elements:
                        temp_elements = []
                        for article in product_elements:
                            thumbnail = article.find('div', class_=re.compile(r'thumbnail-container', re.I))
                            if thumbnail:
                                temp_elements.append(thumbnail)
                        product_elements = temp_elements
                
                page_products = []
                
                for idx, element in enumerate(product_elements):
                    try:
                        # Extraire le nom du produit
                        name = None
                        name_elem = element.find('h2', class_='product-title')
                        if not name_elem:
                            name_elem = element.find('h2', class_=re.compile(r'product-title', re.I))
                        
                        if name_elem:
                            name_link = name_elem.find('a')
                            if name_link:
                                name = name_link.get_text(strip=True).replace('...', '').strip()
                            else:
                                name = name_elem.get_text(strip=True)
                        else:
                            name_elem = element.find(['h2', 'h3'], class_=re.compile(r'title', re.I))
                            if name_elem:
                                name_link = name_elem.find('a')
                                name = name_link.get_text(strip=True) if name_link else name_elem.get_text(strip=True)
                        
                        if not name or len(name) < 3:
                            continue
                        
                        name = ' '.join(name.split())
                        
                        # Extraire le prix
                        price = 0.0
                        price_elem = element.find('span', class_='price')
                        if price_elem:
                            price_text = price_elem.get_text(strip=True)
                            price_text = price_text.replace('\xa0', ' ').replace('TND', '').strip()
                            price_match = re.search(r'(\d+[.,]\d+)', price_text.replace(',', '.'))
                            if price_match:
                                price = float(price_match.group(1).replace(',', '.'))
                        
                        if price <= 0:
                            price_container = element.find('div', class_='product-price-and-shipping')
                            if price_container:
                                price_text = price_container.get_text()
                                price_match = re.search(r'(\d+[.,]\d+)\s*TND', price_text)
                                if price_match:
                                    price = float(price_match.group(1).replace(',', '.'))
                        
                        if price <= 0:
                            continue
                        
                        # Extraire l'image
                        image_url = None
                        product_image_div = element.find('div', class_='product-image')
                        if product_image_div:
                            img_elem = product_image_div.find('img')
                            if img_elem:
                                image_url = img_elem.get('data-full-size-image-url') or img_elem.get('src')
                                if image_url:
                                    if image_url.startswith('//'):
                                        image_url = 'https:' + image_url
                                    elif image_url.startswith('/'):
                                        image_url = 'https://pharma-shop.tn' + image_url
                                    elif not image_url.startswith('http'):
                                        image_url = 'https://pharma-shop.tn/' + image_url.lstrip('/')
                        
                        # Extraire le lien du produit
                        product_url = None
                        name_link_elem = element.find('h2', class_=re.compile(r'product-title', re.I))
                        if name_link_elem:
                            link_elem = name_link_elem.find('a', href=True)
                            if link_elem:
                                product_url = link_elem.get('href')
                        
                        if not product_url:
                            thumbnail = element.find('a', class_='product-thumbnail')
                            if thumbnail:
                                product_url = thumbnail.get('href')
                        
                        if not product_url:
                            product_image_div = element.find('div', class_='product-image')
                            if product_image_div:
                                link_elem = product_image_div.find('a', href=True)
                                if link_elem:
                                    product_url = link_elem.get('href')
                        
                        if product_url:
                            if product_url.startswith('//'):
                                product_url = 'https:' + product_url
                            elif product_url.startswith('/'):
                                product_url = 'https://pharma-shop.tn' + product_url
                            elif not product_url.startswith('http'):
                                product_url = 'https://pharma-shop.tn/' + product_url.lstrip('/')
                        
                        # Extraire la marque
                        brand = 'Marque inconnue'
                        brand_elem = element.find('div', class_='txt-marque')
                        if brand_elem:
                            brand_link = brand_elem.find('a')
                            if brand_link:
                                brand = brand_link.get_text(strip=True)
                            else:
                                brand = brand_elem.get_text(strip=True)
                        
                        if brand == 'Marque inconnue' or not brand:
                            name_words = name.split()
                            if name_words:
                                brand = name_words[0]
                        
                        # Déterminer la catégorie
                        category = 'MOISTURIZER'
                        name_lower = name.lower()
                        if any(word in name_lower for word in ['nettoyant', 'cleanser', 'démaquillant', 'gel moussant', 'mousse nettoyante', 'eau micellaire', 'mousse']):
                            category = 'CLEANSER'
                        elif any(word in name_lower for word in ['sérum', 'serum', 'ampoule']):
                            category = 'SERUM'
                        elif any(word in name_lower for word in ['solaire', 'sun', 'spf', 'anthelios']):
                            category = 'SUNSCREEN'
                        elif any(word in name_lower for word in ['masque', 'mask', 'gommage']):
                            category = 'MASK'
                        elif any(word in name_lower for word in ['tonique', 'toner', 'lotion']):
                            category = 'TONER'
                        elif any(word in name_lower for word in ['exfoliant', 'scrub']):
                            category = 'EXFOLIANT'
                        elif any(word in name_lower for word in ['anti-âge', 'anti-age', 'anti rides', 'liftant']):
                            category = 'TREATMENT'
                        
                        # Déterminer les problèmes ciblés
                        target_issues = []
                        if any(word in name_lower for word in ['acné', 'acne', 'imperfection', 'sebiaclear']):
                            target_issues.append('acne')
                        if any(word in name_lower for word in ['rides', 'anti-âge', 'anti-age']):
                            target_issues.append('wrinkles')
                        if any(word in name_lower for word in ['tache', 'éclaircissant', 'depigmentant', 'eclaircissant']):
                            target_issues.append('dark_spots')
                        if any(word in name_lower for word in ['rougeur', 'sensible', 'apaisant']):
                            target_issues.append('redness')
                        
                        # Extraire la taille
                        size = None
                        size_match = re.search(r'(\d+)\s*(ml|g|gr|kg|l)', name.lower())
                        if size_match:
                            size = f"{size_match.group(1)}{size_match.group(2).upper()}"
                        
                        page_products.append({
                            'name': name,
                            'brand': brand,
                            'description': name,
                            'price': price,
                            'size': size,
                            'category': category,
                            'target_skin_types': ['NORMAL'],
                            'target_issues': target_issues,
                            'image': image_url,
                            'url': product_url or base_url,
                            'source_site': 'pharma-shop.tn',
                            'source_url': base_url,
                        })
                        
                    except Exception as e:
                        print(f"   ⚠️ Erreur lors de l'extraction du produit {idx+1}: {e}")
                        continue
                
                all_products.extend(page_products)
                print(f"   ✅ Page {page}/{estimated_pages}: {len(page_products)} produits trouvés (Total: {len(all_products)})")
                
                # Si aucune page suivante ou moins de produits que prévu, arrêter
                if len(page_products) == 0 and page > 1:
                    print(f"⚠️ Aucun produit trouvé sur la page {page}, arrêt du scraping")
                    break
                
                # Pause entre les requêtes
                if page < estimated_pages:
                    time.sleep(1.5)
                    
            except requests.exceptions.Timeout:
                print(f"⏱️ Timeout sur la page {page}, passage à la suivante...")
                continue
            except requests.exceptions.RequestException as e:
                print(f"⚠️ Erreur de requête sur la page {page}: {e}")
                continue
            except Exception as e:
                print(f"❌ Erreur lors du scraping de la page {page}: {e}")
                import traceback
                print(traceback.format_exc())
                continue
        
        print(f"\n✅ Scraping terminé: {len(all_products)} produits extraits")
        return all_products
        
    except Exception as e:
        print(f"❌ Erreur lors du chargement de la première page: {e}")
        import traceback
        print(traceback.format_exc())
        return []


def save_products_to_database(products_data):
    """
    Sauvegarde les produits dans la base de données Django
    
    Args:
        products_data: Liste de dictionnaires contenant les données des produits
    
    Returns:
        Tuple (saved_count, updated_count, skipped_count)
    """
    saved_count = 0
    updated_count = 0
    skipped_count = 0
    
    print(f"\n💾 Sauvegarde de {len(products_data)} produits dans la base de données...")
    
    for idx, product_data in enumerate(products_data):
        try:
            name = product_data.get('name', '').strip()
            brand = product_data.get('brand', '').strip()
            source_site = product_data.get('source_site', 'pharma-shop.tn')
            url = product_data.get('url')
            
            if not name or not brand:
                skipped_count += 1
                continue
            
            # Chercher d'abord par URL (le plus fiable)
            existing_product = None
            if url:
                existing_product = ScrapedProduct.objects.filter(url=url).first()
            
            # Si pas trouvé par URL, chercher par nom+marque+source_site
            if not existing_product:
                existing_product = ScrapedProduct.objects.filter(
                    name=name,
                    brand=brand,
                    source_site=source_site
                ).first()
            
            if existing_product:
                # Mettre à jour seulement si c'est vraiment un doublon (même URL)
                if url and existing_product.url == url:
                    # Mise à jour
                    for key, value in product_data.items():
                        if hasattr(existing_product, key) and value is not None:
                            if key == 'target_skin_types' or key == 'target_issues':
                                if isinstance(value, list):
                                    setattr(existing_product, key, value)
                            elif key == 'price':
                                try:
                                    setattr(existing_product, key, float(value))
                                except (ValueError, TypeError):
                                    pass
                            else:
                                setattr(existing_product, key, value)
                    
                    if not existing_product.source_site:
                        existing_product.source_site = source_site
                    
                    existing_product.is_active = True
                    existing_product.save()
                    updated_count += 1
                else:
                    # Même nom/marque mais URL différente = produit différent, créer
                    existing_product = None
            else:
                # Pas de doublon trouvé
                existing_product = None
            
            if not existing_product:
                # Créer un nouveau produit
                try:
                    ScrapedProduct.objects.create(
                        name=name,
                        brand=brand,
                        description=product_data.get('description', '') or name,
                        ingredients=product_data.get('ingredients', ''),
                        price=float(product_data.get('price', 0)) if product_data.get('price') else 0,
                        size=product_data.get('size'),
                        category=product_data.get('category', 'MOISTURIZER'),
                        target_skin_types=product_data.get('target_skin_types', ['NORMAL']),
                        target_issues=product_data.get('target_issues', []),
                        image=product_data.get('image'),
                        url=product_data.get('url'),
                        source_site=source_site,
                        source_url=product_data.get('source_url'),
                        is_active=True,
                    )
                    saved_count += 1
                except Exception as create_error:
                    print(f"   ❌ Erreur lors de la création du produit {idx+1} ({name[:30]}...): {create_error}")
                    skipped_count += 1
                    continue
            
            # Afficher la progression tous les 50 produits
            if (saved_count + updated_count) % 50 == 0:
                print(f"   ✅ {saved_count + updated_count} produits traités...")
                
        except Exception as e:
            print(f"   ❌ Erreur lors du traitement du produit {idx+1}: {e}")
            skipped_count += 1
            continue
    
    print(f"\n✅ Sauvegarde terminée:")
    print(f"   - {saved_count} nouveaux produits créés")
    print(f"   - {updated_count} produits mis à jour")
    print(f"   - {skipped_count} produits ignorés")
    
    # Vérifier le total dans la base de données
    total_in_db = ScrapedProduct.objects.filter(source_site='pharma-shop.tn').count()
    active_in_db = ScrapedProduct.objects.filter(source_site='pharma-shop.tn', is_active=True).count()
    print(f"\n📊 Vérification base de données:")
    print(f"   - Total produits pour pharma-shop.tn: {total_in_db} (actifs: {active_in_db})")
    
    return saved_count, updated_count, skipped_count


def main():
    """Fonction principale"""
    print("=" * 80)
    print("🕷️  SCRAPER PHARMA-SHOP.TN - TOUS LES PRODUITS")
    print("=" * 80)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # URL à scraper
    url = 'https://pharma-shop.tn/839-visage'
    
    # Scraper tous les produits
    products = scrape_pharma_shop_tn(url)
    
    if not products:
        print("\n❌ Aucun produit trouvé. Vérifiez votre connexion internet et l'URL.")
        return
    
    print(f"\n📦 {len(products)} produits scrapés avec succès!")
    
    # Sauvegarder dans la base de données
    saved, updated, skipped = save_products_to_database(products)
    
    print("\n" + "=" * 80)
    print("✅ SCRAPING TERMINÉ AVEC SUCCÈS!")
    print("=" * 80)
    print(f"📊 Résumé:")
    print(f"   - Produits scrapés: {len(products)}")
    print(f"   - Nouveaux produits: {saved}")
    print(f"   - Produits mis à jour: {updated}")
    print(f"   - Produits ignorés: {skipped}")
    print(f"   - Total dans la base: {ScrapedProduct.objects.filter(source_site='pharma-shop.tn', is_active=True).count()}")
    print("=" * 80)


if __name__ == '__main__':
    main()

