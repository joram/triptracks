# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0008_packinglistitem_original_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='packinglistitem',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 23, 56, 26, 768892, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='packinglistitem',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 23, 56, 31, 608779, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
