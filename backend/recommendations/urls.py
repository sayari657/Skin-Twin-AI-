from django.urls import path
from . import views

urlpatterns = [
    path('analysis/<int:analysis_id>/', views.get_recommendations, name='get_recommendations'),
    path('products/', views.get_products, name='get_products'),
    path('products/<int:product_id>/', views.get_product, name='get_product'),
]












