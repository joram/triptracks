import graphene
from apps.accounts.mutations import GetOrCreateUser
from apps.routes.schema import RoutesQuery, AddBucketListRoute, RemoveBucketListRoute, RemoveOwnedRoute
from apps.trips.schema import TripQuery
from apps.trips.mutations import CreateOrUpdateTripPlan, DeleteTripPlan
from apps.packing.schema import PackingQuery
from apps.integrations.mutations import ConnectToStrava


class Query(graphene.ObjectType, TripQuery, PackingQuery, RoutesQuery):
    pass


class Mutations(graphene.ObjectType):
    get_or_create_user = GetOrCreateUser.Field()
    add_bucket_list_route = AddBucketListRoute.Field()
    remove_bucket_list_route = RemoveBucketListRoute.Field()
    remove_owned_route = RemoveOwnedRoute.Field()
    create_or_update_trip_plan = CreateOrUpdateTripPlan.Field()
    delete_trip_plan = DeleteTripPlan.Field()
    connect_to_strava = ConnectToStrava.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
