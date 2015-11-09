import json

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt

from common.models import Map, Plan

def create(request):
	plan, _ = Plan.objects.get_or_create(name="untitled plan", owner_id=1)
	return redirect('edit-plan', plan.id)


@csrf_exempt
def edit(request, plan_id):
	if request.is_ajax():
		update_plan(request, plan_id)
	plan = Plan.objects.get(id=plan_id)
	context = {
		'plan': plan,
		'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY}
	return render_to_response("create_plan/base.html", context)

def update_plan(request, plan_id):
	if request.is_ajax():
		plan = Plan.objects.get(id=plan_id)
		data = json.loads(request.body)
		action = data.get('action')
		if action == "update_map":
			map_object = plan.map_object
			map_object.markers = data.get('markers', [])
			map_object.save()
		return HttpResponse()

