import json
import os

from django.conf import settings
from django.shortcuts import render_to_response, redirect
from django.template.context_processors import csrf
from django.http import JsonResponse

from apps.common.models import Route
from apps.common.forms.tracks_file import TracksFileForm


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


cached_all_routes = None
def api_all(request):
    global cached_all_routes
    if cached_all_routes is not None:
        return cached_all_routes

    route = Route.objects.all()[0]
    routes = [{
        'center': {"coordinates": [route.center[0], route.center[1]]},
        'name': route.name,
        'lines': {"coordinates": [[list(p) for p in line] for line in route.lines]}
    } for route in list(Route.objects.all())]
    cached_all_routes = JsonResponse(routes, safe=False)
    return cached_all_routes

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
    route.center = 'POINT(-123.329773 48.407326)'
    context = {
        'route': route,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY}
    return render_to_response("route/edit.html", context)


def view(request, route_id):
    route = Route.objects.get(id=route_id)
    if not route.center:
        route.center = 'POINT(-123.329773 48.407326)'
    else:
        route.center = str(route.center).split(";")[1].replace(" (", "(")
    print route.center
    context = {
        'route': route,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY}
    return render_to_response("route/view.html", context)


def list_routes(request):
    routes = []
    for route in Route.objects.all():
        if route.center is None:
            route.center = 'POINT(-123.329773 48.407326)'
        routes.append(route)

    context = {
        'routes': routes,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY}
    return render_to_response("route/list.html", context)