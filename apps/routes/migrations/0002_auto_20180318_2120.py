# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-18 21:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tracksfile',
            name='filename',
            field=models.CharField(max_length=512),
        ),
    ]
