import json
from django.contrib.gis.db import models

class Route(models.Model):
	markers = models.MultiPointField(blank=True, null=True)
	lines = models.MultiLineStringField(blank=True, null=True)
	objects = models.GeoManager()

	class Meta:
		app_label = 'common'