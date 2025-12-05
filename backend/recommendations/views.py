import re
from django.db.models import Q
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Product, Recommendation
from .serializers import ProductSerializer, RecommendationSerializer
from detection.models import SkinAnalysis
from .recommender import product_recommender
from scraped_products.models import ScrapedProduct
from products.views import convert_scraped_to_product


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_recommendations(request, analysis_id):
    """Obtenir les recommandations pour une analyse"""
    try:
        analysis = SkinAnalysis.objects.get(id=analysis_id, user=request.user)
        
        # Générer les recommandations (inclut maintenant les produits scrapés)
        recommendations = product_recommender.get_recommendations(analysis, limit=50)  # Augmenter pour avoir plus de choix
        
        # Normaliser le nom d'un produit pour la comparaison
        def normalize_product_name(name, brand):
            """Normalise le nom d'un produit pour la comparaison"""
            if not name:
                return ''
            normalized = name.lower().strip()
            # Enlever les caractères spéciaux et espaces multiples
            normalized = re.sub(r'[^\w\s]', '', normalized)
            normalized = re.sub(r'\s+', ' ', normalized)
            return normalized
        
        # Dictionnaire pour regrouper les produits similaires
        # Clé: (nom_normalisé, marque_normalisée), Valeur: liste de produits avec leurs liens
        grouped_products = {}
        
        # Première passe : collecter tous les produits recommandés
        for rec in recommendations:
            product = rec['product']
            
            # Vérifier si c'est un produit scrapé (ID > 1000000)
            if hasattr(product, 'id') and product.id >= 1000000:
                # C'est un produit scrapé
                scraped_id = product.id - 1000000
                try:
                    scraped_product = ScrapedProduct.objects.get(id=scraped_id)
                    product_data = convert_scraped_to_product(scraped_product)
                except ScrapedProduct.DoesNotExist:
                    continue
            else:
                # C'est un produit de la base de données
                serializer = ProductSerializer(product)
                product_data = serializer.data
            
            # Créer une clé de regroupement basée sur le nom et la marque normalisés
            product_name = product_data.get('name', '') or product_data.get('brand', '')
            product_brand = product_data.get('brand', '')
            key = (normalize_product_name(product_name, product_brand), normalize_product_name(product_brand, ''))
            
            if key not in grouped_products:
                grouped_products[key] = {
                    'product': product_data,
                    'relevance_score': rec['relevance_score'],
                    'confidence_score': rec['confidence_score'],
                    'reasons': rec['reasons'],
                    'all_sources': []  # Liste de tous les liens disponibles
                }
            
            # Ajouter le lien de ce produit à la liste des sources
            if product_data.get('url') and product_data.get('source_site'):
                link_info = {
                    'url': product_data['url'],
                    'source_site': product_data['source_site'],
                    'price': product_data.get('price'),
                    'description': product_data.get('description', '')
                }
                # Vérifier si ce lien n'existe pas déjà
                if not any(link['url'] == link_info['url'] for link in grouped_products[key]['all_sources']):
                    grouped_products[key]['all_sources'].append(link_info)
        
        # Chercher d'autres produits similaires dans la base de données pour chaque produit recommandé
        # Cela permet de trouver le même produit sur d'autres sites
        
        # Récupérer tous les IDs déjà dans les recommandations pour les exclure
        already_included_ids = []
        for p in grouped_products.values():
            product_id = p['product'].get('id', 0)
            if product_id >= 1000000:
                already_included_ids.append(product_id - 1000000)
        
        for key, grouped_data in list(grouped_products.items()):
            product_name = grouped_data['product'].get('name', '')
            product_brand = grouped_data['product'].get('brand', '')
            product_category = grouped_data['product'].get('category', '')
            
            if product_name:
                # Recherche plus flexible : chercher par nom ET marque
                # Extraire les mots-clés importants du nom (enlever les mots communs)
                name_words = product_name.lower().split()
                # Mots à ignorer (articles, prépositions, etc.)
                stop_words = {'le', 'la', 'les', 'de', 'du', 'des', 'et', 'pour', 'avec', 'sans', 'sur'}
                keywords = [w for w in name_words if len(w) > 3 and w not in stop_words][:3]  # Prendre les 3 premiers mots significatifs
                
                # Construire une requête flexible
                query = Q(is_active=True)
                
                # Chercher par nom (contient les mots-clés)
                if keywords:
                    for keyword in keywords:
                        query &= Q(name__icontains=keyword)
                else:
                    # Si pas de mots-clés, chercher par nom complet (au moins 10 caractères)
                    if len(product_name) >= 10:
                        query &= Q(name__icontains=product_name[:50])
                
                # Chercher aussi par marque si disponible
                if product_brand and len(product_brand) > 2:
                    query |= Q(brand__icontains=product_brand)
                
                # Exclure les produits déjà inclus
                if already_included_ids:
                    query &= ~Q(id__in=already_included_ids)
                
                # Chercher des produits similaires dans ScrapedProduct
                # Prioriser les produits de la même catégorie
                if product_category:
                    query_with_category = query & Q(category=product_category)
                    similar_products = list(ScrapedProduct.objects.filter(query_with_category).distinct()[:15])
                    # Si pas assez de résultats avec la catégorie, chercher sans catégorie
                    if len(similar_products) < 5:
                        similar_products.extend(
                            list(ScrapedProduct.objects.filter(query).exclude(id__in=[p.id for p in similar_products]).distinct()[:10])
                        )
                else:
                    similar_products = list(ScrapedProduct.objects.filter(query).distinct()[:15])
                
                for similar_product in similar_products:
                    # Vérifier si c'est vraiment le même produit (même nom et marque normalisés)
                    similar_name_norm = normalize_product_name(similar_product.name, similar_product.brand)
                    similar_brand_norm = normalize_product_name(similar_product.brand, '')
                    
                    # Comparaison plus flexible : accepter si le nom normalisé correspond à 80% ou plus
                    # OU si c'est exactement le même produit
                    is_same_product = (
                        (similar_name_norm == key[0] and similar_brand_norm == key[1]) or
                        (similar_name_norm == key[0] and len(key[0]) > 10) or  # Nom long et identique
                        (similar_brand_norm == key[1] and key[1] and len(key[1]) > 3)  # Marque identique
                    )
                    
                    # Vérifier aussi la similarité par mots-clés
                    if not is_same_product and keywords:
                        similar_name_words = set(similar_product.name.lower().split())
                        matching_keywords = sum(1 for kw in keywords if kw in ' '.join(similar_name_words))
                        # Si au moins 2 mots-clés correspondent, considérer comme similaire
                        if matching_keywords >= 2:
                            is_same_product = True
                    
                    if is_same_product:
                        # C'est le même produit ou très similaire, ajouter son lien
                        if similar_product.url and similar_product.source_site:
                            link_info = {
                                'url': similar_product.url,
                                'source_site': similar_product.source_site,
                                'price': float(similar_product.price) if similar_product.price else None,
                                'description': similar_product.description or ''
                            }
                            # Vérifier si ce lien n'existe pas déjà
                            if not any(link['url'] == link_info['url'] for link in grouped_data['all_sources']):
                                grouped_data['all_sources'].append(link_info)
                                # Ajouter cet ID à la liste pour éviter de le traiter à nouveau
                                if similar_product.id not in already_included_ids:
                                    already_included_ids.append(similar_product.id)
        
        # Recherche supplémentaire : pour chaque produit recommandé, chercher TOUS les produits
        # de la même marque et catégorie sur TOUS les sites pour diversifier les sources
        for key, grouped_data in list(grouped_products.items()):
            product_brand = grouped_data['product'].get('brand', '')
            product_category = grouped_data['product'].get('category', '')
            
            # Si on a moins de 3 sources, chercher plus largement
            if len(grouped_data['all_sources']) < 3 and product_brand and product_category:
                # Chercher tous les produits de la même marque et catégorie sur tous les sites
                brand_category_products = ScrapedProduct.objects.filter(
                    Q(is_active=True) &
                    Q(brand__icontains=product_brand) &
                    Q(category=product_category)
                ).exclude(
                    id__in=already_included_ids
                ).distinct()[:10]
                
                for alt_product in brand_category_products:
                    # Vérifier que c'est un site différent de ceux déjà trouvés
                    existing_sites = [s['source_site'] for s in grouped_data['all_sources']]
                    if alt_product.source_site and alt_product.source_site not in existing_sites:
                        if alt_product.url:
                            link_info = {
                                'url': alt_product.url,
                                'source_site': alt_product.source_site,
                                'price': float(alt_product.price) if alt_product.price else None,
                                'description': alt_product.description or alt_product.name or ''
                            }
                            grouped_data['all_sources'].append(link_info)
                            if alt_product.id not in already_included_ids:
                                already_included_ids.append(alt_product.id)
                            
                            # Limiter à 5 sources différentes par produit
                            if len(grouped_data['all_sources']) >= 5:
                                break
        
        # Convertir en format pour le frontend
        formatted_recommendations = []
        for key, grouped_data in grouped_products.items():
            product_data = grouped_data['product'].copy()
            
            # Ajouter tous les liens disponibles dans le champ 'sources' ou 'links'
            if grouped_data['all_sources']:
                product_data['sources'] = grouped_data['all_sources']
                # Garder aussi l'URL principale pour compatibilité
                if not product_data.get('url') and grouped_data['all_sources']:
                    product_data['url'] = grouped_data['all_sources'][0]['url']
                    product_data['source_site'] = grouped_data['all_sources'][0]['source_site']
            
            formatted_recommendations.append({
                'product': product_data,
                'relevance_score': grouped_data['relevance_score'],
                'confidence_score': grouped_data['confidence_score'],
                'reasons': grouped_data['reasons']
            })
        
        # Trier par score de pertinence et limiter à 20
        formatted_recommendations.sort(key=lambda x: x['relevance_score'], reverse=True)
        formatted_recommendations = formatted_recommendations[:20]
        
        return Response(formatted_recommendations)
        
    except SkinAnalysis.DoesNotExist:
        return Response(
            {'error': 'Analyse non trouvée'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        import traceback
        print(f"❌ Erreur lors de la génération des recommandations: {str(e)}")
        print(traceback.format_exc())
        return Response(
            {'error': f'Erreur lors de la génération des recommandations: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_products(request):
    """Obtenir tous les produits"""
    try:
        products = Product.objects.filter(is_active=True)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': f'Erreur lors du chargement des produits: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_product(request, product_id):
    """Obtenir un produit spécifique"""
    try:
        product = Product.objects.get(id=product_id, is_active=True)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response(
            {'error': 'Produit non trouvé'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': f'Erreur lors du chargement du produit: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )












