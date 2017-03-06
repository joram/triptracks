# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_item'),
    ]

    operations = [
        migrations.CreateModel(
            name='TracksFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tracks_file', models.FileField(upload_to=b'/home/joram/code/trip-planner/trip_planner_www/uploads')),
            ],
        ),
    ]
