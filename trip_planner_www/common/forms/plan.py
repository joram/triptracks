from django.forms import ModelForm
from common.models import Plan


class PlanForm(ModelForm):
	class Meta:
		model = Plan
		fields = ['name']

