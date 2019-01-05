import graphene
from models.route import Route, get_cache
from apps.trips.models import Plan, TripAttendee
from apps.accounts.models import User
from graphene_django.types import DjangoObjectType


class UserType(DjangoObjectType):

  class Meta:
    model = User


class TripPlanType(DjangoObjectType):
  owner = graphene.Field(UserType)
  attendees = graphene.List(lambda: UserType)

  def resolve_owner(self, info, *args, **kwargs):
    print(args)
    print(kwargs)
    print(dir(info.to_dict()))
    print(vars(info))
    return User.objects.all()[0]

  def resolve_attendees(self, info):
    return User.objects.all()

  class Meta:
        model = Plan


class Query(graphene.ObjectType):
  routes = graphene.List(Route, geohash=graphene.String(), zoom=graphene.Int())
  trip_plans = graphene.List(TripPlanType)
  trip_plan = graphene.Field(TripPlanType, pub_id=graphene.String())
  # users = graphene.List(UserType)

  def resolve_routes(self, info, geohash, zoom):
    return get_cache(zoom).get(geohash)

  def resolve_trip_plans(self, info):
    return Plan.objects.all()

  def resolve_trip_plan(self, info, pub_id):
    return Plan.objects.get(pub_id=pub_id)


schema = graphene.Schema(query=Query)
