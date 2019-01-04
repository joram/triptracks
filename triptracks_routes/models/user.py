import graphene


class User(graphene.ObjectType):
  pub_id = graphene.ID()
  name = graphene.String()

  def resolver_trips(self, info):
    from models.trip import Trip
    return Trip()
  
  def resolver_routes(self, info):
    from models.route import Route
    return Route()
