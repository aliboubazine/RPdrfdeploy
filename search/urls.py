from django.conf import settings
from django.urls import path,include
from search.views import SearchUser,SearchArticle,MoreLikeUser,MoreLikeArticle

urlpatterns = [
    path('api/user/search/<str:query>/',SearchUser.as_view()),
    path('api/article/search/<str:query>/',SearchArticle.as_view()),
    path('api/user/morelike/<str:query>/',MoreLikeUser.as_view()),
    path('api/article/morelike/<str:query>/',MoreLikeArticle.as_view())
]