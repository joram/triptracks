import graphene
from apps.trips.models import Plan
from apps.routes.models import RouteGraphene, RouteMetadata, BucketListRoute
from apps.trips.schema import TripPlanType
from apps.packing.schema import PackingListType
from apps.packing.models import PackingList
from apps.accounts.schema import CreateUser
from apps.routes.schema import AddBucketListRoute, RemoveBucketListRoute
from utils.auth import get_authenticated_user


class Query(graphene.ObjectType):
  route = graphene.Field(RouteGraphene, pub_id=graphene.String())
  routes = graphene.List(
    RouteGraphene,
    geohash=graphene.String(),
    zoom=graphene.Int(),
    page=graphene.Int(),
    page_size=graphene.Int(),
  )
  routes_search = graphene.List(RouteGraphene, search_text=graphene.String(), limit=graphene.Int())
  bucket_list_routes = graphene.List(RouteGraphene)

  # trip_plans = graphene.List(TripPlanType)
  # trip_plan = graphene.Field(TripPlanType, pub_id=graphene.String())
  # packing_lists = graphene.List(PackingListType)
  # packing_list = graphene.Field(PackingListType, pub_id=graphene.String())

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

    routes = [RouteGraphene(
      name=data[0],
      pub_id=data[1],
      bounds=data[2],
      lines=data[3],
    ) for data in qs]
    return routes

  def resolve_routes_search(self, info, search_text, limit=10):
    limit = min(limit, 10)
    route_metas = RouteMetadata.objects.filter(name__icontains=search_text).values_list(
      "lines_zoom_15",
      "name",
      "description",
      "pub_id",
      "bounds",
    )[:limit]
    routes = [RouteGraphene(
      lines=data[0],
      name=data[1],
      description=data[2],
      pub_id=data[3],
      bounds=data[4],
    ) for data in route_metas]
    return routes

  def resolve_bucket_list_routes(self, info):
    user = get_authenticated_user(info)
    if user is None:
      return []
    qs = BucketListRoute.objects.filter(user_pub_id=user.pub_id)
    route_metas = RouteMetadata.objects.filter(id__in=[blr.route_pub_id for blr in qs]).values_list(
      "lines_zoom_15",
      "name",
      "description",
      "pub_id",
      "bounds",
    )
    routes = [RouteGraphene(
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


class Mutations(graphene.ObjectType):
    create_user = CreateUser.Field()
    add_bucket_list_route = AddBucketListRoute.Field()
    remove_bucket_list_route = RemoveBucketListRoute.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
