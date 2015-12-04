import os
import json

from django.conf import settings
from django.contrib.gis.geos import fromstr
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.gis.gdal import DataSource

from common.models import Route, Plan
from common.forms.route import RouteForm
from common.forms.plan import PlanForm


def tmp_load_data(request):
	Route.objects.all().delete()
	examples_dir = os.path.join(settings.BASE_DIR, '../scripts/example routes/')
	for filename in os.listdir(examples_dir):
		filepath = os.path.join(examples_dir, filename)
		Route.objects.route_from_file(filepath)
	return HttpResponse("ok")

def create(request):
	route = Route.objects.create()
	return redirect('edit-route', route.id)


def edit(request, route_id):
	route = Route.objects.get(id=route_id)
	context = {
		'route': route,
		'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY}
	return render_to_response("edit_route.html", context)

def list_routes(request):
	context = {
		'routes': Route.objects.all(),
		'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY}
	return render_to_response("list_routes.html", context)