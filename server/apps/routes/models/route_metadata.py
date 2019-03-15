from django.db import models
from utils.fields import ShortUUIDField
from django.contrib.postgres.fields import JSONField


class RouteMetadata(models.Model):
    SOURCE_CHOICES = (
        ("summitpost", 'Summitpost'),
        ("trailpeak", 'Trailpeak'),
    )

    pub_id = ShortUUIDField(prefix="route", max_length=38)
    name = models.CharField(max_length=256)
    mountain_name = models.CharField(max_length=256)
    geohash = models.CharField(max_length=32)
    bounds = JSONField()
    description = models.TextField(null=True, blank=True)
    suggested_gear = models.TextField(null=True, blank=True)
    source_url = models.TextField(null=True, blank=True)
    source = models.CharField(max_length=16, choices=SOURCE_CHOICES)
