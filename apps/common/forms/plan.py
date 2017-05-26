from django.forms import ModelForm
from apps.common.models import Plan


class PlanForm(ModelForm):
	class Meta:
		model = Plan
		fields = ['name']

