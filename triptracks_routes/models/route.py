import geohash2
import uuid
import random
import graphene
from utils import lines_from_gpx
from models.user import User

ZOOM_LEVELS = {
    0: 1,
    1: 1,
    2: 1,
    3: 5,
    4: 5,
    5: 5,
    6: 10,
    7: 10,
    8: 10,
    9: 25,
    10: 25,
    11: 100,
    12: 100,
    13: 500,
    14: 500,
    15: 1000,
    16: 1000,
    17: 1500,
    18: 1500,
    19: 2000,
    20: 2000,
}


def get_cache(zoom=1):
    max_verts = ZOOM_LEVELS[zoom]
    from stores.routes import RoutesStore
    from stores.cached_routes import CachedRoutesStore
    return CachedRoutesStore(max_verts, RoutesStore())


class Route(graphene.ObjectType):
    pub_id = graphene.ID()
    name = graphene.String()
    geohash = graphene.String()
    zoom = graphene.Int()
    description = graphene.String()
    lines = graphene.JSONString()
    owner = graphene.Field(User)
    is_public = graphene.Boolean()

    def resolve_owner(self, info):
        return User(pub_id="user_???", name="bob")

    @classmethod
    def from_data(cls, data):
        filepath = data["gpx_filepath"].replace(".json", ".gpx")
        route = Route(
          lines=lines_from_gpx(filepath),
          name=data["name"].strip("\n "),
          description=data["description"],
        )
        return route

    def __init__(self, lines, name=None, description=None, pub_id=None, geohash=None, zoom=None):
        super(Route, self).__init__()
        self.pub_id = pub_id
        self.geohash = geohash
        self.zoom = zoom
        self.name = name
        self.description = description
        self.lines = lines

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
        h1 = geohash2.encode(lat1, lng1)
        h2 = geohash2.encode(lat2, lng2)
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
