from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chat_with_ai, name='chat_with_ai'),
    path('sessions/', views.get_chat_sessions, name='get_chat_sessions'),
    path('sessions/new/', views.create_new_session, name='create_new_session'),
    path('sessions/<str:session_id>/', views.get_chat_session, name='get_chat_session'),
    path('sessions/<str:session_id>/delete/', views.delete_chat_session, name='delete_chat_session'),
    path('suggestions/', views.get_ai_suggestions, name='get_ai_suggestions'),
]


