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
            'tags',
            'nbposts',
            'suivisnb',
            'last_login',
            'is_superuser'          
        ]
        related_models = [User,Article,SiteUrl]
    
    def get_instances_from_related(self,related_instance):
        if isinstance(related_instance,User):
            return related_instance.suivis
        if isinstance(related_instance,User):
            return related_instance.Siteslist.all()                 

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
            'realfile',
            'tags',
            'recommendation',
            'nbvus',
            'date_posted',
            'auteurstr'
        ]
        related_models = [User,Article]

    def get_instances_from_related(self,related_instance):
        if isinstance(related_instance,Article):
            return related_instance.auteur.all()
        elif isinstance(related_instance,Article):
            return related_instance.sauvegarde.all()
        elif isinstance(related_instance,Article):
            return related_instance.recommendationlist.all()

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

    def get_instances_from_related(self,related_instance):
        if isinstance(related_instance,SiteUrl):
            return related_instance.owner                          