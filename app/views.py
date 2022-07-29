from rest_framework.decorators import api_view, renderer_classes
from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from django.contrib.auth import login
from rest_framework import permissions
from .models import Article,User
from .serializers import ArticleSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.decorators import parser_classes
from rest_framework.decorators import authentication_classes, permission_classes

# User APIs

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(request)
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })
# Login API
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token = AuthToken.objects.create(user)[1]
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token,
        })
# Delete API
class DeleteAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


    def delete(self, request, *args, **kwargs):
        user=self.request.user
        user.delete()

        return Response({"result":"user delete"})

# Articles APIs
@api_view(('GET','POST','PUT','DELETE',))
@csrf_exempt
@parser_classes([JSONParser])
def ArticleApi(request,id=0):
    if request.method=='GET':
        articles = Article.objects.all()
        articles_serializer = ArticleSerializer(articles,many=True)
        return Response(articles_serializer.data)
    elif request.method=='POST':
        article_data=request.data
        articles_serializer=ArticleSerializer(data=article_data)
        if articles_serializer.is_valid(raise_exception=True):
            articles_serializer.save()
            return Response("Added Successfully")
        return Response("Failed to Add")
    elif request.method=='PUT':
        article_data=request.data
        article=Article.objects.get(A_Id=article_data['A_Id'])
        articles_serializer=ArticleSerializer(article,data=article_data)
        if articles_serializer.is_valid():
            articles_serializer.save()
            return Response("Updated Successfully")
        return Response("Failed to Update")
    elif request.method=='DELETE':
        article=Article.objects.get(A_Id=id)
        article.delete()
        return Response("Deleted Successfully")                           

# All Users Api
@api_view(('GET','PUT',))
@authentication_classes([])
@permission_classes([])
def UsersApi(request,):
    if request.method=='GET' :
       users = User.objects.all()
       users_serializer = UserSerializer(users,many=True)
       return Response(users_serializer.data) 
    elif request.method=='PUT':
        user_data=request.data
        user=User.objects.get(U_Id=user_data['U_Id'])
        user_serializer=UserSerializer(user,data=user_data)
        if user_serializer.is_valid(raise_exception=True):
            user_serializer.save()
            return Response("Updated Successfully")
        return Response("Failed to Update")   

# User By ID
@api_view(('GET',))
@authentication_classes([])
@permission_classes([])
def UserById(request,id=0):
    if request.method=='GET':
        user = User.objects.get(U_Id=id)
        user_serializer=UserSerializer(user)
        return Response(user_serializer.data)

# User into auteur
@api_view(('PUT',))
def UserToAuteur(request,id=0):
    if request.method=='PUT':
        user = User.objects.get(U_Id=id)
        setattr(user,'is_superuser',True)
        user.save()
        user_serializer=UserSerializer(user)
        return Response(user_serializer.data)

# Article By ID
@api_view(('GET',))
@authentication_classes([])
@permission_classes([])
def ArticleById(request,id=0):
    if request.method=='GET':
        article = Article.objects.get(A_Id=id)
        article_serializer=ArticleSerializer(article)
        return Response(article_serializer.data)

# Add Sauvegarde 
@api_view(('PUT',))
def AddSauvegarde(request,id_a=0,id_u=0):
    if request.method=='PUT':
        article=Article.objects.get(A_Id=id_a)
        article.sauvegarde.add(id_u)
        article.save()
        article_serializer=ArticleSerializer(article)
        return Response(article_serializer.data)

# Remove Sauvegarde
@api_view(('PUT',))
def RemoveSauvegarde(request,id_a=0,id_u=0):
    if request.method=='PUT':
        article=Article.objects.get(A_Id=id_a)
        article.sauvegarde.remove(id_u)
        article.save()
        article_serializer=ArticleSerializer(article)
        return Response(article_serializer.data)

# Add Recommendation 
@api_view(('PUT',))
def AddRecommendation(request,id_a=0,id_u=0):
    if request.method=='PUT':
        article=Article.objects.get(A_Id=id_a)
        article.recommendationlist.add(id_u)
        article.recommendation=article.recommendation+1
        article.save()
        article_serializer=ArticleSerializer(article)
        return Response(article_serializer.data)

# Remove Recommendation
@api_view(('PUT',))
def RemoveRecommendation(request,id_a=0,id_u=0):
    if request.method=='PUT':
        article=Article.objects.get(A_Id=id_a)
        article.recommendationlist.remove(id_u)
        article.recommendation=article.recommendation-1
        article.save()
        article_serializer=ArticleSerializer(article)
        return Response(article_serializer.data)

# Update Article By Id 
@api_view(('PATCH',))
def UpdateArticle(request,id_a=0):
    if request.method=='PATCH':
        article_data=request.data
        article=Article.objects.get(A_Id=id_a)
        article_serializer=ArticleSerializer(article,data=article_data,partial=True)
        if article_serializer.is_valid():
            article_serializer.save()
            return Response(article_serializer.data)
        return Response("Failed to Add")

# Update User By Id 
@api_view(('PATCH',))
def UpdateUser(request,id_u=0):
    if request.method=='PATCH':
        user_data=request.data
        user=User.objects.get(U_Id=id_u)
        user_serializer=UserSerializer(user,data=user_data,partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data)
        return Response("Failed to Add")     