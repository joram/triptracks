# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_auto_20160107_0331'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='packinglist',
            name='plan',
        ),
        migrations.AddField(
            model_name='packinglistitem',
            name='item',
            field=models.ForeignKey(default=0, to='common.Item'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='packinglist',
            name='name',
            field=models.CharField(default=b'', max_length=30, blank=True),
        ),
    ]
