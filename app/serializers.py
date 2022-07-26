from dataclasses import fields
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from recommendationplatform import settings
from allauth.account.utils import setup_user_email
from allauth.account.adapter import get_adapter
from django.contrib.auth import get_user_model
from .models import Article,User
from django.contrib.auth import authenticate

from app import models

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

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(
                ("The two password fields didn't match."))
        return data

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'user_type': self.validated_data.get('user_type', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'etablissement': self.validated_data.get('etablissement', ''),
            'fonction': self.validated_data.get('fonction', ''),
            'adresse': self.validated_data.get('adresse', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user

        user.save()
        return user

# LogIn Serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Incorrect Credentials Passed.')

#AuteurField
class AuteurField(serializers.StringRelatedField):

    def to_internal_value(self, value):
        auteur = models.User.objects.filter(username=value)
        return auteur.get().U_Id

# Article Serializer
class ArticleSerializer(serializers.ModelSerializer):
    auteur = AuteurField(many=True)
    sauvegarde = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    recommendationlist = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    class Meta :
        model = Article
        fields = ('A_Id','title','resume','recommendation','date_posted','auteur','sauvegarde','recommendationlist')

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    articlelist = ArticleSerializer(many=True, read_only=True)
    sauvegardelist = ArticleSerializer(many=True, read_only=True)
    recommendationlist = ArticleSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('U_Id','username','email','password','first_name','last_name','etablissement','fonction','adresse','is_superuser','last_login','groups','user_permissions','articlelist','sauvegardelist','recommendationlist')
        read_only_fields = ('email', )        
