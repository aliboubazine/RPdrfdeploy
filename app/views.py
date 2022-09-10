from rest_framework.decorators import api_view,parser_classes,authentication_classes,permission_classes
from rest_framework import generics, permissions,status
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer,ArticleSerializer,SiteUrlSerializer,ChangePasswordSerializer,CommentSerializer,ChangeEmailSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Article,User,SiteUrl,Comment
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser,MultiPartParser,FormParser
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

# User APIs

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(request)
        token = AuthToken.objects.create(user)[1]
        current_site = get_current_site(request).domain
        relativeLink = reverse('EmailVerify')
        absurl = 'http://'+current_site+relativeLink+"?token="+token
        email_body = 'Salut '+user.username+'!, veuillez cliquer sur le lien pour activer votre compte \n'+absurl
        data = {'email_body': email_body,'to_email': user.email,'email_subject': 'Activation du compte'}
        Util.send_email(data)
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": token
        })

# Verify Email API
class VerifyEmail(generics.GenericAPIView):
    def get(self):
        pass

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

# Change Password API
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = []

    def get_object(self,id,queryset=None):
        obj = User.objects.get(U_Id=id)
        return obj

    def update(self, request,id, *args, **kwargs):
        self.object = self.get_object(id)
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            email_body = 'Salut '+self.object.username+'!, votre mot de passe a été changé avec succès \n'
            data = {'email_body': email_body,'to_email': self.object.email,'email_subject': 'Changement de mot de passe'}
            Util.send_email(data)
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Change Email API
class ChangeEmailView(generics.UpdateAPIView):
    serializer_class = ChangeEmailSerializer
    model = User
    permission_classes = []

    def get_object(self,id,queryset=None):
        obj = User.objects.get(U_Id=id)
        return obj

    def update(self, request,id, *args, **kwargs):
        self.object = self.get_object(id)
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("password")):
                return Response({"password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.email = serializer.data.get("new_email")
            self.object.save()
            email_body = 'Salut '+self.object.username+'!, ceci est votre nouvelle adresse email pour votre compte \n'
            data = {'email_body': email_body,'to_email': self.object.email,'email_subject': 'Changement Email'}
            Util.send_email(data)
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'email updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
@parser_classes([JSONParser,MultiPartParser,FormParser])
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

# User Into Auteur
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
@api_view(('PATCH',))
def AddSauvegarde(request,id_a=0,id_u=0):
    if request.method=='PATCH':
        article=Article.objects.get(A_Id=id_a)
        article.sauvegarde.add(id_u)
        article.save()
        article_serializer=ArticleSerializer(article)
        return Response(article_serializer.data)

# Remove Sauvegarde
@api_view(('PATCH',))
def RemoveSauvegarde(request,id_a=0,id_u=0):
    if request.method=='PATCH':
        article=Article.objects.get(A_Id=id_a)
        article.sauvegarde.remove(id_u)
        article.save()
        article_serializer=ArticleSerializer(article)
        return Response(article_serializer.data)

# Add Recommendation 
@api_view(('PATCH',))
def AddRecommendation(request,id_a=0,id_u=0):
    if request.method=='PATCH':
        article=Article.objects.get(A_Id=id_a)
        article.recommendationlist.add(id_u)
        article.recommendation=article.recommendation+1
        article.save()
        article_serializer=ArticleSerializer(article)
        return Response(article_serializer.data)

# Remove Recommendation
@api_view(('PATCH',))
def RemoveRecommendation(request,id_a=0,id_u=0):
    if request.method=='PATCH':
        article=Article.objects.get(A_Id=id_a)
        article.recommendationlist.remove(id_u)
        article.recommendation=article.recommendation-1
        article.save()
        article_serializer=ArticleSerializer(article)
        return Response(article_serializer.data)

# Add NbVus 
@api_view(('PATCH',))
def AddNbVus(request,id_a=0):
    if request.method=='PATCH':
        article=Article.objects.get(A_Id=id_a)
        article.nbvus=article.nbvus+1
        article.save()
        article_serializer=ArticleSerializer(article)
        return Response(article_serializer.data)

# Add NbPosts 
@api_view(('PATCH',))
def AddNbPosts(request,id_u=0):
    if request.method=='PATCH':
        user=User.objects.get(U_Id=id_u)
        user.nbposts=user.nbposts+1
        user.save()
        user_serializer=UserSerializer(user)
        return Response(user_serializer.data)

# Sub NbPosts 
@api_view(('PATCH',))
def SubNbPosts(request,id_u=0):
    if request.method=='PATCH':
        user=User.objects.get(U_Id=id_u)
        user.nbposts=user.nbposts-1
        user.save()
        user_serializer=UserSerializer(user)
        return Response(user_serializer.data)                        

# Update Article By Id 
@api_view(('PATCH',))
@parser_classes([JSONParser,MultiPartParser,FormParser])
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

# Add Suivis
@api_view(('PUT',))
def AddSuivis(request,id_u=0,id_s=0):
    if request.method=='PUT':
        user=User.objects.get(U_Id=id_u)
        user2=User.objects.get(U_Id=id_s)
        user.suivislist.add(user2)
        user.suivisnb=user.suivisnb+1
        user.save()
        user_serializer=UserSerializer(user)
        return Response(user_serializer.data)

# Remove Suivis
@api_view(('PUT',))
def RemoveSuivis(request,id_u=0,id_s=0):
    if request.method=='PUT':
        user=User.objects.get(U_Id=id_u)
        user2=User.objects.get(U_Id=id_s)
        user.suivislist.remove(user2)
        user.suivisnb=user.suivisnb-1
        user.save()
        user_serializer=UserSerializer(user)
        return Response(user_serializer.data)   

# Site Url APIs
@api_view(('GET','POST','PUT','DELETE',))
def SiteUrlApi(request,id=0):
    if request.method=='GET':
        siteurls = SiteUrl.objects.all()
        siteurls_serializer = SiteUrlSerializer(siteurls,many=True)
        return Response(siteurls_serializer.data)
    elif request.method=='POST':
        siteurl_data=request.data
        siteurl_serializer=SiteUrlSerializer(data=siteurl_data)
        if siteurl_serializer.is_valid(raise_exception=True):
            siteurl_serializer.save()
            return Response("Added Successfully")
        return Response("Failed to Add")
    elif request.method=='PUT':
        siteurl_data=request.data
        siteurl=SiteUrl.objects.get(S_Id=siteurl_data['S_Id'])
        siteurl_serializer=SiteUrlSerializer(siteurl,data=siteurl_data)
        if siteurl_serializer.is_valid():
            siteurl_serializer.save()
            return Response("Updated Successfully")
        return Response("Failed to Update")
    elif request.method=='DELETE':
        siteurl=SiteUrl.objects.get(S_Id=id)
        siteurl.delete()
        return Response("Deleted Successfully")

# Comment APIs
@api_view(('GET','POST','PUT','DELETE',))
def CommentApi(request,id=0):
    if request.method=='GET':
        Comments = Comment.objects.all()
        comments_serializer = CommentSerializer(Comments,many=True)
        return Response(comments_serializer.data)
    elif request.method=='POST':
        comment_data=request.data
        comment_serializer=CommentSerializer(data=comment_data)
        if comment_serializer.is_valid(raise_exception=True):
            comment_serializer.save()
            return Response("Added Successfully")
        return Response("Failed to Add")
    elif request.method=='PUT':
        comment_data=request.data
        comment=Comment.objects.get(C_Id=comment_data['C_Id'])
        comment_serializer=CommentSerializer(comment,data=comment_data)
        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response("Updated Successfully")
        return Response("Failed to Update")
    elif request.method=='DELETE':
        comment=Comment.objects.get(C_Id=id)
        comment.delete()
        return Response("Deleted Successfully")                     