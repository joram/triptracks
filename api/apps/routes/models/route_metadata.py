from django.db import models
from utils.fields import ShortUUIDField
from django.contrib.postgres.fields import JSONField
from graphene_django import DjangoObjectType


class RouteMetadata(models.Model):
    SOURCE_CHOICES = (
        ("summitpost", 'Summitpost'),
        ("trailpeak", 'Trailpeak'),
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

    # def route(self, zoom):
    #     return Route(
    #         lines=self.get_lines(zoom),
    #         name=self.name,
    #         description=self.description,
    #         pub_id=self.pub_id,
    #         zoom=1,
    #         bounds=self.bounds,
    #         source_image_url=self.source_image_url,
    #
    #         # TODO
    #         owner_pub_id="user_whoknows",
    #         is_public=True,
    #     )


class RouteGraphene(DjangoObjectType):

    class Meta:
        model = RouteMetadata