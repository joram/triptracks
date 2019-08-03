from django.conf import settings
from django.db import models
from utils.fields import ShortUUIDField
from django.contrib.postgres.fields import JSONField
from graphene_django import DjangoObjectType
from utils.lines import reduced_lines, max_vertices


class RouteMetadata(models.Model):
    SOURCE_CHOICES = (
        ("summitpost", 'Summitpost'),
        ("trailpeak", 'Trailpeak'),
        ("strava", 'Strava'),
    )

    pub_id = ShortUUIDField(prefix="route", max_length=38, db_index=True)
    name = models.CharField(max_length=256, db_index=True)
    mountain_name = models.CharField(max_length=256)
    geohash = models.CharField(max_length=32, db_index=True)
    bounds = JSONField()
    description = models.TextField(null=True, blank=True)
    suggested_gear = models.TextField(null=True, blank=True)
    has_image = models.BooleanField(default=False)
    has_gpx = models.BooleanField(default=False)

    source = models.CharField(max_length=16, choices=SOURCE_CHOICES)
    source_url = models.TextField(null=True, blank=True)
    source_image_url = models.TextField(null=True, blank=True)
    source_gpx_url = models.TextField(null=True, blank=True)

    owner_pub_id = models.CharField(max_length=128, default="user_3ffrCPmfjrQwrbh9FcKXcYqV")
    is_public = models.BooleanField(default=True)

    lines_zoom_1 = JSONField(null=True, blank=True)
    lines_zoom_2 = JSONField(null=True, blank=True)
    lines_zoom_3 = JSONField(null=True, blank=True)
    lines_zoom_4 = JSONField(null=True, blank=True)
    lines_zoom_5 = JSONField(null=True, blank=True)
    lines_zoom_6 = JSONField(null=True, blank=True)
    lines_zoom_7 = JSONField(null=True, blank=True)
    lines_zoom_8 = JSONField(null=True, blank=True)
    lines_zoom_9 = JSONField(null=True, blank=True)
    lines_zoom_10 = JSONField(null=True, blank=True)
    lines_zoom_11 = JSONField(null=True, blank=True)
    lines_zoom_12 = JSONField(null=True, blank=True)
    lines_zoom_13 = JSONField(null=True, blank=True)
    lines_zoom_14 = JSONField(null=True, blank=True)
    lines_zoom_15 = JSONField(null=True, blank=True)
    lines_zoom_16 = JSONField(null=True, blank=True)
    lines_zoom_17 = JSONField(null=True, blank=True)
    lines_zoom_18 = JSONField(null=True, blank=True)
    lines_zoom_19 = JSONField(null=True, blank=True)
    lines_zoom_20 = JSONField(null=True, blank=True)

    def to_graphene(self, zoom):
        zoom_key = f"lines_zoom_{zoom}"
        lines = getattr(self, zoom_key)
        if lines is None:
            lines = []

        params = {
            'name': self.name,
            'pub_id': self.pub_id,
            'bounds': self.bounds,
            "source_image_url": self.image(),
            "description": self.description,
            zoom_key: lines,
        }
        return RouteGraphene(**params)

    def image(self, width=290, height=386):
        if self.source_image_url not in ["", None]:
            return self.source_image_url

        vertices = []
        if self.lines_zoom_10 is not None:
            for line in self.lines_zoom_10:
                for p in line:
                    vertices.append(f"{p[0]},{p[1]}")
        path = f"color:0x0000ff|weight:5|{'|'.join(vertices)}"
        url = f"https://maps.googleapis.com/maps/api/staticmap?size={width}x{height}&maptype=roadmap&key={settings.GOOGLE_MAPS_API_KEY}&path={path}"
        return url

    def get_lines(self, zoom):
        return {
            1: self.lines_zoom_1,
            2: self.lines_zoom_2,
            3: self.lines_zoom_3,
            4: self.lines_zoom_4,
            5: self.lines_zoom_5,
            6: self.lines_zoom_6,
            7: self.lines_zoom_7,
            8: self.lines_zoom_8,
            9: self.lines_zoom_9,
            10: self.lines_zoom_10,
            11: self.lines_zoom_11,
            12: self.lines_zoom_12,
            13: self.lines_zoom_13,
            14: self.lines_zoom_14,
            15: self.lines_zoom_15,
            16: self.lines_zoom_16,
            17: self.lines_zoom_17,
            18: self.lines_zoom_18,
            19: self.lines_zoom_19,
        }[zoom]

    def set_lines(self, lines):
        self.lines_zoom_1 = reduced_lines(lines, max_vertices(1))
        self.lines_zoom_2 = reduced_lines(lines, max_vertices(2))
        self.lines_zoom_3 = reduced_lines(lines, max_vertices(3))
        self.lines_zoom_4 = reduced_lines(lines, max_vertices(4))
        self.lines_zoom_5 = reduced_lines(lines, max_vertices(5))
        self.lines_zoom_6 = reduced_lines(lines, max_vertices(6))
        self.lines_zoom_7 = reduced_lines(lines, max_vertices(7))
        self.lines_zoom_8 = reduced_lines(lines, max_vertices(8))
        self.lines_zoom_9 = reduced_lines(lines, max_vertices(9))
        self.lines_zoom_10 = reduced_lines(lines, max_vertices(10))
        self.lines_zoom_11 = reduced_lines(lines, max_vertices(11))
        self.lines_zoom_12 = reduced_lines(lines, max_vertices(12))
        self.lines_zoom_13 = reduced_lines(lines, max_vertices(13))
        self.lines_zoom_14 = reduced_lines(lines, max_vertices(14))
        self.lines_zoom_15 = reduced_lines(lines, max_vertices(15))
        self.lines_zoom_16 = reduced_lines(lines, max_vertices(16))
        self.lines_zoom_17 = reduced_lines(lines, max_vertices(17))
        self.lines_zoom_18 = reduced_lines(lines, max_vertices(18))
        self.lines_zoom_19 = reduced_lines(lines, max_vertices(19))
        self.lines_zoom_20 = reduced_lines(lines, max_vertices(20))


class RouteGraphene(DjangoObjectType):

    class Meta:
        model = RouteMetadata