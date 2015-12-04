from django.db import models
from django.contrib.auth.models import User
from common.models import PackingList, Itinerary, Route


class Plan(models.Model):
    name = models.CharField(max_length=30)
    owner = models.ForeignKey(User)
    route = models.ForeignKey("Route")

    @property
    def packing_list(self):
    	pl, _ = PackingList.objects.get_or_create(plan_id=self.id);
    	return pl

    @property
    def itinerary(self):
    	it, _ = Itinerary.objects.get_or_create(plan_id=self.id);
    	return it

    @property
    def route(self):
    	r, _ = Route.objects.get_or_create(plan_id=self.id);
    	return r

    def __str__(self):
        return self.name

    class Meta:
    	app_label = 'common'