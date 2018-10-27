import pprint
from stravalib import Client as StravaClient
from apps.integrations.models import StravaAccount, StravaActivity
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from apps.common.decorators import login_required
from django.conf import settings
from apps.integrations.clients.strava import StravaClient


@login_required
def connect(request):
    if StravaAccount.objects.filter(user_pub_id=request.session.get("user_pub_id")).exists():
        return HttpResponse("strava already connected")

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


def webhooks(request):

    # registering webhooks validation
    if request.method == "GET":
        data = dict(request.GET)
        pprint.pprint(data)
        if "hub.mode" in data.keys():
            return HttpResponse("invalid")
        if data.get("hub.verify_token")[0] == settings.STRAVA_VERIFY_TOKEN:
            return HttpResponse("invalid")
        return JsonResponse({"hub.challenge": data.get("hub.challenge")[0]})

    # regular webhook
    owner_id = request.POST.get("owner_id")
    object_id = request.POST.get("object_id")
    object_type = request.POST.get("object_type")

    if object_type != "activity":
        print "only interested in activities, not {}".format(object_type)
        return HttpResponse("ok")

    qs = StravaAccount.objects.filter(strava_account_id=owner_id)
    if not qs.exists():
        print "user doesn't exists for strava_account_id:{}".format(owner_id)
        return HttpResponse("ok")

    account = qs[0]
    activity = account.get_client().get_activity(object_id)

    qs = StravaActivity.objects.filter(strava_id=activity.get("id"))
    if qs.exists():
        print "TODO: update activity"
        return HttpResponse("ok")

    strava_activity, created = StravaActivity.objects.get_or_create_from_strava_activity(
        activity.id,
        activity.name,
        account.user_pub_id,
    )
    print "new activity {} created:{}".format(strava_activity, created)
    return HttpResponse("ok")


@login_required
def authorized(request):
    if StravaAccount.objects.filter(user_pub_id=request.session.get("user_pub_id")).exists():
        return HttpResponse("strava already connected")

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
