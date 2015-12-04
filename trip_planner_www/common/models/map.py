import json
from django.contrib.gis.db import models

class Map(models.Model):
	markers = models.MultiPointField(blank=True, null=True)
	lines = models.MultiLineStringField(blank=True, null=True)
	plan = models.ForeignKey("Plan")
	objects = models.GeoManager()

	class Meta:
		app_label = 'common'