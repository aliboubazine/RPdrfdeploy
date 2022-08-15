from django.urls import path,include

urlpatterns = [
    path('', include('app.urls')),
    path('', include('search.urls')),
]
