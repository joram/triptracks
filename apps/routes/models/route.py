from django.contrib.gis.db import models
from django.contrib.gis.geos import LineString, MultiLineString
import zipfile
import gpxpy.gpx
from pykml import parser
from django.conf import settings
from utils.fields import ShortUUIDField


class RouteManager(models.GeoManager):

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

    def _lines_from_gpx(self, tracks_file):
        gpx = gpxpy.parse(tracks_file.tracks_file)
        lines = []
        for track in gpx.tracks:
            for segment in track.segments:
                line = []
                for point in segment.points:
                    line.append((point.latitude, point.longitude, point.elevation))
                lines.append(line)

        for route in gpx.routes:
            line = []
            for point in route.points:
                line.append((point.latitude, point.longitude, point.elevation))
            lines.append(line)

        return lines

    def _lines_from_kmz(self, tracks_file):
        lines = []

        zf = zipfile.ZipFile(tracks_file.tracks_file)
        contents = []
        for info in zf.infolist():
            contents.append(zf.read(info.filename))

        for content in contents:
            root = parser.fromstring(content)
            lines = self._load_kml_str(root)
        return lines

    def _lines_from_kml(self, tracks_file):
        lines = []

        contents = tracks_file.tracks_file.read().split["\n"]
        for content in contents:
            root = parser.fromstring(content)
            lines = self._load_kml_str(root)

        return lines

    def create_from_route(self, tracks_file, max_vertices=1000000):
        lines = []
        name = tracks_file.tracks_file.name

        if tracks_file.tracks_file.path.endswith(".gpx"):
            lines = self._lines_from_gpx(tracks_file)
        if tracks_file.tracks_file.path.endswith(".kml"):
            lines = self._lines_from_kml(tracks_file)
        if tracks_file.tracks_file.path.endswith(".kmz"):
            lines = self._lines_from_kmz(tracks_file)

        geo_lines = []
        for line in lines:
            if len(line) < 2:
                continue
            geo_line = []
            nth_vertex = max(1, int(len(line) / max_vertices))
            for (lat, lng, alt) in line[0::nth_vertex]:
                geo_line.append((lat, lng))
            geo_lines.append(LineString(geo_line))
        lines = MultiLineString(geo_lines)

        center = None
        if lines:
            center = lines.centroid

        return self.create(lines=lines, name=name, center=center)


class Route(models.Model):
    # pub_id = ShortUUIDField(prefix="rt_")
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

        path = "color:0x0000ff|weight:5"
        for p in self.vertices(30):
            path += "|%s,%s" % (p[1], p[0])

        url = "https://maps.googleapis.com/maps/api/staticmap?" \
              "zoom={zoom}&size={size}&maptype={maptype}&key={key}&center={center}&path={path}".format(
                    zoom=13,
                    size="200x200",
                    maptype="roadmap",
                    key=settings.GOOGLE_MAPS_API_KEY,
                    center="{},{}".format(self.center.y, self.center.x),
                    path=path,
              )

        return url
