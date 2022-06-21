from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer
from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.viewsets import ModelViewSet
from .models import Article,UserManager,User
from .serializers import ArticleSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

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
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)
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
def ArticleApi(request,id=0):
    if request.method=='GET':
        articles = Article.objects.all()
        articles_serializer = ArticleSerializer(articles,many=True)
        return Response(articles_serializer.data)
    elif request.method=='POST':
        article_data=JSONParser().parse(request)
        articles_serializer=ArticleSerializer(data=article_data)
        if articles_serializer.is_valid():
            articles_serializer.save()
            return Response("Added Successfully")
        return Response("Failed to Add")
    elif request.method=='PUT':
        article_data=JSONParser().parse(request)
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