from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.utils import timezone

# UserManager Model
class UserManager(BaseUserManager):

    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError(('The given username must be set'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        user = self._create_user(username, email, password, True, True,
                                 **extra_fields)
        user.is_active = True
        user.save(using=self._db)
        return user

# User Model 
class User(AbstractBaseUser, PermissionsMixin):
    U_Id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=250, unique=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    etablissement = models.CharField(max_length=100,blank=True,null=True)
    fonction = models.CharField(max_length=100,blank=True,null=True)
    adresse = models.CharField(max_length=200,blank=True,null=True)
    bio = models.CharField(max_length=2000,blank=True,null=True)
    suivis = models.ForeignKey('self',related_name="suivislist",blank=True,null=True,on_delete=models.CASCADE)
    suivisnb = models.IntegerField(default=0,null=True,blank=True)
    tags = models.CharField(max_length=500, blank=True, null=True)
    nbposts = models.IntegerField(default=0)
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    def __str__(self):
        return '%d : %s' % (self.U_Id, self.username)

# Article Model  
class Article (models.Model):
    A_Id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    resume = models.CharField(max_length=1000)
    auteur = models.ManyToManyField(User,related_name="articlelist",blank=True)
    realfile = models.FileField(blank=True,null=True,upload_to="Files")
    sauvegarde = models.ManyToManyField(User,related_name="sauvegardelist",blank=True)
    recommendationlist = models.ManyToManyField(User,related_name="recommendationlist",blank=True)
    recommendation = models.IntegerField(default=0)
    date_posted = models.DateField()
    tags = models.CharField(max_length=500, blank=True, null=True)
    nbvus = models.IntegerField(default=0)
    auteurstr = models.CharField(max_length=500, blank=True, null=True)
    principal = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# SiteUrl Model
class SiteUrl(models.Model):
    S_Id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=1000)
    owner =  models.ForeignKey(User,related_name="Siteslist",blank=True,null=True,on_delete=models.CASCADE)

    def __str__(self):
        return '%s : %s' % (self.name, self.url)

# Comment Model
class Comment(models.Model):
    C_Id = models.AutoField(primary_key=True)
    contenu = models.CharField(max_length=500)
    comment_date = models.DateField()
    comment_owner =  models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    comment_post =  models.ForeignKey(Article,related_name="commentslist",blank=True,null=True,on_delete=models.CASCADE)
