from dataclasses import fields
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from .documents import UserDocument,ArticleDocument
from elasticsearch_dsl import Q
from elasticsearch_dsl.query import MoreLikeThis
from .serializers import UserDocumentSerializer,ArticleDocumentSerializer

# Search For User
class SearchUser(APIView,LimitOffsetPagination):
    user_serializer = UserDocumentSerializer
    search_document = UserDocument

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
            ]
        )
        search = self.search_document.search().query(q)
        response = search.execute()
        results = self.paginate_queryset(response,request,view=self)
        serializer = self.user_serializer(results,many=True)
        return self.get_paginated_response(serializer.data)

# Search For Article
class SearchArticle(APIView,LimitOffsetPagination):
    article_serializer = ArticleDocumentSerializer
    search_document = ArticleDocument

    def get(self,request,query):
        q = Q(
            'query_string',
            query=query,
            fields=[
                'title',
                'resume',
            ]
        )
        search = self.search_document.search().query(q)
        response = search.execute()
        results = self.paginate_queryset(response,request,view=self)
        serializer = self.article_serializer(results,many=True)
        return self.get_paginated_response(serializer.data)

# More Like This User For Recommendation
class MoreLikeUser(APIView,LimitOffsetPagination):
    user_serializer = UserDocumentSerializer
    search_document = UserDocument

    def get(self,request,query):

        q = MoreLikeThis(
            like={"_id": query},
            fields=[
                'etablissement',
                'fonction',
                'adresse',
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
class MoreLikeArticle(APIView,LimitOffsetPagination):
    article_serializer = ArticleDocumentSerializer
    search_document = ArticleDocument

    def get(self,request,query):

        q = MoreLikeThis(
            like ={"_id": query},
            fields=[
                'title',
                'resume'
            ],
            min_term_freq=1,
            min_doc_freq=1            
        )
        search = self.search_document.search().query(q)
        response = search.execute()
        results = self.paginate_queryset(response,request,view=self)
        serializer = self.article_serializer(results,many=True)
        return self.get_paginated_response(serializer.data)                        