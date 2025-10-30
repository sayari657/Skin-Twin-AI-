from django.urls import path
from . import views

urlpatterns = [
    path('test-register/', views.test_register, name='test_register'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('token/refresh/', views.refresh_token, name='refresh_token'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile-simple/', views.profile_simple, name='profile_simple'),
    path('test-auth/', views.test_auth, name='test_auth'),
    path('test-no-auth/', views.test_no_auth, name='test_no_auth'),
    path('test-jwt-manual/', views.test_jwt_manual, name='test_jwt_manual'),
    path('change-password/', views.change_password, name='change_password'),
    path('delete-account/', views.delete_account, name='delete_account'),
    
    # Endpoints pour les témoignages
    path('testimonials/', views.create_testimonial, name='create_testimonial'),
    path('testimonials/public/', views.get_public_testimonials, name='get_public_testimonials'),
    path('testimonials/user/', views.get_user_testimonials, name='get_user_testimonials'),
    path('testimonials/<int:testimonial_id>/', views.update_testimonial, name='update_testimonial'),
]




