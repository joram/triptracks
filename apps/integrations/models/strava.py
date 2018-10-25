from stravalib import Client as StravaClient
from django.db import models
from jsonfield import JSONField
from utils.fields import ShortUUIDField
from apps.routes.models import Route, TracksFile
from apps.accounts.models import User


class StravaAccount(models.Model):
    pub_id = ShortUUIDField(prefix="strava", max_length=128)
    user_pub_id = models.CharField(max_length=128)
    access_token = models.CharField(max_length=256)
    attributes = JSONField()

    @property
    def user(self):
        return User.objects.get(pub_id=self.user_pub_id)

    def get_client(self):
        return StravaClient(access_token=str(self.access_token))

    def populate_activities(self):
        after = None
        client = self.get_client()
        seen = []
        while True:
            for activity in client.get_activities(after=after):
                if activity.id in seen:
                    return
                seen.append(activity.id)

                qs = StravaActivity.objects.filter(strava_id=activity.id)
                if qs.exists():
                    yield qs[0], False
                    continue

                gpx_data = client.get_gpx_file(activity.id)
                tracks_file = TracksFile.objects.get_or_create_from_data(gpx_data, "{}.gpx".format(str(activity.name)))
                route = Route.objects.create_from_route(tracks_file, activity.name)
                route.is_public = False
                route.owner_pub_id = self.user_pub_id
                route.save()

                yield StravaActivity.objects.create(
                    strava_account_pub_id=self.pub_id,
                    strava_id=activity.id,
                    route_pub_id=route.pub_id
                ), True
                after = activity.start_date


class StravaActivity(models.Model):
    pub_id = ShortUUIDField(prefix="st_act", max_length=128)
    strava_account_pub_id = models.CharField(max_length=128)
    strava_id = models.IntegerField()
    route_pub_id = models.CharField(max_length=128, null=True)

    @property
    def route(self):
        return Route.objects.get(pub_id=self.route_pub_id)
