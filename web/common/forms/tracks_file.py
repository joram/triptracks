from django.forms import ModelForm
from web.common.models import TracksFile


class TracksFileForm(ModelForm):
	class Meta:
		model = TracksFile
		fields = ['tracks_file']