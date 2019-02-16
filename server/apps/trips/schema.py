import graphene
from apps.accounts.schema import UserType
from apps.trips.models import Plan, TripAttendee
from apps.routes.models import Route
from apps.routes.stores import get_cache
from apps.accounts.models import User
from apps.packing.schema import PackingListType, PackingList
from graphene_django.types import DjangoObjectType


class TripPlanType(DjangoObjectType):
  route = graphene.Field(Route)
  owner = graphene.Field(UserType)
  attendees = graphene.List(lambda: UserType)
  packing_list = graphene.Field(PackingListType)

  def resolve_owner(self, info, *args, **kwargs):
    return User.objects.get(pub_id=self.user_pub_id)

  def resolve_route(self, info, *args, **kwargs):
    return get_cache(0).get_by_pub_id(self.route_pub_id)

  def resolve_attendees(self, info):
    attendees = TripAttendee.objects.filter(plan_pub_id=self.pub_id)
    user_pub_ids = [self.user_pub_id]+[a.user_pub_id for a in attendees]
    return User.objects.filter(pub_id__in=user_pub_ids)

  def resolve_packing_list(self, info):
    return PackingList.objects.get(pub_id=self.packing_list_pub_id)

  class Meta:
    model = Plan