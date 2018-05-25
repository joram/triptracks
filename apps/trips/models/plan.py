from django.db import models
from utils.fields import ShortUUIDField
from apps.routes.models import Route
from apps.packing.models import PackingList


class Plan(models.Model):
    pub_id = ShortUUIDField(prefix="plan", max_length=32)
    name = models.CharField(max_length=256)
    summary = models.TextField(null=True, blank=True)

    route_pub_id = models.CharField(max_length=32)
    packing_list_pub_id = models.CharField(max_length=32)

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

    def __str__(self):
        return self.name
