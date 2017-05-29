from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import UserManager


class User(AbstractBaseUser):
    google_id = models.CharField(max_length=256)
    image_url = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    email = models.CharField(max_length=256, unique=True)
    last_authenticated = models.DateTimeField()
    USERNAME_FIELD = 'email'

    objects = UserManager()
