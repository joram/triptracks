import graphene
from apps.accounts.schema import GetOrCreateUser
from apps.routes.schema import RoutesQuery, AddBucketListRoute, RemoveBucketListRoute, RemoveOwnedRoute
from apps.trips.schema import TripQuery
from apps.packing.schema import PackingQuery


class Query(graphene.ObjectType, TripQuery, PackingQuery, RoutesQuery):
    pass


class Mutations(graphene.ObjectType):
    get_or_create_user = GetOrCreateUser.Field()
    add_bucket_list_route = AddBucketListRoute.Field()
    remove_bucket_list_route = RemoveBucketListRoute.Field()
    remove_owned_route = RemoveOwnedRoute.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
