from django.forms import ModelForm
from apps.packing.models import Route


class RouteForm(ModelForm):

	class Meta:
		model = Route
		fields = ['markers', 'lines']
