import graphene
from apps.trips.models import Plan
from apps.routes.models import RouteGraphene, RouteMetadata, BucketListRoute
from apps.trips.schema import TripPlanType
from apps.packing.schema import PackingListType
from apps.packing.models import PackingList
from apps.accounts.schema import CreateUser
from apps.routes.schema import AddBucketListRoute, RemoveBucketListRoute
from apps.integrations.models.strava import StravaActivity, StravaAccount
from apps.integrations.schema import StravaActivityGraphene
from utils.auth import get_authenticated_user


class FakeUser(object):
    # pub_id = "user_3ffrCPmfjrQwrbh9FcKXcYqV"  # me
   pub_id = "user_6tfBmhtFvPvXdCMmPVYr4QwS"  # matthieu


class IntegrationsQuery(object):
    strava_activities = graphene.List(StravaActivityGraphene)

    def resolve_strava_activities(self, info):
        try:
          user = get_authenticated_user(info)
          if user is None:
            user = FakeUser()
            # return []
          account = StravaAccount.objects.get(user_pub_id=user.pub_id)
          qs = StravaActivity.objects.filter(strava_account_pub_id=account.pub_id)
          return qs
        except Exception as e:
          print(e)

class RoutesQuery(object):
  route = graphene.Field(RouteGraphene, pub_id=graphene.String(), zoom=graphene.Int())
  routes = graphene.List(
    RouteGraphene,
    zoom=graphene.Int(),
    geohash=graphene.String(),
    page=graphene.Int(),
    page_size=graphene.Int(),
  )
  routes_search = graphene.List(RouteGraphene, search_text=graphene.String(), limit=graphene.Int())
  bucket_list_routes = graphene.List(RouteGraphene)

  def resolve_route(self, info, pub_id, zoom):
    zoom_key = f"lines_zoom_{zoom}"
    data = RouteMetadata.objects.filter(pub_id=pub_id).values_list(
      "name",
      "pub_id",
      "bounds",
      zoom_key,
      "source_image_url",
      "description",
      "lines_zoom_15",
    )[0]

    lines = data[3] if data[3] is not None else []
    params = {
      'name': data[0],
      'pub_id': data[1],
      'bounds': data[2],
      zoom_key: lines,
      "source_image_url": data[4],
      "description": data[5],
      "lines_zoom_15": data[6],
    }
    rg = RouteGraphene(**params)
    return rg

  def resolve_routes(self, info, geohash, zoom, page, page_size):
    zoom_key = f"lines_zoom_{zoom}"
    qs = RouteMetadata.objects.filter(geohash__startswith=geohash).values_list(
      "name",
      "pub_id",
      "bounds",
      zoom_key,
      "source_image_url",
    )

    # paginating
    a = page_size * page
    b = page_size * (page + 1)
    qs = qs[a:b]

    def genRoute(data):
      lines = data[3] if data[3] is not None else []
      params = {
        'name': data[0],
        'pub_id': data[1],
        'bounds': data[2],
        zoom_key: lines,
        "source_image_url": data[4],
      }
      rg = RouteGraphene(**params)
      # import pdb; pdb.set_trace()
      return rg

    return [genRoute(data) for data in qs]

  def resolve_routes_search(self, info, search_text, limit=10):
    limit = min(limit, 10)
    route_metas = RouteMetadata.objects.filter(name__icontains=search_text).values_list(
      "name",
      "description",
      "pub_id",
      "bounds",
      "source_image_url"
    )[:limit]
    routes = [RouteGraphene(
      name=data[0],
      description=data[1],
      pub_id=data[2],
      bounds=data[3],
      source_image_url=data[4],
    ) for data in route_metas]
    return routes

  def resolve_bucket_list_routes(self, info):
    user = get_authenticated_user(info)
    if user is None:
      return []
    route_pub_ids = BucketListRoute.objects.filter(user_pub_id=user.pub_id).values_list("route_pub_id")
    qs = RouteMetadata.objects.filter(pub_id__in=route_pub_ids).values_list(
      "name",
      "pub_id",
      "bounds",
      "description",
      "source_image_url",
    )
    return [RouteGraphene(
      pub_id=pub_id,
      name=name,
      bounds=bounds,
      description=description,
      source_image_url=source_image_url,
    ) for (name, pub_id, bounds, description, source_image_url) in qs]


class TripQuery(object):
    trip_plans = graphene.List(TripPlanType)
    trip_plan = graphene.Field(TripPlanType, pub_id=graphene.String())

    def resolve_trip_plans(self, info):
        if info.context is not None:
            user = info.context.user
        return Plan.objects.all()

    def resolve_trip_plan(self, info, pub_id):
        return Plan.objects.get(pub_id=pub_id)


class PackingQuery(object):

    packing_lists = graphene.List(PackingListType)
    packing_list = graphene.Field(PackingListType, pub_id=graphene.String())

    def resolve_packing_lists(self, info):
      return PackingList.objects.all()

    def resolve_packing_list(self, info, pub_id):
      return PackingList.objects.get(pub_id=pub_id)


class Query(graphene.ObjectType, TripQuery, PackingQuery, RoutesQuery, IntegrationsQuery):
    pass


class Mutations(graphene.ObjectType):
    create_user = CreateUser.Field()
    add_bucket_list_route = AddBucketListRoute.Field()
    remove_bucket_list_route = RemoveBucketListRoute.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
