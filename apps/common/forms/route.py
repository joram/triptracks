from django.forms import ModelForm
from apps.common.models import Route


class RouteForm(ModelForm):

	class Meta:
		model = Route
		fields = ['markers', 'lines']
