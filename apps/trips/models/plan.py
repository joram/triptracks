from django.db import models

from apps.routes.models import Route
from apps.packing.models import PackingList

from yr.libyr import Yr
from utils.fields import ShortUUIDField


class Plan(models.Model):
    pub_id = ShortUUIDField(prefix="plan", max_length=32)
    name = models.CharField(max_length=256)
    summary = models.TextField(null=True, blank=True)

    route_pub_id = models.CharField(max_length=32, null=True)
    packing_list_pub_id = models.CharField(max_length=32, null=True)

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
        data = {}
        try:
            weather = Yr(location_xyz=(self.route.center[1], self.route.center[0], 0))

            for forecast in weather.forecast():
                from_dt = forecast["@from"]
                if from_dt not in data:
                    data[from_dt] = {}

                for key in forecast["location"].keys():
                    if key.startswith("@"):
                        continue
                    for second_key in ["@value", "@percent", "@name"]:
                        value = forecast["location"].get(key, {}).get(second_key)
                        if value:
                            try:
                                value = float(value)
                            except:
                                pass
                            data[from_dt][key] = value
                            break
        except Exception as e:
            print e

        return data

    def __str__(self):
        return self.name
