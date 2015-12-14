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
            coord = (lat, lng, alt)
            coords.append(coord)
        return coords

    def route_from_file(self, filepath, max_vertices=100):
        contents = []
        if filepath.endswith(".kmz"):
            contents = self._load_kmz_content(filepath)
        if filepath.endswith(".kml"):
            contents = self._load_kml_content(filepath)

        geo_line = []
        for content in contents:
            root = parser.fromstring(content)
            line_tuples = self._load_kml_str(root)
            nth_vertex = max(1, int(len(line_tuples) / max_vertices))
            for (lat, lng, alt) in line_tuples[0::nth_vertex]:
                geo_line.append((lat, lng))
        line = LineString(geo_line)
        lines = MultiLineString([line])
        name = filepath.split("/")[-1].split(".")[0]
        return self.create(lines=lines, name=name)


class Route(models.Model):
    name = models.CharField(max_length=120)
    markers = models.MultiPointField(blank=True, null=True)
    lines = models.MultiLineStringField(blank=True, null=True)
    center = models.PointField(blank=True, null=True)
    objects = RouteManager()

    def vertices(self, max_verts=None):
        nth_vertex = len(self.lines[0])
        if max_verts:
            nth_vertex = max(1, int(len(self.lines[0])/max_verts))
        return self.lines[0][0::nth_vertex]

    def save(self, *args, **kwargs):
        envelope = self.lines.envelope
        self.center = self.lines.centroid
        return super(Route, self).save(*args, **kwargs)

    @property
    def static_tile_image_src(self):
        url = "https://maps.googleapis.com/maps/api/staticmap?zoom=13&size=200x200&maptype=roadmap"
        url += "&center=%s,%s" % (self.center.y, self.center.x)
        url += "&path=color:0x0000ff|weight:5"
        for p in self.vertices(30):
            url += "|%s,%s" % (p[1], p[0])
        return url

    class Meta:
        app_label = 'common'
