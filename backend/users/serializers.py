from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, UserTestimonial


class UserRegistrationSerializer(serializers.Serializer):
    """Serializer pour l'inscription des utilisateurs - version complète"""
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    
    # Champs optionnels - tous les champs du frontend
    first_name = serializers.CharField(max_length=150, required=False, allow_blank=True, allow_null=True)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True, allow_null=True)
    age = serializers.IntegerField(required=False, allow_null=True)
    gender = serializers.ChoiceField(choices=[('M', 'Homme'), ('F', 'Femme'), ('O', 'Autre')], required=False, allow_null=True)
    location_country = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    location_region = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    skin_type = serializers.ChoiceField(
        choices=[('DRY', 'Sèche'), ('OILY', 'Grasse'), ('COMBINATION', 'Mixte'), ('NORMAL', 'Normale'), ('SENSITIVE', 'Sensible')],
        required=False, allow_null=True
    )
    
    # Champs médicaux
    diabetes = serializers.BooleanField(required=False, default=False)
    hypertension = serializers.BooleanField(required=False, default=False)
    blood_disorders = serializers.BooleanField(required=False, default=False)
    autoimmune_diseases = serializers.BooleanField(required=False, default=False)
    pregnancy = serializers.BooleanField(required=False, default=False)
    
    # Champs de style de vie
    sun_exposure = serializers.ChoiceField(
        choices=[('LOW', 'Faible'), ('MODERATE', 'Modérée'), ('HIGH', 'Élevée')],
        required=False, allow_null=True
    )
    sunscreen_usage = serializers.ChoiceField(
        choices=[('NEVER', 'Jamais'), ('SOMETIMES', 'Parfois'), ('DAILY', 'Quotidien')],
        required=False, allow_null=True
    )
    diet = serializers.ChoiceField(
        choices=[('BALANCED', 'Équilibrée'), ('HIGH_FAT_SUGAR', 'Riche en graisses/sucres'), ('VEGETARIAN', 'Végétarienne')],
        required=False, allow_null=True
    )
    hydration = serializers.ChoiceField(
        choices=[('LOW', 'Faible'), ('MODERATE', 'Modérée'), ('HIGH', 'Élevée')],
        required=False, allow_null=True
    )
    smoking = serializers.BooleanField(required=False, default=False)
    alcohol = serializers.BooleanField(required=False, default=False)
    sleep_hours = serializers.ChoiceField(
        choices=[('LOW', 'Faible'), ('MODERATE', 'Modérée'), ('HIGH', 'Élevée')],
        required=False, allow_null=True
    )
    
    # Champs familiaux et actuels
    family_dermatological_history = serializers.BooleanField(required=False, default=False)
    current_skin_problems = serializers.ListField(
        child=serializers.CharField(),
        required=False, allow_empty=True, default=list
    )
    current_treatments = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    current_cosmetics = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    known_allergies = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    skin_goals = serializers.ListField(
        child=serializers.CharField(),
        required=False, allow_empty=True, default=list
    )
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Ce nom d'utilisateur existe déjà.")
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Cette adresse email existe déjà.")
        return value
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        
        # Générer un username unique basé sur l'email
        email = validated_data['email']
        base_username = email.split('@')[0]  # Partie avant @
        username = base_username
        counter = 1
        
        # S'assurer que le username est unique
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        
        validated_data['username'] = username
        
        # Créer l'utilisateur avec tous les champs validés
        try:
            user = User.objects.create_user(**validated_data)
            return user
        except Exception as e:
            print(f"Erreur lors de la création de l'utilisateur: {str(e)}")
            raise e


class UserLoginSerializer(serializers.Serializer):
    """Serializer pour la connexion des utilisateurs"""
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        print(f"DEBUG LOGIN - Email: {email}")
        print(f"DEBUG LOGIN - Password: {password}")
        print(f"DEBUG LOGIN - Email type: {type(email)}")
        print(f"DEBUG LOGIN - Password type: {type(password)}")
        
        if email and password:
            print(f"DEBUG LOGIN - Tentative d'authentification pour: {email}")
            try:
                # Trouver l'utilisateur par email
                user = User.objects.get(email=email)
                print(f"DEBUG LOGIN - Utilisateur trouvé: {user.username}")
                
                # Authentifier avec le username trouvé
                authenticated_user = authenticate(username=user.username, password=password)
                print(f"DEBUG LOGIN - Résultat authenticate: {authenticated_user}")
                
                if not authenticated_user:
                    print("DEBUG LOGIN - Authentification échouée")
                    raise serializers.ValidationError('Email ou mot de passe incorrect.')
                if not authenticated_user.is_active:
                    print("DEBUG LOGIN - Compte désactivé")
                    raise serializers.ValidationError('Compte désactivé.')
                print(f"DEBUG LOGIN - Authentification réussie pour: {authenticated_user.username}")
                attrs['user'] = authenticated_user
            except User.DoesNotExist:
                print("DEBUG LOGIN - Utilisateur non trouvé avec cet email")
                raise serializers.ValidationError('Email ou mot de passe incorrect.')
        else:
            print("DEBUG LOGIN - Email ou password manquant")
            raise serializers.ValidationError('Email et mot de passe requis.')
        
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer pour le profil utilisateur"""
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'age', 'gender', 'location_country', 'location_region',
            'skin_type', 'diabetes', 'hypertension', 'blood_disorders',
            'autoimmune_diseases', 'pregnancy', 'sun_exposure',
            'sunscreen_usage', 'diet', 'hydration', 'smoking',
            'alcohol', 'sleep_hours', 'family_dermatological_history',
            'current_skin_problems', 'current_treatments',
            'current_cosmetics', 'known_allergies', 'skin_goals',
            'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer pour changer le mot de passe"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    new_password_confirm = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("Les nouveaux mots de passe ne correspondent pas.")
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Ancien mot de passe incorrect.")
        return value


class UserTestimonialSerializer(serializers.ModelSerializer):
    """Serializer pour les témoignages utilisateurs"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    user_first_name = serializers.CharField(source='user.first_name', read_only=True)
    user_last_name = serializers.CharField(source='user.last_name', read_only=True)
    
    class Meta:
        model = UserTestimonial
        fields = [
            'id', 'user', 'user_username', 'user_first_name', 'user_last_name',
            'rating', 'comment', 'is_public', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']




