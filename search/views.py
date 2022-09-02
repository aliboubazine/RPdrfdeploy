from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination,PageNumberPagination
from .documents import UserDocument,ArticleDocument
from elasticsearch_dsl import Q
from elasticsearch_dsl.query import MoreLikeThis
from .serializers import UserDocumentSerializer,ArticleDocumentSerializer

# Search For User
class SearchUser(APIView,PageNumberPagination):
    user_serializer = UserDocumentSerializer
    search_document = UserDocument
    page_size = 10

    def get(self,request,query):
        q = Q(
            'query_string',
            query=query,
            fields=[
                'username',
                'email',
                'first_name',
                'last_name',
                'etablissement',
                'fonction',
                'adresse',
                'tags'
            ]
        )
        search = self.search_document.search().query(q)
        response = search.execute()
        results = self.paginate_queryset(response,request,view=self)
        serializer = self.user_serializer(results,many=True)
        return self.get_paginated_response(serializer.data)

# Search For Article
class SearchArticle(APIView,PageNumberPagination):
    article_serializer = ArticleDocumentSerializer
    search_document = ArticleDocument
    page_size = 10

    def get(self,request,query):
        q = Q(
            'query_string',
            query=query,
            fields=[
                'title',
                'resume',
                'tags'
            ]
        )
        search = self.search_document.search().query(q)
        response = search.execute()
        results = self.paginate_queryset(response,request,view=self)
        serializer = self.article_serializer(results,many=True)
        return self.get_paginated_response(serializer.data)

# More Like This User For Recommendation
class MoreLikeUser(APIView,PageNumberPagination):
    user_serializer = UserDocumentSerializer
    search_document = UserDocument
    page_size = 10

    def get(self,request,query):

        q = MoreLikeThis(
            like={"_id": query},
            fields=[
                'etablissement',
                'fonction',
                'adresse',
                'tags'
            ],
            min_term_freq=1,
            min_doc_freq=1
        )
        search = self.search_document.search().query(q)
        response = search.execute()
        results = self.paginate_queryset(response,request,view=self)
        serializer = self.user_serializer(results,many=True)
        return self.get_paginated_response(serializer.data)

# More Like This Article For Recommendation
class MoreLikeArticle(APIView,PageNumberPagination):
    article_serializer = ArticleDocumentSerializer
    search_document = ArticleDocument
    page_size = 10

    def get(self,request,query):

        q = MoreLikeThis(
            like ={"_id": query},
            fields=[
                'title',
                'resume',
                'tags'
            ],
            min_term_freq=1,
            min_doc_freq=1            
        )
        search = self.search_document.search().query(q)
        response = search.execute()
        results = self.paginate_queryset(response,request,view=self)
        serializer = self.article_serializer(results,many=True)
        return self.get_paginated_response(serializer.data)

# Most recent articles without tags 
class MostRecentArticle(APIView,PageNumberPagination):
    page_size = 10
    article_serializer = ArticleDocumentSerializer
    search_document = ArticleDocument
    
    def get(self,request):
        search = self.search_document.search().sort('-date_posted')
        search = search[0:1000]
        response = search.execute()
        results = self.paginate_queryset(response,request,view=self)
        serializer = self.article_serializer(results,many=True)
        return self.get_paginated_response(serializer.data)

# Most viewed articles  
class MostViewedArticle(APIView,PageNumberPagination):
    page_size = 10
    article_serializer = ArticleDocumentSerializer
    search_document = ArticleDocument
    
    def get(self,request):
        search = self.search_document.search().sort('-nbvus')
        search = search[0:1000]
        response = search.execute()
        results = self.paginate_queryset(response,request,view=self)
        serializer = self.article_serializer(results,many=True)
        return self.get_paginated_response(serializer.data)

# Most viewed articles  
class MostPostUser(APIView,PageNumberPagination):
    page_size = 10
    user_serializer = UserDocumentSerializer
    search_document = UserDocument
    
    def get(self,request):
        search = self.search_document.search().sort('-nbposts')
        search = search[0:1000]
        response = search.execute()
        results = self.paginate_queryset(response,request,view=self)
        serializer = self.user_serializer(results,many=True)
        return self.get_paginated_response(serializer.data)                

# Most recent articles with tags
class MostRecentArticleTags(APIView,PageNumberPagination):
    page_size = 10
    article_serializer = ArticleDocumentSerializer
    search_document = ArticleDocument

    def get(self,request,query):
        q = Q(
            'query_string',
            query=query,
            fields=[
                'tags'
            ]
        )
        search = self.search_document.search().query(q)
        search = search.sort('-date_posted')
        search = search[0:1000]
        response = search.execute()
        results = self.paginate_queryset(response,request,view=self)
        serializer = self.article_serializer(results,many=True)
        return self.get_paginated_response(serializer.data)

# Most recommended articles  
class MostRecommendedArticle(APIView,PageNumberPagination):
    page_size = 10
    article_serializer = ArticleDocumentSerializer
    search_document = ArticleDocument
    
    def get(self,request):
        search = self.search_document.search().sort('-recommendation')
        search = search[0:1000]
        response = search.execute()
        results = self.paginate_queryset(response,request,view=self)
        serializer = self.article_serializer(results,many=True)
        return self.get_paginated_response(serializer.data)                      