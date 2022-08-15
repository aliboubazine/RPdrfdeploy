from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from recommendationplatform import settings
from .models import Article,User,SiteUrl
from django.contrib.auth import authenticate
from app import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}          
    email = serializers.EmailField(required=settings.ACCOUNT_EMAIL_REQUIRED)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    def save(self,request):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            etablissement=self.validated_data['etablissement'],
            fonction=self.validated_data['fonction'],
            adresse=self.validated_data['adresse'],
            bio=self.validated_data['bio'],
            last_login=self.validated_data['last_login'],
            tags=self.validated_data['tags']
        )
        password1=self.validated_data['password1']
        password2=self.validated_data['password2']

        if password1 != password2:
            raise serializers.ValidationError({'password':'password must match.'})
        
        user.set_password(password1)
        user.save()
        return user

# LogIn Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=settings.ACCOUNT_EMAIL_REQUIRED)
    password = serializers.CharField()

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError('Incorrect Credentials')

        user = authenticate(username=user.username, password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Incorrect Credentials Passed.')

# Auteur Field
class AuteurField(serializers.StringRelatedField):

    def to_internal_value(self, value):
        auteur = models.User.objects.filter(username=value)
        return auteur.get().U_Id

# Site Url Serializer
class SiteUrlSerializer(serializers.ModelSerializer):
    class Meta :
        model = SiteUrl
        fields = ('S_Id','name','url','owner')

# Article Serializer
class ArticleSerializer(serializers.ModelSerializer):
    auteur = AuteurField(many=True)
    sauvegarde = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    recommendationlist = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    class Meta :
        model = Article
        fields = ('A_Id','title','resume','fichier','urlfichier','tags','recommendation','date_posted','auteur','sauvegarde','recommendationlist')

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    articlelist = ArticleSerializer(many=True, read_only=True)
    sauvegardelist = ArticleSerializer(many=True, read_only=True)
    recommendationlist = ArticleSerializer(many=True, read_only=True)
    suivislist = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    Siteslist = SiteUrlSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('U_Id','username','email','password','first_name','last_name','etablissement','fonction','adresse','bio','tags','suivisnb','last_login','is_superuser','articlelist','sauvegardelist','recommendationlist','suivislist','Siteslist')
        read_only_fields = ('email', ) 