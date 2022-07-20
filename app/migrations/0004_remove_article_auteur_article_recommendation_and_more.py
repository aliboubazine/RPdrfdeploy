# Generated by Django 4.0.4 on 2022-07-13 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_article_auteur'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='auteur',
        ),
        migrations.AddField(
            model_name='article',
            name='recommendation',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='article',
            name='resume',
            field=models.CharField(max_length=1000),
        ),
    ]