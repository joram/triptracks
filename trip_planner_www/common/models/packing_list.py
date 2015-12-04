from django.db import models

class PackingList(models.Model):
	name = models.CharField(max_length=30)
	plan = models.ForeignKey("Plan")

	class Meta:
		app_label = 'common'

class PackingListItem(models.Model):
	GROUP = "G"
	PERSONAL = "P"
	ITEM_TYPE_CHOICES = ((GROUP, 'Group'), (PERSONAL, 'Personal'))

	packing_list = models.ForeignKey("PackingList")
	name = models.CharField(max_length=30)
	item_type = models.ChoicesField(
		max_length=2,
		choices=ITEM_TYPE_CHOICES,
		default=PERSONAL)

	class Meta:
		app_label = 'common'