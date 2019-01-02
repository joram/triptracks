import Geohash
import os
import gpxpy.gpx
from pykml import parser
import pprint
import uuid
import random


def lines_from_gpx(filepath):
    try:
        if filepath.endswith(".json"):
            filepath = filepath.replace(".json", ".gpx")
        with open(filepath) as f:
            gpx = gpxpy.parse(f)
    except Exception as e:
        print(filepath)
        print(e)
        return []
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

def reduced_lines(original_lines, max_vertices):
    lines = []
    for original_line in original_lines:
        total_vertices = len(original_line)
        max_vertices = min(max_vertices, total_vertices)
        step = int(total_vertices / max_vertices)
        line = []
        for i in range(0, len(original_line)-1, step):
            line.append(original_line[i])
            line.append(original_line[-1])
        lines.append(line)
    return lines


class Route(object):

    @classmethod
    def from_data(cls, data):
        filepath = data["gpx_filepath"].replace(".json", ".gpx")
        route = Route(
          lines=lines_from_gpx(filepath),
          name=data["name"].strip("\n "),
          description=data["description"],
          gpx=filepath,
        )
        return route

    def __init__(self, lines, name=None, description=None, gpx=None, pub_id=None):
        self.name = name
        self.description = description
        self.lines = lines
        self.gpx = gpx
        self.pub_id = pub_id

        if self.pub_id is None:
          rd = random.Random()
          rd.seed(name)
          self.pub_id = "route_" + str(uuid.UUID(int=rd.getrandbits(128))).replace("-", "")

    def details(self, max_vertices=100000000):
        return {
          "name": self.name,
          "description": self.description,
          "pub_id": self.pub_id,
          "gpx": self.gpx,
          "lines": self.lines,
        }

    def __str__(self):
        geohash=self.geohash()
        if geohash.endswith("000"):
            geohash = self.gpx

        return u"{uuid}[{name}]{geohash}".format(
            uuid=self.pub_id,
            name=self.name,
            geohash=geohash,
        )

    def __unicode__(self):
        return self.__str__()

    def geohash(self):
        ((lat1, lng1), (lat2, lng2)) = self.bbox()
        h1 = Geohash.encode(lat1, lng1)
        h2 = Geohash.encode(lat2, lng2)
        i = 0
        for c in h1:
            if h2[i] == c:
                i += 1
        matching = h1[:i]
        return matching

    def bbox(self):
        min_lat = None
        max_lat = None
        min_lng = None
        max_lng = None
        for line in self.lines:
            for coord in line:
                lat = coord[0]
                lng = coord[1]
                if min_lat is None:
                    min_lat = lat
                    max_lat = lat
                    min_lng = lng
                    max_lng = lng
                    continue
                min_lat = min(min_lat, lat)
                max_lat = max(max_lat, lat)
                min_lng = min(min_lng, lng)
                max_lng = max(max_lng, lng)
        return ((min_lat, min_lng), (max_lat, max_lng))


    def vertices(self, max_verts=None):
        if self.lines is None or len(self.lines) == 0:
            return []

        line = self.lines[0]
        if not max_verts:
            return list(line)
        if type(line) == float:
            print("????  "+str(line))
            return []
        nth_vertex = len(line)
        if max_verts:
            nth_vertex = max(1, int(len(line)/max_verts))
        vertices = line[0::nth_vertex]
        return [vertices]
    
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
