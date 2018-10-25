from stravalib import Client as StravaClient
from apps.integrations.models import StravaAccount
from django.http import HttpResponse, HttpResponseRedirect
from apps.common.decorators import login_required
from django.conf import settings


@login_required
def connect(request):
    client = StravaClient()
    authorize_url = client.authorization_url(
        client_id=settings.STRAVA_CLIENT_ID,
        redirect_uri=settings.BASE_URL+"/integrations/strava/authorized",
    )
    return HttpResponseRedirect(authorize_url)


@login_required
def collect(request):
    strava_account = StravaAccount.objects.get(user_pub_id=request.session.get("user_pub_id"))
    for activity, created in strava_account.populate_activities():
        print created, activity
    return HttpResponse("collecting")


@login_required
def authorized(request):
    client = StravaClient()
    access_token = client.exchange_code_for_token(
        client_id=settings.STRAVA_CLIENT_ID,
        client_secret=settings.STRAVA_CLIENT_SECRET,
        code=request.GET.get("code"),
    )
    strava_account = StravaAccount.objects.create(
        user_pub_id=request.session.get("user_pub_id"),
        access_token=access_token,
    )

    return HttpResponse("strava connected")
