# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_auto_20151221_2250'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='href',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='img_href',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
    ]
