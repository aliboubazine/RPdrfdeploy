# Generated by Django 4.0.4 on 2022-07-18 05:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_remove_article_auteur_article_auteur'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='auteur',
            field=models.ManyToManyField(blank=True, related_name='articlelist', to=settings.AUTH_USER_MODEL),
        ),
    ]
