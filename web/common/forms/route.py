from django.forms import ModelForm
from web.common.models import Route


class RouteForm(ModelForm):

	class Meta:
		model = Route
		fields = ['markers', 'lines']
