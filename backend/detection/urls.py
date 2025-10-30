from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.SkinAnalysisUploadView.as_view(), name='skin_analysis_upload'),
    path('analysis/<int:analysis_id>/', views.get_analysis, name='get_analysis'),
    path('analyses/', views.get_user_analyses, name='get_user_analyses'),
    path('analyses-simple/', views.get_user_analyses_simple, name='get_user_analyses_simple'),
    path('analysis/<int:analysis_id>/delete/', views.delete_analysis, name='delete_analysis'),
]




