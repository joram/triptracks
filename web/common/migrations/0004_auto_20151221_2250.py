# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_tracksfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tracksfile',
            name='tracks_file',
            field=models.FileField(upload_to=b'/srv/www/trip_planner_www/uploads'),
        ),
    ]
