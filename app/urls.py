from django.urls import re_path
from django.conf import settings
from xml.etree.ElementInclude import include
from rest_framework.routers import DefaultRouter
from django.urls import path,include
from knox import views as knox_views
from .views import RegisterAPI
from .views import LoginAPI
from .views import DeleteAPI
from app import views
from rest_framework import routers


urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('api/users/',views.UsersApi,name='userlist'),
    path('api/article/',views.ArticleApi,name='articleslist'),
    re_path(r'^article/([0-9]+)$',views.ArticleById,name='articledetail'),
    re_path(r'^article/delete/([0-9]+)$',views.ArticleApi),
    re_path(r'^user/([0-9]+)$',views.UserById,name='userdetail'),
    re_path(r'^user/auteur/([0-9]+)$',views.UserToAuteur,name='usertoauteur')
]