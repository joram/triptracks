# Generated by Django 2.1.5 on 2019-03-16 22:12

from django.db import migrations, models
import utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0006_auto_20190315_2317'),
    ]

    operations = [
        migrations.AddField(
            model_name='routemetadata',
            name='has_gpx',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='routemetadata',
            name='has_image',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='routemetadata',
            name='geohash',
            field=models.CharField(db_index=True, max_length=32),
        ),
        migrations.AlterField(
            model_name='routemetadata',
            name='name',
            field=models.CharField(db_index=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='routemetadata',
            name='pub_id',
            field=utils.fields.ShortUUIDField(db_index=True, max_length=38),
        ),
    ]
