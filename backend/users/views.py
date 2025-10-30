from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, UserTestimonial
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, 
    UserProfileSerializer, ChangePasswordSerializer, UserTestimonialSerializer
)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def test_register(request):
    """Endpoint de test pour diagnostiquer les problèmes d'inscription"""
    print("=" * 50)
    print("TEST ENDPOINT - DIAGNOSTIC")
    print(f"Données reçues: {request.data}")
    print(f"Type: {type(request.data)}")
    print(f"Clés: {list(request.data.keys()) if hasattr(request.data, 'keys') else 'N/A'}")
    print(f"Content-Type: {request.content_type}")
    print("=" * 50)
    
    return Response({
        'message': 'Test endpoint fonctionne',
        'received_data': request.data,
        'data_type': str(type(request.data)),
        'keys': list(request.data.keys()) if hasattr(request.data, 'keys') else 'N/A'
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    """Inscription d'un nouvel utilisateur"""
    print("=" * 50)
    print("NOUVELLE REQUÊTE D'INSCRIPTION")
    print(f"Données reçues: {request.data}")
    print(f"Type de données: {type(request.data)}")
    print(f"Clés reçues: {list(request.data.keys()) if hasattr(request.data, 'keys') else 'N/A'}")
    print(f"Content-Type: {request.content_type}")
    print("=" * 50)
    
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        try:
            print("Serializer valide, création de l'utilisateur...")
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            print(f"Utilisateur créé avec succès: {user.username}")
            return Response({
                'user': UserProfileSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(f"ERREUR lors de la création de l'utilisateur: {str(e)}")
            print(f"Type d'erreur: {type(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    print(f"ERREURS DE VALIDATION: {serializer.errors}")
    print(f"Données non valides: {serializer.data}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    """Connexion d'un utilisateur"""
    print("=" * 50)
    print("NOUVELLE REQUÊTE DE CONNEXION")
    print(f"Données reçues: {request.data}")
    print(f"Username: {request.data.get('username')}")
    print(f"Password: {request.data.get('password')}")
    print("=" * 50)
    
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    
    if (not username and not email) or not password:
        return Response({'error': 'Identifiant (email ou username) et mot de passe requis'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Si username ressemble à un email, ou si email fourni → retrouver l'utilisateur par email
        if (username and '@' in username) or email:
            lookup_email = username if (username and '@' in username) else email
            try:
                user_obj = User.objects.get(email=lookup_email)
                username = user_obj.username
            except User.DoesNotExist:
                return Response({'error': 'Utilisateur non trouvé avec cet email'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.get(username=username)
        print(f"Utilisateur trouvé: {user.username}")
        print(f"Utilisateur actif: {user.is_active}")
        
        if user.check_password(password):
            print("Mot de passe correct")
            if user.is_active:
                print("Utilisateur actif, génération des tokens...")
                refresh = RefreshToken.for_user(user)
                print("Tokens générés avec succès")
                
                try:
                    user_data = UserProfileSerializer(user).data
                    print("Utilisateur sérialisé avec succès")
                except Exception as serializer_error:
                    print(f"Erreur de sérialisation: {serializer_error}")
                    user_data = {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                    }
                
                return Response({
                    'user': user_data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Compte désactivé'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            print("Mot de passe incorrect")
            return Response({'error': 'Mot de passe incorrect'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        print("Utilisateur non trouvé")
        return Response({'error': 'Utilisateur non trouvé'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(f"Erreur générale: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return Response({'error': f'Erreur: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout(request):
    """Déconnexion d'un utilisateur"""
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Vue pour consulter et modifier le profil utilisateur"""
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.AllowAny]  # Temporaire : permettre l'accès sans authentification
    
    def get_object(self):
        # Solution temporaire : récupérer l'utilisateur par ID depuis les paramètres
        user_id = self.request.GET.get('user_id')
        if user_id:
            try:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                return User.objects.get(id=user_id)
            except User.DoesNotExist:
                from django.http import Http404
                raise Http404("Utilisateur non trouvé")
        return self.request.user


@api_view(['GET'])
@permission_classes([permissions.AllowAny])  # Public pour permettre l'accès sans authentification
def profile_simple(request):
    """Endpoint de profil simple sans authentification JWT"""
    # Récupérer l'utilisateur par ID depuis les paramètres de requête
    user_id = request.GET.get('user_id') or request.query_params.get('user_id')
    print(f"DEBUG profile_simple - user_id reçu: {user_id}")
    print(f"DEBUG profile_simple - type: {type(user_id)}")
    
    if not user_id:
        return Response({'error': 'user_id requis'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Convertir en entier si nécessaire
        user_id_int = int(user_id)
        print(f"DEBUG profile_simple - user_id_int: {user_id_int}")
        
        # Vérifier si l'utilisateur existe
        user_exists = User.objects.filter(id=user_id_int).exists()
        print(f"DEBUG profile_simple - utilisateur existe: {user_exists}")
        
        if user_exists:
            user = User.objects.get(id=user_id_int)
            print(f"DEBUG profile_simple - utilisateur trouvé: {user.username}")
            return Response(UserProfileSerializer(user).data, status=status.HTTP_200_OK)
        else:
            # Retourner un profil minimal vide plutôt qu'une 404 pour ne pas casser l'UI
            print(f"DEBUG profile_simple - utilisateur avec ID {user_id_int} n'existe pas")
            empty_profile = {
                'id': user_id_int,
                'username': '',
                'email': '',
                'first_name': '',
                'last_name': '',
                'age': None,
                'gender': None,
                'location_country': '',
                'location_region': '',
                'skin_type': None,
                'diabetes': False,
                'hypertension': False,
                'blood_disorders': False,
                'autoimmune_diseases': False,
                'pregnancy': False,
                'sun_exposure': None,
                'sunscreen_usage': None,
                'diet': None,
                'hydration': None,
                'smoking': False,
                'alcohol': False,
                'sleep_hours': None,
                'family_dermatological_history': False,
                'current_skin_problems': [],
                'current_treatments': '',
                'current_cosmetics': '',
                'known_allergies': '',
                'skin_goals': [],
                'date_joined': None,
                'last_login': None,
            }
            return Response(empty_profile, status=status.HTTP_200_OK)
            
    except ValueError:
        print(f"DEBUG profile_simple - user_id invalide: {user_id}")
        return Response({'error': 'user_id invalide'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(f"DEBUG profile_simple - erreur: {e}")
        return Response({'error': f'Erreur serveur: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def test_auth(request):
    """Endpoint de test pour vérifier l'authentification JWT"""
    print(f"Test auth - Utilisateur authentifié: {request.user}")
    print(f"Test auth - Type d'utilisateur: {type(request.user)}")
    print(f"Test auth - ID utilisateur: {request.user.id}")
    
    return Response({
        'message': 'Authentification JWT fonctionne',
        'user_id': request.user.id,
        'username': request.user.username,
        'email': request.user.email
    })

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def test_no_auth(request):
    """Endpoint de test sans authentification"""
    return Response({'message': 'Endpoint sans authentification fonctionne'})

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def test_jwt_manual(request):
    """Test manuel de l'authentification JWT"""
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    print(f"Header Authorization: {auth_header}")
    
    if auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        print(f"Token extrait: {token[:20]}...")
        
        try:
            from rest_framework_simplejwt.tokens import AccessToken
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            print(f"User ID du token: {user_id}")
            
            from django.contrib.auth import get_user_model
            User = get_user_model()
            user = User.objects.get(id=user_id)
            
            return Response({
                'message': 'Token JWT valide',
                'user_id': user_id,
                'username': user.username,
                'email': user.email
            })
        except Exception as e:
            print(f"Erreur lors de la validation du token: {e}")
            return Response({'error': f'Token invalide: {str(e)}'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'Pas de token Bearer fourni'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_password(request):
    """Changer le mot de passe"""
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'message': 'Mot de passe modifié avec succès'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_account(request):
    """Supprimer le compte utilisateur"""
    user = request.user
    user.delete()
    return Response({'message': 'Compte supprimé avec succès'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def test_auth(request):
    """Test d'authentification simple"""
    print(f"DEBUG TEST AUTH - User: {request.user}")
    print(f"DEBUG TEST AUTH - Is authenticated: {request.user.is_authenticated}")
    print(f"DEBUG TEST AUTH - Headers: {dict(request.headers)}")
    return Response({
        'message': 'Authentification réussie',
        'user_id': request.user.id,
        'username': request.user.username,
        'is_authenticated': request.user.is_authenticated
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def test_no_auth(request):
    """Test sans authentification"""
    return Response({
        'message': 'Endpoint accessible sans authentification',
        'method': request.method,
        'headers': dict(request.headers)
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def refresh_token(request):
    """Rafraîchir le token d'accès"""
    refresh_token = request.data.get('refresh')
    if not refresh_token:
        return Response({'error': 'Token de rafraîchissement requis'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        from rest_framework_simplejwt.tokens import RefreshToken
        token = RefreshToken(refresh_token)
        return Response({
            'access': str(token.access_token),
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': 'Token de rafraîchissement invalide'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def test_jwt_manual(request):
    """Test manuel de l'authentification JWT"""
    auth_header = request.headers.get('Authorization', '')
    print(f"DEBUG JWT MANUAL - Auth header: {auth_header}")
    
    if not auth_header.startswith('Bearer '):
        return Response({'error': 'Token Bearer manquant'}, status=status.HTTP_401_UNAUTHORIZED)
    
    token = auth_header.split(' ')[1]
    print(f"DEBUG JWT MANUAL - Token: {token}")
    
    try:
        from rest_framework_simplejwt.tokens import AccessToken
        access_token = AccessToken(token)
        user_id = access_token['user_id']
        print(f"DEBUG JWT MANUAL - User ID from token: {user_id}")
        
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.get(id=user_id)
        
        return Response({
            'message': 'Token JWT valide',
            'user_id': user.id,
            'username': user.username,
            'token_payload': {
                'user_id': access_token['user_id'],
                'exp': access_token['exp'],
                'iat': access_token['iat']
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"DEBUG JWT MANUAL - Error: {str(e)}")
        return Response({'error': f'Token JWT invalide: {str(e)}'}, status=status.HTTP_401_UNAUTHORIZED)


# ===== ENDPOINTS POUR LES TÉMOIGNAGES UTILISATEURS =====

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_testimonial(request):
    """Créer un nouveau témoignage utilisateur"""
    try:
        serializer = UserTestimonialSerializer(data=request.data)
        if serializer.is_valid():
            # Assigner l'utilisateur manuellement
            testimonial = serializer.save(user=request.user)
            return Response({
                'message': 'Témoignage créé avec succès',
                'testimonial': UserTestimonialSerializer(testimonial).data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_public_testimonials(request):
    """Récupérer les témoignages publics pour la page d'accueil"""
    try:
        testimonials = UserTestimonial.objects.filter(is_public=True).order_by('-created_at')[:10]
        serializer = UserTestimonialSerializer(testimonials, many=True)
        return Response({
            'testimonials': serializer.data,
            'count': testimonials.count()
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_testimonials(request):
    """Récupérer les témoignages de l'utilisateur connecté"""
    try:
        testimonials = UserTestimonial.objects.filter(user=request.user).order_by('-created_at')
        serializer = UserTestimonialSerializer(testimonials, many=True)
        return Response({
            'testimonials': serializer.data,
            'count': testimonials.count()
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def update_testimonial(request, testimonial_id):
    """Modifier ou supprimer un témoignage"""
    try:
        testimonial = UserTestimonial.objects.get(id=testimonial_id, user=request.user)
        
        if request.method == 'PUT':
            serializer = UserTestimonialSerializer(testimonial, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message': 'Témoignage modifié avec succès',
                    'testimonial': serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            testimonial.delete()
            return Response({'message': 'Témoignage supprimé avec succès'}, status=status.HTTP_204_NO_CONTENT)
            
    except UserTestimonial.DoesNotExist:
        return Response({'error': 'Témoignage non trouvé'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

