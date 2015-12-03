from django.db import models

class PackingList(models.Model):
	name = models.CharField(max_length=30)
	plan = models.ForeignKey("Plan")

	class Meta:
		app_label = 'common'