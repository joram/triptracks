from django.db import models
from utils.fields import ShortUUIDField


class RouteMetadata(models.Model):
    pub_id = ShortUUIDField(prefix="route", max_length=32)
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
