# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-18 21:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('routes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('href', models.URLField()),
                ('img_href', models.URLField()),
                ('attributes', jsonfield.fields.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Itinerary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=5000)),
            ],
            options={
                'verbose_name_plural': 'Itineraries',
            },
        ),
        migrations.CreateModel(
            name='PackingList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=b'', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='PackingListItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('original_name', models.CharField(max_length=30)),
                ('item_type', models.CharField(choices=[(b'G', b'Group'), (b'P', b'Personal')], default=b'P', max_length=2)),
                ('quantity', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='packing.Item')),
                ('packing_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='packing.PackingList')),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.User')),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='routes.Route')),
            ],
        ),
        migrations.AddField(
            model_name='itinerary',
            name='plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='packing.Plan'),
        ),
    ]
