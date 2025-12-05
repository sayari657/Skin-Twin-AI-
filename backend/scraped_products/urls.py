from django.urls import path
from . import views

urlpatterns = [
    # Produits scrapés
    path('products/', views.ScrapedProductListCreateView.as_view(), name='scraped-products-list'),
    path('products/<int:pk>/', views.ScrapedProductDetailView.as_view(), name='scraped-product-detail'),
    path('products/search/', views.search_products, name='search-products'),
    
    # Sessions de scraping
    path('sessions/', views.ScrapingSessionListCreateView.as_view(), name='scraping-sessions-list'),
    path('sessions/<int:pk>/', views.ScrapingSessionDetailView.as_view(), name='scraping-session-detail'),
    
    # Actions de scraping
    path('start-session/', views.start_scraping_session, name='start-scraping-session'),
    path('save-products/', views.save_scraped_products, name='save-scraped-products'),
    path('scrape-web/', views.scrape_web_products, name='scrape-web-products'),
    
    # Statistiques
    path('stats/', views.scraping_stats, name='scraping-stats'),
]


