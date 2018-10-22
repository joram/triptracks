import json
from django.conf import settings
from stravalib.client import Client as BaseStravaClient


class StravaClient(BaseStravaClient):
    pass

#
#     def __init__(self, access_token):
#         BaseStravaClient.__init__(self)
#         self.access_token = access_token
#
#     def auth_url(self):
#         authorize_url = BaseStravaClient.authorization_url(
#             self,
#             client_id=settings.STRAVA_CLIENT_ID,
#             redirect_uri=settings.BASE_URL+"/integrations/strava/authorized",
#         )
#         return authorize_url
#
#     def get_access_token(self, request):
#         access_token = self.exchange_code_for_token(
#             client_id=settings.STRAVA_CLIENT_ID,
#             client_secret=settings.STRAVA_CLIENT_SECRET,
#             code=request.GET.get("code"),
#         )
#         print json.dumps({
#             "code": request.GET.get("code"),
#             "access_token": access_token,
#         })
#         return access_token
#
#     def get_gpx_files(self):
#         for activity in self.get_activities():
#             yield activity, self.get_gpx_file(activity.id)
