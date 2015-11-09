from django.db import models

class Itinerary(models.Model):
	name = models.CharField(max_length=5000)
	plan = models.ForeignKey("Plan")

	class Meta:
		app_label = 'common'