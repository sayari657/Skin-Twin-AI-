from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_products, name='get_products'),
    path('<int:product_id>/', views.get_product, name='get_product'),
]












