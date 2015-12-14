from django.contrib.gis import forms
from django.forms import ModelForm
from common.models import Route


class RouteForm(ModelForm):
	class Meta:
		model = Route
		fields = ['markers', 'lines']