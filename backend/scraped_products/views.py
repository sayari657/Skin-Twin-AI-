from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Count, Q
from django.utils import timezone
import requests
from bs4 import BeautifulSoup
import re
from .models import ScrapedProduct, ScrapingSession, ScrapingLog
from .serializers import (
    ScrapedProductSerializer, ScrapedProductCreateSerializer,
    ScrapingSessionSerializer, ScrapingLogSerializer, ScrapingStatsSerializer
)


class ScrapedProductListCreateView(generics.ListCreateAPIView):
    """Vue pour lister et créer des produits scrapés"""
    
    queryset = ScrapedProduct.objects.filter(is_active=True)
    permission_classes = [permissions.AllowAny]  # Temporaire pour le développement
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ScrapedProductCreateSerializer
        return ScrapedProductSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtrage par catégorie
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Filtrage par marque
        brand = self.request.query_params.get('brand')
        if brand:
            queryset = queryset.filter(brand__icontains=brand)
        
        # Filtrage par prix
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Recherche textuelle
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(brand__icontains=search) |
                Q(description__icontains=search)
            )
        
        return queryset.order_by('-created_at')


class ScrapedProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Vue pour récupérer, modifier et supprimer un produit scrapé"""
    
    queryset = ScrapedProduct.objects.all()
    serializer_class = ScrapedProductSerializer
    permission_classes = [permissions.AllowAny]  # Temporaire pour le développement


class ScrapingSessionListCreateView(generics.ListCreateAPIView):
    """Vue pour lister et créer des sessions de scraping"""
    
    queryset = ScrapingSession.objects.all()
    serializer_class = ScrapingSessionSerializer
    permission_classes = [permissions.AllowAny]  # Temporaire pour le développement


class ScrapingSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Vue pour récupérer, modifier et supprimer une session de scraping"""
    
    queryset = ScrapingSession.objects.all()
    serializer_class = ScrapingSessionSerializer
    permission_classes = [permissions.AllowAny]  # Temporaire pour le développement


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def scraping_stats(request):
    """Endpoint pour obtenir les statistiques de scraping"""
    
    # Statistiques générales
    total_products = ScrapedProduct.objects.filter(is_active=True).count()
    total_sessions = ScrapingSession.objects.count()
    active_sessions = ScrapingSession.objects.filter(status='RUNNING').count()
    
    # Produits par catégorie
    products_by_category = dict(
        ScrapedProduct.objects.filter(is_active=True)
        .values('category')
        .annotate(count=Count('id'))
        .values_list('category', 'count')
    )
    
    # Produits par source
    products_by_source = dict(
        ScrapedProduct.objects.filter(is_active=True)
        .values('source_site')
        .annotate(count=Count('id'))
        .values_list('source_site', 'count')
    )
    
    # Produits récents
    recent_products = ScrapedProduct.objects.filter(is_active=True).order_by('-created_at')[:10]
    
    # Sessions récentes
    recent_sessions = ScrapingSession.objects.order_by('-started_at')[:5]
    
    stats = {
        'total_products': total_products,
        'total_sessions': total_sessions,
        'active_sessions': active_sessions,
        'products_by_category': products_by_category,
        'products_by_source': products_by_source,
        'recent_products': ScrapedProductSerializer(recent_products, many=True).data,
        'recent_sessions': ScrapingSessionSerializer(recent_sessions, many=True).data
    }
    
    return Response(stats)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def start_scraping_session(request):
    """Endpoint pour démarrer une nouvelle session de scraping"""
    
    session_name = request.data.get('session_name', f'Scraping {timezone.now().strftime("%Y-%m-%d %H:%M")}')
    source_sites = request.data.get('source_sites', [])
    
    # Créer la session
    session = ScrapingSession.objects.create(
        session_name=session_name,
        source_sites=source_sites,
        status='PENDING',
        created_by=request.user if request.user.is_authenticated else None
    )
    
    # Créer un log
    ScrapingLog.objects.create(
        session=session,
        log_type='INFO',
        message=f'Session de scraping "{session_name}" créée'
    )
    
    return Response(ScrapingSessionSerializer(session).data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def save_scraped_products(request):
    """Endpoint pour sauvegarder des produits scrapés"""
    
    products_data = request.data.get('products', [])
    session_id = request.data.get('session_id')
    
    if not products_data:
        return Response({'error': 'Aucun produit fourni'}, status=status.HTTP_400_BAD_REQUEST)
    
    saved_count = 0
    updated_count = 0
    skipped_count = 0
    errors = []
    
    print(f"💾 Sauvegarde de {len(products_data)} produits...")
    
    for idx, product_data in enumerate(products_data):
        try:
            # Extraire les données nécessaires
            name = product_data.get('name', '').strip()
            brand = product_data.get('brand', '').strip()
            source_site = product_data.get('source_site', 'pharma-shop.tn').strip()
            
            if not name or not brand:
                skipped_count += 1
                print(f"   Produit {idx+1}: Nom ou marque manquant (nom='{name}', brand='{brand}')")
                continue
            
            # Vérifier si le produit existe déjà
            # Priorité : URL > nom+marque+source_site > nom+marque
            existing_product = None
            
            # 1. Chercher d'abord par URL (le plus fiable pour éviter les doublons)
            if product_data.get('url'):
                existing_product = ScrapedProduct.objects.filter(
                    url=product_data.get('url')
                ).first()
                if existing_product:
                    print(f"   Produit {idx+1} ({name[:30]}...): Trouvé par URL (doublon), mise à jour")
            
            # 2. Si pas trouvé par URL, chercher par nom+marque+source_site
            if not existing_product:
                existing_product = ScrapedProduct.objects.filter(
                    name=name,
                    brand=brand,
                    source_site=source_site
                ).first()
                if existing_product:
                    print(f"   Produit {idx+1} ({name[:30]}...): Trouvé par nom+marque+source (doublon), mise à jour")
            
            # 3. Si pas trouvé, chercher sans source_site (pour les anciens produits)
            if not existing_product:
                existing_product = ScrapedProduct.objects.filter(
                    name=name,
                    brand=brand
                ).filter(Q(source_site__isnull=True) | Q(source_site='')).first()
                if existing_product:
                    print(f"   Produit {idx+1} ({name[:30]}...): Trouvé sans source_site, mise à jour avec source_site={source_site}")
            
            if existing_product:
                # Mettre à jour le produit existant seulement si c'est vraiment un doublon (même URL)
                # Sinon, créer un nouveau produit même si le nom/marque est similaire
                if product_data.get('url') and existing_product.url == product_data.get('url'):
                    # C'est vraiment un doublon (même URL), mettre à jour
                    print(f"   Produit {idx+1} ({name[:30]}...): Mise à jour du produit existant (ID: {existing_product.id}) - même URL")
                    for key, value in product_data.items():
                        if hasattr(existing_product, key) and value is not None:
                            # Gérer les champs spéciaux
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
                    
                    # S'assurer que source_site est défini
                    if not existing_product.source_site:
                        existing_product.source_site = source_site
                    
                    existing_product.is_active = True
                    existing_product.save()
                    updated_count += 1
                else:
                    # Même nom/marque mais URL différente = produit différent, créer un nouveau
                    print(f"   Produit {idx+1} ({name[:30]}...): Même nom/marque mais URL différente, création d'un nouveau produit")
                    existing_product = None  # Forcer la création
            else:
                # Pas de doublon trouvé, créer un nouveau produit
                existing_product = None
            
            if not existing_product:
                # Créer un nouveau produit avec tous les champs nécessaires
                try:
                    print(f"   Produit {idx+1} ({name[:30]}...): Création d'un nouveau produit")
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
                    import traceback
                    print(traceback.format_exc())
                    skipped_count += 1
                    errors.append(f"Produit {name[:30]}: {str(create_error)}")
                    continue
            
            if (saved_count + updated_count) % 10 == 0:
                print(f"   ✅ {saved_count + updated_count} produits traités...")
                
        except Exception as e:
            print(f"   ❌ Erreur lors du traitement du produit {idx+1}: {e}")
            import traceback
            print(traceback.format_exc())
            skipped_count += 1
            errors.append(f"Produit {idx+1}: {str(e)}")
            continue
    
    print(f"✅ Sauvegarde terminée: {saved_count} nouveaux, {updated_count} mis à jour, {skipped_count} ignorés")
    
    # Vérifier que les produits sont bien dans la base de données
    # Utiliser le source_site du premier produit ou 'pharma-shop.tn' par défaut
    first_source_site = products_data[0].get('source_site', 'pharma-shop.tn') if products_data else 'pharma-shop.tn'
    total_in_db = ScrapedProduct.objects.filter(source_site=first_source_site).count()
    active_in_db = ScrapedProduct.objects.filter(source_site=first_source_site, is_active=True).count()
    all_total = ScrapedProduct.objects.all().count()
    all_active = ScrapedProduct.objects.filter(is_active=True).count()
    print(f"📊 Vérification base de données:")
    print(f"   - Total produits pour {first_source_site}: {total_in_db} (actifs: {active_in_db})")
    print(f"   - Total produits scrapés (tous sites): {all_total} (actifs: {all_active})")
    
    # Mettre à jour la session si fournie
    if session_id:
        try:
            session = ScrapingSession.objects.get(id=session_id)
            session.total_products_found += len(products_data)
            session.total_products_saved += saved_count
            session.total_products_skipped += skipped_count
            session.save()
            
            # Créer des logs
            ScrapingLog.objects.create(
                session=session,
                log_type='SUCCESS',
                message=f'{saved_count} produits sauvegardés ({updated_count} mis à jour)'
            )
            
            if skipped_count > 0:
                ScrapingLog.objects.create(
                    session=session,
                    log_type='WARNING',
                    message=f'{skipped_count} produits ignorés'
                )
                
        except ScrapingSession.DoesNotExist:
            pass
    
    return Response({
        'success': True,
        'saved_products': saved_count,
        'updated_products': updated_count,
        'skipped_products': skipped_count,
        'total_processed': len(products_data),
        'errors': errors[:10] if errors else []  # Retourner les 10 premières erreurs
    })


def scrape_pharma_shop_tn(soup, base_url):
    """Scraper spécifique pour pharma-shop.tn"""
    products = []
    
    # Chercher les produits dans les divs avec classe "thumbnail-container" (avec ou sans "reviews-loaded")
    product_elements = soup.find_all('div', class_=re.compile(r'thumbnail-container', re.I))
    
    # Alternative: chercher aussi dans les articles avec classe "product-miniature"
    if not product_elements:
        product_elements = soup.find_all('article', class_=re.compile(r'product-miniature', re.I))
        # Si on trouve des articles, chercher le thumbnail-container à l'intérieur
        if product_elements:
            temp_elements = []
            for article in product_elements:
                thumbnail = article.find('div', class_=re.compile(r'thumbnail-container', re.I))
                if thumbnail:
                    temp_elements.append(thumbnail)
            product_elements = temp_elements
    
    print(f"Trouvé {len(product_elements)} éléments de produits")
    
    if len(product_elements) == 0:
        print("⚠️ Aucun produit trouvé. Vérification de la structure HTML...")
        # Debug: afficher quelques éléments pour comprendre la structure
        all_divs = soup.find_all('div', limit=10)
        print(f"   Premiers divs trouvés: {[div.get('class') for div in all_divs if div.get('class')]}")
    
    for idx, element in enumerate(product_elements):
        try:
            # Extraire le nom du produit depuis h2.product-title ou h2.h3.product-title
            name = None
            name_elem = element.find('h2', class_='product-title')
            if not name_elem:
                # Essayer avec h2.h3.product-title
                name_elem = element.find('h2', class_=re.compile(r'product-title', re.I))
            
            if name_elem:
                name_link = name_elem.find('a')
                if name_link:
                    name = name_link.get_text(strip=True)
                    # Nettoyer le nom (enlever les points de suspension)
                    name = name.replace('...', '').strip()
                else:
                    name = name_elem.get_text(strip=True)
            else:
                # Fallback: chercher dans les autres éléments
                name_elem = element.find(['h2', 'h3'], class_=re.compile(r'title', re.I))
                if name_elem:
                    name_link = name_elem.find('a')
                    name = name_link.get_text(strip=True) if name_link else name_elem.get_text(strip=True)
            
            if not name or len(name) < 3:
                print(f"   Produit {idx+1}: Nom invalide ou manquant")
                continue
            
            # Nettoyer le nom
            name = ' '.join(name.split())
            
            # Extraire le prix depuis span.price
            price = 0.0
            price_elem = element.find('span', class_='price')
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                # Enlever &nbsp; et autres caractères
                price_text = price_text.replace('\xa0', ' ').replace('TND', '').strip()
                # Gérer les virgules comme séparateurs décimaux
                price_match = re.search(r'(\d+[.,]\d+)', price_text.replace(',', '.'))
                if price_match:
                    price = float(price_match.group(1).replace(',', '.'))
            
            # Si pas trouvé, chercher dans product-price-and-shipping
            if price <= 0:
                price_container = element.find('div', class_='product-price-and-shipping')
                if price_container:
                    price_text = price_container.get_text()
                    price_match = re.search(r'(\d+[.,]\d+)\s*TND', price_text)
                    if price_match:
                        price = float(price_match.group(1).replace(',', '.'))
            
            if price <= 0:
                print(f"   Produit {idx+1} ({name[:30]}...): Prix invalide ou manquant")
                continue
            
            # Extraire l'image depuis product-image > img
            image_url = None
            product_image_div = element.find('div', class_='product-image')
            if product_image_div:
                img_elem = product_image_div.find('img')
                if img_elem:
                    # Priorité: data-full-size-image-url > src
                    image_url = img_elem.get('data-full-size-image-url') or img_elem.get('src')
                    if image_url:
                        if image_url.startswith('//'):
                            image_url = 'https:' + image_url
                        elif image_url.startswith('/'):
                            image_url = base_url.rstrip('/') + image_url
                        elif not image_url.startswith('http'):
                            image_url = base_url.rstrip('/') + '/' + image_url.lstrip('/')
            
            # Extraire le lien du produit depuis h2.product-title > a ou thumbnail > a
            product_url = None
            name_link_elem = element.find('h2', class_=re.compile(r'product-title', re.I))
            if name_link_elem:
                link_elem = name_link_elem.find('a', href=True)
                if link_elem:
                    product_url = link_elem.get('href')
            
            # Fallback: chercher dans thumbnail
            if not product_url:
                thumbnail = element.find('a', class_='product-thumbnail')
                if thumbnail:
                    product_url = thumbnail.get('href')
            
            # Fallback: chercher n'importe quel lien dans product-image
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
                    product_url = base_url.rstrip('/') + product_url
                elif not product_url.startswith('http'):
                    product_url = base_url.rstrip('/') + '/' + product_url.lstrip('/')
            
            # Extraire la marque depuis div.txt-marque > a
            brand = 'Marque inconnue'
            brand_elem = element.find('div', class_='txt-marque')
            if brand_elem:
                brand_link = brand_elem.find('a')
                if brand_link:
                    brand = brand_link.get_text(strip=True)
                else:
                    brand = brand_elem.get_text(strip=True)
            
            # Fallback: extraire du nom si pas trouvé
            if brand == 'Marque inconnue' or not brand:
                name_words = name.split()
                if name_words:
                    brand = name_words[0]
            
            # Déterminer la catégorie basée sur le nom
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
            
            # Extraire la taille si disponible (généralement dans le nom ou description)
            size = None
            size_match = re.search(r'(\d+)\s*(ml|g|gr|kg|l)', name.lower())
            if size_match:
                size = f"{size_match.group(1)}{size_match.group(2).upper()}"
            
            products.append({
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
            
            if len(products) % 10 == 0:
                print(f"   {len(products)} produits extraits...")
                
        except Exception as e:
            print(f"   Erreur lors de l'extraction du produit {idx+1}: {e}")
            import traceback
            print(traceback.format_exc())
            continue
    
    print(f"✅ Total produits extraits: {len(products)}")
    return products


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def scrape_web_products(request):
    """Endpoint pour scraper des produits depuis une URL web"""
    
    url = request.data.get('url')
    search_query = request.data.get('search_query', '')
    source_site = request.data.get('source_site', 'unknown')
    max_pages = request.data.get('max_pages', 1)  # Nombre de pages à scraper
    auto_save = request.data.get('auto_save', False)  # Sauvegarder automatiquement
    
    if not url and not search_query:
        return Response({'error': 'URL ou terme de recherche requis'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Headers pour éviter les blocages
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        # Si c'est une recherche, construire l'URL de recherche
        if search_query and not url:
            if 'amazon' in source_site.lower():
                url = f"https://www.amazon.fr/s?k={search_query.replace(' ', '+')}"
            elif 'sephora' in source_site.lower():
                url = f"https://www.sephora.fr/search?keyword={search_query.replace(' ', '+')}"
            elif 'nocibe' in source_site.lower():
                url = f"https://www.nocibe.fr/recherche?q={search_query.replace(' ', '+')}"
            else:
                url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}+soin+peau"
        
        all_products = []
        base_url = '/'.join(url.split('/')[:3])  # Extraire le domaine de base
        
        # Scraper pharma-shop.tn spécifiquement
        if 'pharma-shop.tn' in url:
            try:
                # Détecter le nombre total de pages depuis la première page
                print(f"🔍 Connexion à {url}...")
                first_response = requests.get(url, headers=headers, timeout=30)
                first_response.raise_for_status()
                print(f"✅ Page chargée avec succès (Status: {first_response.status_code})")
                first_soup = BeautifulSoup(first_response.content, 'html.parser')
            except requests.exceptions.Timeout:
                return Response({
                    'success': False,
                    'error': f'Timeout lors de la connexion à {url}. Le serveur met trop de temps à répondre.'
                }, status=status.HTTP_408_REQUEST_TIMEOUT)
            except requests.exceptions.ConnectionError:
                return Response({
                    'success': False,
                    'error': f'Erreur de connexion à {url}. Vérifiez votre connexion internet.'
                }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            except requests.exceptions.HTTPError as e:
                return Response({
                    'success': False,
                    'error': f'Erreur HTTP {e.response.status_code} lors de l\'accès à {url}: {str(e)}'
                }, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                import traceback
                error_trace = traceback.format_exc()
                print(f"❌ Erreur lors du chargement de la première page: {e}")
                print(error_trace)
                return Response({
                    'success': False,
                    'error': f'Erreur lors du chargement de la page: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # Chercher le texte "Affichage 1-24 de X article(s)"
            pagination_text = first_soup.find(string=re.compile(r'Affichage.*de\s+(\d+)\s+article', re.I))
            total_products = 0
            if pagination_text:
                match = re.search(r'de\s+(\d+)\s+article', pagination_text)
                if match:
                    total_products = int(match.group(1))
                    # Calculer le nombre de pages (24 produits par page généralement)
                    estimated_pages = (total_products // 24) + 1
                    max_pages = min(max_pages, estimated_pages, 100)  # Limiter à 100 pages max
            
            # Chercher aussi dans la pagination
            pagination = first_soup.find('div', class_=re.compile(r'pagination', re.I))
            if pagination:
                page_links = pagination.find_all('a', href=True)
                if page_links:
                    # Extraire le numéro de page le plus élevé
                    max_page_num = 1
                    for link in page_links:
                        href = link.get('href', '')
                        page_match = re.search(r'[?&]p=(\d+)', href)
                        if page_match:
                            page_num = int(page_match.group(1))
                            max_page_num = max(max_page_num, page_num)
                    if max_page_num > 1:
                        max_pages = min(max_pages, max_page_num)
            
            print(f"Scraping {max_pages} pages de pharma-shop.tn (environ {total_products} produits)...")
            
            total_saved = 0
            for page in range(1, max_pages + 1):
                page_url = url
                if page > 1:
                    # Ajouter le paramètre de page
                    if '?' in url:
                        page_url = f"{url}&p={page}"
                    else:
                        page_url = f"{url}?p={page}"
                
                try:
                    print(f"📄 Scraping page {page}/{max_pages}: {page_url}")
                    response = requests.get(page_url, headers=headers, timeout=30)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    page_products = scrape_pharma_shop_tn(soup, base_url)
                    all_products.extend(page_products)
                    
                    print(f"✅ Page {page}/{max_pages}: {len(page_products)} produits trouvés (Total: {len(all_products)})")
                    
                    # Sauvegarder par lots si auto_save est activé
                    if auto_save and len(page_products) > 0:
                        try:
                            saved_count = save_products_batch(page_products, source_site)
                            total_saved += saved_count
                            print(f"  💾 {saved_count} produits sauvegardés dans la base de données (Total sauvegardé: {total_saved})")
                        except Exception as save_error:
                            print(f"  ⚠️ Erreur lors de la sauvegarde: {save_error}")
                            import traceback
                            print(traceback.format_exc())
                    
                    # Si aucune page suivante ou moins de produits que prévu, arrêter
                    if len(page_products) == 0 and page > 1:
                        print(f"⚠️ Aucun produit trouvé sur la page {page}, arrêt du scraping")
                        break
                    
                    # Petite pause entre les requêtes pour éviter les blocages
                    import time
                    time.sleep(1.5)  # Augmenter à 1.5 secondes pour être plus respectueux
                    
                except requests.exceptions.Timeout:
                    print(f"⏱️ Timeout sur la page {page}, passage à la suivante...")
                    continue
                except requests.exceptions.RequestException as e:
                    print(f"⚠️ Erreur de requête sur la page {page}: {e}")
                    continue
                except Exception as e:
                    import traceback
                    print(f"❌ Erreur lors du scraping de la page {page}: {e}")
                    print(traceback.format_exc())
                    continue
            
            # Si auto_save est activé, retourner les résultats avec le nombre de produits sauvegardés
            if auto_save:
                if len(all_products) == 0:
                    return Response({
                        'success': False,
                        'error': 'Aucun produit trouvé. Vérifiez que l\'URL est correcte et que le site est accessible.',
                        'products': [],
                        'total_found': 0,
                        'total_saved': 0,
                        'url': url,
                    }, status=status.HTTP_404_NOT_FOUND)
                
                return Response({
                    'success': True,
                    'products': all_products[:50],  # Retourner seulement les 50 premiers pour l'affichage
                    'total_found': len(all_products),
                    'total_saved': total_saved,
                    'url': url,
                    'message': f'{total_saved} produits sauvegardés sur {len(all_products)} trouvés dans la base de données'
                })
            
            # Si auto_save est désactivé
            if len(all_products) == 0:
                return Response({
                    'success': False,
                    'error': 'Aucun produit trouvé. Vérifiez que l\'URL est correcte et que le site est accessible.',
                    'products': [],
                    'total_found': 0,
                    'url': url,
                }, status=status.HTTP_404_NOT_FOUND)
            
            return Response({
                'success': True,
                'products': all_products,
                'total_found': len(all_products),
                'url': url,
            })
        else:
            # Logique générique pour les autres sites
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            product_elements = soup.find_all(['div', 'article', 'li'], class_=re.compile(r'product|item|card', re.I))
            
            for element in product_elements[:50]:  # Limiter à 50 produits pour les autres sites
                try:
                    name_elem = element.find(['h1', 'h2', 'h3', 'h4', 'span', 'a'], class_=re.compile(r'title|name|product', re.I))
                    name = name_elem.get_text(strip=True) if name_elem else 'Produit sans nom'
                    
                    price_elem = element.find(['span', 'div', 'p'], class_=re.compile(r'price|prix|cost', re.I))
                    price_text = price_elem.get_text(strip=True) if price_elem else ''
                    price_match = re.search(r'(\d+[.,]\d+)', price_text.replace(',', '.'))
                    price = float(price_match.group(1)) if price_match else 0.0
                    
                    img_elem = element.find('img')
                    image_url = img_elem.get('src') or img_elem.get('data-src') if img_elem else None
                    if image_url and not image_url.startswith('http'):
                        image_url = base_url + image_url if image_url.startswith('/') else url + '/' + image_url
                    
                    link_elem = element.find('a')
                    product_url = link_elem.get('href') if link_elem else None
                    if product_url and not product_url.startswith('http'):
                        product_url = base_url + product_url if product_url.startswith('/') else url + '/' + product_url
                    
                    brand = name.split()[0] if name else 'Marque inconnue'
                    
                    category = 'MOISTURIZER'
                    name_lower = name.lower()
                    if any(word in name_lower for word in ['nettoyant', 'cleanser', 'démaquillant']):
                        category = 'CLEANSER'
                    elif any(word in name_lower for word in ['sérum', 'serum']):
                        category = 'SERUM'
                    elif any(word in name_lower for word in ['solaire', 'sun', 'spf']):
                        category = 'SUNSCREEN'
                    elif any(word in name_lower for word in ['masque', 'mask']):
                        category = 'MASK'
                    elif any(word in name_lower for word in ['tonique', 'toner']):
                        category = 'TONER'
                    elif any(word in name_lower for word in ['exfoliant', 'scrub']):
                        category = 'EXFOLIANT'
                    
                    if name and name != 'Produit sans nom' and price > 0:
                        all_products.append({
                            'name': name,
                            'brand': brand,
                            'description': name,
                            'price': price,
                            'category': category,
                            'target_skin_types': ['NORMAL'],
                            'target_issues': [],
                            'image': image_url,
                            'url': product_url or url,
                            'source_site': source_site,
                            'source_url': url,
                        })
                except Exception as e:
                    print(f"Erreur lors de l'extraction d'un produit: {e}")
                    continue
            
            # Sauvegarder si auto_save est activé
            if auto_save and len(all_products) > 0:
                total_saved = save_products_batch(all_products, source_site)
                return Response({
                    'success': True,
                    'products': all_products,
                    'total_found': len(all_products),
                    'total_saved': total_saved,
                    'url': url,
                    'message': f'{total_saved} produits sauvegardés sur {len(all_products)} trouvés'
                })
        
        # Pour les autres sites ou si auto_save est désactivé
        return Response({
            'success': True,
            'products': all_products,
            'total_found': len(all_products),
            'url': url,
        })
        
    except requests.exceptions.Timeout as e:
        return Response({
            'success': False,
            'error': f'Timeout lors de la connexion. Le serveur met trop de temps à répondre: {str(e)}'
        }, status=status.HTTP_408_REQUEST_TIMEOUT)
    except requests.exceptions.ConnectionError as e:
        return Response({
            'success': False,
            'error': f'Erreur de connexion. Vérifiez votre connexion internet: {str(e)}'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    except requests.exceptions.RequestException as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"❌ Erreur de requête HTTP: {e}")
        print(error_trace)
        return Response({
            'success': False,
            'error': f'Erreur lors de la requête HTTP: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"❌ Erreur inattendue lors du scraping: {e}")
        print(error_trace)
        return Response({
            'success': False,
            'error': f'Erreur lors du scraping: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def save_products_batch(products_data, source_site='pharma-shop.tn'):
    """Sauvegarde un lot de produits dans la base de données"""
    saved_count = 0
    skipped_count = 0
    
    for product_data in products_data:
        try:
            # Vérifier si le produit existe déjà (par nom, marque et URL)
            existing_product = ScrapedProduct.objects.filter(
                name=product_data.get('name'),
                brand=product_data.get('brand'),
                source_site=source_site
            ).first()
            
            if existing_product:
                # Mettre à jour le produit existant
                for key, value in product_data.items():
                    if hasattr(existing_product, key) and value:
                        setattr(existing_product, key, value)
                existing_product.is_active = True
                existing_product.save()
                saved_count += 1
            else:
                # Créer un nouveau produit
                ScrapedProduct.objects.create(
                    name=product_data.get('name'),
                    brand=product_data.get('brand'),
                    description=product_data.get('description', ''),
                    price=product_data.get('price', 0),
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
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du produit {product_data.get('name', 'Unknown')}: {e}")
            skipped_count += 1
            continue
    
    return saved_count


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def search_products(request):
    """Endpoint pour rechercher des produits scrapés"""
    
    query = request.query_params.get('q', '')
    category = request.query_params.get('category', '')
    brand = request.query_params.get('brand', '')
    
    queryset = ScrapedProduct.objects.filter(is_active=True)
    
    if query:
        queryset = queryset.filter(
            Q(name__icontains=query) |
            Q(brand__icontains=query) |
            Q(description__icontains=query)
        )
    
    if category:
        queryset = queryset.filter(category=category)
    
    if brand:
        queryset = queryset.filter(brand__icontains=brand)
    
    products = queryset.order_by('-created_at')[:50]  # Limiter à 50 résultats
    
    return Response(ScrapedProductSerializer(products, many=True).data)




