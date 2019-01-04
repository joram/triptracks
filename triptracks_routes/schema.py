import graphene
from models.route import Route, get_cache
from models.trip import Trip


class Query(graphene.ObjectType):
  routes = graphene.List(Route, geohash=graphene.String(), zoom=graphene.Int())
  trips = graphene.List(Trip, user_pub_id=graphene.String())

  def resolve_routes(self, info, geohash, zoom):
    return get_cache(zoom).get(geohash)

  def resolve_trips(self, info, user_pub_id):
    return [Trip()]


schema = graphene.Schema(query=Query)
