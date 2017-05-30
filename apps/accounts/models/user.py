from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import UserManager
from utils.fields import ShortUUIDField


class User(AbstractBaseUser):
    google_credentials = JSONField()
    email = models.CharField(max_length=256, unique=True)
    is_admin = models.BooleanField(default=False)
    pub_id = ShortUUIDField(prefix="user", max_length=128)

    USERNAME_FIELD = 'email'

    objects = UserManager()
