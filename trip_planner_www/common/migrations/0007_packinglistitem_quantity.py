# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0006_auto_20160107_2158'),
    ]

    operations = [
        migrations.AddField(
            model_name='packinglistitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
