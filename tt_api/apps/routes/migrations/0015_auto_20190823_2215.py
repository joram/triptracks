# Generated by Django 2.2.3 on 2019-08-23 22:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0014_auto_20190823_2057'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RouteMetadata',
            new_name='Route',
        ),
        migrations.RenameModel(
            old_name='RouteLine',
            new_name='RouteLines',
        ),
    ]
