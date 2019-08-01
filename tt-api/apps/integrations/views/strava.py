import json
import pprint
from stravalib import Client
from apps.integrations.models import StravaAccount, StravaActivity
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from utils.decorators import login_required
from django.conf import settings


@login_required
def connect(request):
    authorize_url = Client().authorization_url(
        client_id=settings.STRAVA_CLIENT_ID,
        redirect_uri=settings.BASE_URL+"/integrations/strava/authorized",
    )
    return HttpResponseRedirect(authorize_url)


# @login_required
def collect(request):
    if request.user is None:
        return

    qs = StravaAccount.objects.filter(user_pub_id=request.user.pub_id)
    if qs.count() == 0:
        print("no strava account for user", request.user)
        return

    strava_account = qs[0]
    for activity, created in strava_account.populate_activities():
        print(created, activity)

    return HttpResponse("collecting")


# class FakeRequest():
#     def __init__(self, u):
#         self.user = u
#
# from apps.accounts.models import User
# for user in User.objects.all():
#     collect(FakeRequest(user))


@csrf_exempt
def webhooks(request):

    # registering webhooks validation
    if request.method == "GET":
        data = dict(request.GET)
        pprint.pprint(data)
        if "hub.mode" in data.keys():
            return HttpResponse()
        if data.get("hub.verify_token")[0] == settings.STRAVA_VERIFY_TOKEN:
            return HttpResponse()
        return JsonResponse({"hub.challenge": data.get("hub.challenge")[0]})

    # regular webhook
    data = json.loads(request.body)
    pprint.pprint(data)
    aspect_type = data.get("aspect_type")
    event_time = data.get("event_time")
    object_id = data.get("object_id")
    object_type = data.get("object_type")
    owner_id = data.get("owner_id")
    subscription_id = data.get("subscription_id")
    updates = data.get("updates", {})

    if object_type != "activity":
        print("only interested in activities, not {}".format(object_type))
        return HttpResponse()

    if aspect_type == "delete":
        print("only interested in creates or updates, not deletes")
        return HttpResponse()

    qs = StravaAccount.objects.filter(strava_athlete_id=owner_id)
    if not qs.exists():
        print("user doesn't exists for strava_account_id:{}".format(owner_id))
        return HttpResponse()

    account = qs[0]
    activity = account.get_client().get_activity(object_id)
    qs = StravaActivity.objects.filter(strava_id=activity.id)
    if qs.exists():
        print("TODO: update activity")
        return HttpResponse()

    strava_activity, created = StravaActivity.objects.get_or_create_from_strava_activity(
        account.strava_athlete_id,
        activity.id,
        activity.name,
        account.user_pub_id,
    )
    print("new activity {} created:{}".format(strava_activity, created))
    return HttpResponse()


@login_required
def authorized(request):
    print(dict(request.GET))
    qs = StravaAccount.objects.filter(user_pub_id=request.session.get("user_pub_id"))
    if qs.exists():
        for a in qs:
            athlete = a.get_client().get_athlete()
            a.strava_account_id = athlete.id
            a.save()

        return HttpResponse("strava already connected")

    client = Client()
    access_token = client.exchange_code_for_token(
        client_id=settings.STRAVA_CLIENT_ID,
        client_secret=settings.STRAVA_CLIENT_SECRET,
        code=request.GET.get("code"),
    )
    athlete = client.get_athlete()

    StravaAccount.objects.create(
        user_pub_id=request.session.get("user_pub_id"),
        access_token=access_token,
        strava_account_id=athlete.id,
    )

    return HttpResponse("strava connected")
