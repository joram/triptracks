import requests
from django.conf import settings


class StravaClient(object):

    def register_webhooks(self):
        requests.post("https://api.strava.com/api/v3/push_subscriptions", headers={
        }, data={
            "client_id": settings.STRAVA_CLIENT_ID,
            "client_secret": settings.STRAVA_CLIENT_SECRET,
            "callback_url": "https://app.triptracks.io/integrations/strava/webhooks",
            "verify_token": settings.STRAVA_VERIFY_TOKEN,
        })
