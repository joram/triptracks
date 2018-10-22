from django.db import models
from jsonfield import JSONField
from utils.fields import ShortUUIDField


class StravaAccount(models.Model):
    pub_id = ShortUUIDField(prefix="strava", max_length=128)
    user_pub_id = models.CharField(max_length=128)
    access_token = models.CharField(max_length=256)
    attributes = JSONField()
