from django.conf import settings
from django.contrib.gis.db import models


def tracks_file_path(instance, filename):
    path = 'uploads/tracks/track_{0}_{1}'.format(instance.id, filename)
    return path


class TracksFile(models.Model):

    tracks_file = models.FileField(upload_to=tracks_file_path)

    class Meta:
        app_label = 'routes'
