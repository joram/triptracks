from django.db import models

from apps.routes.models import Route
from apps.packing.models import PackingList

from yr.libyr import Yr
import json
from utils.fields import ShortUUIDField


class Plan(models.Model):
    pub_id = ShortUUIDField(prefix="plan", max_length=32)
    name = models.CharField(max_length=256)
    summary = models.TextField(null=True, blank=True)

    route_pub_id = models.CharField(max_length=32)
    packing_list_pub_id = models.CharField(max_length=32)

    start_datetime = models.DateTimeField(blank=True, null=True)
    end_datetime = models.DateTimeField(blank=True, null=True)

    @property
    def route(self):
        if self.route_pub_id:
            return Route.objects.get(pub_id=self.route_pub_id)

    @property
    def packing_list(self):
        if not self.packing_list_pub_id:
            pl = PackingList.objects.create()
            self.packing_list_pub_id = pl.pub_id
            self.save()
        return PackingList.objects.get(pub_id=self.packing_list_pub_id)

    @property
    def daterange(self):
        if not self.start_datetime:
            return ""
        if not self.end_datetime:
            return ""
        s = "{} - {}".format(
            self.start_datetime.strftime("%m/%d/%Y"),
            self.end_datetime.strftime("%m/%d/%Y")
        )
        return s

    @property
    def forecast(self):
        weather = Yr(location_xyz=(self.route.center[1], self.route.center[0], 0))

        data = []
        for forecast in weather.forecast(as_json=True):
            data.append(json.loads(forecast))

        import pprint
        pprint.pprint(data)
        return data

    def __str__(self):
        return self.name
