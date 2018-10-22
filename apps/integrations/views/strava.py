from apps.integrations.clients.strava import StravaClient
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from apps.common.decorators import login_required
from apps.integrations.models import StravaAccount

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

    # strava_account = StravaAccount.objects.create(
    #     user_pub_id=request.session.get("user_pub_id"),
    #     access_token=access_token,
    # )
    #
    # client.access_token = access_token
    # athlete = client.get_athlete()
    # routes = client.get_routes(athlete.id)
    # for activity in client.get_activities():
    #     streams = client.get_activity_streams(activity.id)

    return HttpResponse("strava connected")
