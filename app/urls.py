from django.urls import re_path,path
from django.conf import settings
from knox import views as knox_views
from .views import RegisterAPI,LoginAPI,DeleteAPI,ChangePasswordView,VerifyEmail
from app import views

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(),name='Register'),
    path('api/login/', LoginAPI.as_view(),name='LogIn'),
    path('api/logout/', knox_views.LogoutView.as_view(),name='LogOut'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(),name='LogOutAll'),
    path('emailverify/', VerifyEmail.as_view(), name="EmailVerify"),
    path('api/changepassword/', ChangePasswordView.as_view(), name='ChangePassword'),
    path('api/users/',views.UsersApi,name='UsersList'),
    path('api/articles/',views.ArticleApi,name='ArticlesList'),
    path('api/sitesurls/',views.SiteUrlApi,name='SitesUrlsList'),
    path('api/user/delete/', DeleteAPI.as_view(),name='DeleteUser'),
    re_path(r'^api/article/([0-9]+)$',views.ArticleById,name='ArticleDetails'),
    re_path(r'^api/article/delete/([0-9]+)$',views.ArticleApi,name='DeleteArticle'),
    re_path(r'^api/sitesurl/delete/([0-9]+)$',views.SiteUrlApi,name='DeleteSitesUrl'),
    re_path(r'^api/user/([0-9]+)$',views.UserById,name='UserDetails'),
    re_path(r'^api/user/auteur/([0-9]+)$',views.UserToAuteur,name='UserToAuteur'),
    re_path(r'^api/user/sauvegarde/([0-9]+)/([0-9]+)$',views.AddSauvegarde,name='UserAddSauvegarde'),
    re_path(r'^api/user/sauvegarde/delete/([0-9]+)/([0-9]+)$',views.RemoveSauvegarde,name='UserDeleteSauvegarde'),
    re_path(r'^api/user/recommende/([0-9]+)/([0-9]+)$',views.AddRecommendation,name='UserAddRecommendation'),
    re_path(r'^api/user/recommende/delete/([0-9]+)/([0-9]+)$',views.RemoveRecommendation,name='UserDeleteRecommendation'),
    re_path(r'^api/article/vu/([0-9]+)$',views.AddNbVus,name='AddNbVus'),
    re_path(r'^api/user/post/([0-9]+)$',views.AddNbPosts,name='AddNbPosts'),
    re_path(r'^api/user/subpost/([0-9]+)$',views.SubNbPosts,name='SubNbPosts'),
    re_path(r'^api/article/update/([0-9]+)$',views.UpdateArticle,name='UpdateArticle'),
    re_path(r'^api/user/update/([0-9]+)$',views.UpdateUser,name='UpdateUser'),
    re_path(r'^api/user/suivis/([0-9]+)/([0-9]+)$',views.AddSuivis,name='UserAddSuivis'),
    re_path(r'^api/user/suivis/delete/([0-9]+)/([0-9]+)$',views.RemoveSuivis,name='UserRemoveSuivis')
]