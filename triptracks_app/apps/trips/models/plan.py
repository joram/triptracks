from django.db import models

from apps.accounts.models import User
from apps.routes.models import Route
from apps.packing.models import PackingList

from apps.integrations.yrno_forecast import get_daily_weather, get_icons
from utils.fields import ShortUUIDField
from utils.email import send_trip_invitation_email


class Plan(models.Model):
    pub_id = ShortUUIDField(prefix="plan", max_length=32)
    user_pub_id = models.CharField(max_length=128)
    name = models.CharField(max_length=256)
    summary = models.TextField(null=True, blank=True)

    route_pub_id = models.CharField(max_length=32, null=True)
    packing_list_pub_id = models.CharField(max_length=32, null=True)

    start_datetime = models.DateTimeField(blank=True, null=True)
    end_datetime = models.DateTimeField(blank=True, null=True)

    @property
    def route(self):
        if self.route_pub_id:
            return Route.objects.get(pub_id=self.route_pub_id)

    @property
    def packing_list(self):
        if not self.packing_list_pub_id:
            pl = PackingList.objects.create()
            self.packing_list_pub_id = pl.pub_id
            self.save()
        return PackingList.objects.get(pub_id=self.packing_list_pub_id)

    @property
    def daterange(self):
        if not self.start_datetime:
            return ""
        if not self.end_datetime:
            return ""
        s = "{} - {}".format(
            self.start_datetime.strftime("%m/%d/%Y"),
            self.end_datetime.strftime("%m/%d/%Y")
        )
        return s

    @property
    def forecast(self):
        f = get_daily_weather(self.route.center[1], self.route.center[0])
        return f

    @property
    def forecast_icons(self):
        return get_icons(self.route.center[1], self.route.center[0])

    @property
    def attendees(self):
        user_pub_ids = [User.objects.get(pub_id=self.user_pub_id).pub_id]
        user_pub_ids = user_pub_ids + [ta.user_pub_id for ta in TripAttendee.objects.filter(plan_pub_id=self.pub_id)]
        users = User.objects.filter(pub_id__in=user_pub_ids)
        return users

    def add_attendee(self, inviting_user, user):
        if user.pub_id == self.user_pub_id:
            return
        TripAttendee.objects.get_or_create(user_pub_id=user.pub_id, plan_pub_id=self.pub_id)
        if user.send_invitation_emails:
            send_trip_invitation_email(from_user=inviting_user, to_user=user, trip=self)

    def remove_attendee(self, user):
        if user.pub_id == self.user_pub_id:
            return
        TripAttendee.objects.filter(user_pub_id=user.pub_id, plan_pub_id=self.pub_id).delete()

    def __str__(self):
        return self.name


class TripAttendee(models.Model):
    plan_pub_id = models.CharField(max_length=32)
    user_pub_id = models.CharField(max_length=128)
