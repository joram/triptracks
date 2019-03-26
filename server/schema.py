import graphene
from apps.trips.models import Plan
from apps.routes.models import Route, RouteMetadata
from apps.trips.schema import TripPlanType
from apps.packing.schema import PackingListType
from apps.packing.models import PackingList


class Query(graphene.ObjectType):
  route = graphene.Field(Route, pub_id=graphene.String())
  routes = graphene.List(
    Route,
    geohash=graphene.String(),
    zoom=graphene.Int(),
    page=graphene.Int(),
    page_size=graphene.Int(),
  )
  routes_search = graphene.List(Route, search_text=graphene.String(), limit=graphene.Int())
  trip_plans = graphene.List(TripPlanType)
  trip_plan = graphene.Field(TripPlanType, pub_id=graphene.String())
  packing_lists = graphene.List(PackingListType)
  packing_list = graphene.Field(PackingListType, pub_id=graphene.String())

  def resolve_route(self, info, pub_id):
    rm = RouteMetadata.objects.get(pub_id=pub_id)
    return rm.route(zoom=14)

  def resolve_routes(self, info, geohash, zoom, page, page_size):

    qs = RouteMetadata.objects.filter(geohash__startswith=geohash).values_list(
      "name",
      "pub_id",
      "bounds",
      f"lines_zoom_{zoom}",
    )

    # paginating
    print(f"serving {qs.count()} routes at {geohash}::{zoom}. from {page_size*page} to {page_size*(page+1)}")
    a = page_size * page
    b = page_size * (page + 1)
    qs = qs[a:b]

    routes = [Route(
      name=data[0],
      pub_id=data[1],
      bounds=data[2],
      lines=data[3],
    ) for data in qs]
    return routes

  def resolve_routes_search(self, info, search_text, limit=10):
    limit = min(limit, 10)
    route_metas = RouteMetadata.objects.filter(name__icontains=search_text).values_list(
      f"lines_zoom_15",
      "name",
      "description",
      "pub_id",
      "bounds",
    )[:limit]
    routes = [Route(
      lines=data[0],
      name=data[1],
      description=data[2],
      pub_id=data[3],
      bounds=data[4],
    ) for data in route_metas]
    return routes

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
