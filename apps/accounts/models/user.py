from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    name = models.CharField(max_length=256, unique=True)
    USERNAME_FIELD = 'name'
