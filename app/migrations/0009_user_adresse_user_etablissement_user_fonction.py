# Generated by Django 4.0.4 on 2022-07-22 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_article_sauvegarde'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='adresse',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='etablissement',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='fonction',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
