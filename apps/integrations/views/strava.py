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
    print dir(athlete)
    print athlete
