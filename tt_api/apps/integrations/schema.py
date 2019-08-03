from graphene_django import DjangoObjectType
from apps.integrations.models.strava import StravaActivity


class StravaActivityGraphene(DjangoObjectType):

    class Meta:
        model = StravaActivity
