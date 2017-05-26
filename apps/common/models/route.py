from django.contrib.gis.db import models
from django.contrib.gis.geos import LineString, MultiLineString, Point
from django.conf import settings

import os
import zipfile
import gpxpy.gpx
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

    def route_from_gpx(self, tracks_file):
        gpx = gpxpy.parse(tracks_file.tracks_file)
        line_tuples = []
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    line_tuples.append((point.latitude, point.longitude, point.elevation))

        for waypoint in gpx.waypoints:
            line_tuples.append((waypoint.latitude, waypoint.longitude, 0))

        for route in gpx.routes:
            for point in route.points:
                line_tuples.append((point.latitude, point.longitude, point.elevation))

        return line_tuples

    def route_from_file(self, filepath, max_vertices=100):
        line_tuples = []
        if filepath.endswith("kmz"):
            contents = self._load_kmz_content(filepath)
            for content in contents:
                root = parser.fromstring(content)
                line_tuples = self._load_kml_str(root)

        if filepath.endswith(".kml"):
            contents = self._load_kml_content(filepath)
            for content in contents:
                root = parser.fromstring(content)
                line_tuples = self._load_kml_str(root)

        name = filepath  # TODO
        return self._route_from_line(line_tuples, name)

    def create_from_route(self, tracks_file):
        line_tuples = []

        if tracks_file.tracks_file.path.endswith(".gpx"):
            line_tuples = self.route_from_gpx(tracks_file)

        return self._route_from_line(line_tuples, tracks_file.tracks_file.name)

    def _route_from_line(self, line_tuples, name, max_vertices=10000):
        if len(line_tuples) < 2:
            print "empty line"
            return

        geo_line = []
        nth_vertex = max(1, int(len(line_tuples) / max_vertices))
        for (lat, lng, alt) in line_tuples[0::nth_vertex]:
            geo_line.append((lat, lng))
        line = LineString(geo_line)
        lines = MultiLineString([line])

        center = None
        if lines:
            center = lines.centroid

        return self.create(lines=lines, name=name, center=center)

    def load_demo_tracks(self):
        tracks_dir = os.path.join(settings.BASE_DIR, "../data/tracks")
        for filename in os.listdir(tracks_dir):
            filepath = os.path.join(tracks_dir, filename)
            try:
                route = self.route_from_file(filepath)
                print "%s %s" % (route, filepath)
            except Exception as e:
                print filepath
                print e


class Route(models.Model):
    name = models.CharField(max_length=120)
    markers = models.MultiPointField(blank=True, null=True)
    lines = models.MultiLineStringField(blank=True, null=True)
    center = models.PointField(blank=True, null=True)
    objects = RouteManager()

    def vertices(self, max_verts=None):
        if len(self.lines) == 0:
            return []

        line = self.lines[0]
        if not max_verts:
            return list(line)

        nth_vertex = len(line)
        if max_verts:
            nth_vertex = max(1, int(len(line)/max_verts))
        vertices = line[0::nth_vertex]
        return vertices

    def save(self, *args, **kwargs):
        if self.lines:
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
