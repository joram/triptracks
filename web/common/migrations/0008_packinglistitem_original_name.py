# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0007_packinglistitem_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='packinglistitem',
            name='original_name',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
    ]
