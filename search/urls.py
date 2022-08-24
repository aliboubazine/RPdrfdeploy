from django.conf import settings
from django.urls import path
from search.views import SearchUser,SearchArticle,MoreLikeUser,MoreLikeArticle,MostRecentArticle,MostRecentArticleTags,MostRecommendedArticle

urlpatterns = [
    path('api/user/search/<str:query>/',SearchUser.as_view(),name='SearchUser'),
    path('api/article/search/<str:query>/',SearchArticle.as_view(),name='SearchArticle'),
    path('api/user/morelike/<str:query>/',MoreLikeUser.as_view(),name='MoreLikeThisUser'),
    path('api/article/morelike/<str:query>/',MoreLikeArticle.as_view(),name='MoreLikeThisArticle'),
    path('api/article/mostrecent/',MostRecentArticle.as_view(),name='MostRecentArticle'),
    path('api/article/mostrecent/tags/<str:query>/',MostRecentArticleTags.as_view(),name='MostRecentArticleTags'),
    path('api/article/mostrecommended/',MostRecommendedArticle.as_view(),name='MostRecommendedArticle')
]