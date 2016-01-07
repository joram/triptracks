from django.db import models
from django.conf import settings

import os


class TracksFile(models.Model):
	tracks_file = models.FileField(upload_to=os.path.join(settings.BASE_DIR, "uploads"))

	class Meta:
		app_label = 'common'

