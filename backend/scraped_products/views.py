from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Count, Q
from django.utils import timezone
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
    
    saved_products = []
    skipped_products = []
    
    for product_data in products_data:
        try:
            # Vérifier si le produit existe déjà
            existing_product = ScrapedProduct.objects.filter(
                name=product_data.get('name'),
                brand=product_data.get('brand'),
                source_site=product_data.get('source_site')
            ).first()
            
            if existing_product:
                skipped_products.append(product_data)
                continue
            
            # Créer le produit
            product = ScrapedProduct.objects.create(**product_data)
            saved_products.append(product)
            
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du produit: {e}")
            skipped_products.append(product_data)
    
    # Mettre à jour la session si fournie
    if session_id:
        try:
            session = ScrapingSession.objects.get(id=session_id)
            session.total_products_found += len(products_data)
            session.total_products_saved += len(saved_products)
            session.total_products_skipped += len(skipped_products)
            session.save()
            
            # Créer des logs
            ScrapingLog.objects.create(
                session=session,
                log_type='SUCCESS',
                message=f'{len(saved_products)} produits sauvegardés'
            )
            
            if skipped_products:
                ScrapingLog.objects.create(
                    session=session,
                    log_type='WARNING',
                    message=f'{len(skipped_products)} produits ignorés (doublons)'
                )
                
        except ScrapingSession.DoesNotExist:
            pass
    
    return Response({
        'saved_products': len(saved_products),
        'skipped_products': len(skipped_products),
        'total_processed': len(products_data)
    })


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




