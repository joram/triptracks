# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Itinerary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=5000)),
            ],
            options={
                'verbose_name_plural': 'Itineraries',
            },
        ),
        migrations.CreateModel(
            name='PackingList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='PackingListItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('item_type', models.CharField(default=b'P', max_length=2, choices=[(b'G', b'Group'), (b'P', b'Personal')])),
                ('packing_list', models.ForeignKey(to='common.PackingList')),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=120)),
                ('markers', django.contrib.gis.db.models.fields.MultiPointField(srid=4326, null=True, blank=True)),
                ('line', django.contrib.gis.db.models.fields.LineStringField(srid=4326, null=True, blank=True)),
                ('center', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='packinglist',
            name='plan',
            field=models.ForeignKey(to='common.Plan'),
        ),
        migrations.AddField(
            model_name='itinerary',
            name='plan',
            field=models.ForeignKey(to='common.Plan'),
        ),
    ]
