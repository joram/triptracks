import json
from django.contrib.gis.db import models
from django.contrib.gis.geos import LineString, MultiLineString

import os
import json
import zipfile
from django.contrib.gis.gdal import DataSource
from pykml import parser

class RouteManager(models.GeoManager):

	def _load_kml_content(self, filename):
		f = open(filename)
		return [f.read()]

	def _load_kmz_content(self, filepath):
		zf = zipfile.ZipFile(filepath)
		file_contents = []
		for info in zf.infolist():
			file_contents.append(zf.read(info.filename))
		return file_contents

	def _load_kml_str(self, node):
		coords = []
		for el in node.findall(".//{http://www.google.com/kml/ext/2.2}coord"):
			(lat, lng, alt) = el.text.split(" ")
			lat = float(lat)
			lng = float(lng)
			alt = float(alt)
			coord = (lat,lng,alt)
			coords.append(coord)
		return coords

	def route_from_file(self, filepath):
		contents = []
		if filepath.endswith(".kmz"):
			contents = self._load_kmz_content(filepath)
		if filepath.endswith(".kml"):
			contents = self._load_kml_content(filepath)

		geo_line = []
		for content in contents:
			root = parser.fromstring(content)
			line = self._load_kml_str(root)
			for (lat, lng, alt) in line:
				geo_line.append((lat, lng))
		lines = MultiLineString(LineString(geo_line))
		print lines.__str__()[0:30]	
		return self.create(lines=lines)

class Route(models.Model):
	markers = models.MultiPointField(blank=True, null=True)
	lines = models.MultiLineStringField(blank=True, null=True)
	objects = RouteManager()

	class Meta:
		app_label = 'common'