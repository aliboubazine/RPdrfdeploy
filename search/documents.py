from django_elasticsearch_dsl import Document,fields
from django_elasticsearch_dsl.registries import registry
from app.models import User,Article,SiteUrl

# User Document
@registry.register_document
class UserDocument(Document):

    articlelist = fields.ObjectField()
    sauvegardelist = fields.ObjectField()
    recommendationlist = fields.NestedField()
    Siteslist = fields.ObjectField()
    suivislist = fields.ObjectField()

    class Index:
        name = 'users'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = User
        fields = [
            'U_Id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'etablissement',
            'fonction',
            'adresse',
            'bio',
            'suivisnb',
            'last_login',
            'is_superuser'          
        ]
        related_models = [User,Article,SiteUrl]

# Article Document
@registry.register_document
class ArticleDocument(Document):

    auteur = fields.ObjectField()
    sauvegarde = fields.ObjectField()
    recommendationlist = fields.ObjectField()

    class Index:
        name = 'articles'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = Article
        fields = [
            'A_Id',
            'title',
            'resume',
            'fichier',
            'urlfichier',
            'recommendation',
            'date_posted'
        ]
        related_models = [User,Article]

# SiteUrl Document
@registry.register_document
class SiteUrlDocument(Document):

    owner = fields.ObjectField()

    class Index:
        name = 'sitesurls'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }  

    class Django:
        model = SiteUrl
        fields = [
            'S_Id',
            'name',
            'url'
        ]
        related_models = [User]  
