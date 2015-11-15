import json

from django.conf import settings
from django.contrib.gis.geos import fromstr
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt

from common.models import Map, Plan
from common.forms.map import MapForm



def create(request):
	plan, _ = Plan.objects.get_or_create(name="untitled plan", owner_id=1)
	return redirect('edit-plan', plan.id)


@csrf_exempt
def edit(request, plan_id):
	if request.is_ajax():
		data = json.loads(request.body)
		form_data = {
			'plan_id': plan_id,
			'markers': fromstr(json.dumps(data.get('markers'))),
			'lines': fromstr(json.dumps(data.get('lines')))}
		form = MapForm(form_data)
		if form.is_valid():
			form.save()
			return HttpResponse("OK")
		return HttpResponse("%s" % form.errors)

	plan = Plan.objects.get(id=plan_id)
	context = {
		'plan': plan,
		'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY}
	return render_to_response("create_plan/base.html", context)
