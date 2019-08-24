import graphene
from apps.routes.models import Route, BucketListRoute, RouteType
from utils.auth import get_authenticated_user
from apps.integrations.models.strava import StravaActivity, StravaAccount


class RoutesQuery(object):
    route = graphene.Field(RouteType, pub_id=graphene.String(), zoom=graphene.Int())
    routes = graphene.List(
      RouteType,
      zoom=graphene.Int(),
      geohash=graphene.String(),
      page=graphene.Int(),
      page_size=graphene.Int(),
    )
    routes_search = graphene.List(RouteType, search_text=graphene.String(), limit=graphene.Int())
    owner_routes = graphene.List(RouteType)
    bucket_list_routes = graphene.List(RouteType)

    def resolve_route(self, info, pub_id, zoom):
      return Route.objects.get(pub_id=pub_id)

    def resolve_routes(self, info, geohash, zoom, page, page_size):
      qs = Route.objects.filter(geohash__startswith=geohash, is_public=True)

      # paginate
      a = page_size * page
      b = page_size * (page + 1)
      qs = qs[a:b]

      return qs

    def resolve_routes_search(self, info, search_text, limit=10):
      limit = min(limit, 10)
      return Route.objects.filter(name__icontains=search_text, is_public=True)[:limit]

    def resolve_bucket_list_routes(self, info):
      user = get_authenticated_user(info)
      if user is None:
        return []

      route_pub_ids = BucketListRoute.objects.filter(user_pub_id=user.pub_id).values_list("route_pub_id")
      return Route.objects.filter(pub_id__in=route_pub_ids)

    def resolve_owner_routes(self, info):
      user = get_authenticated_user(info)
      if user is None:
        return []

      account = StravaAccount.objects.get(user_pub_id=user.pub_id)
      route_pub_ids = StravaActivity.objects.filter(strava_account_pub_id=account.pub_id).values_list("route_pub_id")
      route_pub_ids = [a[0] for a in route_pub_ids]
      return Route.objects.filter(pub_id__in=route_pub_ids)


class AddBucketListRoute(graphene.Mutation):
    class Arguments:
        route_pub_id = graphene.String()

    ok = graphene.Boolean()

    def mutate(self, info, route_pub_id):
        user = get_authenticated_user(info)
        print("", user, "adding to bucket list", route_pub_id)
        print(Route.objects.all()[0])

        if user is None:
            print("user doesn't exist", route_pub_id)
            return AddBucketListRoute(ok=False)

        qs = Route.objects.filter(pub_id=route_pub_id).values_list("pub_id")
        if not qs.exists():
            print("route doesn't exist", route_pub_id)
            return AddBucketListRoute(ok=False)

        BucketListRoute.objects.create(user_pub_id=user.pub_id, route_pub_id=route_pub_id)
        print(BucketListRoute.objects.all().count())
        return AddBucketListRoute(ok=True)


class RemoveBucketListRoute(graphene.Mutation):
    class Arguments:
        route_pub_id = graphene.String()

    ok = graphene.Boolean()

    def mutate(self, info, route_pub_id):
        user = get_authenticated_user(info)
        print("", user, "removing from bucket list", route_pub_id)
        if user is None:
            return RemoveBucketListRoute(ok=False)

        qs = Route.objects.filter(pub_id=route_pub_id)
        if not qs.exists():
            return RemoveBucketListRoute(ok=False)

        qs = BucketListRoute.objects.filter(user_pub_id=user.pub_id, route_pub_id=route_pub_id)
        print("removing %d" % qs.count())
        qs.delete()
        return RemoveBucketListRoute(ok=True)


class RemoveOwnedRoute(graphene.Mutation):
    class Arguments:
        route_pub_id = graphene.String()

    ok = graphene.Boolean()

    def mutate(self, info, route_pub_id):
        user = get_authenticated_user(info)
        print("", user, "removing owned list", route_pub_id)
        if user is None:
            return RemoveOwnedRoute(ok=False)

        qs = Route.objects.filter(pub_id=route_pub_id, owner_pub_id=user.pub_id)
        if not qs.exists():
            return RemoveOwnedRoute(ok=False)

        StravaActivity.objects.filter(route_pub_id=route_pub_id).delete()
        qs.delete()

        return RemoveOwnedRoute(ok=True)
