import os
import json

from django.conf import settings
from django.contrib.gis.geos import fromstr
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.gis.gdal import DataSource
from django.template.context_processors import csrf

from web.common.models import Route, Plan
from web.common.forms.route import RouteForm
from web.common.forms.plan import PlanForm
from web.common.forms.tracks_file import TracksFileForm

def tmp_load_data(request):
	Route.objects.all().delete()
	examples_dir = os.path.join(settings.BASE_DIR, '../data/example routes/')
	for filename in os.listdir(examples_dir):
		filepath = os.path.join(examples_dir, filename)
		Route.objects.route_from_file(filepath)
	return redirect('list-routes')

def create(request):
	route = Route.objects.create()
	return redirect('edit-route', route.id)

def upload(request):

	if request.method == "POST":
		form = TracksFileForm(request.POST, request.FILES)
		if form.is_valid():
			print request.FILES.get('tracks_file')
			form.save()
			return redirect('home')
		print form.errors

	form = TracksFileForm()
	context = {'form': form}
	context.update(csrf(request))
	return render_to_response("upload_routes.html", context)

def edit(request, route_id):
	route = Route.objects.get(id=route_id)
	context = {
		'route': route,
		'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY}
	return render_to_response("route/edit.html", context)

def view(request, route_id):
	route = Route.objects.get(id=route_id)
	context = {
		'route': route,
		'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY}
	return render_to_response("route/view.html", context)

def list_routes(request):
	context = {
		'routes': Route.objects.all(),
		'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY}
	return render_to_response("route/list.html", context)