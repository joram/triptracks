import os
from django.contrib.gis.db import models
from django.core.files import File


def tracks_file_path(instance, filename):
    path = 'uploads/tracks/track_{0}_{1}'.format(instance.id, filename)
    return path


class TracksFileManager(models.Manager):

    def get_or_create_from_filepath(self, filepath):
        filename = os.path.basename(filepath)

        trailFiles = TracksFile.objects.filter(filename=filename)
        if trailFiles.exists():
            return trailFiles[0]

        f = open(filepath)
        return TracksFile.objects.create(tracks_file=File(f, name=filename), filename=filename)


class TracksFile(models.Model):

    tracks_file = models.FileField(upload_to=tracks_file_path)
    filename = models.CharField(max_length=512)

    objects = TracksFileManager()

    class Meta:
        app_label = 'routes'
