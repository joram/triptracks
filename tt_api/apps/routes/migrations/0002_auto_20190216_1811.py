# Generated by Django 2.1.5 on 2019-02-16 18:11

from django.db import migrations
import utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routemetadata',
            name='pub_id',
            field=utils.fields.ShortUUIDField(max_length=38),
        ),
    ]
