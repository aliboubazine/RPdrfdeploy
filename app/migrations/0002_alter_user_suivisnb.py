# Generated by Django 4.0.4 on 2022-08-08 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='suivisnb',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
