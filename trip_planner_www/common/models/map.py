import json
from django.contrib.gis.db import models

class Point(models.Model):
	location = models.PointField()
	plan = models.ForeignKey("Map")
	objects = models.GeoManager()

	class Meta:
		app_label = 'common'

class Map(models.Model):
	markers = models.MultiPointField(blank=True, null=True)
	lines = models.MultiLineStringField(blank=True, null=True)
	plan = models.ForeignKey("Plan")
	objects = models.GeoManager()

	class Meta:
		app_label = 'common'