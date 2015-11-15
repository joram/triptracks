from django.contrib.gis import forms
from common.models import Map

class MapForm(forms.Form):
	plan_id = forms.IntegerField(required=True)
	markers = forms.MultiPointField(required=True)
	lines = forms.MultiLineStringField(required=True)

	def save(self):
		plan_id = self.cleaned_data.get('plan_id')
		markers = self.cleaned_data.get('markers')
		lines = self.cleaned_data.get('lines')
		
		m, _ = Map.objects.get_or_create(plan__id=plan_id)
		m.markers = markers
		m.lines = lines
		m.save()