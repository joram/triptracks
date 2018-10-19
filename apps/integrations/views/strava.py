from apps.integrations.clients.strava import StravaClient
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from apps.common.decorators import login_required


@login_required
def connect(request):
    client = StravaClient()
    uri = client.auth_url()
    print uri
    return HttpResponseRedirect(uri)


@login_required
def authorized(request):
    client = StravaClient()
    access_token = client.get_access_token(request)

    client.access_token = access_token
    athlete = client.get_athlete()
    routes = client.get_routes(athlete.id)
    route_data = []
    for route in routes:
        route_data.append({
            "name": route.name,
            "description": route.description,
            "map": {
                "id": route.map.id,
                "polyline": route.map.polyline,
                "summary_polyline": route.map.summary_polyline,
            }
        })
    import json
    s = json.dumps(route_data, sort_keys=True, indent = 4, separators = (',', ': '))
    print s
    return HttpResponse(s)
