import graphene
from models.route import Route, get_cache
from apps.trips.models import Plan, TripAttendee
from apps.accounts.models import User
from graphene_django.types import DjangoObjectType


class UserType(DjangoObjectType):
  profile_image = graphene.String()
  name = graphene.String()

  def resolve_profile_image(self, info):
    if self.google_credentials is None:
      return None
    return self.google_credentials.get("picture")

  def resolve_name(self, info):
    print(self.google_credentials)
    if self.google_credentials is None:
      return None
    return self.google_credentials.get("name")

  class Meta:
    exclude_fields = ('password', 'email', 'googleCredentials')
    model = User


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
  routes = graphene.List(Route, geohash=graphene.String(), zoom=graphene.Int())
  trip_plans = graphene.List(TripPlanType)
  trip_plan = graphene.Field(TripPlanType, pub_id=graphene.String())
  # users = graphene.List(UserType)

  def resolve_routes(self, info, geohash, zoom):
    return get_cache(zoom).get(geohash)

  def resolve_trip_plans(self, info):
    user = info.context.user
    user.is_anonymous
    return Plan.objects.all()

  def resolve_trip_plan(self, info, pub_id):
    return Plan.objects.get(pub_id=pub_id)


schema = graphene.Schema(query=Query)
