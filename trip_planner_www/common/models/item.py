from django.db import models
from django.contrib.auth.models import User
from common.models import PackingList, Itinerary, Route
from jsonfield import JSONField

class Item(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    attributes = JSONField()

    def __str__(self):
        return self.name

    class Meta:
    	app_label = 'common'