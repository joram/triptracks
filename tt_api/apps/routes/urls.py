import requests
from django.http.response import HttpResponse, FileResponse
from django.urls import path, re_path
from apps.routes.models import Route
from apps.routes.stores.gpx import GPXS3Store


def download_gpx(request, pub_id):
    route = Route.objects.get(pub_id=pub_id)
    if route is None:
        return HttpResponse("route missing")

    content = GPXS3Store().get("%s.gpx" % route.pub_id)
    if content is None:
        resp = requests.get(route.source_gpx_url)
        GPXS3Store().put("%s.gpx" % route.pub_id, resp.content)
        content = resp.content

    filename = "%s.gpx" % route.name.lower().replace(" ", "_")
    response = HttpResponse(content=content, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response

urlpatterns = [
    re_path(r'^route/(?P<pub_id>[_\w]+)/gpx$', download_gpx),
]
