from django.forms import ModelForm
from apps.routes.models import TracksFile


class TracksFileForm(ModelForm):

  class Meta:
    model = TracksFile
    fields = ['tracks_file']
