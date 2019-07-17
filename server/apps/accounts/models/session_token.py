
from django.db import models
from graphene_django import DjangoObjectType
from utils.fields import ShortUUIDField


class SessionToken(models.Model):
    pub_id = ShortUUIDField(prefix="sess", max_length=32)
    session_key = ShortUUIDField(prefix="session", max_length=32)
    user_pub_id = models.CharField(max_length=128)
    expires = models.DateTimeField()


class SessionTokenGraphene(DjangoObjectType):
    class Meta:
        model = SessionToken
