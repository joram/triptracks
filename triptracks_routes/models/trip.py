import graphene
from models.user import User


class Trip(graphene.ObjectType):
  pub_id = graphene.ID()
  name = graphene.String()
  owner = graphene.Field(User)
  attendees = graphene.List(lambda: User)

  def resolver_owner(self, info):
    return User(name="bob")

  def resolver_attendees(self, info):
    return [User(name="alice"), User(name="chris")]
