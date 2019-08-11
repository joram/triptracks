import json
import pprint
from apps.integrations.models import StravaAccount, StravaActivity
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


@csrf_exempt
def webhooks(request):

    # registering webhooks validation
    if request.method == "GET":
        data = dict(request.GET)
        pprint.pprint(data)
        if "hub.mode" not in data.keys():
            return HttpResponse()
        if data.get("hub.verify_token")[0] != settings.STRAVA_VERIFY_TOKEN:
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
    print("getting activity", object_id)
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

