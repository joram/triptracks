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
    strava_athlete_id = models.IntegerField()
    attributes = JSONField()

    @property
    def user(self):
        return User.objects.get(pub_id=self.user_pub_id)

    def get_client(self):
        return StravaClient(access_token=str(self.access_token))

    def get_activities(self):
        import requests
        import time
        page = 1
        while True:
            url = "https://www.strava.com/api/v3/athlete/activities?page={page}".format(page=page)
            headers = {"Authorization": "Bearer {token}".format(token=self.access_token)}
            resp = requests.get(url, headers=headers)
            if resp.status_code != 200:
                print(resp.content)
                print(resp.status_code)
                time.sleep(30)
                continue
            activities = resp.json()

            if len(activities) == 0:
                break
            print("--- new page [{}] count:{} ---".format(page, len(activities)))
            for activity in activities:
                yield activity
            page += 1

    def populate_activities(self):
        client = self.get_client()
        for activity in self.get_activities():
            qs = StravaActivity.objects.filter(strava_id=activity.get("id"))
            if qs.exists():
                yield qs[0], False
                continue

            gpx_data = client.get_gpx_file(activity.get("id"))
            if gpx_data is None:
                print("no tracks")
                continue

            try:
                tracks_file = TracksFile.objects.get_or_create_from_data(gpx_data, "{}.gpx".format(str(activity.get("name"))))
                route = Route.objects.create_from_route(tracks_file, activity.get("name"))
                route.is_public = False
                route.owner_pub_id = self.user_pub_id
                route.save()
            except Exception as e:
                print(e)
                continue

            yield StravaActivity.objects.create(
                strava_account_pub_id=self.pub_id,
                strava_id=activity.get("id"),
                route_pub_id=route.pub_id
            ), True

    def __str__(self):
        return u"strava_account:{}".format(self.user.name)

    def __unicode__(self):
        return self.__str__()


class StravaActivityManager(models.Manager):

    def get_or_create_from_strava_activity(self, strava_athlete_id, strava_activity_id, strava_activity_name, user_pub_id):
        qs = StravaActivity.objects.filter(strava_id=strava_activity_id)
        if qs.exists():
            return qs[0], False

        account = StravaAccount.objects.get(strava_athlete_id=strava_athlete_id)
        gpx_data = account.get_client().get_gpx_file(strava_activity_id)
        if gpx_data is None:
            print("no tracks")
            return None, False

        try:
            tracks_file = TracksFile.objects.get_or_create_from_data(gpx_data,
                                                                     "{}.gpx".format(strava_activity_name))
            route = Route.objects.create_from_route(tracks_file, strava_activity_name)
            route.is_public = False
            route.owner_pub_id = user_pub_id
            route.save()
        except Exception as e:
            print(e)
            return None, False

        return StravaActivity.objects.create(
            strava_account_pub_id=account.pub_id,
            strava_id=strava_activity_id,
            route_pub_id=route.pub_id
        ), True


class StravaActivity(models.Model):
    pub_id = ShortUUIDField(prefix="st_act", max_length=128)
    strava_account_pub_id = models.CharField(max_length=128)
    strava_id = models.IntegerField()
    route_pub_id = models.CharField(max_length=128, null=True)

    objects = StravaActivityManager()

    @property
    def account(self):
        return StravaAccount.objects.get(pub_id=self.strava_account_pub_id)

    @property
    def route(self):
        return Route.objects.get(pub_id=self.route_pub_id)

    def __str__(self):
        return u"strava_activity:{}".format(self.route.name)

    def __unicode__(self):
        return self.__str__()