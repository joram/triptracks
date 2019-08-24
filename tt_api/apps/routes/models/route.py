from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import JSONField
import graphene
from graphene_django import DjangoObjectType

from apps.routes.models import RouteLines
from utils.fields import ShortUUIDField
from utils.lines import reduced_lines


class Route(models.Model):
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

    def _lines(self, zoom):
        return RouteLines.objects.get(route_pub_id=self.pub_id, zoom=zoom).lines

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
        RouteLines.objects.filter(route_pub_id=self.pub_id).delete()
        for zoom in range(1, 21):
            RouteLines.objects.create(route_pub_id=self.pub_id, zoom=zoom, lines=reduced_lines(lines, zoom))


class RouteType(DjangoObjectType):
    lines_zoom_13 = graphene.Field(graphene.JSONString)

    def resolve_lines_zoom_1(self, info, *args, **kwargs):
        return self._lines(1)

    def resolve_lines_zoom_2(self, info, *args, **kwargs):
        return self._lines(2)

    def resolve_lines_zoom_3(self, info, *args, **kwargs):
        return self._lines(3)

    def resolve_lines_zoom_4(self, info, *args, **kwargs):
        return self._lines(4)

    def resolve_lines_zoom_5(self, info, *args, **kwargs):
        return self._lines(5)

    def resolve_lines_zoom_6(self, info, *args, **kwargs):
        return self._lines(6)

    def resolve_lines_zoom_7(self, info, *args, **kwargs):
        return self._lines(7)

    def resolve_lines_zoom_8(self, info, *args, **kwargs):
        return self._lines(8)

    def resolve_lines_zoom_9(self, info, *args, **kwargs):
        return self._lines(9)

    def resolve_lines_zoom_10(self, info, *args, **kwargs):
        return self._lines(10)

    def resolve_lines_zoom_11(self, info, *args, **kwargs):
        return self._lines(11)

    def resolve_lines_zoom_12(self, info, *args, **kwargs):
        return self._lines(12)

    def resolve_lines_zoom_13(self, info, *args, **kwargs):
        return self._lines(13)

    def resolve_lines_zoom_14(self, info, *args, **kwargs):
        return self._lines(14)

    def resolve_lines_zoom_15(self, info, *args, **kwargs):
        return self._lines(15)

    def resolve_lines_zoom_16(self, info, *args, **kwargs):
        return self._lines(16)

    def resolve_lines_zoom_17(self, info, *args, **kwargs):
        return self._lines(17)

    def resolve_lines_zoom_18(self, info, *args, **kwargs):
        return self._lines(18)

    def resolve_lines_zoom_19(self, info, *args, **kwargs):
        return self._lines(19)

    def resolve_lines_zoom_20(self, info, *args, **kwargs):
        return self._lines(20)

    class Meta:
        model = Route
