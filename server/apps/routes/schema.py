import graphene
from apps.routes.models import Route, BucketListRoute
from utils.auth import get_authenticated_user


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
        return AddBucketListRoute(ok=True)


class RemoveBucketListRoute(graphene.Mutation):
    class Arguments:
        route_pub_id = graphene.String()

    ok = graphene.Boolean()

    def mutate(self, info, route_pub_id):
        user = get_authenticated_user(info)
        if user is None:
            return RemoveBucketListRoute(ok=False)

        qs = Route.objects.filter(pub_id=route_pub_id)
        if not qs.exists():
            return RemoveBucketListRoute(ok=False)

        BucketListRoute.objects.filter(user_pub_id=user.pub_id, route_pub_id=route_pub_id).delete()
        return RemoveBucketListRoute(ok=True)
