import graphene
from apps.accounts.schema import UserType
from apps.trips.models import Plan, TripAttendee
from apps.routes.models import RouteGraphene, RouteMetadata
from apps.accounts.models import User
from apps.packing.schema import PackingListType, PackingList
from graphene_django.types import DjangoObjectType
from utils.auth import get_authenticated_user


class TripPlanType(DjangoObjectType):
  route = graphene.Field(RouteGraphene)
  owner = graphene.Field(UserType)
  attendees = graphene.List(lambda: UserType)
  packing_list = graphene.Field(PackingListType)

  def resolve_owner(self, info, *args, **kwargs):
    return User.objects.get(pub_id=self.user_pub_id)

  def resolve_route(self, info, *args, **kwargs):
    try:
      return RouteMetadata.objects.get(pub_id=self.route_pub_id)
    except RouteMetadata.DoesNotExist:
      return RouteGraphene()

  def resolve_attendees(self, info):
    attendees = TripAttendee.objects.filter(plan_pub_id=self.pub_id)
    user_pub_ids = [self.user_pub_id]+[a.user_pub_id for a in attendees]
    return User.objects.filter(pub_id__in=user_pub_ids)

  def resolve_packing_list(self, info):
    return PackingList.objects.get(pub_id=self.packing_list_pub_id)

  class Meta:
    model = Plan


class TripQuery(object):
    trip_plans = graphene.List(TripPlanType)
    trip_plan = graphene.Field(TripPlanType, pub_id=graphene.String())

    def resolve_trip_plans(self, info):
      user = get_authenticated_user(info)
      if user is None:
        return []
      return Plan.objects.filter(user_pub_id=user.pub_id).order_by("-start_datetime")

    def resolve_trip_plan(self, info, pub_id):
      return Plan.objects.get(pub_id=pub_id)


