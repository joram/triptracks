import graphene
from apps.accounts.schema.user import UserType
from routes.models.route import get_cache
from apps.trips.models import Plan
from apps.accounts.models import User
from graphene_django.types import DjangoObjectType
from routes.models.route import Route


class TripPlanType(DjangoObjectType):
  owner = graphene.Field(UserType)
  attendees = graphene.List(lambda: UserType)

  @classmethod
  def get_node(cls, id, info):
    try:
      post = cls._meta.model.objects.get(id=id)
    except cls._meta.model.DoesNotExist:
      return None

    if post.published or info.context.user == post.owner:
      return post
    return None

  def resolve_owner(self, info, *args, **kwargs):
    return User.objects.all()[0]

  def resolve_attendees(self, info):
    return User.objects.all()

  class Meta:
    model = Plan


class Query(graphene.ObjectType):

  route = graphene.List(Route, pub_id=graphene.String())
  routes = graphene.List(Route, geohash=graphene.String(), zoom=graphene.Int())
  trip_plans = graphene.List(TripPlanType)
  trip_plan = graphene.Field(TripPlanType, pub_id=graphene.String())
  # users = graphene.List(UserType)

  def resolve_route(self, info, pub_id):
    return get_cache(0).get_by_pub_id(pub_id)

  def resolve_routes(self, info, geohash, zoom):
    return get_cache(zoom).get(geohash)

  def resolve_trip_plans(self, info):
    if info.context is not None:
      user = info.context.user
      user.is_anonymous
    return Plan.objects.all()

  def resolve_trip_plan(self, info, pub_id):
    return Plan.objects.get(pub_id=pub_id)


schema = graphene.Schema(query=Query)
