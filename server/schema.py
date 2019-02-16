import graphene
from apps.routes.stores import get_cache
from apps.trips.models import Plan
from apps.routes.models import Route, RouteMetadata
from apps.trips.schema import TripPlanType
from apps.packing.schema import PackingListType
from apps.packing.models import PackingList


class Query(graphene.ObjectType):

  route = graphene.Field(Route, pub_id=graphene.String())
  routes = graphene.List(Route, geohash=graphene.String(), zoom=graphene.Int())
  routes_search = graphene.List(Route, search_text=graphene.String(), limit=graphene.Int())
  trip_plans = graphene.List(TripPlanType)
  trip_plan = graphene.Field(TripPlanType, pub_id=graphene.String())
  packing_lists = graphene.List(PackingListType)
  packing_list = graphene.Field(PackingListType, pub_id=graphene.String())

  def resolve_route(self, info, pub_id):
    return get_cache(0).get_by_pub_id(pub_id)

  def resolve_routes(self, info, geohash, zoom):
    return get_cache(zoom).get(geohash)

  def resolve_routes_search(self, info, search_text, limit=10):
    limit = min(limit, 10)
    cache = get_cache(0)
    route_metas = RouteMetadata.objects.filter(name__icontains=search_text)[:limit]
    return [cache.get_by_pub_id(rm.pub_id) for rm in route_metas]

  def resolve_trip_plans(self, info):
    if info.context is not None:
      user = info.context.user
      user.is_anonymous
    return Plan.objects.all()

  def resolve_trip_plan(self, info, pub_id):
    return Plan.objects.get(pub_id=pub_id)

  def resolve_packing_lists(self, info):
    return PackingList.objects.all()

  def resolve_packing_list(self, info, pub_id):
    return PackingList.objects.get(pub_id=pub_id)


schema = graphene.Schema(query=Query)
