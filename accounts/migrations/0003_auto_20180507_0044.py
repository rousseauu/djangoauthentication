# Generated by Django 2.0.5 on 2018-05-06 18:44

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userprofile_image'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='userprofile',
            managers=[
                ('nokahali', django.db.models.manager.Manager()),
            ],
        ),
    ]
