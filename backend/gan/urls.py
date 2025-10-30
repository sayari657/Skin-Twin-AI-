from django.urls import path
from . import views

urlpatterns = [
    path('simulate/', views.create_simulation, name='create_simulation'),
    path('simulation/<int:simulation_id>/', views.get_simulation, name='get_simulation'),
    path('simulations/', views.get_user_simulations, name='get_user_simulations'),
]




