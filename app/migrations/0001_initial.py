# Generated by Django 4.0.4 on 2022-08-05 15:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('U_Id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=30, unique=True)),
                ('email', models.EmailField(max_length=250, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=30, null=True)),
                ('last_name', models.CharField(blank=True, max_length=30, null=True)),
                ('etablissement', models.CharField(blank=True, max_length=100, null=True)),
                ('fonction', models.CharField(blank=True, max_length=100, null=True)),
                ('adresse', models.CharField(blank=True, max_length=200, null=True)),
                ('bio', models.CharField(blank=True, max_length=2000, null=True)),
                ('suivisnb', models.IntegerField(default=0)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('suivis', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='suivislist', to=settings.AUTH_USER_MODEL)),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SiteUrl',
            fields=[
                ('S_Id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('url', models.CharField(max_length=1000)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Siteslist', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('A_Id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('resume', models.CharField(max_length=1000)),
                ('fichier', models.CharField(blank=True, max_length=300, null=True)),
                ('urlfichier', models.CharField(blank=True, max_length=300, null=True)),
                ('recommendation', models.IntegerField(default=0)),
                ('date_posted', models.DateField()),
                ('auteur', models.ManyToManyField(blank=True, related_name='articlelist', to=settings.AUTH_USER_MODEL)),
                ('recommendationlist', models.ManyToManyField(blank=True, related_name='recommendationlist', to=settings.AUTH_USER_MODEL)),
                ('sauvegarde', models.ManyToManyField(blank=True, related_name='sauvegardelist', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
