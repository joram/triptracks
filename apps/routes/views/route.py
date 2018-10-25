import json
import os

from django.conf import settings
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template.context_processors import csrf
from django.http import JsonResponse

from apps.routes.models import Route
from apps.routes.forms.tracks_file import TracksFileForm
from django.contrib.gis.geos import Polygon
from apps.common.decorators import login_required
from django.middleware.csrf import get_token


@login_required
def tmp_load_data(request):
    Route.objects.all().delete()
    examples_dir = os.path.join(settings.BASE_DIR, '../data/example routes/')
    for filename in os.listdir(examples_dir):
        filepath = os.path.join(examples_dir, filename)
        Route.objects.route_from_file(filepath)
    return redirect('list-routes')


@login_required
def create(request):
    route = Route.objects.create()
    return redirect('edit-route', route.id)


def api_route(request, pub_id):

    route = get_object_or_404(Route, pub_id=pub_id)
    route_details = {
        'center': {"coordinates": [route.center[0], route.center[1]]},
        'name': route.name,
        'description': route.description,
        'image_url': route.image_url,
        'pub_id': pub_id,
        'zoom_level': 1,
        'lines': route.lines_zoom_1,
    }
    return JsonResponse(route_details, safe=False)


def api_all(request):
    # bbox_coords = (xmin, ymin, xmax, ymax)
    # "lat_lo,lng_lo,lat_hi,lng_hi"
    bounds = request.GET['bounds'].split(",")
    filter = request.GET.get('filter', 'all')
    bbox_coords = [float(val) for val in bounds]
    bbox = Polygon.from_bbox(bbox_coords)

    try:
        map_zoom = int(request.GET.get('zoom', "20"))
    except:
        map_zoom = 20
    zoom_level = {
        11: 4,
        12: 4,
        13: 3,
        14: 2,
        15: 1,
        16: 1,
        17: 1,
        18: 1,
        19: 1,
        20: 1,
    }.get(map_zoom, 5)
    zoom_field_name = "lines_zoom_{}".format(zoom_level)

    qs = Route.objects.filter(lines__bboverlaps=bbox)
    if filter == "mine":
        user_pub_id = request.session.get("user_pub_id")
        qs = qs.filter(owner_pub_id=user_pub_id)

    routes = []
    if qs.count() < 10:
        zoom_field_name = "lines_zoom_1"
    qs = qs.values("center", "name", "description", "image_url", "pub_id", zoom_field_name)
    count = 0
    for route in qs:
        count += 1
        center = route["center"]
        if center:
            center = {"coordinates": [center[0], center[1]]}

        routes.append({
            'center': center,
            'name': route["name"],
            'description': route["description"],
            'image_url': route["image_url"],
            'pub_id': route["pub_id"],
            'zoom_level': zoom_level,
            'lines': json.loads(route[zoom_field_name])
        })
    return JsonResponse(routes, safe=False)

@login_required
def upload(request):
    if request.method == "POST":
        form = TracksFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')

    form = TracksFileForm()
    context = {'form': form}
    context.update(csrf(request))
    return render_to_response("upload_routes.html", context)


@login_required
def edit(request, route_id):
    route = Route.objects.get(id=route_id)
    route.center = 'POINT(-123.329773 48.407326)'
    context = {
        'route': route,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY}
    return render_to_response("route/edit.html", context)


@login_required
def browse(request):
    context = {
        "csrf_token": get_token(request),
        "GOOGLE_MAPS_API_KEY": settings.GOOGLE_MAPS_API_KEY,
    }
    return render_to_response("home.html", context)


@login_required
def view(request, route_id):
    route = Route.objects.get(id=route_id)
    if not route.center:
        route.center = 'POINT(-123.329773 48.407326)'
    else:
        route.center = str(route.center).split(";")[1].replace(" (", "(")
    context = {
        'request': request,
        'route': route,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY}
    return render_to_response("route/view.html", context)


@login_required
def mine(request):
    context = {
        'request': request,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY}
    return render_to_response("route/mine.html", context)

