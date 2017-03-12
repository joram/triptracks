import os

from django.conf import settings
from django.shortcuts import render_to_response, redirect
from django.template.context_processors import csrf

from web.common.models import Route
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
    route.center = 'POINT(-123.329773 48.407326)'
    context = {
        'route': route,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY}
    return render_to_response("route/edit.html", context)


def view(request, route_id):
    route = Route.objects.get(id=route_id)
    route.center = 'POINT(-123.329773 48.407326)'

    context = {
        'route': route,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY}
    return render_to_response("route/view.html", context)


def list_routes(request):
    routes = []
    for route in Route.objects.all():
        if route.center is None:
            route.center = 'POINT(-123.329773 48.407326)'
        routes = routes.append(route)

    context = {
        'routes': routes,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY}
    return render_to_response("route/list.html", context)