from django.db import models
from utils.fields import ShortUUIDField


class BucketListRoute(models.Model):
    pub_id = ShortUUIDField(prefix="bktlst", max_length=38, db_index=True)
    route_pub_id = models.CharField(max_length=38)
    user_pub_id = models.CharField(max_length=128)
