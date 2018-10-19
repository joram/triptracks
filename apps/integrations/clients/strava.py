from django.conf import settings
from stravalib.client import Client as BaseStravaClient


class StravaClient(BaseStravaClient):

    def auth_url(self):
        authorize_url = BaseStravaClient.authorization_url(
            self,
            client_id=settings.STRAVA_CLIENT_ID,
            redirect_uri=settings.BASE_URL+"/integrations/strava/authorized",
        )
        return authorize_url

    def get_access_token(self, request):
        access_token = self.exchange_code_for_token(
            client_id=settings.STRAVA_CLIENT_ID,
            client_secret=settings.STRAVA_CLIENT_SECRET,
            code=request.GET.get("code"),
        )
        return access_token