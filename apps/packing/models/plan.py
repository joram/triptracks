from django.db import models
from apps.accounts.models import User
from packing_list import PackingList
from itinerary import Itinerary


class Plan(models.Model):
    name = models.CharField(max_length=30)
    owner = models.ForeignKey(User)
    route = models.ForeignKey("routes.Route")

    @property
    def packing_list(self):
        pl, _ = PackingList.objects.get_or_create(plan_id=self.id);
        return pl

    @property
    def itinerary(self):
        it, _ = Itinerary.objects.get_or_create(plan_id=self.id);
        return it

    def __str__(self):
        return self.name
