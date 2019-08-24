from django.db import models
from django.contrib.postgres.fields import JSONField


class RouteLines(models.Model):
    route_pub_id = models.CharField(max_length=38)
    zoom = models.IntegerField()
    lines = JSONField()

    class Meta:
        unique_together = [
            ('route_pub_id', 'zoom'),
        ]
