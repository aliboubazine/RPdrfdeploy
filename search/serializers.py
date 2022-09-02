from .documents import UserDocument,ArticleDocument
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

# User Document Serializer
class UserDocumentSerializer(DocumentSerializer):
    class Meta :
        document = UserDocument
        fields = [
            'U_Id',
            'username',
            'email',
            'first_name',
            'last_name',
            'etablissement',
            'fonction',
            'adresse',
            'tags',
            'nbposts',
            'suivisnb'
        ]

# Article Document Serializer
class ArticleDocumentSerializer(DocumentSerializer):
    class Meta :
        document = ArticleDocument
        fields = [
            'A_Id',
            'title',
            'resume',
            'tags',
            'recommendation',
            'nbvus',
            'date_posted'
        ]                           