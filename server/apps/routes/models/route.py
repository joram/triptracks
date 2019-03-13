import geohash2
import uuid
import random
import graphene
from utils.lines import lines_from_gpx
from apps.accounts.models import User
from django.conf import settings
from apps.accounts.schema import UserType


class Route(graphene.ObjectType):

    pub_id = graphene.ID()
    owner_pub_id = graphene.String()
    name = graphene.String()
    geohash = graphene.String()
    zoom = graphene.Int()
    bounds = graphene.JSONString()
    description = graphene.String()
    lines = graphene.JSONString()
    owner = graphene.Field(UserType)
    is_public = graphene.Boolean()

    def resolve_owner(self, info):
        return User(pub_id=self.owner_pub_id)

    def resolve_geohash(self, info):
        return self._geohash()

    @classmethod
    def from_data(cls, data):
        filepath = data["gpx_filepath"].replace(".json", ".gpx")
        route = Route(
          lines=lines_from_gpx(filepath),
          name=data["name"].strip("\n "),
          description=data["description"],
        )
        return route

    def __init__(self, lines, name=None, description=None, pub_id=None, zoom=None, owner_pub_id=None, is_public=False):
        super(Route, self).__init__()
        self.pub_id = pub_id
        self.owner_pub_id = owner_pub_id
        self.zoom = zoom
        self.name = name
        self.description = description
        self.lines = lines
        self.is_public = is_public

        if self.pub_id is None:
          rd = random.Random()
          rd.seed(name)
          self.pub_id = "route_" + str(uuid.UUID(int=rd.getrandbits(128))).replace("-", "")

    def details(self, max_vertices=100000000):
        return {
          "name": self.name,
          "description": self.description,
          "pub_id": self.pub_id,
          "lines": self.vertices(max_vertices),
          "owner_pub_id": self.owner_pub_id,
          "is_public": self.is_public,
        }

    def __str__(self):
        geohash = self._geohash()
        if geohash.endswith("000"):
            geohash = "unknown"

        return u"{uuid}[{name}]{geohash}".format(
            uuid=self.pub_id,
            name=self.name,
            geohash=geohash,
        )

    def __unicode__(self):
        return self.__str__()

    def _geohash(self):
        (lat1, lng1), (lat2, lng2) = self.bbox()
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
        return (min_lat, min_lng), (max_lat, max_lng)

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
        # deprecated func
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
