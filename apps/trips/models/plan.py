from django.db import models
from utils.fields import ShortUUIDField


class Plan(models.Model):
    pub_id = ShortUUIDField(prefix="plan_", max_length=32)
    name = models.CharField(max_length=256)
    summary = models.TextField(null=True, blank=True)

    route_pub_id = models.CharField(max_length=32)
    packing_list_pub_id = models.CharField(max_length=32)

    def __str__(self):
        return self.name
