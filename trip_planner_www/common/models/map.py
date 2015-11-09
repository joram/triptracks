import json
from django.db import models
from jsonfield import JSONField

class Map(models.Model):
	markers = JSONField(default=[])
	lines = JSONField(default=[])
	plan = models.ForeignKey("Plan")

	@property
	def json_string(self):
		return json.dumps({
			'markers': self.markers,
			'lines': self.lines})
	class Meta:
		app_label = 'common'