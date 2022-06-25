from django.urls import re_path
from django.conf import settings
from xml.etree.ElementInclude import include
from rest_framework.routers import DefaultRouter
from django.urls import path,include
from knox import views as knox_views
from .views import RegisterAPI
from .views import LoginAPI
from .views import DeleteAPI
from .views import ArticleApi



urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('api/delete/', DeleteAPI.as_view(), name='delete'),
    path('api/article/', ArticleApi.as_view(), name='article'),
    path('api/article/([0-9]+)', ArticleApi.as_view(), name='deletearticle'),
#    re_path(r'^article$',views.ArticleApi),
#    re_path(r'^article/([0-9]+)$',views.ArticleApi),
]